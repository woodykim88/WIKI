"""
SaladLab LLM Wiki — Prototype Web Server
BM25 검색 + Claude Q&A + 문서 브라우저 + 지식 그래프
"""
import os
import re
import json
import hashlib
from pathlib import Path
from typing import Optional

import yaml
import markdown
import numpy as np
from rank_bm25 import BM25Okapi
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

WIKI_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = WIKI_ROOT / "10_Wiki"
META_DIR = WIKI_ROOT / "20_Meta"

app = FastAPI(title="SaladLab Wiki")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ── Document Loading ──

def parse_frontmatter(content: str) -> tuple[dict, str]:
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                return fm, parts[2].strip()
            except yaml.YAMLError:
                pass
    return {}, content


def load_documents() -> list[dict]:
    docs = []
    for md_file in sorted(WIKI_DIR.rglob("*.md")):
        raw = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(raw)
        rel_path = str(md_file.relative_to(WIKI_ROOT))
        raw_title = fm.get("title") or body.split("\n", 1)[0].lstrip("# ").strip() or md_file.stem
        title = re.sub(r"[\[\]>*]", "", raw_title).strip()
        doc_id = hashlib.md5(rel_path.encode()).hexdigest()[:12]
        docs.append({
            "id": doc_id,
            "title": title,
            "path": rel_path,
            "category": _extract_category(rel_path),
            "tags": fm.get("tags", []),
            "confidence": fm.get("confidence_score", 0),
            "body": body,
            "raw": raw,
        })
    return docs


def _extract_category(path: str) -> str:
    parts = path.replace("10_Wiki/", "").split("/")
    if len(parts) >= 2:
        return "/".join(parts[:-1])
    return "기타"


DOCUMENTS: list[dict] = []
BM25_INDEX: Optional[BM25Okapi] = None
TOKENIZED_CORPUS: list[list[str]] = []


def _tokenize(text: str) -> list[str]:
    text = re.sub(r"[^\w가-힣]", " ", text)
    return [t for t in text.split() if len(t) > 1]


def build_search_index():
    global DOCUMENTS, BM25_INDEX, TOKENIZED_CORPUS
    DOCUMENTS = load_documents()
    TOKENIZED_CORPUS = [_tokenize(d["title"] + " " + " ".join(d["tags"]) + " " + d["body"]) for d in DOCUMENTS]
    if TOKENIZED_CORPUS:
        BM25_INDEX = BM25Okapi(TOKENIZED_CORPUS)


build_search_index()


# ── Search ──

def search_docs(query: str, top_k: int = 5) -> list[dict]:
    if not BM25_INDEX:
        return []
    tokens = _tokenize(query)
    if not tokens:
        return []
    scores = BM25_INDEX.get_scores(tokens)
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for idx in top_indices:
        if scores[idx] > 0:
            doc = DOCUMENTS[idx]
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "path": doc["path"],
                "category": doc["category"],
                "score": float(scores[idx]),
                "snippet": doc["body"][:300],
            })
    return results


# ── Claude Q&A ──

def get_anthropic_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    import anthropic
    return anthropic.Anthropic(api_key=api_key)


SYSTEM_PROMPT = """너는 SaladLab의 사내 위키 지식 전문가다.
아래 제공된 위키 문서 컨텍스트만을 기반으로 질문에 답변하라.

규칙:
1. 컨텍스트에 없는 정보는 "위키에 해당 정보가 없습니다"라고 답하라. 절대 추측하지 마라.
2. 답변에 출처를 반드시 표기하라. 형식: 📄 [문서명]
3. 수식, 상태 전이, 테이블 데이터는 원문 그대로 인용하라 (요약 금지).
4. 관련 문서가 여러 개일 경우, 가장 관련성 높은 순서로 참조하라.
5. 답변은 한국어로 작성하라.
6. 마크다운 형식으로 답변하라."""


class QARequest(BaseModel):
    question: str


@app.post("/api/qa")
async def ask_question(req: QARequest):
    results = search_docs(req.question, top_k=5)
    if not results:
        return {"answer": "관련 문서를 찾지 못했습니다.", "sources": []}

    context_parts = []
    for i, r in enumerate(results):
        doc = next((d for d in DOCUMENTS if d["id"] == r["id"]), None)
        if doc:
            context_parts.append(f"### 문서 {i+1}: {doc['title']}\n경로: {doc['path']}\n\n{doc['body'][:3000]}")

    context = "\n\n---\n\n".join(context_parts)

    client = get_anthropic_client()
    if not client:
        answer = _build_search_answer(req.question, results)
        return {"answer": answer, "sources": results}

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"[컨텍스트]\n{context}\n\n---\n[질문]\n{req.question}"}],
        )
        return {"answer": message.content[0].text, "sources": results}
    except Exception:
        answer = _build_search_answer(req.question, results)
        return {"answer": answer, "sources": results}


def _build_search_answer(question: str, results: list[dict]) -> str:
    lines = [f"**\"{question}\"** 에 대한 검색 결과입니다.\n"]
    for i, r in enumerate(results):
        doc = next((d for d in DOCUMENTS if d["id"] == r["id"]), None)
        if not doc:
            continue
        relevance = min(int(r["score"] / max(results[0]["score"], 1) * 100), 100)
        body = doc["body"]
        excerpt = _extract_relevant_section(body, question)
        lines.append(f"### {i+1}. 📄 {doc['title']}")
        lines.append(f"> 📁 `{doc['path']}` · 관련도 {relevance}%\n")
        lines.append(excerpt)
        lines.append("")
    if not results:
        lines.append("관련 문서를 찾지 못했습니다.")
    else:
        lines.append("---")
        lines.append("*💡 Anthropic API 키를 설정하면 AI가 이 문서들을 종합하여 자연어로 답변합니다.*")
    return "\n".join(lines)


def _extract_relevant_section(body: str, query: str) -> str:
    query_tokens = set(_tokenize(query))
    sections = re.split(r"\n(?=#{1,3} )", body)
    best_section = ""
    best_score = 0
    for section in sections:
        tokens = set(_tokenize(section))
        overlap = len(query_tokens & tokens)
        if overlap > best_score:
            best_score = overlap
            best_section = section
    if not best_section:
        best_section = body
    lines = best_section.strip().split("\n")
    excerpt = "\n".join(lines[:20])
    if len(lines) > 20:
        excerpt += "\n\n*(... 이하 생략)*"
    return excerpt


# ── Document APIs ──

@app.get("/api/docs")
async def list_documents(q: str = Query(default="")):
    if q:
        return search_docs(q, top_k=20)
    return [{"id": d["id"], "title": d["title"], "path": d["path"], "category": d["category"], "tags": d["tags"]} for d in DOCUMENTS]


@app.get("/api/docs/{doc_id}")
async def get_document(doc_id: str):
    doc = next((d for d in DOCUMENTS if d["id"] == doc_id), None)
    if not doc:
        raise HTTPException(404, "Document not found")
    html = markdown.markdown(doc["body"], extensions=["tables", "fenced_code", "toc", "nl2br"])
    return {"id": doc["id"], "title": doc["title"], "path": doc["path"], "category": doc["category"],
            "tags": doc["tags"], "html": html, "raw": doc["raw"]}


@app.get("/api/docs/{doc_id}/raw")
async def download_document(doc_id: str):
    doc = next((d for d in DOCUMENTS if d["id"] == doc_id), None)
    if not doc:
        raise HTTPException(404, "Document not found")
    return PlainTextResponse(doc["raw"], media_type="text/markdown; charset=utf-8",
                             headers={"Content-Disposition": f'attachment; filename="{doc["title"]}.md"'})


@app.get("/api/graph")
async def get_graph():
    graph_file = META_DIR / "Graph.json"
    if not graph_file.exists():
        raise HTTPException(404, "Graph.json not found")
    return json.loads(graph_file.read_text(encoding="utf-8"))


@app.get("/api/categories")
async def get_categories():
    cats = {}
    for d in DOCUMENTS:
        cat = d["category"]
        if cat not in cats:
            cats[cat] = []
        cats[cat].append({"id": d["id"], "title": d["title"]})
    return cats


@app.post("/api/reindex")
async def reindex():
    build_search_index()
    return {"status": "ok", "document_count": len(DOCUMENTS)}


# ── Frontend ──

@app.get("/", response_class=HTMLResponse)
async def index():
    return FRONTEND_HTML


FRONTEND_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SaladLab Wiki</title>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {
  --bg: #0d1117; --bg2: #161b22; --bg3: #21262d;
  --border: #30363d; --text: #e6edf3; --text2: #8b949e;
  --accent: #58a6ff; --accent2: #3fb950; --accent3: #f0883e;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; height:100vh; display:flex; flex-direction:column; }

/* Nav */
nav { background:var(--bg2); border-bottom:1px solid var(--border); padding:0 24px; display:flex; align-items:center; height:56px; flex-shrink:0; }
nav h1 { font-size:18px; color:var(--accent); margin-right:32px; }
nav .tabs { display:flex; gap:4px; }
nav .tab { padding:8px 16px; border-radius:6px; cursor:pointer; font-size:14px; color:var(--text2); transition:all .15s; }
nav .tab:hover { background:var(--bg3); color:var(--text); }
nav .tab.active { background:var(--accent); color:#fff; }

/* Main */
main { flex:1; overflow:hidden; display:flex; }

/* Panels */
.panel { display:none; flex:1; overflow:hidden; }
.panel.active { display:flex; }

/* Q&A */
#qa { flex-direction:column; }
#qa-messages { flex:1; overflow-y:auto; padding:24px; }
.msg { max-width:800px; margin:0 auto 16px; padding:16px 20px; border-radius:12px; line-height:1.7; font-size:14px; }
.msg.user { background:var(--accent); color:#fff; margin-left:auto; max-width:600px; }
.msg.bot { background:var(--bg2); border:1px solid var(--border); }
.msg.bot h1,.msg.bot h2,.msg.bot h3 { color:var(--accent); margin:12px 0 8px; }
.msg.bot h1 { font-size:18px; } .msg.bot h2 { font-size:16px; } .msg.bot h3 { font-size:14px; }
.msg.bot p { margin:6px 0; }
.msg.bot code { background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:13px; }
.msg.bot pre { background:var(--bg); padding:12px; border-radius:8px; overflow-x:auto; margin:8px 0; }
.msg.bot pre code { background:none; padding:0; }
.msg.bot table { border-collapse:collapse; margin:8px 0; width:100%; }
.msg.bot th,.msg.bot td { border:1px solid var(--border); padding:6px 10px; font-size:13px; text-align:left; }
.msg.bot th { background:var(--bg3); }
.msg.bot ul,.msg.bot ol { margin:6px 0 6px 20px; }
.msg .sources { margin-top:12px; padding-top:12px; border-top:1px solid var(--border); }
.msg .sources a { color:var(--accent); font-size:12px; cursor:pointer; margin-right:12px; display:inline-block; margin-bottom:4px; }
.msg .sources a:hover { text-decoration:underline; }
#qa-input { border-top:1px solid var(--border); padding:16px 24px; background:var(--bg2); display:flex; gap:12px; max-width:850px; margin:0 auto; width:100%; }
#qa-input input { flex:1; background:var(--bg); border:1px solid var(--border); border-radius:8px; padding:12px 16px; color:var(--text); font-size:14px; outline:none; }
#qa-input input:focus { border-color:var(--accent); }
#qa-input button { background:var(--accent); color:#fff; border:none; border-radius:8px; padding:12px 24px; font-size:14px; cursor:pointer; }
#qa-input button:hover { opacity:.9; }
#qa-input button:disabled { opacity:.5; cursor:not-allowed; }
.loading { display:inline-block; } .loading::after { content:'...'; animation:dots 1.5s steps(4) infinite; }
@keyframes dots { 0%{content:''} 25%{content:'.'} 50%{content:'..'} 75%{content:'...'} }

/* Docs */
#docs { flex-direction:row; }
#doc-sidebar { width:300px; border-right:1px solid var(--border); overflow-y:auto; background:var(--bg2); flex-shrink:0; }
#doc-search { width:100%; padding:12px 16px; background:var(--bg); border:none; border-bottom:1px solid var(--border); color:var(--text); font-size:13px; outline:none; }
#doc-search:focus { border-bottom-color:var(--accent); }
.cat-group { border-bottom:1px solid var(--border); }
.cat-header { padding:10px 16px; font-size:12px; color:var(--accent); font-weight:600; cursor:pointer; display:flex; justify-content:space-between; }
.cat-header:hover { background:var(--bg3); }
.cat-items { display:none; }
.cat-items.open { display:block; }
.cat-item { padding:8px 16px 8px 28px; font-size:13px; color:var(--text2); cursor:pointer; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.cat-item:hover { background:var(--bg3); color:var(--text); }
.cat-item.active { background:var(--bg3); color:var(--accent); border-left:2px solid var(--accent); }
#doc-content { flex:1; overflow-y:auto; padding:32px 48px; }
#doc-content .doc-header { margin-bottom:24px; padding-bottom:16px; border-bottom:1px solid var(--border); }
#doc-content .doc-title { font-size:24px; color:var(--text); margin-bottom:8px; }
#doc-content .doc-meta { font-size:12px; color:var(--text2); }
#doc-content .doc-actions { margin-top:8px; display:flex; gap:8px; }
#doc-content .doc-actions button { background:var(--bg3); border:1px solid var(--border); color:var(--text); padding:6px 14px; border-radius:6px; font-size:12px; cursor:pointer; }
#doc-content .doc-actions button:hover { border-color:var(--accent); color:var(--accent); }
#doc-body { line-height:1.8; font-size:14px; }
#doc-body h1 { font-size:22px; color:var(--accent); margin:24px 0 12px; }
#doc-body h2 { font-size:18px; color:var(--accent); margin:20px 0 10px; padding-bottom:4px; border-bottom:1px solid var(--border); }
#doc-body h3 { font-size:15px; color:var(--accent3); margin:16px 0 8px; }
#doc-body p { margin:8px 0; }
#doc-body code { background:var(--bg3); padding:2px 6px; border-radius:4px; font-size:13px; }
#doc-body pre { background:var(--bg); padding:16px; border-radius:8px; overflow-x:auto; margin:12px 0; border:1px solid var(--border); }
#doc-body pre code { background:none; padding:0; }
#doc-body table { border-collapse:collapse; margin:12px 0; width:100%; }
#doc-body th,#doc-body td { border:1px solid var(--border); padding:8px 12px; font-size:13px; text-align:left; }
#doc-body th { background:var(--bg3); font-weight:600; }
#doc-body ul,#doc-body ol { margin:8px 0 8px 24px; }
#doc-body li { margin:4px 0; }
#doc-body blockquote { border-left:3px solid var(--accent); padding-left:16px; color:var(--text2); margin:12px 0; }
#doc-body a { color:var(--accent); text-decoration:none; }
#doc-body a:hover { text-decoration:underline; }
.empty-state { display:flex; align-items:center; justify-content:center; height:100%; color:var(--text2); font-size:14px; }

/* Graph */
#graph { position:relative; }
#graph svg { width:100%; height:100%; }
#graph-tooltip { position:absolute; padding:10px 14px; background:var(--bg2); border:1px solid var(--border); border-radius:8px; font-size:13px; pointer-events:none; opacity:0; transition:opacity .15s; z-index:10; max-width:350px; }
#graph-tooltip .gt-title { font-weight:600; color:var(--accent); }
#graph-tooltip .gt-path { color:var(--text2); font-size:11px; margin-top:4px; }
#graph-legend { position:absolute; top:16px; left:16px; background:var(--bg2); border:1px solid var(--border); border-radius:8px; padding:12px 16px; font-size:12px; z-index:5; }
#graph-legend h3 { color:var(--accent); margin-bottom:8px; font-size:13px; }
.gl-item { display:flex; align-items:center; gap:8px; margin:4px 0; }
.gl-dot { width:10px; height:10px; border-radius:50%; }
</style>
</head>
<body>

<nav>
  <h1>SaladLab Wiki</h1>
  <div class="tabs">
    <div class="tab active" onclick="showPanel('qa')">Q&A</div>
    <div class="tab" onclick="showPanel('docs')">Documents</div>
    <div class="tab" onclick="showPanel('graph')">Graph</div>
  </div>
</nav>

<main>
  <!-- Q&A Panel -->
  <div id="qa" class="panel active">
    <div id="qa-messages">
      <div class="msg bot">
        안녕하세요! SaladLab 위키에 대해 무엇이든 질문해주세요.<br>
        <span style="color:var(--text2);font-size:12px">예: "알파리뷰 포인트 지급 정책이 뭐야?", "리뷰 종류에는 뭐가 있어?", "위젯 시스템 V2 아키텍처 알려줘"</span>
      </div>
    </div>
    <div id="qa-input">
      <input id="q-input" type="text" placeholder="위키에 대해 질문하세요..." onkeydown="if(event.key==='Enter')askQ()">
      <button id="q-btn" onclick="askQ()">질문</button>
    </div>
  </div>

  <!-- Docs Panel -->
  <div id="docs" class="panel">
    <div id="doc-sidebar">
      <input id="doc-search" type="text" placeholder="문서 검색..." oninput="filterDocs(this.value)">
      <div id="doc-tree"></div>
    </div>
    <div id="doc-content">
      <div class="empty-state">좌측에서 문서를 선택하세요</div>
    </div>
  </div>

  <!-- Graph Panel -->
  <div id="graph" class="panel">
    <div id="graph-legend">
      <h3>Knowledge Graph</h3>
      <div class="gl-item"><div class="gl-dot" style="background:#58a6ff"></div> Projects</div>
      <div class="gl-item"><div class="gl-dot" style="background:#3fb950"></div> PRD</div>
      <div class="gl-item"><div class="gl-dot" style="background:#f0883e"></div> Core System</div>
      <div class="gl-item"><div class="gl-dot" style="background:#f778ba"></div> Review Policy (Dev)</div>
      <div class="gl-item"><div class="gl-dot" style="background:#a371f7"></div> Meetings</div>
      <div class="gl-item"><div class="gl-dot" style="background:#ffd33d"></div> Data Analysis</div>
    </div>
    <div id="graph-tooltip"><div class="gt-title"></div><div class="gt-path"></div></div>
  </div>
</main>

<script>
const API = '';
let allDocs = [];
let graphRendered = false;

function showPanel(id) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelector(`.tab[onclick="showPanel('${id}')"]`).classList.add('active');
  if (id === 'graph' && !graphRendered) { renderGraph(); graphRendered = true; }
  if (id === 'docs' && allDocs.length === 0) loadDocTree();
}

// ── Q&A ──
async function askQ() {
  const input = document.getElementById('q-input');
  const btn = document.getElementById('q-btn');
  const q = input.value.trim();
  if (!q) return;

  const msgs = document.getElementById('qa-messages');
  msgs.innerHTML += `<div class="msg user">${escHtml(q)}</div>`;
  msgs.innerHTML += `<div class="msg bot" id="thinking"><span class="loading">생각하는 중</span></div>`;
  msgs.scrollTop = msgs.scrollHeight;
  input.value = '';
  btn.disabled = true;

  try {
    const res = await fetch(API + '/api/qa', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({question: q})
    });
    const data = await res.json();
    const el = document.getElementById('thinking');

    let html = marked.parse(data.answer);
    if (data.sources && data.sources.length > 0) {
      html += '<div class="sources">📎 참조 문서: ';
      data.sources.forEach(s => {
        html += `<a onclick="showPanel('docs');loadDoc('${s.id}')">${s.title}</a>`;
      });
      html += '</div>';
    }
    el.removeAttribute('id');
    el.innerHTML = html;
  } catch(e) {
    document.getElementById('thinking').innerHTML = '⚠️ 오류가 발생했습니다: ' + e.message;
    document.getElementById('thinking').removeAttribute('id');
  }
  btn.disabled = false;
  msgs.scrollTop = msgs.scrollHeight;
}

// ── Docs ──
async function loadDocTree() {
  const res = await fetch(API + '/api/categories');
  const cats = await res.json();
  const tree = document.getElementById('doc-tree');
  tree.innerHTML = '';

  for (const [cat, docs] of Object.entries(cats).sort()) {
    const group = document.createElement('div');
    group.className = 'cat-group';
    const header = document.createElement('div');
    header.className = 'cat-header';
    header.textContent = cat;
    const badge = document.createElement('span');
    badge.textContent = docs.length;
    badge.style.cssText = 'background:var(--bg3);padding:2px 8px;border-radius:10px;font-size:11px;color:var(--text2)';
    header.appendChild(badge);
    header.onclick = () => items.classList.toggle('open');

    const items = document.createElement('div');
    items.className = 'cat-items';
    docs.forEach(d => {
      const item = document.createElement('div');
      item.className = 'cat-item';
      item.textContent = d.title;
      item.onclick = () => loadDoc(d.id);
      items.appendChild(item);
      allDocs.push({...d, category: cat, el: item});
    });
    group.appendChild(header);
    group.appendChild(items);
    tree.appendChild(group);
  }
  // open first category
  const first = tree.querySelector('.cat-items');
  if (first) first.classList.add('open');
}

async function loadDoc(id) {
  const res = await fetch(API + '/api/docs/' + id);
  const doc = await res.json();
  const content = document.getElementById('doc-content');

  document.querySelectorAll('.cat-item').forEach(el => el.classList.remove('active'));
  const match = allDocs.find(d => d.id === id);
  if (match && match.el) {
    match.el.classList.add('active');
    const catItems = match.el.parentElement;
    if (!catItems.classList.contains('open')) catItems.classList.add('open');
  }

  content.innerHTML = `
    <div class="doc-header">
      <div class="doc-title">${escHtml(doc.title)}</div>
      <div class="doc-meta">📁 ${escHtml(doc.path)} · 🏷️ ${(doc.tags||[]).join(', ') || '태그 없음'}</div>
      <div class="doc-actions">
        <button onclick="copyRaw('${id}')">📋 원본 복사</button>
        <button onclick="downloadRaw('${id}','${escHtml(doc.title)}')">⬇️ 다운로드</button>
      </div>
    </div>
    <div id="doc-body">${doc.html}</div>`;
}

async function copyRaw(id) {
  const res = await fetch(API + '/api/docs/' + id);
  const doc = await res.json();
  await navigator.clipboard.writeText(doc.raw);
  alert('원본 마크다운이 클립보드에 복사되었습니다!');
}

function downloadRaw(id, title) {
  window.open(API + '/api/docs/' + id + '/raw', '_blank');
}

function filterDocs(query) {
  const q = query.toLowerCase();
  allDocs.forEach(d => {
    const match = !q || d.title.toLowerCase().includes(q);
    d.el.style.display = match ? '' : 'none';
  });
  if (q) document.querySelectorAll('.cat-items').forEach(el => el.classList.add('open'));
}

// ── Graph ──
async function renderGraph() {
  const res = await fetch(API + '/api/graph');
  const data = await res.json();
  const container = document.getElementById('graph');
  const w = container.clientWidth, h = container.clientHeight;

  const colorMap = {2:'#58a6ff',3:'#3fb950',4:'#f0883e',5:'#f778ba',6:'#a371f7',7:'#ffd33d'};
  const svg = d3.select('#graph').append('svg').attr('width',w).attr('height',h);
  const g = svg.append('g');
  svg.call(d3.zoom().scaleExtent([0.2,5]).on('zoom', e => g.attr('transform',e.transform)));

  const linkCount = {};
  data.nodes.forEach(n => linkCount[n.id] = 0);
  data.links.forEach(l => { linkCount[l.source]=(linkCount[l.source]||0)+1; linkCount[l.target]=(linkCount[l.target]||0)+1; });

  const sim = d3.forceSimulation(data.nodes)
    .force('link', d3.forceLink(data.links).id(d=>d.id).distance(80))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('center', d3.forceCenter(w/2, h/2))
    .force('collision', d3.forceCollide().radius(30));

  const link = g.selectAll('line').data(data.links).join('line')
    .attr('stroke','#30363d').attr('stroke-opacity',0.4).attr('stroke-width',d=>d.value||1);

  const node = g.selectAll('g.node').data(data.nodes).join('g').attr('class','node')
    .call(d3.drag().on('start',(e,d)=>{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y})
      .on('drag',(e,d)=>{d.fx=e.x;d.fy=e.y}).on('end',(e,d)=>{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null}));

  node.append('circle')
    .attr('r', d => 5 + (linkCount[d.id]||0)*1.5)
    .attr('fill', d => colorMap[d.group]||'#666')
    .attr('stroke','#0d1117').attr('stroke-width',1.5)
    .style('cursor','pointer');

  node.append('text').text(d=>d.id.length>20?d.id.slice(0,18)+'…':d.id)
    .attr('dx',12).attr('dy',4).attr('font-size','10px').attr('fill','#c9d1d9')
    .style('text-shadow','0 0 4px #0d1117,0 0 4px #0d1117').style('pointer-events','none');

  const tooltip = document.getElementById('graph-tooltip');
  node.on('mouseover',(e,d)=>{
    tooltip.querySelector('.gt-title').textContent = d.id;
    tooltip.querySelector('.gt-path').textContent = d.path||'';
    tooltip.style.opacity=1; tooltip.style.left=(e.pageX+12)+'px'; tooltip.style.top=(e.pageY-28)+'px';
    link.attr('stroke-opacity',l=>(l.source.id===d.id||l.target.id===d.id)?1:0.1);
    node.select('circle').attr('opacity',n=>{
      if(n.id===d.id) return 1;
      const connected = data.links.some(l=>(l.source.id===d.id&&l.target.id===n.id)||(l.target.id===d.id&&l.source.id===n.id));
      return connected?1:0.2;
    });
  }).on('mouseout',()=>{
    tooltip.style.opacity=0;
    link.attr('stroke-opacity',0.4);
    node.select('circle').attr('opacity',1);
  }).on('click',(e,d)=>{
    // find doc by path
    const match = allDocs.find(doc => d.path && d.path.includes(doc.title));
    if(match) { showPanel('docs'); loadDoc(match.id); }
  });

  sim.on('tick',()=>{
    link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
    node.attr('transform',d=>`translate(${d.x},${d.y})`);
  });

  setTimeout(()=>{
    const xs=data.nodes.map(n=>n.x),ys=data.nodes.map(n=>n.y);
    const bx=[Math.min(...xs)-50,Math.max(...xs)+50],by=[Math.min(...ys)-50,Math.max(...ys)+50];
    const bw=bx[1]-bx[0],bh=by[1]-by[0];
    const scale=Math.min(w/bw,h/bh,1.5)*0.85;
    const tx=w/2-((bx[0]+bx[1])/2)*scale,ty=h/2-((by[0]+by[1])/2)*scale;
    svg.transition().duration(800).call(d3.zoom().transform,d3.zoomIdentity.translate(tx,ty).scale(scale));
  }, 2500);
}

function escHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
</script>
</body>
</html>"""


if __name__ == "__main__":
    import uvicorn
    print(f"\\n📚 SaladLab Wiki Server")
    print(f"   Documents loaded: {len(DOCUMENTS)}")
    print(f"   Open: http://localhost:8000\\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
