# P-Reinforce Wiki — Claude Code 프로젝트 컨텍스트

이 프로젝트는 옵시디언 기반의 단일 지식 창고(Personal Wiki)입니다.
SaladLab 소속 PM이 업무 중 생성하는 미팅록, PRD, 제품 가이드 등을 자동 분류·구조화합니다.

## 핵심 스킬 파일

지식동기화 작업 시 반드시 아래 스킬을 먼저 읽고 절차를 따릅니다:
- `Skill_LLMWIKI_강화학습기반구조화 로직.md` — P-Reinforce 코어 로직 (분류, 위키 템플릿, Git 동기화)
- `Skill_LLMWIKI_Notion_Cleaner.md` — Staging → Raw 전처리 (서식 평탄화, 가치 평가)

## 폴더 구조 요약

| 경로 | 역할 |
|------|------|
| `00_Staging/` | 외부 데이터 입력 대기 |
| `00_Raw/YYYY-MM-DD/` | Cleaner 통과한 원본 보관 |
| `10_Wiki/🛠️ Projects/` | 제품별 지식 (SaladLab) |
| `10_Wiki/💡 Topics/` | 개념 중심 분류 (코어시스템, 데이터분석, 미팅록) |
| `10_Wiki/PRD/` | PRD + FSD |
| `20_Meta/` | Graph.json, Policy.md, Index.md |

## 작업 후 필수 절차

1. `20_Meta/Index.md` — 문서 추가/삭제 시 목차 갱신
2. `20_Meta/Graph.json` — 지식 연결 변경 시 노드/링크 갱신
3. `20_Meta/Policy.md` — 사용자 피드백 발생 시 이력 추가
4. Git commit — `[P-Reinforce] 지식동기화 - {{요약}}` 형식

## 분류 정책 핵심

- 유사도 ≥ 85% → 기존 폴더 배치
- 유사도 < 85% → 신규 폴더 생성
- 폴더 내 파일 > 12개 → 세분화 제안
- **폐지된 카테고리**: Decisions, Skills, FSD, BRD (Policy.md 참조)
- **Anti-Compression Rule**: 수식, 상태 전이, 테이블 행은 절대 요약 금지
