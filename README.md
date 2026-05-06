# P-Reinforce Wiki (The Autonomous Gardener)

P-Reinforce는 사용자가 입력한 파편화된 지식을 스스로 분류하고, 구조화하며, 연결하는 **"강화학습 기반 영속적 위키 결합 시스템"**입니다.

## 디렉토리 구조

```text
WIKI/
├── 00_Staging/              # [입력 대기] 노션 등 외부에서 수집된 원시 데이터
│   └── Trash/               # Cleaner가 반려한 문서
│
├── 00_Raw/                  # [정제 완료] Cleaner 통과한 원본 (날짜별 보관)
│   └── YYYY-MM-DD/
│
├── 10_Wiki/                 # [지식 엔진] P-Reinforce가 관리하는 메인 무대
│   ├── 🛠️ Projects/         # 목표 중심 — 프로젝트별 지식 묶음
│   │   └── SaladLab/        #   알파리뷰·업셀·푸시·앱스 가이드
│   ├── 💡 Topics/           # 개념 중심 — 자율 생성 분류
│   │   ├── 코어시스템/       #   Type/Status, DB 스키마
│   │   ├── 데이터분석/       #   리뷰 데이터 분석, 인사이트
│   │   └── 미팅록/          #   회의 기록, 조직 논의
│   └── PRD/                 # 프로덕트 요구사항 정의서 + 기능 명세
│       └── SaladLab/
│
├── 20_Meta/                 # [시스템] 에이전트 메타데이터
│   ├── Graph.json           # 지식 간 연결 그래프
│   ├── Policy.md            # RL 분류 정책 (사용자 피드백 반영)
│   └── Index.md             # 전체 목차 (Table of Contents)
│
├── scripts/                 # 유틸리티 스크립트
├── rag_mcp_server/          # RAG 기반 MCP 서버
│
├── Skill_LLMWIKI_강화학습기반구조화 로직.md   # P-Reinforce 코어 스킬
└── Skill_LLMWIKI_Notion_Cleaner.md            # 노션 데이터 전처리 스킬
```

## 데이터 흐름

```
노션/외부 → 00_Staging → [Notion Cleaner] → 00_Raw/YYYY-MM-DD/
                                                    ↓
                                            [P-Reinforce]
                                                    ↓
                                            10_Wiki/ (위키화)
                                                    ↓
                                            20_Meta/ (그래프·인덱스 갱신)
                                                    ↓
                                            git commit & push
```

## 판단 원리 (RL Logic)

보상 함수: `R = 0.4×(분류 정확도) + 0.35×(그래프 조밀성) + 0.25×(사용자 만족도)`

| 규칙 | 임계치 |
|------|--------|
| 기존 폴더 배치 | 유사도 ≥ 85% |
| 신규 폴더 생성 | 유사도 < 85% |
| 폴더 세분화 제안 | 파일 > 12개 |

## 에이전트 훈련 가이드

- **칭찬**: "이 분류 완벽해." → 유사 주제 가중치 극대화
- **수정**: "이건 '코딩'이 아니라 '비즈니스' 폴더로 옮겨줘." → 경계선 재설정
- **방치**: 에이전트 구조를 그대로 사용 → 암묵적 보상, 정책 고착
