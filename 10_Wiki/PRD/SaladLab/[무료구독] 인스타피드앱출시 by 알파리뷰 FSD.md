---
id: "무료구독_인스타피드앱출시_FSD"
category: "[[10_Wiki/PRD/SaladLab]]"
confidence_score: 0.98
tags: [fsd, saladlab, free-version, system-architecture]
last_reinforced: 2026-05-21
github_commit: ""
---

# [[[무료구독] 인스타피드앱출시 by 알파리뷰 FSD]]

## 📌 한 줄 통찰 (The Karpathy Summary)

> Quota 차감 풀, 상태 머신 전이, 작성 경로 트래킹, 비용 가드레일 등 비즈니스 제한을 가능케 하는 플랫폼 운영 레이어의 엔지니어링 기능 상세 명세서.

## 📐 도메인 모델 개요 (Domain Model Overview)

| # | 도메인 | 핵심 개념 |
| - | - | - |
| 1 | 통합 횟수제한 시스템 | 월 50건 Quota 풀 차감 정책, 카운터 라이프사이클 및 quota_usage DB 스키마 명세 |
| 2 | 리뷰 작성 경로 트래킹 | `review_source_type` (enum) 및 FK 연결 데이터 모델링 규격 |
| 3 | 무료버전 상태 머신 | `visitor`에서 `trial/paid`에 이르는 상태 전이 테이블 및 예외 전이 정책 |
| 4 | 마이그레이션 & 기타 제한 | 데이터 마이그레이션 매트릭스 및 L1~L4 레벨별 기능 제한 프레임워크 |
| 5 | 비용 & 유료 잠식 리스크 | 예상 규모별 가드레일, Kill / Rollback Rule 성패 지표 매트릭스 |
| 6 | 데이터 수집 & CS 프로토콜 | 공통 식별 키, 3계층 이벤트 스키마 및 CS 시점별 대응 스크립트 |

---

## 📖 핵심 도메인별 상세 (Domain Deep-Dive)

### 📖-1. 통합 횟수제한 시스템 (Quota Quota Pool)

*   **Quota 차감 대상 액션 및 차감 수**:

    | 액션 | 차감 수 | 비고 |
    |---|---|---|
    | 알림톡 리뷰 요청 발송 | 1 | 카드 등록 상점에 한함 |
    | 리뷰 작성 (요청 경유) | 1 | 발송(1) + 작성(1) = 합산 2카운트 |
    | 스태프 리뷰 작성 | 1 | 건당 |
    | 소셜미디어 가져오기 (인스타) | 1 | 건당 |
    | 소셜미디어 가져오기 (네이버 블로그) | 1 | 건당 |

*   **한도 정책**: 월 50건 한도 + 카드 등록 필수.
*   **카운터 라이프사이클**:
    *   **월간 카운터**: 매월 1일 00:00 UTC/KST 리셋 (배치 대신 `year_month` 기준 실시간 집계 WHERE 절로 처리 가능).
    *   **상태 전이 시**: 무료 → 유료 전환 시 카운터 비활성화(무제한). 유료 → 무료 다운그레이드 시 해당 월 잔여분부터 즉시 적용.
    *   **재설치 우회 차단**: `mall_id + multi_mall_no` 기준으로 탈퇴 후에도 한도 히스토리를 영구 보존한다.
*   **한도 도달 시 동작**:
    *   *70% (35건)*: 안내 배너 노출 "이번 달 한도 70% 소진".
    *   *90% (45건)*: 경고 알림 "10건 남음" 및 업그레이드 넛지 모달 트리거.
    *   *100% 초과*: 리뷰 요청/스태프/가져오기 API 비활성화. "이번 달 놓친 리뷰 요청 N건" 손실 프레임 UI 노출.
*   **데이터베이스 물리 스펙**:
    *   **카운트 테이블 (`quota_usage`)**:
        ```sql
        CREATE TABLE quota_usage (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            shop_id VARCHAR(50) NOT NULL,
            year_month VARCHAR(7) NOT NULL, -- YYYY-MM
            action_type VARCHAR(20) NOT NULL, -- REQUEST, STAFF, SOCIAL
            count INT NOT NULL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY uq_shop_period_action (shop_id, year_month, action_type)
        );
        ```
    *   **이력 테이블 (`quota_history`)**:
        ```sql
        CREATE TABLE quota_history (
            shop_id VARCHAR(50) PRIMARY KEY,
            mall_id VARCHAR(50) NOT NULL,
            multi_mall_no INT NOT NULL DEFAULT 0,
            free_started_at TIMESTAMP NOT NULL,
            total_used INT NOT NULL DEFAULT 0,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            INDEX idx_mall_identifier (mall_id, multi_mall_no)
        );
        ```

### 📖-2. 리뷰 작성 경로 트래킹 (Source Tracking)

*   **트래킹 대상 경로 (source_type enum)**:

    | source_type (enum) | 설명 | 구현 상태 |
    |---|---|---|
    | `revisit_banner` | 재방문 배너 경유 작성 | ❌ 신규 개발 필요 |
    | `review_request` | 알림톡 리뷰 요청 경유 | △ request_id FK 연결 필요 |
    | `staff` | 스태프 리뷰 직접 작성 | ✅ 기존 구분 가능 |
    | `social_instagram` | 인스타그램 가져오기 | ✅ 기존 구분 가능 |
    | `social_naver_blog` | 네이버 블로그 가져오기 | ✅ 기존 구분 가능 |
    | `qr_code` | 오프라인 QR 코드 경유 (예약) | ❌ 설계 시 enum 예약 |
    | `reminder` | 리뷰 작성 리마인더 경유 (예약) | ❌ 설계 시 enum 예약 |

*   **데이터 모델 스키마 확장**:
    *   `review_source_type` (VARCHAR(30), nullable): 상기 enum 매핑.
    *   `request_id` (BIGINT, nullable FK): `ReviewRequest` 테이블과 1:1 연결.
    *   `campaign_id` (VARCHAR(50), nullable): 재방문 배너 종류 식별자.
    *   `import_source` (TEXT, nullable): 소셜 가져오기 원본 API 페이로드 또는 URL.

### 📖-3. 무료버전 상태 머신 (State Machine)

*   **정규 상태 전이 테이블**:

    | From | To | 트리거 (Trigger) | 시스템 동작 (Action) |
    |---|---|---|---|
    | `visitor` | `installed` | 무료 앱 스토어 설치 버튼 클릭 | shop_id 테이블 내 `free_plan` 플래그 활성화 |
    | `installed` | `free_onboarding` | 어드민 최초 접속 | 무료 전용 온보딩 플로우(기본정보 입력) 렌더링 |
    | `free_onboarding` | `free_active` | 온보딩 완료 및 완료 버튼 클릭 | Quota 카운터 활성화, 무료 기본 기능 즉시 개방 |
    | `free_active` | `quota_reached` | 누적 Quota 50건 도달 | 관련 수집/요청 API 차단, 넛지 대시보드 갱신 |
    | `quota_reached` | `free_active` | 매월 1일 00:00 리셋 배치 실행 | `quota_usage` 카운터 초기화 및 차단 해제 |
    | `free_active/reached` | `trial` | 무료 상점의 유료 체험 신청 | Quota 제한 제거, 체험 유료 스펙 즉시 오픈 |
    | `free_active/reached` | `paid` | 정식 요금제 결제 승인 | Quota 해제, 모든 프리미엄 기능 개방 |

*   **예외 상태 전이 규칙**:
    *   `trial` → `free_active`: 체험 기간 만료 시 자동 강등을 막고 이탈 유도를 차단할 정책 수립 필요 (과금 유도 락 단계로 진입 유력).
    *   `paid` → `free_active`: 결제 실패 확정 혹은 자발적 다운그레이드 시, 기존 데이터는 보존하되 위젯 등의 L1~L3 잠금 상태를 즉각 가동함. 월 주문건 100건 초과 여부를 감시한다.

### 📖-4. 마이그레이션 & 기타 제한 (Migration & Core Constraint)

*   **데이터 마이그레이션 매트릭스**:

    | 데이터 유형 | 무료 설치 시 | 무료 → 유료 전환 시 | 앱 삭제 시 | 재설치 시 |
    |---|---|---|---|---|
    | 카페24 기존 리뷰 | ❌ 이관 안 함 | ✅ 이관 시작 (유료 전용) | N/A | ❌ |
    | 스태프 리뷰 | N/A | ✅ 그대로 유지 | 30일 보관 후 삭제 | 영구 히스토리 복원 |
    | 소셜 리뷰 메타 | N/A | ✅ 그대로 유지 | 30일 보관 후 삭제 | 영구 히스토리 복원 |
    | Quota 이력 | N/A (카운트 시작) | 비활성화 (무제한) | **영구 보존 (삭제 금지)** | **이전 히스토리 복원** |

*   **L1~L4 제한 레벨 프레임워크**:
    *   **L1 (완전 비노출)**: UI 상에서 존재 자체가 보이지 않음. (예: 포토리뷰/평점/게시판 외 프리미엄 위젯 18종)
    *   **L2 (노출 + 비활성)**: 메뉴는 노출되나 Gray-out 처리 및 클릭 시 유료 설명 모달 표시. (예: 리마인더 알림톡, 동영상 리뷰)
    *   **L3 (수정 가능 + 저장 차단)**: 옵션 선택 및 미리보기는 허용하되, 저장하기 클릭 시 업셀 팝업 트리거. (예: 포인트 금액 수정, 컬러 수정)
    *   **L4 (제한 수량 허용)**: 한도 소진 시 차단. (예: 리뷰 연결 1개 한도, 월 Quota 50건)

### 📖-5. 비용 & 유료 잠식 리스크 (Risk Management)

*   **비용 가드레일 매트릭스**:

    | 비용 항목 | 발생 조건 | 예상 규모 / 원가 | 가드레일 정책 |
    |---|---|---|---|
    | **알림톡 발송** | 리뷰 요청 알림톡 발송 | 건당 100원 할증 (원가 약 12원) | 카드 등록 필수화로 무분별 발송 제어 |
    | **인프라/트래픽** | 무료 위젯/피드 렌더링 | 상점당 월 CPU/저장량 역산 | 상점당 일 단위 API 호출 Rate Limit 적용 |
    | **CS 운영** | 무료 상점 상담 문의 | 어드민 설치 직후 대량 발생 | 채널톡 1차 자동 FAQ 응답, CS 처리 우선순위 최하위 |
    | **카드등록 포인트** | 최초 카드 등록 성공 | 상점당 1회 3,000원 무상 지급 | 월간 총 무상 포인트 지급 풀(Pool) 상한선 설정 |

*   **Kill / Rollback Switch 성패 지표**:

    | 지표 유형 | 대상 지표 | 임계값 (Trigger) | 대응 프로토콜 |
    |---|---|---|---|
    | ⚠️ 위험 신호 (Kill) | 6주 내 전체 유료 체험 상점 수 | **10% 이상 감소** | 무료 요금제 신규 가입 전면 중단 및 롤백 |
    | ⚠️ 위험 신호 (Kill) | 6주 내 알파리뷰 전체 매출액 | **10% 이상 감소** | 무료 쿼터 축소 및 결제 유도 조건 강화 |
    | ✅ 성공 지표 | 무료 → 체험/유료 전이율 | 주간 추적 | 성공 시 마케팅 투자 확대 |
    | 📊 보조 지표 | 과금 → 무료 다운그레이드 수 | 주간 10건 초과 시 경고 | 다운그레이드 차단 필터(주문 100건↑) 정교화 |

### 📖-6. 데이터 수집 & CS 프로토콜

*   **공통 식별 키 스펙**: `shop_id, mall_id, multi_mall_no, plan_type, free_version_yn, request_id, campaign_id`
*   **이벤트 계층 모델**:
    *   **Life-Cycle 계층**: `install`, `onboarding_start`, `free_activated`, `quota_reached`, `paywall_exposed`, `trial_start`, `paid_success`, `uninstall`
    *   **Function 계층**: `review_request_sent`, `review_written`, `staff_review_created`, `social_imported`, `pin_toggled`, `review_linked`
*   **CS 시점별 표준 대응 스크립트**:

    | 발생 시점 | 예상 문의 사유 | 대응 가이드 및 링크 |
    |---|---|---|
    | 카드 등록 시 | "왜 카드를 의무 등록해야 하나요?" | 알림톡 발송 통신 비용 예치 목적 안내 FAQ 제공 |
    | 한도 도달 시 | "요청 발송이 안 되고 멈춰 있습니다" | 50건 쿼터 소진 안내 및 Premium 업그레이드 링크 자동 안내 |
    | 잠긴 기능 클릭 시 | "포인트 지급 조건 수정이 안 됩니다" | L3 정책 설명: "체험은 가능하나 적용은 Premium 기능입니다" 안내 |

---

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)

*   **[2026-05-21] 통합**: 기존 PRD 상에 모호하게 흩어져 있던 Quota 차감 방식(작성 완료 시 1회 추가 차감 등)의 백엔드 트래킹 데이터 필드와 DB 스키마 구조를 물리 설계 수준으로 통일하여 보강함.

---

## 🔗 지식 연결 (Graph)

*   **Parent:** [[10_Wiki/PRD/SaladLab]]
*   **Related:** [[알파리뷰 무료버전 BRD]], [[[무료구독] 인스타피드앱출시 by 알파리뷰 PRD]], [[코어_데이터베이스_스키마_가이드]]
*   **Raw Source:** [[00_Raw/알파리뷰 무료버전 첫문서/[무료구독] 인스타피드앱출시 by 알파리뷰 FSD.md]]
