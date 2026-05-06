# Graph Report - .  (2026-05-06)

## Corpus Check
- 3 files · ~172,127 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 14 nodes · 17 edges · 3 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]

## God Nodes (most connected - your core abstractions)
1. `run_server()` - 5 edges
2. `clean_notion_markdown()` - 3 edges
3. `handle_tools_call()` - 3 edges
4. `process_batch()` - 2 edges
5. `handle_query()` - 2 edges
6. `send_response()` - 2 edges
7. `handle_initialize()` - 2 edges
8. `handle_tools_list()` - 2 edges
9. `1. 노션 토글(<details><summary>)을 마크다운 헤더(###) 기반으로 평탄화     2. 과도한 빈 줄 여백 제거` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.43
Nodes (6): handle_initialize(), handle_query(), handle_tools_call(), handle_tools_list(), run_server(), send_response()

### Community 1 - "Community 1"
Cohesion: 0.67
Nodes (3): clean_notion_markdown(), process_batch(), 1. 노션 토글(<details><summary>)을 마크다운 헤더(###) 기반으로 평탄화     2. 과도한 빈 줄 여백 제거

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **1 isolated node(s):** `1. 노션 토글(<details><summary>)을 마크다운 헤더(###) 기반으로 평탄화     2. 과도한 빈 줄 여백 제거`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 2`** (2 nodes): `is_valid_file()`, `build_index.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `1. 노션 토글(<details><summary>)을 마크다운 헤더(###) 기반으로 평탄화     2. 과도한 빈 줄 여백 제거` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._