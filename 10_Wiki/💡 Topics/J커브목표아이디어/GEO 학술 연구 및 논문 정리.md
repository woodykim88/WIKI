---
id: geo-academic-research-papers-20260515
title: "GEO 학술 연구 및 논문 정리"
source: "conversation-20260515, arXiv, KDD 2024, NAACL 2025, BrightEdge"
category: "[[10_Wiki/💡 Topics/J커브목표아이디어]]"
confidence_score: 0.85
tags: [GEO, 논문, 학술연구, AI인용, 구조화데이터, LLM, 검색최적화]
status: active
last_reinforced: 2026-05-15
---

# GEO 학술 연구 및 논문 정리

## 📌 한 줄 통찰

> GEO 핵심 논문(Aggarwal et al., KDD 2024)에 따르면, 통계·인용문·출처를 포함하면 AI 가시성이 40%+ 증가한다. 리뷰 데이터는 이 요소를 자연적으로 포함하는 최적의 GEO 자산이다.

---

## 1. 핵심 논문: GEO: Generative Engine Optimization

| 항목 | 내용 |
|------|------|
| 제목 | GEO: Generative Engine Optimization |
| 저자 | Pranjal Aggarwal, Vishvak Murahari, Tanmay Rajpurohit, Ashwin Kalyan, Karthik Narasimhan, Ameet Deshpande |
| 소속 | Princeton University, Georgia Tech, Allen Institute of AI, IIT Delhi |
| 발표 | **KDD 2024** (30th ACM SIGKDD, 바르셀로나) |
| arXiv | [2311.09735](https://arxiv.org/abs/2311.09735) (초기 2023.11, 최신 v3 2024.06) |
| 공식 사이트 | [generative-engines.com](https://generative-engines.com/) |

### GEO 전략별 AI 가시성 증가 효과

| 전략 | 설명 | 가시성 증가폭 |
|------|------|:---:|
| **Statistics Addition** | 정량적 통계 포함 | **+40% 이상** |
| **Cite Sources** | 신뢰할 수 있는 출처 인용 추가 | **+40% 이상** |
| **Quotation Addition** | 관련 출처의 인용문 포함 | **+40% 이상** |
| **Fluency Optimization** | 텍스트 유창성 개선 | 유의미 |
| **Easy-to-Understand** | 언어 단순화 | 유의미 |
| **최적 조합** (Fluency + Statistics) | | 단일 전략 대비 **+5.5%** |

### 도메인별 최적 전략

- **Law & Government, Opinion**: Statistics Addition이 가장 효과적
- **People & Society, Explanation, History**: Quotation Addition이 가장 효과적

### 리뷰 데이터와의 연결

리뷰는 GEO 논문의 최적 요소를 자연적으로 포함:

| GEO 최적 요소 | 리뷰 데이터의 대응 |
|-------------|-----------------|
| 통계 (Statistics) | 별점, 리뷰 수, 재구매율 |
| 인용문 (Quotations) | 실제 사용자의 원문 |
| 출처 인용 (Citations) | 구매 인증, 외부 플랫폼 연동 |
| 최신성 (Freshness) | 매일 새 리뷰 생성 |

---

## 2. LLM 소스 인용/선택 관련 연구

### 2.1 Source Coverage and Citation Bias in LLM-based vs. Traditional Search Engines

- arXiv: [2512.09483](https://arxiv.org/abs/2512.09483) (2024.12)
- 55,936개 쿼리, 6개 LLM 검색 엔진 + 2개 전통 검색 엔진 분석
- LLM-SE는 TSE보다 **더 다양한 도메인을 인용** (37% 고유 도메인)
- **ChatGPT가 인용한 소스의 평균 도메인 연령: 17년** → 확립된 기관 우대
- 그러나 신뢰성, 정치적 중립성, 안전성에서는 TSE를 능가하지 못함

### 2.2 Large Language Models Reflect Human Citation Patterns with a Heightened Citation Bias

- NAACL 2025 Findings
- LLM은 인간의 인용 패턴을 반영하되, **고인용 논문 선호 편향이 더 강함**

### 2.3 2025 AI Visibility Report (The Digital Bloom)

- AI 시스템은 백링크보다 **브랜드 권위와 콘텐츠 포괄성**을 우선시
- **브랜드 검색량**(백링크가 아닌)이 AI 인용의 가장 강력한 예측 변수
- AI 봇 트래픽의 65%는 **지난 1년 내 발행된 콘텐츠** 대상
- ChatGPT와 Perplexity **양쪽 모두 인용되는 도메인은 11%에 불과**
- 출처: [The Digital Bloom — 2025 AI Citation Report](https://thedigitalbloom.com/learn/2025-ai-citation-llm-visibility-report/)

---

## 3. 구조화 데이터의 AI 인용 영향 — 실증 수치

| 지표 | 수치 | 출처 |
|------|:---:|------|
| Google AI Overview 인용 페이지 중 구조화 데이터 보유 | **65%** | BrightEdge |
| ChatGPT 인용 페이지 중 구조화 데이터 보유 | **71%** | BrightEdge |
| 구조화 데이터 + FAQ 사이트의 AI 인용 증가 | **+44%** | BrightEdge |
| 텍스트+이미지+구조화 데이터 통합 시 AI 선택률 | **+156%** | xSeek (15,847건) |
| Product + Offer 쌍 구현 이커머스의 상업 AI 인용 | **+29%** | xSeek |

### 반론 및 한계

- **2024년 12월 Search/Atlas 연구**: 스키마 커버리지와 인용률 사이 **상관관계 없음** 발견
- 현재까지 스키마의 AI 검색 가시성 영향에 대한 **동료 심사 연구는 없음**
- Google 공식 입장: AI Overviews를 위한 특별한 schema.org는 불필요

→ PRD의 기능 5(AI 크롤러 측정)가 이 불확실성을 자체 검증하는 장치로 적절

---

## 4. Google AI Overviews 성장 추이

- 2025년 2월 31% → 2026년 2월 **48%** (전체 추적 쿼리 기준)
- 200개 이상 국가, 40개 이상 언어에서 제공
- AI Overviews에 인용된 페이지의 65%가 구조화 데이터 포함

---

## 🔗 지식 연결

- **Related:** [[GEO 시대 리뷰 AI-Readability 글로벌 동향]], [[AI 크롤러 동작 및 JS 렌더링 실증]], [[리뷰 구조화 데이터 채택 현황]]
- **Parent:** [[10_Wiki/💡 Topics/J커브목표아이디어]]
