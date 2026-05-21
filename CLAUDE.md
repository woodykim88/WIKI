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
| `00_Staging_탐색/` | 외부 데이터 입력 및 자동 분류 대기 |
| `00_Raw/YYYY-MM-DD/` | 백그라운드 원본 백업 보관 (Source of Truth) |
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

## 지름길 명령어 트리거 (Quick Shortcut Triggers)

사용자가 아래의 키워드로 명령을 내리면, 에이전트는 즉시 본 프로젝트에 최적화된 **'원스톱 완전 자동화 전처리 파이프라인'**을 즉각 실행합니다.

- **트리거 키워드**: `WIKI 지식동기화 시작하자!`, `지식동기화 시작`, `위키 동기화 실행`
- **수행할 작업 순서**:
  1. `00_Staging_탐색/` 폴더 내의 모든 원시 마크다운 문서 목록을 조회한다.
  2. 각 문서를 `Skill_LLMWIKI_Notion_Cleaner.md` 지침에 맞춰 평탄화 및 가치 검수한다. (반려 문서는 `00_Staging_탐색/Trash/` 폴더로 즉시 격리 폐기한다.)
  3. 합격된 정제 문서는 백업용 복사본을 `00_Raw/YYYY-MM-DD/` 하위에 조용히 생성 보관한다.
  4. 정제 완료된 문서를 대상으로 `Skill_LLMWIKI_강화학습기반구조화 로직.md` 지침을 적용하여 `10_Wiki/` 하위 적정 폴더 경로로 다이렉트 분류 및 영속적 저장한다.
  5. 배치가 완료되면 `00_Staging_탐색/` 내 원시 스크랩 대상 원본은 모두 완전 삭제 청소한다.
  6. 변경 사항이 반영되도록 `20_Meta/Graph.json` 및 `20_Meta/Index.md`를 빌드(Graphify 갱신)한다.
  7. `git add .` 후 `git commit -m "[P-Reinforce] 지식동기화 - 원스톱 자동 파이프라인 가동"` 커밋을 작성하고 GitHub 원격 `main` 브랜치로 `git push`를 실행하여 원스톱 동기화를 완료한다.
