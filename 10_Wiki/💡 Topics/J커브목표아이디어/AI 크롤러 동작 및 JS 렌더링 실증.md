---
id: ai-crawler-js-rendering-evidence-20260515
title: "AI 크롤러 동작 및 JS 렌더링 실증"
source: "conversation-20260515, Vercel/Cloudflare/OpenAI/Anthropic/Perplexity 공식 문서"
category: "[[10_Wiki/💡 Topics/J커브목표아이디어]]"
confidence_score: 0.90
tags: [AI크롤러, GPTBot, ClaudeBot, PerplexityBot, SSR, CSR, JavaScript렌더링]
status: active
last_reinforced: 2026-05-15
---

# AI 크롤러 동작 및 JS 렌더링 실증

## 📌 한 줄 통찰

> 주요 AI 크롤러(GPTBot, ClaudeBot, PerplexityBot) 중 JavaScript를 렌더링하는 크롤러는 없다. CSR 기반 리뷰 위젯은 AI에게 보이지 않으며, 정적 HTML 또는 JSON-LD 마크업이 필수다.

---

## 1. 크롤러별 JS 렌더링 능력 — 실증 데이터

| 크롤러 | JS 렌더링 | 근거 | 출처 |
|--------|:---:|------|------|
| **GPTBot** (OpenAI) | ❌ | 5억 건 이상 fetch 분석, JS 실행 증거 0 | Vercel 분석 |
| **ClaudeBot** (Anthropic) | ❌ | 공식 문서 — 중요 콘텐츠는 초기 HTML 응답에 포함 필요 | Anthropic 공식 |
| **PerplexityBot** | ❌ | HTML 소스만 읽음, JS 렌더링 없음 | Perplexity 공식 |
| **Googlebot** | ✅ | WRS(Web Rendering Service)로 JS 실행 가능 | Google 공식 |

**핵심**: GPTBot은 JS 파일을 다운로드(요청의 약 11.5%)하지만 **실행하지는 않음**.

---

## 2. 크롤러별 공식 문서 및 정책

### 2.1 OpenAI (GPTBot / OAI-SearchBot / ChatGPT-User)

- 공식 문서: [developers.openai.com/api/docs/bots](https://developers.openai.com/api/docs/bots)
- **2025년 12월 9일 정책 변경**: ChatGPT-User는 사용자 발의 작업에 대해 **robots.txt를 더 이상 준수하지 않음**
- OAI-SearchBot과 GPTBot는 중복 크롤링 방지를 위해 정보 공유
- 세 가지 크롤러 각각 별도로 robots.txt 제어 필요

### 2.2 Anthropic (ClaudeBot / Claude-User / Claude-SearchBot)

- 공식 문서: [support.claude.com](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- **2026년 2월 업데이트**: ClaudeBot(훈련 데이터), Claude-User(사용자 질문 시 fetch), Claude-SearchBot(검색 인덱싱) 분리
- robots.txt 존중, **Crawl-delay 확장 지원**

### 2.3 Perplexity (PerplexityBot / Perplexity-User)

- 공식 문서: [docs.perplexity.ai/docs/resources/perplexity-crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers)
- PerplexityBot은 robots.txt 준수 (변경 사항 ~24시간 내 전파)
- **AI 파운데이션 모델 훈련에는 사용되지 않음** — 검색 결과 참조 및 링크용 인덱싱에만 사용
- Perplexity-User는 robots.txt를 따르지 않으며, 실시간 브라우징처럼 동작
- Cloudflare 보고: Perplexity가 스텔스/미공개 크롤러를 사용하여 no-crawl 지시 우회 증거 발견

---

## 3. Cloudflare 2025 AI 크롤러 트래픽 통계

| 크롤러 | 2024.5 점유율 | 2025.5 점유율 | 요청 증감률 |
|--------|:---:|:---:|:---:|
| GPTBot | 2.2% | 7.7% | +305% |
| ClaudeBot | 11.7% | 5.4% | -46% |
| PerplexityBot | ~0% | 0.2% | +157,490% |
| Meta-ExternalAgent | 신규 | 19% | 신규 진입 |

- GPTBot은 전체 크롤러 중 #9 → #3으로 상승
- robots.txt 차단이 가장 많은 크롤러: GPTBot (250개 도메인 완전 차단, 62개 부분 차단)
- ChatGPT는 현재 Googlebot보다 **3.6배 더 많이** 크롤링

출처:
- [Vercel — The rise of the AI crawler](https://vercel.com/blog/the-rise-of-the-ai-crawler)
- [Cloudflare — From Googlebot to GPTBot](https://blog.cloudflare.com/from-googlebot-to-gptbot-whos-crawling-your-site-in-2025/)

---

## 4. 알파리뷰에 대한 시사점

알파리뷰 위젯은 현재 **CSR(Client-Side Rendering)** 으로 동작한다.

```
현재 흐름:
  AI 크롤러 방문 → 상품 페이지 HTML 수신 → JS 미실행 → 리뷰 본문 없음
  → AI는 AggregateRating(별점 4.8, 리뷰 273개)만 인식

목표 흐름:
  AI 크롤러 방문 → 상품 페이지 HTML 수신 → 정적 HTML에 리뷰 포함
  → AI가 개별 리뷰 본문, 별점, 작성자, 이미지 URL까지 인식
```

**기능 1(정적 HTML 출력)이 게이트키퍼**: 이것이 해결되지 않으면 구조화 마크업(기능 2), 출처 신호(기능 4) 등 나머지 기능이 전부 무력화됨.

---

## 🔗 지식 연결

- **Related:** [[GEO 시대 리뷰 AI-Readability 글로벌 동향]], [[[리뷰] AI-readablility 확보]]
- **Parent:** [[10_Wiki/💡 Topics/J커브목표아이디어]]
