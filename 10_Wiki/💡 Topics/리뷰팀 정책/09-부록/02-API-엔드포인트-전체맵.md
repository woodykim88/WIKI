# API 엔드포인트 전체 맵

> Alpha Review 프로젝트의 모든 URL 라우팅을 정리한 문서.
> 소스: `projectreview/projectreview/urls.py` 및 각 앱의 `urls.py`
>
> 모든 shop-scoped 엔드포인트는 `shops/<int:shop_id>` 접두사를 가지며, 멀티테넌시를 지원한다.

---

## 1. 최상위 라우팅 구조

```
# V1 엔드포인트 (shop-scoped)
shops/<int:shop_id>              → shop.urls
shops/<int:shop_id>/alarms       → alarm.urls
shops/<int:shop_id>/policy       → shopreviewpolicy.urls
shops/<int:shop_id>/reviews      → review.urls
shops/<int:shop_id>/mypage       → mypage.urls
shops/<int:shop_id>/alimtalk     → alimtalk.urls
shops/<int:shop_id>/seeds        → seed.urls
shops/<int:shop_id>/ticker       → ticker.urls
shops/<int:shop_id>/external     → external.urls
shops/<int:shop_id>/widgets      → widget.urls
shops/<int:shop_id>/products     → product.urls
shops/<int:shop_id>/orders       → order.urls
shops/<int:shop_id>/feed         → instagramfeed.urls
shops/<int:shop_id>/reports      → report.urls

# V2 엔드포인트 (shop-scoped)
v2/shops/<int:shop_id>/reviews   → review.v2.urls
v2/shops/<int:shop_id>/widgets   → widget.v2.urls.dashboard_urls
v2/shops/<int:shop_id>/products  → product.v2.urls
v2/shops/<int:shop_id>/stats     → analytics.urls

# 공통 엔드포인트 (shop 독립)
webhook                          → webhook.urls
alimtalk                         → alimtalk.common_urls
widget                           → widget.common_urls
review                           → review.common_urls
api_widget                       → widget.view_widget.urls
feed                             → instagramfeed.widget_urls

# V2 공통
v2/api-widget                    → widget.v2.urls.script_urls
v2/widget                        → widget.v2.urls.urls (preview)

# 시스템
healthcheck                      → HealthCheck__View
```

---

## 2. 샵 설정 (shop.urls)

> 접두사: `shops/<int:shop_id>`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/initial` | ShopInitial__View | 샵 초기 설정 |
| `/context` | Shop__View | 샵 컨텍스트 조회 |
| `/comment/auto-setting` | ShopOption__ListView | 자동 댓글 설정 |
| `/shop-option` | ShopOption__View | 샵 옵션 관리 |
| `/auto-crawling` | ShopAutocrawling__View | 자동 크롤링 상태 |
| `/auto-crawling/set` | ShopAutoCrawling__SetAutoTransferView | 자동 이관 설정 |
| `/admin-log` | ShopAdminLog__View | 관리자 로그 |
| `/batch-analysis/eligibility` | BatchAnalysisEligibility__View | 배치 분석 자격 확인 |

### 디자인 설정

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/design/common` | DesignCommon__View | 공통 디자인 |
| `/design/detail-page` | DesignDetailPage__View | 상세 페이지 디자인 |
| `/design/write-page` | ShopWritePage__View | 작성 페이지 디자인 |
| `/design/collect` | DesignCollect__View | 수집 디자인 |
| `/design/collect/empty-page` | DesignEmptyPage__View | 빈 리뷰 페이지 |
| `/design/collect/revisit-page` | DesignRevisitPage__View | 재방문 팝업 |
| `/design/collect/banner-page` | DesignBannerPage__View | 배너 페이지 |
| `/design/collect/qr-page` | DesignQRcodePage__View | QR 코드 |

### 통계

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/stats/graph/ratings` | StatisticsGraph__ReviewRatingsView | 평점 그래프 |
| `/stats/graph/count` | StatisticsGraph__ReviewNumberCountView | 리뷰 수 그래프 |
| `/stats/graph/writings` | StatisticsGraph__ReviewWritingView | 작성률 그래프 |
| `/stats/graph/rewards` | StatisticsGraph__RewardView | 적립금 그래프 |
| `/stats/graph/voc` | StatisticsGraph__VocView | VOC 그래프 |
| `/stats/graph/voc/products` | StatisticsGraph__VocProductView | VOC 상품별 |
| `/stats/scores` | StatisticsScoreCard__View | 스코어카드 |
| `/stats/ranking/ratings` | StatisticsRanking__ReviewRatingsView | 평점 랭킹 |
| `/stats/ranking/count` | StatisticsRanking__ReviewNumberCountView | 리뷰 수 랭킹 |
| `/stats/survey` | Statistics__ReviewSurveyView | 설문 통계 |
| `/stats/survey/subjective/<int:question_id>` | ShopSurveyAnswer__ListView | 주관식 답변 |
| `/stats/ranking/survey` | Statistics__ReviewSurveyRankingView | 설문 랭킹 |
| `/stats/reviews` | StatisticsReview__ListView | 리뷰 통계 목록 |
| `/stats/products` | StaticsProduct__ListView | 상품 통계 목록 |

---

## 3. 리뷰 관리 (review.urls)

> 접두사: `shops/<int:shop_id>/reviews`

### 배지/라벨

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/badge` | Badge__ListView | 배지 목록 |
| `/badge/<int:id>` | Badge__DetailView | 배지 상세 |
| `/badge/<int:id>/active` | Badge__ActiveView | 배지 활성화 |
| `/badge/reset` | Badge__ResetView | 배지 초기화 |
| `/label` | Label__ListView | 라벨 목록 |
| `/label/<int:id>` | Label__DetailView | 라벨 상세 |

### 빠른리뷰/해시태그/키워드

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/quick/comments` | QuickReview__ListView | 빠른리뷰 댓글 목록 |
| `/quick/comments/<int:id>` | QuickReview__DetailView | 빠른리뷰 댓글 상세 |
| `/hashtag` | Hashtag__ListView | 해시태그 목록 |
| `/keyword/init` | ReviewKeyword__InitialView | 키워드 초기화 |
| `/keyword/group` | KeywordGroup__View | 키워드 그룹 관리 |

### 설문조사

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/survey` | SurveyForm__View | 설문 폼 관리 |
| `/survey/question` | SurveyQuestion__View | 설문 질문 관리 |
| `/survey/question/<int:id>` | SurveyQuestion__DetailView | 설문 질문 상세 |
| `/survey/statistics/products` | ReviewProductStatistics__View | 설문 상품 통계 |
| `/survey/answers/reviews` | SurveyAnswerReview__ListView | 설문 답변 리뷰 목록 |

### 관리자 리뷰 작성

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/staff` | StaffReview__ListView | 관리자 리뷰 목록 |
| `/staff/products` | StaffReviewProduct__ListView | 관리자 리뷰 상품 목록 |
| `/staff/survey` | StaffReviewSurvey__View | 관리자 설문 리뷰 |
| `/staff/validation/products` | StaffReview__ValidationProductView | 상품 유효성 검증 |
| `/staff/<int:product_id>` | StaffReview__View | 관리자 리뷰 작성 |

### 리뷰 목록 관리

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/reviewlist` | ReviewList__PostingStatusView | 게시 상태 변경 |
| `/reviewlist/reward/<int:reward_at>` | ReviewList__ReviewRewardView | 보상 조회 |
| `/reviewlist/reward/withdraw/<int:id>` | ReviewList__ReviewRewardWithdrawView | 보상 회수 |
| `/reviewlist/reward/change` | ReviewList__ReviewRewardChangeView | 보상 변경 |
| `/reviewlist/reward/change/bulk` | ReviewList__ReviewRewardBulkChangeView | 보상 일괄 변경 |
| `/reviewlist/reward/hold/<int:id>` | ReviewList__ReviewRewardHoldView | 보상 보류 |
| `/reviewlist/product` | ReviewList__ProductView | 상품별 리뷰 |
| `/reviewlist/copy` | ReviewList__CopyView | 리뷰 복사 |
| `/reviewlist/delete` | ReviewList__DeleteView | 리뷰 삭제 |
| `/reviewlist/sort` | ReviewList__SortView | 리뷰 정렬 |
| `/reviewlist/productchange` | ReviewList__ProductChangeView | 상품 변경 |
| `/reviewlist/sortchange` | ReviewList__SortChangeView | 정렬 변경 |
| `/reviewlist/comment/update/<int:review_id>` | ReviewList___ReviewCommentView | 댓글 수정 |
| `/reviewlist/media/delete/<int:review_id>/<int:media_id>/<str:is_type>` | ReviewList__ReviewMediaView | 미디어 삭제 |
| `/reviewlist/memo<int:review_id>` | ReviewList__ReviewMemoView | 메모 관리 |
| `/reviewlist/review/label/<int:review_id>/<int:label_id>` | Reviewlabel__View | 리뷰 라벨 |
| `/reviewlist/review/label/bulk/<int:label_id>` | ReviewlabelBulk__View | 리뷰 라벨 일괄 |
| `/reviewlist/review/badge/<int:review_id>/<int:badge_id>` | Reviewbadge__View | 리뷰 배지 |
| `/reviewlist/review/rawdata` | ReviewList__RawDataRequestLogView | 원본 데이터 요청 |
| `/reviewlist/review/edit/<int:review_id>` | ReviewList__EditView | 리뷰 수정 |

### 비디오/업로드/이관

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/video/compress` | ReviewVideo__CompressView | 비디오 압축 |
| `/video/middle` | Review__ReviewVideoMiddleView | 중간 화질 비디오 |
| `/upload` | Review__ReviewUploadView | 리뷰 업로드 |
| `/transfer` | Review__InitialTransferView | 최초 이관 |
| `/transfer/estimation` | TestReview__InitialTransferView | 이관 예상 |
| `/transfer/widgetset-preview` | TestReview__InitialTransferWidgetSetupView | 위젯 세트 프리뷰 |

### 리뷰 요청

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/review-requests` | Review__ReviewRequestListView | 리뷰 요청 목록 |
| `/review-requests/request` | Review__ReviewRequestView | 리뷰 요청 생성 |
| `/review-requests/<int:request_id>/orders` | Review__ReviewRequestOrderListView | 요청별 주문 목록 |
| `/review-requests/<int:request_id>/orders/<int:id>` | Review__ReviewRequestOrderView | 요청별 주문 상세 |

### 챌린지

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/challenges` | ReviewChallengeList__View | 챌린지 목록 |
| `/challenges/<int:challenge_id>` | ReviewChallenge__View | 챌린지 상세 |
| `/challenges/check` | ReviewChallengeCheck__View | 챌린지 확인 |

### AI 태그/분석

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/tags` | ReviewTag__ListView | 태그 목록 |
| `/tags/common` | ReviewSharedTag__ListView | 공통 태그 목록 |
| `/tags/review-count` | ReviewTagRelation__View | 태그별 리뷰 수 |
| `/tags/<int:tag_id>` | ReviewTag__View | 태그 상세 |
| `/tags/<int:tag_id>/status` | ReviewTagUpdateStatus__View | 태그 상태 변경 |
| `/analysis-config` | ReviewAnalysisConfig__View | 분석 설정 |
| `/batch-analysis` | BatchAnalysis__View | 배치 분석 요청/조회 |
| `/v2/tags` | ReviewTag__ListView_V2 | 태그 목록 V2 |
| `/v2/tags/<int:tag_id>` | ReviewTag__View_V2 | 태그 상세 V2 |
| `/v2/tags/<int:tag_id>/status` | ReviewTagUpdateStatus__View_V2 | 태그 상태 V2 |
| `/v2/analysis-config` | ReviewAnalysisConfigList__View_V2 | 분석 설정 V2 |

---

## 4. 리뷰 V2 (review.v2.urls)

> 접두사: `v2/shops/<int:shop_id>/reviews`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `` | Review__ListView | 리뷰 목록 V2 |
| `/staff/status` | StaffReviewUploadStatus__View | 관리자 업로드 상태 |
| `/challenge` | ReviewChallenge__ListView | 챌린지 목록 V2 |
| `/phrases/tags` | ReviewPhraseTagInfo__View | 문구 태그 정보 |

---

## 5. 리뷰 정책 (shopreviewpolicy.urls)

> 접두사: `shops/<int:shop_id>/policy`

### 리뷰 제한

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/shop-permit` | ShopPermit__View | 리뷰 허용/제한 설정 |
| `/shop-permit/category` | ShopPermitCategory__View | 카테고리별 제한 |
| `/shop-permit/category/delete` | ShopPermitCategory__DeleteView | 카테고리 제한 삭제 |
| `/shop-permit/category/<int:id>` | ShopPermitCategory__DetailView | 카테고리 제한 상세 |
| `/shop-permit/product` | ShopPermitProduct__View | 상품별 제한 |
| `/shop-permit/product/delete` | ShopPermitProduct__DeleteView | 상품 제한 삭제 |
| `/shop-permit/product/<int:id>` | ShopPermitProduct__DetailView | 상품 제한 상세 |

### 정책/보상/검수

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/shop-policy` | ShopPolicy__View | 리뷰 정책 설정 |
| `/shop-reward` | ShopReward__ListView | 보상 설정 |
| `/confirm-option` | ShopConfirmOption__View | 검수 옵션 |
| `/shop-instagram` | ShopIntagram__View | 인스타그램 설정 |

### 댓글/키워드/공지

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/comment` | ShopCommentReview__ListView | 자동 댓글 목록 |
| `/comment/<int:comment_id>` | ShopCommentReview__DetailView | 자동 댓글 상세 |
| `/comment/<int:comment_id>/delete` | ShopCommentReview__DeleteView | 자동 댓글 삭제 |
| `/comment/reset` | ShopCommentReview__ResetView | 자동 댓글 초기화 |
| `/alert-keywords` | AlertKeyword__ListView | 알림 키워드 목록 |
| `/alert-keywords/<int:id>` | AlertKeyword__DetailView | 알림 키워드 상세 |
| `/alert-keywords/delete` | AlertKeyword__DeleteView | 알림 키워드 삭제 |
| `/alternative-keywords` | AlternativeKeyword__ListView | 대체어 목록 |
| `/alternative-keywords/<int:id>` | AlternativeKeyword__DetailView | 대체어 상세 |
| `/alternative-keywords/delete` | AlternativeKeyword__DeleteView | 대체어 삭제 |
| `/widget-notices` | WidgetNotice__ListView | 위젯 공지 목록 |
| `/widget-notices/<int:id>` | WidgetNotice__DetailView | 위젯 공지 상세 |
| `/keyword-option` | ShopKeywordReview__View | 키워드 리뷰 옵션 |
| `/wysiwygi/create` | WYSIWYGImage__View | WYSIWYG 이미지 업로드 |

---

## 6. 위젯 관리 (widget.urls) — V1

> 접두사: `shops/<int:shop_id>/widgets`
> **주의**: TO BE DEPRECATED — 구버전 위젯 제거 시 삭제 예정

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/sets` | WidgetSet__View | 위젯 세트 목록 |
| `/sets/<int:id>` | WidgetSet__DetailView | 위젯 세트 상세 |
| `/sets/<int:set_id>/widgets/<int:id>` | Widget__DetailView | 위젯 상세 |
| `/sets/init` | WidgetSet__InitialView | 위젯 세트 초기화 |

---

## 7. 위젯 V2 — 대시보드 (widget.v2.urls.dashboard_urls)

> 접두사: `v2/shops/<int:shop_id>/widgets`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/options/defaults` | WidgetOptionDefault__DashBoardView | 기본 옵션 |
| `/sets` | WidgetSet__DashBoardListView | 위젯 세트 목록 |
| `/sets/<int:widget_set_id>` | WidgetSet__DashBoardView | 위젯 세트 상세 |
| `/usage-stats` | WidgetTypeUsageStats__DashBoardView | 위젯 사용 통계 |
| `/sets/init` | WidgetSetInitial__DashBoardView | 위젯 초기화 |

---

## 8. 위젯 V2 — 스크립트 API (widget.v2.urls.script_urls)

> 접두사: `v2/api-widget`
> 이커머스 사이트에 삽입된 위젯 스크립트가 호출하는 API

### 기본 정보

| 경로 | 뷰 | 설명 |
|---|---|---|
| `` | Widget__View | 위젯 데이터 |
| `/check` | WidgetCheck__View | 위젯 체크 |
| `/meta` | WidgetMetaData__View | 메타데이터 |
| `/sets` | WidgetSet__View | 위젯 세트 |
| `/options` | WidgetOption__View | 위젯 옵션 |
| `/options/defaults` | WidgetOptionDefault__View | 기본 옵션 |
| `/permission` | WidgetPermission__View | 권한 확인 |
| `/shop-designs` | WidgetShopDesign__View | 샵 디자인 |
| `/survey-filters` | WidgetSurveyFilter__View | 설문 필터 |

### 리뷰 상세

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/reviews/<int:review_id>` | WidgetDetail__View | 리뷰 상세 |
| `/reviews/more` | WidgetDetailReviewList__View | 리뷰 더보기 |
| `/reviews/comments` | WidgetReviewComment__View | 리뷰 댓글 |
| `/reviews/badges` | WidgetReviewBadge__View | 리뷰 배지 |
| `/reviews/surveys` | WidgetReviewSurvey__View | 리뷰 설문 |
| `/reviews/keywords` | WidgetReviewKeyword__View | 리뷰 키워드 |

### 티커/재방문

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/extra/ticker/option` | WidgetExtraTickerOption__View | 티커 옵션 |
| `/extra/ticker/main` | WidgetExtraTickerMain__View | 메인 티커 |
| `/extra/ticker/product` | WidgetExtraTickerProduct__View | 상품 티커 |
| `/extra/revisit-popup` | WidgetExtraRevisitPopup__View | 재방문 팝업 |

### 모듈

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/module/review/count` | WidgetModuleReviewCount__View | 리뷰 수 |
| `/module/like` | WidgetModuleLike__View | 좋아요 |
| `/module/removelike` | WidgetModuleRemovelike__View | 좋아요 취소 |
| `/module/report` | WidgetModuleReport__View | 리뷰 신고 |
| `/module/write` | WidgetModuleWrite__View | 리뷰 작성 |
| `/module/widget/code` | WidgetModuleWidgetCode__View | 위젯 코드 |

---

## 9. 위젯 V2 — 프리뷰 (widget.v2.urls.urls)

> 접두사: `v2/widget`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/sets` | WidgetSetInstall__View | 위젯 세트 설치 |

---

## 10. 위젯 V1 — 프론트엔드 API (widget.view_widget.urls)

> 접두사: `api_widget`
> 이커머스 사이트에서 위젯이 직접 호출하는 V1 API (구버전)

### 위젯 서브 페이징

| 경로 | 함수 뷰 | 설명 |
|---|---|---|
| `/widget_sub/widget/highlight` | widget_sub_reviewHighlight | 평점 하이라이트 |
| `/widget_sub/widget/photo/paging` | widget_sub_photo_paging | 포토 페이징 |
| `/widget_sub/widget/smartpick/paging` | widget_sub_smartpick_paging | 스마트픽 페이징 |
| `/widget_sub/widget/boardAlphareview/paging` | widget_sub_boardAlphareview_paging | 게시판 페이징 |
| `/widget_sub/widget/simplephoto/paging` | widget_sub_simplephoto_paging | 심플포토 페이징 |
| `/widget_sub/widget/sns/paging` | widget_sub_sns_paging | SNS 페이징 |
| `/widget_sub/widget/best/paging` | widget_sub_best_paging | 베스트 페이징 |
| `/widget_sub/widget/best_text/paging` | widget_sub_best_text_paging | 베스트 텍스트 페이징 |
| `/widget_sub/widget/notice/paging` | widget_sub_notice_paging | 공지 페이징 |
| `/widget_sub/widget/boardgallery/paging` | widget_sub_boardGallery_paging | 갤러리 페이징 |
| `/widget_sub/widget/boardCafe24/paging` | widget_sub_boardCafe24_paging | CAFE24 게시판 페이징 |
| `/widget_sub/widget/boardProductList/paging` | widget_sub_boardProductList_paging | 상품 리스트 페이징 |
| `/widget_sub/widget/boardProductSlider/paging` | widget_sub_boardProductSlider_paging | 상품 슬라이더 페이징 |
| `/widget_sub/widget/writeButton/paging` | widget_sub_writebutton_paging | 작성 버튼 페이징 |
| `/widget_sub/widget/briefing/filter` | widget_sub_briefing_filter | 브리핑 필터 |
| `/widget_sub/widget/briefing/review` | widget_sub_briefing_review | 브리핑 리뷰 |
| `/widget_sub/widget/briefing/stat` | widget_sub_briefing_stat | 브리핑 통계 |

### 위젯 코어

| 경로 | 함수 뷰 | 설명 |
|---|---|---|
| `/widget` | widget_get | 위젯 조회 |
| `/widget_sub` | widget_sub_get | 서브 위젯 조회 |
| `/widget/checked_widget` | checked_is_widget | 위젯 존재 여부 |
| `/widget/story` | widget_story_detail | 스토리 상세 |
| `/widget/count` | widget_review_count | 리뷰 수 |
| `/widget/total` | widget_review_total | 전체 리뷰 |
| `/widget/pagination` | widget_review_pagination | 페이지네이션 |
| `/widget/filter` | widget_review_filter | 리뷰 필터 |
| `/widget/detail` | widget_detail | 리뷰 상세 |
| `/widget/detail/list` | widget_detail_list | 상세 목록 |
| `/widget/detail/review` | widget_detail_review | 상세 리뷰 |

### 프론트 모듈

| 경로 | 함수 뷰 | 설명 |
|---|---|---|
| `/front/floating` | module_popup_floating | 플로팅 팝업 |
| `/front/popup` | module_popup | 팝업 |
| `/front/order_item/get` | module_order_item_get | 주문 아이템 조회 |

### 모듈

| 경로 | 함수 뷰 | 설명 |
|---|---|---|
| `/module/review/count` | module_review_count | 리뷰 수 |
| `/module/review_write` | module_review_write | 리뷰 작성 |
| `/module/writebtn_auto` | module_writebtn_auto | 자동 작성 버튼 |
| `/module/writebtn_auto_position` | module_writebtn_auto_position | 작성 버튼 위치 |
| `/module/ticker_main` | module_ticker_main | 메인 티커 |
| `/module/ticker_product` | module_ticker_product | 상품 티커 |
| `/module/ticker_product_position` | module_ticker_product_position | 상품 티커 위치 |
| `/module/widget_set/code` | module_widget_set_code | 위젯 세트 코드 |
| `/module/session` | module_session | 세션 |
| `/module/review/product/like` | module_review_product_like | 리뷰 좋아요 |
| `/module/review/product/dislike` | module_review_product_dislike | 리뷰 싫어요 |
| `/module/review_report` | module_reviewReport | 리뷰 신고 |

---

## 11. 위젯 공통 (widget.common_urls)

> 접두사: `widget`
> **주의**: TO BE DEPRECATED

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/option/base` | WidgetOptionBase__View | 위젯 옵션 기본 |
| `/type-counts` | Widget__TypeCountView | 위젯 타입 카운트 |
| `/sets/preview` | WidgetSetPreview__View | 위젯 세트 프리뷰 |

---

## 12. 알림톡 (alimtalk.urls)

> 접두사: `shops/<int:shop_id>/alimtalk`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/setting` | AlimtalkSetting__View | 알림톡 설정 |
| `/logs` | AlimtalkMessageLog__View | 발송 로그 |
| `/logs/<int:id>/resend` | AlimtalkMessageLog__ResendView | 재발송 |
| `/logs/<int:id>/cancel` | AlimtalkMessageLog__CancelView | 발송 취소 |

### 알림톡 공통 (alimtalk.common_urls)

> 접두사: `alimtalk`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/test` | AlimtalkMessage__TestView | 테스트 발송 |

---

## 13. 상품 (product.urls)

> 접두사: `shops/<int:shop_id>/products`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `` | Product__ListView | 상품 목록 |
| `/<int:product_id>` | Product__DetailView | 상품 상세 |
| `/connections` | ProductConnectionGroup__ListView | 상품 연결 그룹 목록 |
| `/connections/delete` | ProductConnectionGroup__DeleteView | 연결 그룹 삭제 |
| `/connections/<int:id>` | ProductConnectionGroup__DetailView | 연결 그룹 상세 |
| `/connections/products` | ProductConnectionGroupProduct__ListView | 연결 상품 목록 |
| `/option-sets` | ProductOptionSet__ListView | 옵션 세트 목록 |
| `/option-sets/<int:id>` | ProductOptionSet__DetailView | 옵션 세트 상세 |
| `/review-number` | Product__UpdateReviewNumberView | 리뷰 수 업데이트 |

### 상품 V2 (product.v2.urls)

> 접두사: `v2/shops/<int:shop_id>/products`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/connections` | ProductConnectionGroup__ListView | 연결 그룹 목록 V2 |
| `/connections/<int:group_id>` | ProductConnectionGroup__View | 연결 그룹 상세 V2 |

---

## 14. 주문 (order.urls)

> 접두사: `shops/<int:shop_id>/orders`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/backdate-alimtalk` | OrderItem__BackdateView | 소급 알림톡 발송 |
| `/backdate-count` | OrderItem__BackdateCountView | 소급 대상 카운트 |

---

## 15. 외부연동 (external.urls)

> 접두사: `shops/<int:shop_id>/external`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/instagram` | InstagramMedia__ListView | 인스타그램 미디어 목록 |
| `/instagram/connection` | InstagramMedia__ConnectionVeiw | 인스타그램 연동 |
| `/blog/url` | NaverBlog__UrlView | 네이버 블로그 URL |
| `/blog` | NaverBlog__View | 네이버 블로그 관리 |
| `/smartstore` | SmartstoreReview__View | 스마트스토어 리뷰 |
| `/smartstore/product` | SmartstoreProduct__View | 스마트스토어 상품 |
| `/smartstore/product/<int:id>` | SmartstoreProduct__DetailView | 스마트스토어 상품 상세 |

---

## 16. 웹훅 (webhook.urls)

> 접두사: `webhook`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/review` | Review__WebhookView | 카페24 리뷰 웹훅 |
| `/review/facebook` | Review__WebhookFacebookView | Facebook/Instagram 웹훅 |

---

## 17. 마이페이지 (mypage.urls)

> 접두사: `shops/<int:shop_id>/mypage`
> 고객(소비자)이 사용하는 API

### 간편 조회 (Short)

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/short/` | MypageCommon__View | 공통 조회 |
| `/short/shop` | MypageShortShop__View | 샵 정보 |
| `/short/customer` | MypageShortCustomer__View | 고객 정보 |
| `/short/order` | MypageShortOrder__View | 주문 정보 |
| `/short/orderitem` | MypageShortOrderItem__View | 주문 아이템 |

### 고객 기능

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/common` | MypageCommon__View | 공통 |
| `/signin` | MypageSignin__View | 로그인 |
| `/status` | MypageStatus__View | 상태 |
| `/point` | MypagePoint__View | 포인트 |
| `/notice` | MypageNotice__View | 공지사항 |
| `/keyword` | MypageKeyword__View | 키워드 |
| `/survey/profile` | MypageSurveyProfile__View | 설문 프로필 |
| `/customer/search` | MypageCustomerSearch__View | 고객 검색 |

### 주문/리뷰

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/orderlist` | MypageOrderList__View | 주문 목록 |
| `/reviewlist` | MypageReviewList__View | 리뷰 목록 |
| `/order` | MypageOrder__View | 주문 조회 |
| `/order/unverified` | MypageOrderUnverified__View | 미검증 주문 |
| `/review` | MypageReview__View | 리뷰 작성 |
| `/review/quick` | MypageReviewQuick__View | 빠른리뷰 작성 |
| `/review/result` | MypageReviewResult__View | 리뷰 결과 |
| `/reviewmore` | MypageReviewMore__View | 리뷰 더보기 |
| `/reviewdelete` | MypageReviewDelete__View | 리뷰 삭제 |
| `/nonmember` | MypageNonmember__View | 비회원 |
| `/nonmember/apply` | MypageNonmemberApply__View | 비회원 포인트 신청 |
| `/challenges` | MyPageReviewChallenge__View | 챌린지 |
| `/challenges/check` | MyPageCheckReviewChallenge__View | 챌린지 확인 |

---

## 18. 시딩/캠페인 (seed.urls)

> 접두사: `shops/<int:shop_id>/seeds`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `` | SeedCampaign__ListView | 캠페인 목록 |
| `/summary` | SeedCampaign__SummaryView | 캠페인 요약 |
| `/<int:id>` | SeedCampaign__DetailView | 캠페인 상세 |

---

## 19. 세일즈 티커 (ticker.urls)

> 접두사: `shops/<int:shop_id>/ticker`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `` | Ticker__View | 티커 설정 |
| `/main` | Ticker__MainView | 메인 페이지 티커 |
| `/product` | Ticker__ProductView | 상품 페이지 티커 |

---

## 20. 인스타그램 피드 (instagramfeed.urls)

> 접두사: `shops/<int:shop_id>/feed`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `` | ShopInstagramFeed__View | 인스타그램 피드 설정 |
| `/design` | InstagramFeedDesignSetting__View | 피드 디자인 |
| `/media` | InstagramFeedInstagramMedia__ListView | 피드 미디어 목록 |
| `/media/count` | InstagramFeedInstagramMediaCount__View | 피드 미디어 수 |

---

## 21. 알람 (alarm.urls)

> 접두사: `shops/<int:shop_id>/alarms`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/request` | AlarmEvnet__View | 알람 이벤트 요청 |

---

## 22. 리포트 (report.urls)

> 접두사: `shops/<int:shop_id>/reports`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `` | ReviewAnalysisReport__ListView | 분석 리포트 목록 |

---

## 23. 분석 V2 (analytics.urls)

> 접두사: `v2/shops/<int:shop_id>/stats`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/voc-tags/graph` | AnalyticsTagTrendGraphView | VOC 태그 트렌드 그래프 |
| `/voc-tags/rankings` | AnalyticsKeywordRankingView | VOC 키워드 랭킹 |
| `/voc-tags/reviews` | AnalyticsKeywordReviewContentView | VOC 키워드 리뷰 |
| `/voc-tags/insights` | AnalyticsTagInsightView | VOC 태그 인사이트 |
| `/voc-tags/<int:tag_id>/detail` | AnalyticsTagDetailView | VOC 태그 상세 |

---

## 24. 리뷰 공통 (review.common_urls)

> 접두사: `review`

| 경로 | 뷰 | 설명 |
|---|---|---|
| `/survey/category/main` | SurveyQuestion__CategoryMainView | 설문 카테고리 대분류 |
| `/survey/category/sub` | SurveyQuestion__CategorySubView | 설문 카테고리 소분류 |
| `/keyword/category/main` | ReviewKeyword__CategoryMainView | 키워드 카테고리 대분류 |
| `/keyword/category/sub` | ReviewKeyword__CategorySubView | 키워드 카테고리 중분류 |
| `/keyword/category/subsub` | ReviewKeyword__CategorySubsubView | 키워드 카테고리 소분류 |

---

## 엔드포인트 통계 요약

| 도메인 | V1 엔드포인트 | V2 엔드포인트 | 합계 |
|---|---|---|---|
| 샵 설정/디자인/통계 | 28 | - | 28 |
| 리뷰 관리 | 56 | 4 | 60 |
| 리뷰 정책 | 25 | - | 25 |
| 위젯 (대시보드) | 4 | 5 | 9 |
| 위젯 (스크립트/프론트) | 44 | 25 | 69 |
| 위젯 공통 | 3 | 1 | 4 |
| 알림톡 | 5 | - | 5 |
| 상품 | 9 | 2 | 11 |
| 주문 | 2 | - | 2 |
| 외부연동 | 7 | - | 7 |
| 웹훅 | 2 | - | 2 |
| 마이페이지 | 24 | - | 24 |
| 시딩/캠페인 | 3 | - | 3 |
| 티커 | 3 | - | 3 |
| 인스타그램 피드 | 4 | - | 4 |
| 알람 | 1 | - | 1 |
| 리포트 | 1 | - | 1 |
| 분석 V2 | - | 5 | 5 |
| 리뷰 공통 | 5 | - | 5 |
| 시스템 | 1 | - | 1 |
| **합계** | **~227** | **~42** | **~269** |
