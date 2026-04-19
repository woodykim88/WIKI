---
id: b92fcd62-8e75-430b-b5db-d86f912c96b7
category: "[[10_Wiki/🛠️ Projects/SaladLab]]"
confidence_score: 0.96
tags: [알파리뷰, 데이터모델, DB, Backend, SaladLab, 리뷰, 상태관리, ORM]
last_reinforced: 2026-04-13
github_commit: ""
---

# [[[AI] 리뷰 데이터 모델 및 상태 관리]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 알파리뷰의 Review 모델은 단순 평가 데이터를 넘어, 상태 머신(게시/혜택 상태)과 15개 이상의 하위 테이블을 관장하며, 원본/복사본 메커니즘(review_origin)을 통해 데이터 무결성을 추적하는 서비스의 마스터 허브 역할을 한다.

## 📐 도메인 모델 개요 (Domain Model Overview)

| # | 도메인 | 핵심 개념 |
|---|--------|-----------|
| 1 | Review 본체 | 핵심 필드, 콘텐츠 플래그, 사용자 정보, 통계, 외부 연동, SNS 인증, 리뷰 번호 체계 |
| 2 | 미디어 모델 | ReviewPhoto(원본/썸네일/대형 WEBP), ReviewVideo(4단계 압축), ReviewMediaIndex(통합 순서) |
| 3 | 부가 모델 | ReviewLog(상태 변경), ReviewComment(댓글), ReviewViews(IP 조회수), ReviewReport(신고), ReviewReward(포인트), ReviewAI(감성분석), ReviewNegativePhrase(부정 문장) |
| 4 | 상태 전이 | PostingStatus(게시예정/대기/됨/숨김), RewardStatus(15개 상태), CreaterType(9종), ReviewType(4종), Platform(6종) |
| 5 | 비즈니스 로직 | save() 전처리/후처리, delete() 하드삭제+인스타 수동삭제, is_verified, reward_target_review, platform_display |
| 6 | Usecase 흐름 | 일반/빠른/SNS 리뷰 작성, 리뷰 수정(원본-편집본), 삭제(CASCADE), 혜택 지급 흐름 |

---

## 📖 핵심 도메인별 상세 (Domain Deep-Dive)

### 📖-1. Review 본체 (핵심 모델)

**모듈 경로:** `projectreview/review/models.py`
**타입 정의:** `projectreview/common/types.py`

**도메인 간 관계:**
```
Shop (1) ─── (N) Review (N) ─── (1) Product
                    │
                    ├── (1) OrderItem
                    ├── (N) ReviewPhoto
                    ├── (N) ReviewVideo
                    ├── (N) ReviewMediaIndex
                    ├── (N) ReviewLog
                    ├── (N) ReviewComment
                    ├── (N) ReviewViews
                    ├── (N) ReviewReport
                    ├── (N) ReviewReward
                    ├── (1) ReviewAI
                    ├── (N) ReviewNegativePhrase
                    ├── (N) ReviewBadgeRelation ─── Badge
                    ├── (N) ReviewLabelRelation ─── Label
                    ├── (N) ReviewKeywordRelation ─── Keyword
                    ├── (N) ReviewChallengeRelation ─── ReviewChallenge
                    └── (1) ReviewSurveyFormRelation ─── SurveyForm
```

**주요 필드:**

| 필드 | 타입 | 설명 |
|---|---|---|
| shop_id | IntegerField | 쇼핑몰 고유 ID (FK 아닌 정수 직접 참조) |
| product_id | IntegerField (nullable) | 상품 고유 ID (레거시 정수 참조) |
| product_fk | ForeignKey → Product | 상품 FK (SET_NULL). product_id와 병행 사용 |
| order_item_id | IntegerField (nullable) | 주문상품 고유 ID (레거시 정수 참조) |
| order_item_fk | ForeignKey → OrderItem | 주문상품 FK (SET_NULL) |
| review_type | PositiveSmallIntegerField | Review__ReviewType choices |
| creater_type | PositiveSmallIntegerField | Review__CreaterType choices |
| content | TextField | 리뷰 텍스트 내용 |
| ratings | PositiveSmallIntegerField | 별점 (1~5). save() 시 클램핑 |
| platform | CharField(63) | Review__Platform choices |
| posting_status | IntegerField | 게시 상태 |
| reward_status | IntegerField | 혜택 상태 |
| is_visible | BooleanField | 게시(노출) 여부 |
| is_reward | BooleanField | 혜택 지급 여부 |
| is_deleted | BooleanField | 관리자 삭제 여부 (소프트 삭제) |
| review_origin | OneToOneField → self | 원본 리뷰 참조 (편집 시 원본-편집본 연결) |

**콘텐츠 플래그:** is_photo, is_video, is_survey, is_keyword

**사용자 정보:** user_id (소셜: @k=카카오, @n=네이버, deprecated), user_name, profile_image (CDN default), sns_user_id, sns_review_id

**통계 필드:** view_count, like_count, comment_count, sns_like_count (= like_count + comment_count), total_point

**리뷰 번호 체계:**
- review_no: 레거시 번호
- review_no_new: base62 인코딩 → 짧은 URL 생성
- `get_notnullable_review_no()`: review_no_new가 있으면 base62 문자열, 없으면 review_no 반환

**GA 이벤트 (ga_event):** 10자리 비트 문자열

| 인덱스 | 이벤트 |
|---|---|
| 0 | review_submit |
| 1 | review_submit_quick |
| 2 | review_submit_normal |
| 3 | review_submit_text |
| 4 | review_submit_photo |
| 5 | review_submit_video |
| 6 | review_submit_survey |
| 7 | review_modify |
| 8~9 | (예약) |

**인덱스 설계 주요 조회 패턴:**
- 기본: (shop_id), (shop_id, product_fk), (shop_id, review_no), (shop_id, review_no_new)
- 시간순: (shop_id, created_at), (shop_id, ratings, created_at), (shop_id, like_count, created_at)
- 작성자별: (shop_id, creater_type, is_deleted, created_at)
- 위젯 필터: (shop_id, product_fk/id, is_visible, is_photo, is_video, is_survey, review_type, sort, created_at) - 정렬 기준별 각각 인덱스

---

### 📖-2. 미디어 모델

**ReviewPhoto:**

| 필드 | 타입 | 설명 |
|---|---|---|
| image | ImageField | 원본. 경로: review/images/YYYY/MM/DD/ |
| thumbnail | ProcessedImageField | 100x100, WEBP, quality=60 |
| large | ProcessedImageField | 너비 900px 리사이즈, WEBP, quality=60 |
| image_cafe24 | CharField(511) | CAFE24 이미지 URL |
| is_human_detect | BooleanField | AI 인물 감지 여부 |
| duplicate_review_ids | TextField | AI 중복 감지 리뷰 ID 목록 |

이미지 처리 파이프라인: 원본 → imagekit Thumbnail(100,100) → 100x100 WEBP / ResizeToFit(width=900) → 900px WEBP

**ReviewVideo:** 4단계 압축 (origin → compress → middle → thumbnail). 모든 필드 커스텀 `CompressVideoField` (common/fields.py)

**ReviewMediaIndex:** photo와 video 중 하나만 참조. index 필드로 노출 순서 통합 관리.

---

### 📖-3. 부가 모델

**ReviewLog:** status + reason + created_at (상태 변경 이력)

**ReviewComment:**
- writer_type: 1(랜덤/자동생성), 2(관리자), 3(회원), 4(비회원)
- content_auto: 자동 답변 여부 (기본 True)

**ReviewReward:**
- point, payed_status(기본: "지급대기"), to_be_pay_date, payed_date
- is_custom_payed: 추가 지급 여부
- ⚠️ payed_reason: 1000자 제한

**ReviewAI:** sentiment(기본: "긍정"), positive/negative/neutrality/thoroughness 점수, review_category

**ReviewNegativePhrase:** AI 감지 부정 문장 별도 저장

---

### 📖-4. 상태 전이

**게시 상태 (PostingStatus):**
```
리뷰 생성 → 게시대기(11, default) → 게시됨(20) ↔ 숨김(21)
                                     ↑
                 게시예정(10) ─────────┘ (예약 시간 도래)
```

| 값 | 이름 | 설명 |
|---|---|---|
| 10 | 게시예정 | 예약 게시 |
| 11 | 게시대기 | 관리자 검수 필요 (default) |
| 20 | 게시됨 | 위젯 노출 |
| 21 | 숨김 | 위젯 비노출. 관리자 재게시 → 게시됨(20) |

**혜택 상태 (RewardStatus):** (15개 상태 코드, 전체 테이블은 [[알파리뷰 포인트 지급 정책]] 📖-2 참조)

**작성자 유형 (CreaterType):**

| 값 | 이름 | is_verified |
|---|---|---|
| 1 | 회원 | True (실구매) |
| 2 | 비회원 | True (실구매) |
| 3 | NPAY | True (실구매) |
| 4 | 주문생성 | False |
| 5 | 관리자 | False |
| 6 | 시스템 | False |
| 11 | 미검증 | False |
| 29 | 복사 | False |
| 100 | 원본 | False |

**플랫폼 (Platform):** 알파리뷰(기본), CAFE24, 스마트스토어, 지그재그, 인스타그램, 네이버블로그

**알림 사유 (AlertReason):** posting_wating, posting_disabled, reward_wating, reward_disabled, comment, keyword, ratings, unverified, report, revise

---

### 📖-5. 비즈니스 로직

**Review.save() 전처리/후처리:**
```python
def save(self, *args, **kwargs) -> None:
    # [전처리] ratings 클램핑: 0이하 → 1, 5초과 → 5
    # super().save()
    # [후처리1] SNS리뷰 → sns_like_count = like_count + comment_count
    #   ⚠️ super().save() 이후 인스턴스 레벨에서만 변경, DB 미반영
    # [후처리2] Product.is_review_changed = True (캐시 갱신 트리거)
    # [후처리3] OrderItem.quick_written_rating = self.ratings
```

**Review.delete():**
```python
def delete(self, *args, **kwargs):
    # Product.is_review_changed = True
    # Instagram 연관 데이터: ORM CASCADE 아닌 수동 삭제
    # super().delete() → 하드 삭제 수행
    # ⚠️ 코드 주석에 is_deleted=True 전환 예정 (소프트 삭제 마이그레이션)
```

**is_verified (실구매 판별):** 회원(1), 비회원(2), NPAY(3)만 True

**reward_target_review:** 원본(100) 리뷰에서 호출 시 편집본 반환. 혜택 처리는 항상 편집본 기준

**platform_display:** SNS리뷰 또는 인스타그램 → "인스타그램". ⚠️ CAFE24/지그재그는 "알파리뷰"로 표시

**login_provider (deprecated):** @k=카카오, @n=네이버. 더 이상 사용하지 않음

---

### 📖-6. Usecase 흐름

**일반 리뷰 작성:**
1. 리뷰 작성 폼 제출 → Review 인스턴스 생성 (posting_status=11, reward_status=11)
2. save() → ratings 클램핑 + Product.is_review_changed + OrderItem.quick_written_rating
3. ReviewPhoto 생성 → 원본/썸네일(100x100)/대형(900px) WEBP
4. ReviewVideo 생성 → 4단계 CompressVideoField
5. ReviewMediaIndex → 미디어 순서 기록
6. ReviewLog → 상태 변경 이력

**리뷰 수정:**
1. 기존 리뷰 creater_type → 원본(100)으로 변경
2. 새 편집본 생성 → review_origin = 원본(OneToOneField)
3. reward_target_review → 항상 편집본 반환.

**리뷰 삭제:**
1. delete() → Product.is_review_changed = True
2. Instagram 연관 수동 삭제
3. super().delete() → 하드 삭제 + CASCADE로 모든 하위 테이블 삭제

**혜택 지급:**
1. 게시 후 조건 확인 → ReviewReward 생성
2. 지급 실행 → reward_status=20, is_reward=True
3. 비회원 → 비회원지급대기(12) → 회원 전환 후 지급
4. SNS → 유지기간 미달 시 SNS지급대기(13) → 달성 시 지급

---

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)

- **[2026-02-23] 원본 문서 작성:** 담당자 미지정, 상태 "시작 전". AI 리뷰 데이터 모델을 코드 기반으로 정리한 문서.
- **[구조 위험] 하드 삭제 → 소프트 삭제 마이그레이션:** 코드 주석에 `is_deleted = True` 전환이 예정되어 있으나 미완료. 현재 `super().delete()`로 CASCADE 하드 삭제가 발생하여 연관 15개 테이블 데이터가 영구 소실됨.
- **[비정합] sns_like_count 갱신:** `save()` 시 인스턴스 레벨에서만 변경되고 DB에 다시 저장되지 않음. 별도 벌크 업데이트 또는 후속 save 필요.
- **[deprecated] login_provider:** user_id 접미사(@k, @n) 기반 소셜 로그인 판별. 더 이상 사용하지 않으나 코드에 잔존.
- **[레거시] product_id & order_item_id:** FK(product_fk, order_item_fk)와 정수 ID가 병행 사용되는 이중 참조 구조. 레거시 호환 목적.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects/SaladLab]]
- **Related:** [[알파리뷰 포인트 지급 정책]], [[리뷰 종류 정리]], [[알파리뷰 위젯 정책]]
- **Raw Source:** [[Clippings/Where teams and agents work together 3.md]]
