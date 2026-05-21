"""
SaladLab LLM Wiki — Vercel Serverless Function
BM25 검색 + 문서 브라우저 + 지식 그래프
"""
import os
import re
import json
import hashlib
from pathlib import Path
from typing import Optional

import yaml
from rank_bm25 import BM25Okapi
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = PROJECT_ROOT / "10_Wiki"
META_DIR = PROJECT_ROOT / "20_Meta"

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


def _extract_category(path: str) -> str:
    parts = path.replace("10_Wiki/", "").split("/")
    if len(parts) >= 2:
        return "/".join(parts[:-1])
    return "기타"


def _tokenize(text: str) -> list[str]:
    text = re.sub(r"[^\w가-힣]", " ", text)
    return [t for t in text.split() if len(t) > 1]


def _render_md(body: str) -> str:
    import markdown
    return markdown.markdown(body, extensions=["tables", "fenced_code", "toc", "nl2br"])


def load_documents() -> list[dict]:
    docs = []
    for md_file in sorted(WIKI_DIR.rglob("*.md")):
        raw = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(raw)
        rel_path = str(md_file.relative_to(PROJECT_ROOT))
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
            "last_reinforced": fm.get("last_reinforced", ""),
            "owner": fm.get("owner", ""),
            "body": body,
            "raw": raw,
        })
    return docs


DOCUMENTS: list[dict] = []
BM25_INDEX: Optional[BM25Okapi] = None


def build_search_index():
    global DOCUMENTS, BM25_INDEX
    DOCUMENTS = load_documents()
    corpus = [_tokenize(d["title"] + " " + " ".join(d.get("tags") or []) + " " + d["body"]) for d in DOCUMENTS]
    if corpus:
        BM25_INDEX = BM25Okapi(corpus)


build_search_index()


# ── Search ──

def search_docs(query: str, top_k: int = 5) -> list[dict]:
    if not BM25_INDEX:
        return []
    tokens = _tokenize(query)
    if not tokens:
        return []
    scores = BM25_INDEX.get_scores(tokens)
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    results = []
    for idx in ranked:
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


def _build_search_answer(question: str, results: list[dict]) -> str:
    lines = [f"**\"{question}\"** 에 대한 검색 결과입니다.\n"]
    for i, r in enumerate(results):
        doc = next((d for d in DOCUMENTS if d["id"] == r["id"]), None)
        if not doc:
            continue
        relevance = min(int(r["score"] / max(results[0]["score"], 1) * 100), 100)
        excerpt = _extract_relevant_section(doc["body"], question)
        lines.append(f"### {i+1}. 📄 {doc['title']}")
        lines.append(f"> 📁 `{doc['path']}` · 관련도 {relevance}%\n")
        lines.append(excerpt)
        lines.append("")
    if not results:
        lines.append("관련 문서를 찾지 못했습니다.")
    return "\n".join(lines)


# ── Q&A ──

class QARequest(BaseModel):
    question: str


@app.post("/api/qa")
async def ask_question(req: QARequest):
    results = search_docs(req.question, top_k=5)
    if not results:
        return {"answer": "관련 문서를 찾지 못했습니다.", "sources": []}

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        context_parts = []
        for i, r in enumerate(results):
            doc = next((d for d in DOCUMENTS if d["id"] == r["id"]), None)
            if doc:
                context_parts.append(f"### 문서 {i+1}: {doc['title']}\n경로: {doc['path']}\n\n{doc['body'][:3000]}")
        context = "\n\n---\n\n".join(context_parts)
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            msg = client.messages.create(
                model="claude-sonnet-4-6-20250514",
                max_tokens=2000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": f"[컨텍스트]\n{context}\n\n---\n[질문]\n{req.question}"}],
            )
            return {"answer": msg.content[0].text, "sources": results}
        except Exception:
            pass

    answer = _build_search_answer(req.question, results)
    return {"answer": answer, "sources": results}


SYSTEM_PROMPT = """너는 SaladLab의 사내 위키 지식 전문가다.
아래 제공된 위키 문서 컨텍스트만을 기반으로 질문에 답변하라.

규칙:
1. 컨텍스트에 없는 정보는 "위키에 해당 정보가 없습니다"라고 답하라.
2. 답변에 출처를 반드시 표기하라. 형식: 📄 [문서명]
3. 수식, 상태 전이, 테이블 데이터는 원문 그대로 인용하라.
4. 답변은 한국어 마크다운으로 작성하라."""


# ── Document APIs ──

@app.get("/api/docs")
async def list_documents(q: str = Query(default="")):
    if q:
        return search_docs(q, top_k=20)
    return [{"id": d["id"], "title": d["title"], "path": d["path"], "category": d["category"], "tags": d["tags"], "confidence": d["confidence"], "last_reinforced": d.get("last_reinforced", "")} for d in DOCUMENTS]


@app.get("/api/docs/{doc_id}")
async def get_document(doc_id: str):
    doc = next((d for d in DOCUMENTS if d["id"] == doc_id), None)
    if not doc:
        raise HTTPException(404, "Document not found")
    html = _render_md(doc["body"])
    return {"id": doc["id"], "title": doc["title"], "path": doc["path"], "category": doc["category"],
            "tags": doc["tags"], "confidence": doc["confidence"], "last_reinforced": doc.get("last_reinforced", ""),
            "html": html, "raw": doc["raw"], "body": doc["body"]}


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
