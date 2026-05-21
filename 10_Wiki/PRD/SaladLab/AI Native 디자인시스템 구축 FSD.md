---
id: ai-native-design-system-fsd
category: PRD
confidence_score: 5/5
tags: [design-system, headless, adapter-angular, prompt-guideline, ssot]
last_reinforced: 2026-05-21
parent: "[[AI-Native 디자인 시스템 구축 PRD]]"
related: []
---

# Functional Specification: AI Native 디자인 시스템 구축

## 0. 배경 및 참조 문서
* **BRD**: 없음 (목표: 좋은 아이디어가 hand-off 병목 없이 제품이 될 수 있도록 한다)
* **PRD**: [AI Native 디자인 시스템 구축 PRD (Big Batch 버전, 5/4 ~ 6/12)](https://www.notion.so/saladlab/AI-Native-35246f3e549c80a79e9ad0a6be7141fd?source=copy_link)
* **Keyword**: AI Native Design System, SSOT(Single Source of Truth), DESIGN.md, Standalone Component
* **DESIGN.md 사례**: [https://getdesign.md/](https://getdesign.md/) , [https://yozm.wishket.com/magazine/detail/3736/](https://yozm.wishket.com/magazine/detail/3736/)
* **DESIGN.md 문서**: [https://github.com/SaladLabInc/saladlab-design-system/blob/main/packages/sds-design-spec/DESIGN.md](https://github.com/SaladLabInc/saladlab-design-system/blob/main/packages/sds-design-spec/DESIGN.md)

---

## 1. 유저스토리
* **As a [role]**:
  * 샐러드랩의 기획자·디자이너·개발자(즉, AI 코딩 도구를 사용해 UI를 설계·구현·수정하는 모든 직군)로서,
* **I want [goal]**:
  * AI 코딩 도구(Cursor, Antigravity 등)로 UI를 만들거나 수정할 때, 디자인 시스템이 정의한 토큰·컴포넌트·상태 규칙 안에서만 결과물이 생성되기를 원한다.
* **so that [benefit]**:
  * 그래야 AI로 빠르게 초안을 만드는 장점을 유지하면서도, 일관성이 무너져 수정 비용이 폭발적으로 증가하고 퀄리티가 떨어지는 문제를 막을 수 있기 때문이다.

---

## 2. 문제와 솔루션

### 2.1. 문제 정의
AI 코딩 도구가 디자인 시스템의 제약 없이 동작하면서 다음과 같은 근본적인 문제가 발생하고 있다.
* **비효율**: 설계보다 구현이 먼저 일어나면서 이미 만들어진 결과물을 다시 정리하는 반복 문서 작업이 쌓인다.
* **일관성 붕괴**: 색상은 `base.less`, `@saladlabinc/ui` CSS Variables, 앱별 `styles.less` 등 3곳에서 각각 다른 문법으로 정의되어 SSOT(Single Source of Truth)가 불분명하다. 간격은 정의 자체가 없고 `padding: 20px 24px` 같은 하드코딩이 산발적으로 존재한다. z-index는 1000, 10600 등 임의값이 혼재한다. `@saladlabinc/ui`의 50개 이상 컴포넌트가 단일 모듈로 번들링되어 tree-shaking이 불가능하고, 앱별 로컬 컴포넌트도 중복 구현되어 있다 (alpha-review `shared/ui/` 15개, core-dashboard `shared/ui/` 2개).
* **퀄리티 저하**: UIUX 전문성 없이 진행된 설계가 제품에 그대로 남아 완성도 낮은 사용자 경험으로 이어진다.
* **AI 네이티브 개발 불가**: "버튼의 primary 색상은 무엇인가"라는 질문에 답하려면 `base.less`, `@saladlabinc/ui` CSS Variables, 앱별 `styles.less`를 모두 추적해야 한다. 사람은 암묵지로 처리하지만 AI에게는 명시적이고 단일한 소스가 필요하다.

### 2.2. 솔루션
**AI가 디자인 시스템 안에서만 창작하게 만든다.** 디자인 시스템을 "AI 코딩 도구의 동작 범위를 강제하는 인프라"로 정의하고, 다음 3가지 축으로 구축한다.
* **① 토큰의 원본 정의 단일화**: DESIGN.md를 토큰의 원본(원천)으로 두고, 모노레포 내 `packages/tokens/`가 이 정의를 따른다. 이번 베팅에서는 **AI 보조 + 사람 손이 들어가는 수동/반자동 워크플로우**로 운영한다. Figma ↔ 코드 완전 자동 동기화(진정한 의미의 SSOT)는 **Phase 2의 목표**이며 이번 베팅 범위가 아니다.
* **② 컴포넌트 목록의 가시화**: Storybook이 "우리가 가진 컴포넌트 목록"을 공개한다. AI는 새 컴포넌트를 만들기 전 이 목록을 먼저 확인하도록 프롬프트로 제약된다.
* **③ AI 진입점 통제**: DESIGN.md와 AI 프롬프트 가이드라인이 AI 코딩 도구의 context에 항상 포함된다. AI는 이 파일을 읽고 토큰·컴포넌트 규칙 안에서만 코드를 생성한다.
* **검증 방식**: 이번 베팅(6주)에서 디자인 시스템 전체를 만드는 것이 아니라, **토큰 · Headless · Adapter** 3축이 하나의 핵심 컴포넌트와 신규 화면 1개를 통해 **디자인 시스템 내에서 AI가 설계해주는지를** 검증한다.

---

## 3. 유저플로우

### 3.1. 시나리오 A — 기획자가 새 기능 아이디어를 AI로 구현할 수 있다.
1. 기획자가 Cursor·Antigravity에 UI 구현을 요청한다.
2. AI가 DESIGN.md를 context로 읽고, 기존 Standalone Component를 재사용한다.

### 3.2. 시나리오 B — 디자이너가 토큰을 변경하면 AI 보조 + 사람 손이 들어가는 워크플로우로 모노레포 전체에 일관되게 반영할 수 있다. (DESIGN.md 원천)
1. 디자이너는 모노레포 루트의 DESIGN.md에서 `color.primary` 값을 수정한다.
2. IDE(Cursor·Antigravity 등)에서 AI에게 "DESIGN.md 바뀐 값으로 토큰 파일 업데이트해줘"라고 요청한다.
3. AI는 모노레포 내 `packages/tokens/`의 토큰 파일을 수정할 수 있다.
4. 빌드 파이프라인이 `packages/tokens/` 변경을 감지해 CSS Variables를 자동 생성할 수 있다.
5. 모노레포 워크스페이스 의존성을 통해 `packages/components/`, `packages/adapter-angular/`, 그리고 `apps/` 하위의 모든 앱(대시보드 등)에 변경이 자동 전파될 수 있다.
6. 개발자는 Git 브랜치에서 변경 사항을 확인한 뒤 마스터에 커밋할 수 있고, 이후 Cursor·터미널·Antigravity 등 모든 환경에서 별도 수동 수정 없이 동일한 값을 참조할 수 있다.

### 3.3. 시나리오 C — 개발자가 기존 컴포넌트에 새 상태를 추가하면 모노레포 내 모든 사용처에 자동 반영할 수 있다.
1. 개발자는 모노레포의 `packages/headless/button/button.state.ts`를 열 수 있다.
2. 기존 상태 머신을 확인하면서 `loading` 상태를 안전하게 확장할 수 있다.
3. `packages/adapter-angular/`가 headless 변경을 받아 자동으로 Angular Signal로 변환할 수 있다.
4. 워크스페이스 의존성을 통해 해당 컴포넌트를 사용하는 모노레포 내 모든 앱·화면에 자동으로 반영할 수 있다(별도 패키지 배포 단계 없이 즉시 사용 가능).

---

## 4. 공통 정책
* 기존 구조(`@saladlabinc/ui`)를 즉시 교체하지 않고 **신규 코드부터 점진적으로** 새 시스템을 적용한다.
* 초기 단계에서는 모든 UI에 완전한 일관성을 요구하지 않고, **일부 불일치와 임시 구조**를 감수한다.
* 기존 `@saladlabinc/ui`와 새 구조가 **공존**하면서 발생하는 **중복과 운영 복잡성**을 감수한다.
* Phase 1에서는 DESIGN.md를 토큰의 **원본 정의**로 두고, **AI 보조 + 사람 손이 들어가는 수동/반자동 워크플로우**로 운영한다.
* 모든 신규 스타일은 **Semantic Token**으로만 정의한다. 색상·간격·z-index 등 직접 입력 금지.
* 모든 신규 컴포넌트는 **Headless + Adapter-Angular + Standalone** 구조를 따른다.
* AI 코딩 도구는 반드시 **DESIGN.md를 context로 포함**해 동작한다.
* 베팅 기간(6주) 내 완료를 우선하고, 범위 밖 항목은 **다음 베팅으로 미룬다**.

---

## 5. 인수조건 (AC)

| AC no | 구현 확정 | 자가 검수 | 인수조건 (Acceptance Criteria) | 상세 조건 및 정책 |
| :--- | :---: | :---: | :--- | :--- |
| 1 | - | - | Figma variables와 코드 토큰 파일이 동일한 Semantic Token 네이밍 체계를 사용한다 | - |
| 2 | - | - | CSS Variables는 DESIGN.md 기준으로 토큰 파일에서 자동 생성된다 | - |
| 3 | - | - | 신규 화면 1개에 새 디자인 시스템이 적용되어 있고, 디자인 시스템에 있는 컴포넌트 기준 시스템 밖으로 새는 코드가 0건이다 | 스타일·상태·이벤트가 토큰/Headless/Adapter 안에서만 흘러감. 하드코딩된 색상·간격·z-index, 인라인 스타일, 컴포넌트 내부 즉석 상태 정의 모두 0건 |
| 4 | - | - | 디자이너가 **DESIGN.md 1곳만 수정**하면, AI 보조 + 모노레포 빌드를 통해 신규 화면까지 **애플리케이션 코드 수동 수정 0건**으로 반영된다 | ① 디자이너가 DESIGN.md 수정 *(수동)*<br>② IDE에서 AI에 "토큰 갱신해줘" 요청 *(수동)*<br>③ AI가 `packages/tokens/` 토큰 파일 수정 *(반자동)*<br>④ 빌드 스크립트가 CSS Variables 자동 생성 *(자동)*<br>⑤ 모노레포 워크스페이스 의존성으로 `packages/components/`·`apps/` 전파 *(자동)*<br>⑥ 개발자 확인·커밋 *(수동)*<br>➔ **③~⑤ 구간이 자동/반자동으로 동작하고, 애플리케이션 코드 직접 수정 단계가 0건**임을 검증한다. ①②⑥의 사람 개입 자동화는 Phase 2 목표. |
| 5 | - | - | 기존 `@saladlabinc/ui`를 쓰는 다른 화면들이 영향을 받지 않는다 | 회귀 테스트 baseline 대조 통과율 100%. 신·구 시스템 공존이 가능함을 증명 (스쿼드별 핵심 화면 1개 선정해서 컴포넌트 및 상호작용 문제없는지 확인) |
| 6 | - | - | DESIGN.md가 작성되어 있고 AI 코딩 도구의 IDE 규칙 파일로 등록되어 있다 | Cursor·Antigravity 등 팀 사용 IDE에 규칙 파일로 등록. AI가 DESIGN.md를 context로 읽고 토큰·컴포넌트 규칙 안에서만 코드를 생성하는지 검증 |
| 7 | - | - | AI 프롬프트 가이드라인 초안이 작성되어 있다 | AI에게 디자인 설계를 요청하는 방법, 토큰 사용 강제 지침, 기존 컴포넌트 재사용 지침 포함 |
| 8 | - | - | Storybook이 구현·배포되어 있고 "가진 컴포넌트 목록"을 공개한다 | 핵심 컴포넌트가 Storybook에 등재되어 있어 AI/사람 모두가 단일 목록에서 확인 가능. Figma ↔ Storybook 최종 대조 완료 |
| 9 | - | - | 정성적 기준: 별도 Figma 명세나 redline 작성이 감소했다 | 신규 화면 작업 시 디자이너가 별도 redline 문서를 만들지 않아도 개발자가 토큰·컴포넌트·헤드리스 정의만으로 구현이 가능했는지 디자이너별로 확인 (yes/no 기록)<br>실험 기간: 6월 1일 ~ 23일<br>검증: 중간 확인 6월 8일 / 최종 확인 6월 12일 |
| 10 | - | - | 정성적 기준: 디자이너 ↔ 개발자 간 질문/수정 요청 횟수가 감소했다 | 직전 비슷한 규모 작업과 비교해 질문/수정 요청 횟수가 줄었다고 양쪽 모두 체감하는지 확인(회고 기록 기반) |
| 11 | - | - | ~~AI가 DESIGN.md를 수정하면 md 기준으로 토큰값을 자동으로 변경해주고, 토큰 값 1개 변경 시 신규 화면에서 수동 수정 0건으로 자동 반영된다~~ | ~~DESIGN.md → tokens/ 파일 → CSS Variables → 적용 화면까지 1개소 변경으로 전파 검증~~ |

* **Out of Scope**:
  * SSOT(진정한 의미의 SSOT(Figma ↔ 코드 완전 자동 동기화, 옵션 A·Tokens Studio 등)
  * adapter-lit 구현 및 위젯(Lit) 환경 확장
  * 기존 `@saladlabinc/ui` 컴포넌트 마이그레이션
  * 조합 패턴(Patterns) 정의
  * 디자인 시스템 독립 패키지화
  * 전사 온보딩·확산
  * lint 규칙(토큰 외 직접 입력 시 자동 경고/차단)
* **Challenge Task**:
  * "시스템 밖으로 새는 코드" 및 "토큰 1개 변경 시 수정 개소" Before 값을 사전 실측해 비교 baseline 확보
  * DESIGN.md를 처음부터 **표·코드블록·키-값 형식**으로 일관되게 작성해, AI가 별도 해석 없이 그대로 읽을 수 있게 한다 (레퍼런스: Anthropic Claude.md, getdesign.md)
  * Angular 환경에 한정해도 Headless ↔ Adapter 분리가 실무에서 유지 가능한 추상화 수준인지 검증
  * lint 도입 없이 토큰 외 직접 입력을 막을 운영 규율 설계(코드 리뷰 체크리스트 등)

---

## 6. 데모 계획
1. design.md 문서 구성에 대한 소개 (구경)
2. **데모 시나리오 1 — AI 코딩 도구의 디자인 시스템 준수**
   * Cursor 또는 Antigravity에 "신규 카드 UI 만들어줘"라고 요청 ➔ AI가 DESIGN.md를 context로 읽고 Semantic Token과 기존 Standalone Component만 사용해 코드를 생성하는 과정을 시연한다.
3. ~~**데모 시나리오 2 — 토큰 변경 자동 반영**~~
   * ~~DESIGN.md에서 `color.primary` 값을 변경 ➔ AI가 tokens/ 파일을 업데이트 ➔ CSS Variables 자동 생성 ➔ 신규 화면 1개에 자동 반영되는 전체 플로우를 실시간으로 시연한다. 수동 수정 0건임을 확인한다.~~
4. ~~**데모 시나리오 3 — Headless 상태 확장**~~
   * ~~`button.state.ts`에 `loading` 상태를 추가 ➔ adapter-angular가 Angular Signal로 변환 ➔ 해당 컴포넌트를 사용하는 모든 화면에 자동 반영되는 과정을 시연한다.~~
5. ~~**데모 시나리오 4 — 공존 검증**~~
   * ~~기존 `@saladlabinc/ui`를 사용하는 화면이 새 시스템 도입 이후에도 영향받지 않음을 회귀 테스트 baseline 대조로 시연한다.~~
6. ~~**회고 및 다음 베팅 좌표 설정**~~
   * ~~어디가 막혔는가, 무엇을 더 해야 하는가를 디자이너+개발자가 함께 정리해 다음 베팅(Phase 2 — SSOT 자동화)의 출발점을 합의한다.~~

---

## 9. 기타 메모
* **스프린트 구조 (참고)**:
  * Sprint 1 (5/4 ~ 5/15) — *만든다*: Foundation 및 Component 구현 (Figma + 코드)
  * Sprint 2 (5/18 ~ 5/29) — *연결 및 고도화*: DESIGN.md + AI 프롬프트 가이드 초안 작성
  * Sprint 3 (6/1 ~ 6/12) — *검증한다*: AI rule + token + Storybook 통합 검증 및 다음 베팅 좌표 설정
* **Headless가 담는 것 (참고)**:
  * 상태: `disabled`, `loading`, `pressed`, `isOpen`, `isClosing` 등
  * 이벤트: `onClick`, `onKeyDown(Enter/Space)`, `onClose`, `onBackdropClick`, `onEscape` 등
  * 상태 전이 규칙: `loading=true`면 click 무시, `isOpen=true → ESC 누르면 close` 등
  * 부수 동작: focus 관리, ARIA 속성, focus trap, body scroll lock 등
* **Adapter 구조의 필요성**:
  * 대시보드는 Angular, 위젯은 Lit을 사용 ➔ 현재 UI 규칙을 공유하지 않음 ➔ Adapter(번역기 역할)로 해결 예정 (Phase 1에서는 adapter-angular만 구현, adapter-lit은 Phase 3로 이연)
* **장기 비전 (참고)**:
  * Phase 2: SSOT 자동화 (Tokens Studio 등 옵션 A 기반)
  * Phase 3: adapter-lit + Figma MCP + 전사 확산 + 독립 패키지화
* **현재 방식의 장점 유지**: AI를 활용한 초안 속도와 커뮤니케이션 비용 감소 효과는 그대로 유지한다. 이번 베팅은 "속도를 죽이지 않으면서 일관성과 수정 비용 문제를 해결"하는 것이 목표다.
