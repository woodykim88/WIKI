# Graph Report - .  (2026-05-21)

## Corpus Check
- 5 files · ~216,077 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 53 nodes · 78 edges · 12 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]

## God Nodes (most connected - your core abstractions)
1. `run_server()` - 5 edges
2. `load_documents()` - 4 edges
3. `_tokenize()` - 4 edges
4. `build_search_index()` - 4 edges
5. `search_docs()` - 4 edges
6. `ask_question()` - 4 edges
7. `_tokenize()` - 4 edges
8. `load_documents()` - 4 edges
9. `search_docs()` - 4 edges
10. `clean_notion_markdown()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `build_search_index()` --calls--> `_tokenize()`  [EXTRACTED]
  rag_mcp_server/wiki_server.py → rag_mcp_server/wiki_server.py  _Bridges community 8 → community 3_
- `_extract_relevant_section()` --calls--> `_tokenize()`  [EXTRACTED]
  rag_mcp_server/wiki_server.py → rag_mcp_server/wiki_server.py  _Bridges community 8 → community 5_
- `_extract_relevant_section()` --calls--> `_tokenize()`  [EXTRACTED]
  api/index.py → api/index.py  _Bridges community 6 → community 9_
- `build_search_index()` --calls--> `load_documents()`  [EXTRACTED]
  api/index.py → api/index.py  _Bridges community 10 → community 6_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.43
Nodes (6): handle_initialize(), handle_query(), handle_tools_call(), handle_tools_list(), run_server(), send_response()

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (1): SaladLab LLM Wiki — Prototype Web Server BM25 검색 + Claude Q&A + 문서 브라우저 + 지식 그래프

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (3): get_document(), SaladLab LLM Wiki — Vercel Serverless Function BM25 검색 + 문서 브라우저 + 지식 그래프, _render_md()

### Community 3 - "Community 3"
Cohesion: 0.4
Nodes (5): build_search_index(), _extract_category(), load_documents(), parse_frontmatter(), reindex()

### Community 4 - "Community 4"
Cohesion: 0.67
Nodes (3): clean_notion_markdown(), process_batch(), 1. 노션 토글(<details><summary>)을 마크다운 헤더(###) 기반으로 평탄화     2. 과도한 빈 줄 여백 제거

### Community 5 - "Community 5"
Cohesion: 0.5
Nodes (4): ask_question(), _build_search_answer(), _extract_relevant_section(), get_anthropic_client()

### Community 6 - "Community 6"
Cohesion: 0.5
Nodes (4): build_search_index(), list_documents(), search_docs(), _tokenize()

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (3): BaseModel, QARequest, QARequest

### Community 8 - "Community 8"
Cohesion: 0.67
Nodes (3): list_documents(), search_docs(), _tokenize()

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (3): ask_question(), _build_search_answer(), _extract_relevant_section()

### Community 10 - "Community 10"
Cohesion: 0.67
Nodes (3): _extract_category(), load_documents(), parse_frontmatter()

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **3 isolated node(s):** `1. 노션 토글(<details><summary>)을 마크다운 헤더(###) 기반으로 평탄화     2. 과도한 빈 줄 여백 제거`, `SaladLab LLM Wiki — Prototype Web Server BM25 검색 + Claude Q&A + 문서 브라우저 + 지식 그래프`, `SaladLab LLM Wiki — Vercel Serverless Function BM25 검색 + 문서 브라우저 + 지식 그래프`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 11`** (2 nodes): `is_valid_file()`, `build_index.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `QARequest` connect `Community 7` to `Community 1`?**
  _High betweenness centrality (0.272) - this node is a cross-community bridge._
- **Why does `QARequest` connect `Community 7` to `Community 2`?**
  _High betweenness centrality (0.269) - this node is a cross-community bridge._
- **What connects `1. 노션 토글(<details><summary>)을 마크다운 헤더(###) 기반으로 평탄화     2. 과도한 빈 줄 여백 제거`, `SaladLab LLM Wiki — Prototype Web Server BM25 검색 + Claude Q&A + 문서 브라우저 + 지식 그래프`, `SaladLab LLM Wiki — Vercel Serverless Function BM25 검색 + 문서 브라우저 + 지식 그래프` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._