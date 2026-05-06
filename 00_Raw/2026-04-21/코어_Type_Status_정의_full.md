---
status: ready-for-raw
title: "코어 시스템 Type/Status 정의"
source: "https://www.notion.so/saladlab/Type-Status-2be46f3e549c8065bf9cdb91fce005d7"
created: 2026-04-21
cleaned: 2026-04-21
tags: [코어시스템, 데이터스키마, Type, Status]
note: "common/type.py, common/status.py 기준 — 마지막 동기화: 2026-03-31"
---

📜

## 유형(Type)과 상태(Status)

EPIC

비어 있음

Parent item

비어 있음

Sub-item

비어 있음

\[팀구분\]

🧬

코어 - Work Space

담당자

비어 있음

마지막수정

배준수

사람

비어 있음

사용중

생성자

이태용

전사공용

챕터

개발

태그

데이터 스키마

팀구분

비어 있음

Add a property

댓글

> common/type.py
> 
> ,
> 
> common/status.py
> 
> 기준 — 마지막 동기화: 2026-03-31

### 타입 (Type)

#### 앱 타입

class App\_\_Type(IntegerChoices): 공통 = 0 알파리뷰 = 100 알파업셀 = 200 알파푸시 = 300 알파캔버스 = 400

#### 플랜 타입

class Plan\_\_Type(IntegerChoices): 공통 = 0 # 플랜 무관 공통 값 무료 = 1 체험 = 2 라이트 = 300 베이직 = 400 그로스 = 500 비즈니스 = 600 엔터프라이즈1 = 700 엔터프라이즈2 = 800 엔터프라이즈3 = 900 엔터프라이즈4 = 1000 엔터프라이즈5 = 1100 엔터프라이즈6 = 1200

#### 플랜 한도 옵션 타입

class PlanLimitOption\_\_Type(IntegerChoices): 일반 = 100 # 기본 한도 안전 = 200 # 초과 시 자동 차단 무제한 = 300 # 한도 없음

#### 서비스 타입

class Service\_\_Type(IntegerChoices): 공통 = 0 # --- 보조 서비스 (실제 프로덕트가 아닌 과금/운영 단위) --- 기타결제 = 1 # 임의 청구용 예치금 = 2 # 선불 예치금 크레딧 = 3 # 할인 크레딧 메시지포인트 = 4 # 알림톡/친구톡 발송 포인트 트래픽포인트 = 8 # 트래픽 과금 포인트 설치요청 = 5 # CX 설치 요청 빌링 제거요청 = 6 # CX 제거 요청 빌링 미납금 = 7 # 미수금 정산용 위약금 = 9 # 계약 위약금 # --- 알파리뷰 --- 알파리뷰 = 100 롤링위젯 = 101 브리핑위젯 = 102 세일즈티커 = 103 스마트스토어리뷰연동 = 131 AI\_VOC = 132 # --- 알파업셀 --- 알파업셀 = 200 타임세일 = 201 # --- 알파푸시 / 알파캔버스 --- 알파푸시 = 300 알파캔버스 = 400

#### 구독 타입

class Subscription\_\_Type(IntegerChoices): 체험구독 = 1 # 무료 체험 기간 무료구독 = 2 # 무료 플랜 사용 정기구독 = 3 # 카드 자동결제 계약구독 = 4 # 영업팀 계약 기반

#### 구독 기간 타입

class SubscriptionPeriod\_\_Type(IntegerChoices): 월간 = 1 월간\_3개월 = 11 # 3개월 단위 월간 결제 월간\_6개월 = 12 월간\_9개월 = 13 연간 = 2 기타 = 3 모두 = 4 # 전체 기간 대상 (쿠폰 등에서 사용)

#### 구독 전환 방식

class SubscriptionConversion\_\_Method(IntegerChoices): 무료 = 10 # 무료→유료 전환 유료 = 20 # 유료→유료(플랜 변경) 중단 = 90 # 구독 중단

#### 구독 변경 타입

class SubscriptionChange\_\_Type(IntegerChoices): 업그레이드 = 100 다운그레이드 = 200 기타 = 300

#### 구독 변경 케이스

class SubscriptionChange\_\_Case(IntegerChoices): 기타 = 0 구독예약적용 = 100 # 예약된 구독 변경이 적용됨 플랜변경 = 200 서비스개시 = 300 서비스제거 = 400 구독유형전환 = 500 # 체험→정기 등 쿠폰적용 = 600

#### 구독 실행 타입

\# 구독 관련 작업의 실행 컨텍스트를 구분 class SubscriptionExecute\_\_Type(IntegerChoices): 기타 = 0 서비스개시 = 100 구독예약 = 200 서비스제거 = 300 플랜변경 = 400 구독유형변경 = 401 구독생성수정 = 500 해지승인 = 600 일간구독정산 = 700 # 일간 배치 정산 일간구독결제 = 800 # 일간 배치 결제 게좌이체입금확인 = 900 # 계좌이체 입금 확인 처리 수동재결제 = 1000 # 슈퍼관리자 수동 재결제 실패확정 = 1100 # 결제 최종 실패 확정 구독종료 = 1200

#### 구독 생성 원인

\# 구독이 생성된 원인과 경로를 추적 # 100번대: 체험구독, 200번대: 구독생성수정(슈퍼관리자), 300번대: 무료체험 # \_INITIALIZE: 최초 생성, \_RENEW: 갱신, \_CHANGE: 변경 class SubscriptionReason\_\_Type(IntegerChoices): 기타 = 0 체험구독\_INITIALIZE = 101 체험구독\_RENEW = 102 체험구독\_CHANGE = 103 구독생성수정\_INITIALIZE = 201 구독생성수정\_RENEW = 202 구독생성수정\_CHANGE = 203 무료체험\_INITIALIZE = 301 무료체험\_RENEW = 302 무료체험\_CHANGE = 303 취소 = 400 실패확정 = 500 갱신 = 600 복구 = 700 변경 = 800 서비스\_개시 = 900 # 서비스 설치 완료 시 슈퍼관리자\_개시 = 901 # 슈퍼관리자가 직접 개시

#### 구독 예약 사유 타입

class SubscriptionReservationReason\_\_Type(IntegerChoices): 체험구독 = 100 구독생성수정 = 200 # 슈퍼관리자가 구독을 직접 생성/수정 무료체험 = 300

#### 구독 생성/수정 케이스

class SubscriptionMake\_\_Case(TextChoices): CANCEL\_TRIAL\_RESERVE = "A" # 체험 취소 후 예약 CANCEL\_TRIAL\_MAKE = "B" # 체험 취소 후 즉시 생성 RESERVE = "C" # 예약만

#### 구독 과금 이력 타입

\# 업체의 구독 변경 이벤트를 구분 # 100번대: 과금이 추가되는 이벤트 # 200번대: 과금이 변경/감소되는 이벤트 class SubscriptionChargeHistory\_\_Type(IntegerChoices): 최초설치과금 = 101 재설치과금 = 102 유료전환과금 = 103 서비스추가\_최초설치 = 104 서비스추가\_재설치 = 105 플랜변경 = 201 서비스제거 = 202 구독종료 = 203 무료전환 = 204

#### Feature 타입

\# Features 레이어에서 실행 가능한 기능 목록 class Feature\_\_Type(Enum): 구독변경 = "change" 결제일자변경 = "set\_payment\_day" 해지요청 = "request\_terminate" 플랜한도옵션수정 = "change\_plan" 구독갱신 = "renew" 구독중단 = "stop" 구독수정 = "edit" 구독시작 = "start" 메시지포인트자동결제 = "auto\_pay\_message\_point"

#### 쿠폰/할인 타입

class Coupon\_\_Type(IntegerChoices): 할인 = 1 # 구독료 할인 체험 = 2 # 체험 기간 연장 크레딧 = 3 # 크레딧 지급 class Discount\_\_Method(IntegerChoices): 퍼센트 = 1 금액 = 2 class Discount\_\_Type(IntegerChoices): 결합 = 1 # 서비스 결합 할인 연간 = 2 # 연간 구독 할인 계약 = 3 # 계약 구독 할인 기타 = 100 결합\_커스텀 = 101 # 슈퍼관리자 커스텀 결합 할인 연간\_커스텀 = 201 계약\_커스텀 = 301 class DiscountCoupon\_\_Type(IntegerChoices): 일반 = 1 첫결제 = 2 # 첫 결제 시에만 적용

#### 결제 타입

class Payment\_\_Method(IntegerChoices): 카드 = 0 계좌이체 = 1

#### 청구서(Bill) 타입

class Bill\_\_Type(TextChoices): 구독 = "Subscription" # 정기 구독 청구서 보조 = "Assistant" # 설치/제거/메시지포인트 등 보조 청구서 임의 = "Custom" # 슈퍼관리자 수동 청구서

#### 임의 청구서(CustomBill) 타입

\# 슈퍼관리자가 수동으로 생성하는 청구서의 세부 유형 class CustomBill\_\_Type(IntegerChoices): 기타결제 = 1 기타환불 = 2 예치금입금 = 3 예치금환불 = 4 크레딧충전 = 5 크레딧제거 = 6 유료메시지포인트충전 = 10 유료메시지포인트제거 = 7 무료메시지포인트충전 = 11 무료메시지포인트제거 = 12 유료후불비용충전 = 17 유료후불비용제거 = 18 무료후불비용충전 = 13 무료후불비용제거 = 14 미납금결제 = 8 미납금제거 = 9 위약금결제 = 15 위약금제거 = 16

#### 보조 청구서(AssistantBill) 타입

\# 시스템이 자동 생성하는 보조 청구서의 세부 유형 class AssistantBill\_\_Type(IntegerChoices): 설치요청 = 1 # CX 설치 비용 제거요청 = 2 # CX 제거 비용 직접설치 = 3 # 업체 직접 설치 직접제거 = 4 # 업체 직접 제거 메시지포인트 = 5 # 메시지 포인트 충전 후불비용 = 6 # 후불 과금 정산

#### 정산(Adjustment) 타입

class AdjustmentSign\_\_Type(IntegerChoices): 증가 = 1 감소 = 2 # 정산 시 변경 대상 컬럼 class AdjustmentColumn\_\_Type(IntegerChoices): 결제대기 = 1 결제실패 = 2 미납금 = 3 # 정산이 발생하는 구체적인 액션 # 100번대: 생성, 200번대: 결제, 400번대: 실패, 500번대: 환불, 1000번대: 집계, 2000번대: 크레딧/예치금 class AdjustmentAction\_\_Type(IntegerChoices): 결제생성 = 100 구독생성 = 101 카드결제 = 200 계좌이체 = 201 계좌이체실패 = 202 결제최종실패 = 400 결제환불 = 500 구독환불 = 501 비용총계 = 1000 # 월간 비용 총계 미납금 = 1001 # 미납금 이월 크레딧추가적용 = 2000 예치금추가적용 = 2001

#### 일간 정산 기록 타입

\# 일간 정산 금액 기록의 원천 구분 class DailyAdjustmentAmountRecord\_\_Type(IntegerChoices): Bill = 100 Refund = 101 Subscription = 200 AssistantBill = 300 CustomBill = 400 MessagePoint = 500 TrafficPoint = 502 # 일간 정산 비용 기록의 처리 단계 구분 class DailyAdjustmentCostRecord\_\_Type(IntegerChoices): PaymentBuilder = 100 # 결제 빌더 생성 ApplyCredit = 200 # 크레딧 적용 ApplyDeposit = 300 # 예치금 적용 PayByCard = 400 # 카드 결제 CompleteAccount = 500 # 계좌이체 완료 TransferToPenalty = 600 # 위약금 전환 Refund = 700 # 환불 Incomplete = 800 # 미수 FinalFail = 801 # 최종 실패 class DailyAdjustmentCountRecord\_\_Type(IntegerChoices): AssistantBill = 100 CustomBill = 200

#### 이력 요약 타입

\# HistorySummary 모델에서 결제 이력을 요약할 때 사용하는 접미사 키 class HistorySummary\_\_Type(Enum): 일반결제 = "\_payment" 위약금결제 = "\_payment\_penalty\_cash" 미납금결제 = "\_payment\_unpaid\_cash" 예치금결제 = "\_payment\_deposit" 크레딧결제 = "\_payment\_credit" 환불 = "\_refund" 실패확정 = "\_final\_fail" 카드결제 = "\_pay\_by\_card" 크레딧쿠폰 = "\_credit\_coupon" 복구 = "\_revert"

#### 메시지포인트 사용 타입

\# 메시지 발송 시 포인트 소모 시점을 구분 class MessagePoint\_\_UseType(IntegerChoices): 일반소모 = 100 # 메시지 전송 전 포인트 소모 (일반적) 추가소모 = 200 # 메시지 전송 후 추가 소모가 필요할 때 추가잔액 = 300 # 메시지 전송 후 포인트가 남았을 때 (복원)

#### 후불비용(DefferedAmount) 이력 타입

class DefferedAmountHistory\_\_Type(IntegerChoices): 사용 = 100 충전 = 200 소멸 = 300 # 후불비용 변동의 원천 class DefferedAmountHistory\_\_Source(IntegerChoices): API = 1 # API 호출로 직접 처리 QUEUE = 5 # SQS Queue 비동기 처리 월간 = 100 # 월간 시스템 주기에 의한 충전/소모 체험 = 200 # 체험 포인트에 의한 충전/소모 청구서 = 300 # 청구서에 의한 충전/소모 기타 = 999

#### 관리자 계정 타입

class AdminAccount\_\_Type(IntegerChoices): 슈퍼관리자 = 0 # 알파앱스 내부 관리자 쇼핑몰관리자 = 1 # 쇼핑몰 업체 관리자 class AdminAccount\_\_UserRole(IntegerChoices): 관리자 = 0 # 쇼핑몰 대표 관리자 일반사용자 = 1 # 쇼핑몰 일반 사용자 class AdminAccount\_\_EmployeeRole(IntegerChoices): 개발자 = 0 CX = 1 영업 = 2 TECH\_OPERATION = 3 절대자 = 10 # 최고 권한

#### 샵 로그 타입

class ShopLog\_\_Type(IntegerChoices): 사이트 = 1 # 사이트 상태 변경 로그 서비스 = 2 # 서비스 설치/제거 로그 구독상태 = 3 # 구독 상태 변경 로그 구독예약상태 = 39 # 구독 예약 상태 변경 구독체험기간변경 = 40 # 체험 기간 수정 메시지포인트결제 = 4 업다운그레이드 = 5 # 플랜 변경 대시보드설정변경 = 6 디자인관련변경 = 7 기타 = 15 수신거부코드 = 16 # 080 수신거부 번호 변경 웹훅 = 17 슈퍼관리자 = 99 # 슈퍼관리자 수동 조작

#### 설치/제거 요청 타입

class InstallRemoveRequest\_\_Type(IntegerChoices): 자동설치 = 101 # 시스템 자동 설치 직접설치 = 102 # 업체가 직접 설치 설치요청 = 103 # CX팀에 설치 요청 자동제거 = 201 직접제거 = 202 제거요청 = 203 class InstallRemoveRequestData\_\_Key(TextChoices): REVIEW\_\_POINT\_DEFAULT = "리뷰\_포인트지급설정" REVIEW\_\_PUBLISH\_DEFAULT = "리뷰\_검수설정"

#### 이커머스 플랫폼 타입

class EcommercePlatform\_\_Type(TextChoices): CAFE24 = "cafe24" IMWEB = "imweb"

#### 수신거부 번호 등록 유형

class OptOutPhone\_\_Type(IntegerChoices): SELF\_OWNED = 1 # 업체가 직접 등록한 080 번호 SHARED = 2 # 알파앱스 공용 080 번호 + 4자리 코드 PLATFORM = 3 # Ecommerce Platform 제공 수신거부 번호

#### 발신번호 역할

class SenderPhone\_\_Role(IntegerChoices): BUSINESS = 100 # 사업자 번호 EMPLOYEE = 200 # 직원 번호 OTHER = 300 # 기타

#### 타임존

class Timezone(TextChoices): UTC = "UTC" ASIA\_SEOUL = "Asia/Seoul"

#### 환경 타입

class Environment\_\_Type(TextChoices): PRODUCTION = "PRODUCTION" DEV = "DEV" STAGING = "STAGING" LOCAL = "LOCAL"

#### 웹훅 타입

\# 코어 시스템이 처리하는 웹훅의 도메인 구분 class Webhook\_\_Type(Enum): 업체 = "Shop" 고객 = "Customer" 상품 = "Product" 주문 = "Order" 카테고리 = "Category" 혜택 = "ECommercePlatformBenefit" 쿠폰 = "Coupon"

#### Cafe24 웹훅 타입

class Cafe24WebhookEvent\_\_Type(Enum): 최초이관 = 1 # --- 상품 --- 상품생성 = 90001 상품정보변경 = 90002 상품삭제 = 90003 상품복구 = 90022 상품정보일괄변경 = 90041 상품품절상태변경 = 90150 # --- 주문 --- 주문생성 = 90023 주문배송상태변경 = 90024 주문입금상태변경 = 90025 주문취소상태변경 = 90026 주문반품상태변경 = 90027 주문교환상태변경 = 90028 주문환불상태변경 = 90029 주문상품추가 = 90031 주문수령자정보변경 = 90064 주문서삭제 = 90070 # --- 주문 일괄 --- 주문배송상태일괄변경 = 90071 주문취소상태일괄변경 = 90072 주문환불상태일괄변경 = 90073 주문반품상태일괄변경 = 90074 상품장바구니담기 = 90084 # --- 고객 --- 고객회원가입 = 90032 고객정보변경 = 90080 고객로그인 = 90143 고객회원등급변경 = 90144 고객회원탈퇴 = 90147 적립금변동 = 90148 # --- 쿠폰 --- 쿠폰수정 = 90151 쿠폰삭제 = 90152 쿠폰생성 = 90153 쿠폰발급상태변경 = 90154 # --- 카테고리 --- 카테고리생성 = 90042 카테고리수정 = 90043 카테고리삭제 = 90044 카테고리순서변경 = 90045 카테고리상품진열일괄변경 = 90046 # --- 프로모션 --- 프로모션생성 = 90047 프로모션수정 = 90048 프로모션삭제 = 90050 앱삭제 = 90077

#### 아임웹 웹훅 타입

class ImwebWebhookEvent\_\_Type(Enum): 앱삭제 = "INTEGRATION\_CANCELLATION" 상품삭제 = "SITE\_ADMIN\_SERVICE\_PRODUCT\_DELETE" # --- 주문 --- 주문생성 = "ORDER\_CREATE" 주문입금완료 = "ORDER\_DEPOSIT\_COMPLETE" 주문상품준비 = "ORDER\_PRODUCT\_PREPARATION" 주문배송대기 = "ORDER\_SHIPPING\_READY" 주문배송중 = "ORDER\_SHIPPING" 주문배송완료 = "ORDER\_SHIPPING\_COMPLETE" 주문운송장등록 = "ORDER\_INVOICE\_REGISTERED" 주문운송장수정 = "ORDER\_INVOICE\_UPDATED" 주문운송장삭제 = "ORDER\_INVOICE\_DELETED" # --- 고객 --- 고객회원가입 = "END\_USER\_SIGN\_UP" 고객정보변경 = "END\_USER\_INFO\_UPDATE" 고객회원등급변경 = "END\_USER\_GRADE\_UPDATE" 고객일괄등록 = "END\_USER\_SIGN\_UP\_BULK" 고객동의정보수정 = "END\_USER\_AGREE\_INFO\_UPDATE" 고객회원탈퇴 = "END\_USER\_WITHDRAWAL"

#### 코어 내부 이벤트 타입

class InternalEvent\_\_Type(TextChoices): COMMON\_PROCESSED = "System\_\_CommonProcessed" API\_CALLED = "System\_\_ApiCalled" WEBHOOK\_COMSUMED = "System\_\_WebhookConsumed" SHOP\_INITIALIZED = "Shop\_\_Initialized" INSTALL\_REQUEST\_REVIEW = "Service\_\_InstallRequested\_\_Review" INSTALL\_REQUEST\_UPSELL = "Service\_\_InstallRequested\_\_Upsell" INSTALL\_REQUEST\_PUSH = "Service\_\_InstallRequested\_\_Push" REMOVE\_REQUEST\_REVIEW = "Service\_\_RemoveRequested\_\_Review" REMOVE\_REQUEST\_UPSELL = "Service\_\_RemoveRequested\_\_Upsell" REMOVE\_REQUEST\_PUSH = "Service\_\_RemoveRequested\_\_Push" MIGRATION\_START = "Migration\_\_Start" MIGRATION\_END = "Migration\_\_End" MIGRATION\_\_PRODUCT\_START = "Migration\_\_Product\_Start" MIGRATION\_\_PRODUCT\_END = "Migration\_\_Product\_End" MIGRATION\_\_ORDER\_START = "Migration\_\_Order\_Start" MIGRATION\_\_ORDER\_END = "Migration\_\_Order\_End"

#### 웹훅 활성화 상태 변경 사유

class WebhookActiveStatusReason\_\_Type(IntegerChoices): 최초설치\_비활성화 = 100 설치요청접수대기\_비활성화 = 101 샵라이브종료\_비활성화 = 102 설치요청접수\_활성화 = 201 샵라이브\_활성화 = 202 블랙리스트제외\_활성화 = 203 블랙리스트변경\_부분활성화 = 301

#### 알림 이벤트 타입

\# 알림이 발송되는 트리거 이벤트 목록 # 1~99: 코어 공통, 100번대: 알파리뷰, 200번대: 알파업셀, 300번대: 알파푸시 class AlarmEvent\_\_Type(IntegerChoices): 코어\_카드결제\_성공 = 1 코어\_카드결제\_실패\_x일차 = 2 코어\_정기구독\_결제완료 = 3 코어\_정기구독\_결제실패\_x일차 = 4 코어\_카드결제\_미수 = 5 코어\_정기구독\_결제미수 = 6 코어\_계약구독종료\_x일전 = 7 코어\_메시지포인트\_결제완료 = 8 코어\_메시지포인트\_결제실패 = 9 코어\_한도x퍼센트\_안전한도O = 10 # 안전한도 ON 상태에서 한도 N% 도달 코어\_한도x퍼센트\_안전한도X = 11 # 안전한도 OFF 상태에서 한도 N% 도달 코어\_앱삭제 = 12 코어\_사이트\_구독종료 = 13 코어\_사이트\_해지완료 = 14 코어\_프로덕트\_서비스중단 = 15 코어\_슈퍼관리자에의한\_대시보드OFF = 16 코어\_앱삭제\_통합앱외라이브중 = 17 # 통합앱 외 라이브 중인데 앱 삭제 코어\_메시지포인트\_잔액부족\_카드등록필요 = 18 코어\_메시지포인트\_선납충전필요 = 19 코어\_후불비용\_결제완료 = 20 코어\_후불비용\_결제실패 = 21 코어\_페이스북\_토큰\_무효화 = 22 코어\_계좌이체\_입금요청 = 23 코어\_쿠폰\_노출\_첫결제 = 24 코어\_쿠폰\_만료예정 = 25 코어\_쿠폰\_사용완료 = 26 코어\_푸시체험종료\_첫결제할인안내 = 27 # 알파리뷰 (100번대) 리뷰\_프로덕트\_온보딩\_완료 = 101 리뷰\_서비스\_시작 = 102 리뷰\_무료체험\_x일차 = 103 리뷰\_카카오\_프로필\_변경 = 104 리뷰\_프로덕트\_온보딩\_이탈 = 110 리뷰\_서비스해지 = 111 리뷰\_설치요청\_접수 = 112 리뷰\_설치요청\_완료 = 113 리뷰\_제거요청\_접수 = 114 리뷰\_제거요청\_완료 = 115 리뷰\_엑셀\_다운로드 = 120 리뷰\_부정리뷰\_알람 = 130 리뷰\_AI\_VOC\_리포트 = 131 리뷰\_AI\_VOC\_모니터링\_알람 = 132 # 알파업셀 (200번대) 업셀\_프로덕트\_온보딩\_완료 = 201 업셀\_서비스\_시작 = 202 업셀\_무료체험\_x일차 = 203 업셀\_카드등록유도 = 204 업셀\_카드미등록으로인한\_서비스중단 = 205 업셀\_타임세일\_서비스\_시작 = 206 업셀\_설치요청\_접수 = 207 업셀\_설치요청\_완료 = 208 업셀\_제거요청\_완료 = 209 # 알파푸시 (300번대) 푸시\_메시지포인트\_자동충전실패\_캠페인중지 = 301 푸시\_메시지포인트\_자동충전성공\_캠페인활성화요청 = 302 푸시\_프로덕트\_온보딩\_완료 = 303 푸시\_무료체험\_시작 = 304 푸시\_무료체험\_종료\_x일전 = 305 푸시\_무료체험\_시작\_x일차 = 306

#### 알림 메시지 타입

class AlarmMessage\_\_Type(IntegerChoices): 이메일 = 100 알림톡 = 200 배너 = 300 스크림메시지박스 = 400 # 대시보드 내 팝업형 메시지 슬랙 = 500 문자메시지 = 600

#### 메시지 상세 타입

\# 실제 발송되는 메시지의 구체적인 채널/형식 class Message\_\_DetailType(IntegerChoices): 이메일 = 101 친구톡\_텍스트 = 201 친구톡\_이미지 = 202 친구톡\_와이드 = 203 친구톡\_캐러셀 = 204 알림톡 = 205 SMS = 251 LMS = 252 MMS = 253 웹푸시 = 900

#### 대시보드 공지 타입

class DashboardNotice\_\_Type(IntegerChoices): 공지사항 = 100 업데이트 = 200 이벤트 = 300 class DashboardNotice\_\_DisplayType(IntegerChoices): 최초1회 = 100 # 사용자당 1회만 노출 매일1회 = 200 항상 = 300

#### 업셀 위젯 타입

class UpsellWidget\_\_Type(TextChoices): 구매버튼\_상단\_위젯 = "W0001" 장바구니\_리스트\_상단\_위젯 = "W0002" 구매버튼\_상단\_위젯\_옵션형 = "W0003" 상품\_설명\_본문\_상단\_위젯 = "W0004" 상품\_설명\_본문\_하단\_위젯 = "W0005" 상세페이지\_최하단\_추천\_위젯 = "W0006" 전체\_상세페이지\_우상단\_위젯 = "W0007" 구매버튼\_클릭\_위젯 = "N0001" # 팝업형 장바구니버튼\_클릭\_위젯 = "N0002" # 팝업형

#### 큐 메시지 타입

\# SQS 큐에서 처리하는 메시지의 도메인 구분 class QUEUE\_MESSAGE\_\_TYPE(Enum): 주문\_\_이전\_주문\_날짜\_주문\_웹훅\_수신 = "order\_\_previous\_order\_date\_received" 주문 = "ORDER" 주문\_고객구매정보갱신 = "ORDER\_CUSTOMER\_PURCHASE\_INFO\_UPDATE" 고객 = "CUSTOMER" 고객\_마지막주문날짜 = "CUSTOMER\_LAST\_ORDER\_DATE" 상품 = "PRODUCT" 카테고리 = "CATEGORY" 혜택 = "BENEFIT" 택배사 = "PARCEL\_COMPANY"

#### 주문경로 타입

\# 주문이 발생한 경로 (플랫폼별로 다른 값 사용) class OrderPlaceId(Enum): # --- Cafe24 --- CAFE24\_cafe24 = "cafe24" CAFE24\_mobile = "mobile" # 모바일웹 CAFE24\_mobile\_d = "mobile\_d" # 모바일앱 CAFE24\_NCHECKOUT = "NCHECKOUT" # 네이버페이 CAFE24\_KAKAOPAY = "KAKAOPAY" CAFE24\_self = "self" # 카페24 자체 주문 # --- 아임웹 --- IMWEB\_IMWEB = "IMWEB" IMWEB\_NAVERPAY\_ORDER = "NAVERPAY\_ORDER" # 비회원 네이버 결제 IMWEB\_TALKCHECKOUT = "TALKCHECKOUT" # 비회원 카카오 결제 IMWEB\_SMARTSTORE = "SMARTSTORE" # 현재 미사용 etc = "etc"

#### 데이터 마이그레이션 타입

\# 이커머스 플랫폼 → 코어 시스템 데이터 이관 유형 class ShopMigration\_\_Type(IntegerChoices): 상품 = 100 정기배송상품 = 101 고객그룹 = 200 고객 = 300 고객\_라스트오더 = 301 혜택 = 400 혜택\_V2 = 401 # 혜택 구조 개선 임시 타입 쿠폰 = 410 쿠폰발급이력 = 411 적립금이력 = 420 주문 = 500 주문혜택 = 501 카테고리 = 600 카테고리\_V2 = 601 # 카테고리 구조 개선 임시 타입 배송 = 900 리뷰이관 = 1000 # 알파앱스 리뷰 데이터 마이그레이션

#### 배송 관련 타입

class ShippingMethod\_\_Type(TextChoices): 택배 = "shipping\_01" 빠른등기 = "shipping\_02" 직접배송 = "shipping\_04" 퀵배송 = "shipping\_05" 기타 = "shipping\_06" 화물배송 = "shipping\_07" 매장직접수령 = "shipping\_08" 배송필요없음 = "shipping\_09" class ShippingType\_\_Type(TextChoices): 국내배송 = "A" 해외배송 = "C" 국내\_해외배송 = "B" # 배송비 부과 방식 class ShippingFeeType\_\_Type(TextChoices): 배송비무료 = "T" 고정배송비 = "R" 구매금액부과 = "M" # 구매 금액에 따른 부과 구매금액별차등 = "D" 상품무게별차등 = "W" 상품수량별차등 = "C" 상품수량비례부과 = "N" # 배송비 산정 기준금액 class ShippingFeeCriteria\_\_Type(TextChoices): 할인전정상판매가격기준 = "D" # 권장 최종주문금액기준 = "L" 할인적용후결제금액 = "A" 최종실결제금액기준 = "R" class PrepaidShippingFee\_\_Type(TextChoices): 착불 = "C" 선결제 = "P" 착불\_선결제 = "B" class SupplierSelection\_\_Type(TextChoices): 전체공급사 = "A" 특정공급사 = "P" class SupplierShippingCalculation\_\_Type(TextChoices): 전체상품금액합계 = "A" 별도합계 = "S" # 대표운영자와 공급사 상품 별도 합계 class SupplierRegionalSurcharge\_\_Type(TextChoices): 대표운영자\_지역별부과 = "A" 공급사관리자\_설정부과 = "S"

#### 앱 설치 오류 타입

class AppInstallError\_\_Type(IntegerChoices): 부운영자\_계정\_로그인 = 100 # 부운영자 계정으로 설치 시도 인증\_코드\_만료 = 200 설치\_가능\_업체\_수\_초과 = 1000 # 앱 검수 모드에서만 발생 원인\_미상 = 9999

#### 앱 설치 알림 타입

class AppInstallAlarm\_\_Type(Enum): 앱최초설치 = "앱스토어 클릭 👀" 앱설치 = "앱설치 알림 👍" 온보딩중 = "온보딩중 알림 🚀"

#### 티켓 관련 타입

class Ticket\_\_Category(TextChoices): 설치제거 = "설치/제거" 추가요청 = "추가요청" class Ticket\_\_SecondTicketCategory(TextChoices): 설치요청 = "설치요청" 제거요청 = "제거요청" 스마트스토어 = "스마트스토어" 위젯관련 = "위젯관련" 리뷰이관 = "리뷰이관" 기타 = "기타" 이슈 = "이슈" class Ticket\_\_ThirdTicketCategory(TextChoices): # 추가요청 > 스마트스토어 계정확인 = "계정 확인" 상품정보갱신 = "상품정보 갱신" 리뷰이관 = "리뷰 이관" # 추가요청 > 리뷰이관 위젯추가세팅 = "위젯 추가 세팅" 설치후AS = "설치 후 AS" 위젯디자인수정 = "위젯 디자인 수정" 리뷰개수모듈설치 = "리뷰 개수 모듈 설치" 카페24리뷰누락 = "카페24 리뷰 누락" 쇼핑몰간리뷰이관 = "쇼핑몰 간 리뷰 이관" 리뉴얼로인한재설치 = "리뉴얼로 인한 재설치" 기타 = "기타" class Ticket\_\_Label(TextChoices): 일순위 = "1순위" # 긴급, ASAP 이순위 = "2순위" # 업무시간 내 답변 삼순위 = "3순위" # 이번 주 내 답변 class TicketAlarm\_\_Type(Enum): ENROLL = "ENROLL" # 티켓 등록 REOPEN = "REOPEN" # 티켓 재오픈 REMINDER = "REMINDER" # 리마인더 PUSH = "PUSH" # 슈퍼관리자 슬랙 푸시 THREAD\_PUSH = "THREAD\_PUSH" # 스레드 슬랙 푸시

#### 고객 타겟 필터 타입

#### 데이터 인사이트 타입

class DataInsightOutputMethod\_\_Type(TextChoices): SPREADSHEET = "SPREADSHEET" FILE = "FILE" # 자동 리포트 종류 class DataInsightContent\_\_Type(TextChoices): NOT\_PAID\_BILL\_BY\_CARD = "NOT\_PAID\_BILL\_BY\_CARD" NOT\_PAID\_BILL\_BY\_ACCOUNT = "NOT\_PAID\_BILL\_BY\_ACCOUNT" RECENTLY\_INSTALLED\_SHOP = "RECENTLY\_INSTALLED\_SHOP" ADJUSTMENT = "ADJUSTMENT" DAILY\_SNAPSHOT = "DAILY\_SNAPSHOT" EXPIRED\_CONTRACT\_SUBSCRIPTION\_IN\_30DAYS = "EXPIRED\_CONTRACT\_SUBSCRIPTION\_IN\_30DAYS" ALL\_GENERAL\_DATA = "ALL\_GENERAL\_DATA" REVIEW\_PAYMENT = "REVIEW\_PAYMENT" UPSELL\_PAYMENT = "UPSELL\_PAYMENT" DAILY\_SNAPSHOT\_V2 = "DAILY\_SNAPSHOT\_V2" # 알파앱스 지표(cafe24) DAILY\_SNAPSHOT\_V2\_IMWEB = "DAILY\_SNAPSHOT\_V2\_IMWEB" # 알파앱스 지표(imweb) REMOVE\_REQUEST = "REMOVE\_REQUEST" INSTALL\_REQUEST = "INSTALL\_REQUEST" ONBOARDING\_START = "ONBOARDING\_START" class FileExtension\_\_Type(TextChoices): CSV = "CSV" XLSX = "XLSX"

#### 스크립트 파일 타입

\# 이커머스 플랫폼에 삽입되는 JS 스크립트 파일 식별자 class ScriptFile\_\_Type(TextChoices): CORE\_DATA = "alphacore\_alpha\_data.js" ALPHA\_APPS\_RUNTIME = "AlphaAppsRuntime.iife.min.js" # 푸시 PUSH\_LOG = "alphapush\_log.js" PUSH\_MAIN = "alphapush\_main.js" PUSH\_GA = "alphapush\_GA.js" PUSH\_QUICK\_SIGNUP = "alphapush\_quick\_signup.js" PUSH\_GIFT = "alphapush\_gift.js" PUSH\_BANNER = "alphapush\_banner.js" PUSH\_FIRSTORDER = "alphapush\_firstorder.js" PUSH\_MILEAGE = "alphapush\_mileage.js" PUSH\_ONSITE = "alphapush\_onsite.js" PUSH\_FUNNEL = "alphapush\_funnel.js" # 업셀 UPSELL\_SHADOW\_BUNDLE = "alpha-upsell-shadow-bundle.js" UPSELL\_ORDER\_BASKET = "ORDER\_BASKET.js" UPSELL\_ORDER\_FORM = "ORDER\_ORDERFORM.js" UPSELL\_ORDER\_RESULT = "ORDER\_ORDERRESULT.js" UPSELL\_PRODUCT\_DETAIL = "PRODUCT\_DETAIL.js" UPSELL\_GA = "alphaupsell\_GA.js" UPSELL\_LOG = "alphaupsell\_log.js" UPSELL\_ORDER\_BASKET\_WIDGET = "ORDER\_BASKET\_widget.js" UPSELL\_PRODUCT\_DETAIL\_NUDGE = "PRODUCT\_DETAIL\_nudge.js" # 리뷰 REVIEW\_BRIEFING\_WIDGET = "briefing\_widget.js" REVIEW\_LOGIN\_POPUP = "login\_popup.js" REVIEW\_MYSHOP\_ORDER\_LIST = "MYSHOP\_ORDER\_LIST.js" REVIEW\_COUNT = "review\_count.js" REVIEW\_WRITE\_BUTTON\_AUTO = "reviewWrite\_button\_auto.js" REVIEW\_WRITE\_BUTTON = "reviewWrite\_button.js" REVIEW\_TICKER\_MAIN = "ticker\_main.js" REVIEW\_TICKER\_PRODUCT = "ticker\_product.js" REVIEW\_WIDGET = "widget.js" REVIEW\_INSTAGRAM\_FEED = "alphareview\_instagram\_feed.js" REVIEW\_GA = "alphareview\_GA.js" REVIEW\_KEYWORD\_REVIEW = "keyword\_widget.js" REVIEW\_CAFE24\_INITIAL = "alpha-review-cafe24-initial.min.js" REVIEW\_IMWEB\_INITIAL = "alpha-review-imweb-initial.min.js" REVIEW\_IMWEB\_ALPHA\_AU = "imweb-alpha-au.min.js"

#### S3 스토리지 클래스

class S3StorageClass\_\_Type(TextChoices): STANDARD = "STANDARD" # 자주 접근하는 데이터 REDUCED\_REDUNDANCY = "REDUCED\_REDUNDANCY" # AWS 비권장 STANDARD\_IA = "STANDARD\_IA" # 드물게 접근, 밀리초 응답 ONEZONE\_IA = "ONEZONE\_IA" # 단일 AZ, 20% 저렴 INTELLIGENT\_TIERING = "INTELLIGENT\_TIERING" # 자동 비용 최적화 GLACIER = "GLACIER" # 아카이브(분~시간 검색) DEEP\_ARCHIVE = "DEEP\_ARCHIVE" # 최장기 보관(12시간 검색) OUTPOSTS = "OUTPOSTS" # 온프레미스용 GLACIER\_IR = "GLACIER\_IR" # 즉시 검색 아카이브 SNOW = "SNOW" # 오프라인 전송용 EXPRESS\_ONEZONE = "EXPRESS\_ONEZONE" # 마이크로초 지연 FSX\_OPENZFS = "FSX\_OPENZFS" # FSx 백업용

#### API 필터 타입

\# API 쿼리셋 분기 처리에 사용되는 필터 플래그 class APIFilter\_\_Type(Enum): SHOP\_\_BASIC\_SEARCH = "shop\_\_basic\_search" CUSTOMER\_\_BASIC\_SEARCH = "customer\_\_basic\_search" ORDER\_\_BASIC\_SEARCH = "order\_\_basic\_search" ORDER\_\_UPSELL\_ORDERS = "order\_\_upsell\_orders" ORDER\_\_PUSH\_GIFT\_ORDERS = "order\_\_push\_gift\_orders" PRODUCT\_\_BASIC\_SEARCH = "product\_\_basic\_search" PRODUCT\_\_RECOMMENDED = "product\_\_recommended" PRODUCT\_\_AI\_EXCLUDE = "product\_\_ai\_exclude" # 품절/삭제/정기배송 제외 PRODUCT\_\_UPSELL\_SEARCH = "product\_\_upsell\_search"

#### 기타 타입

class Task\_\_Type(TextChoices): ECPLATFORM\_DATA\_MIGRATION = "ECPLATFORM\_DATA\_MIGRATION" # ShopMigration 구버전 (이관 후 제거 예정) class ShopMigration\_\_OldType(IntegerChoices): 상품 = 100 정기배송상품 = 101 고객그룹 = 200 혜택 = 300 주문 = 400 고객 = 500 카테고리 = 600 고객\_라스트오더 = 700 주문혜택 = 800 배송 = 900

### 상태 (Status)

#### 샵 메인상태 (사이트상태)

class Shop\_\_MainStatus(IntegerChoices): 계정활성화 = 100 # Cafe24 인증 완료 앱설치 = 200 # 앱 설치됨 사이트생성 = 300 # 코어 시스템에 사이트 생성 필수세팅완료 = 400 # 온보딩 필수 세팅 완료 라이브 = 500 # 서비스 운영 중 구독종료 = 600 # 구독 종료됨 (재개 가능) 해지완료 = 700 # 완전 해지 리드이탈 = 800 # 온보딩 미완료 이탈 앱삭제 = 900 # 앱 삭제됨

#### 샵 종속상태

class Shop\_\_SubStatus\_\_Key(Enum): 재도입여부 = "재도입여부" 기본정보등록여부 = "기본정보등록여부" 필수정보등록여부 = "필수정보등록여부" 카드등록여부 = "카드등록여부" 라이브유형 = "라이브유형" 구독종료유형 = "구독종료유형" class Shop\_\_SubStatus\_\_Value: class 재도입여부(Enum): 최초도입 = 101 재도입 = 102 class 기본정보등록여부(Enum): 미등록 = 201 등록완료 = 202 class 필수정보등록여부(Enum): 미등록 = 301 등록완료 = 302 class 카드등록여부(Enum): 미등록 = 401 등록완료 = 402 카드등록면제 = 403 # 계약구독 등 카드 불필요 class 라이브유형(Enum): 슈퍼관리자\_구독예약중 = 501 유료구독중 = 502 체험구독중 = 503 무료구독중 = 504 계약구독중 = 505 class 구독종료유형(Enum): 일시중지 = 601 해지요청 = 602 결제실패이탈 = 603 기타 = 604 앱삭제 = 605

#### 샵 결제정보 상태

class ShopPaymentInfo\_\_MainStatus(IntegerChoices): 카드등록대기 = 100 카드등록완료 = 300 카드등록면제 = 500 # 계약구독 등 카드 불필요 class ShopPaymentInfo\_\_SubStatus\_\_Key(Enum): 결제상태 = "결제상태" class ShopPaymentInfo\_\_SubStatus\_\_Value: class 결제상태(Enum): 결제정상 = 101 결제실패중 = 102 # 카드 결제 실패 상태 지속 중

#### 결제 상태

class Payment\_\_MainStatus(IntegerChoices): 대기 = 100 성공 = 200 실패 = 400 미수 = 402 # 결제 실패했으나 서비스는 유지 (재시도 대상) 실패확정 = 403 # 최종 실패 확정 (서비스 중단) 환불 = 600 class PaymentHistory\_\_MainStatus(IntegerChoices): 대기 = 100 성공 = 200 실패 = 400 취소 = 500 class Refund\_\_MainStatus(IntegerChoices): 대기 = 100 성공 = 200 실패 = 400 취소 = 500

#### 쿠폰 상태

\# Coupon: 쿠폰 마스터 데이터의 상태 class Coupon\_\_MainStatus(IntegerChoices): 대기 = 100 # 아직 활성화되지 않음 유효 = 200 # 사용 가능 상태 완료 = 300 # 사용 완료 또는 기간 만료 중단 = 500 # 관리자에 의해 중단됨 # ShopCoupon: 쇼핑몰에 적용된 쿠폰 인스턴스의 상태 class ShopCoupon\_\_MainStatus(IntegerChoices): 대기 = 100 적용중 = 201 # 현재 할인이 적용되고 있음 완료 = 300 만료 = 500

#### 구독 상태

class Subscription\_\_MainStatus(IntegerChoices): 대기 = 100 결제대기 = 200 사용중 = 201 완료 = 300 결제실패 = 400 취소 = 500 취소\_구독변경 = 501 # 구독 변경(업/다운그레이드)으로 인한 기존 구독 취소 취소\_실패확정 = 502 # 결제 최종 실패로 인한 취소 구독중단 = 600 # 일시 중단 (재개 가능) 무효 = 700 무효\_구독변경 = 701 # 구독 변경으로 인해 무효화된 구독 class SubscriptionReservation\_\_MainStatus(IntegerChoices): 예약중 = 1 완료 = 2 취소 = 3

#### 구독 종속상태

class Subscription\_\_SubStatus\_\_Key(Enum): 한도 = "한도" 계약구독여부 = "계약구독여부" class Subscription\_\_SubStatus\_\_Value: class 한도(Enum): 무제한한도 = 101 안전한도 = 102 # 한도 초과 시 자동 차단 일반한도 = 103 # 한도 초과 허용 class 계약구독여부(Enum): 계약구독중 = 201 슈퍼관리자\_계약구독중 = 202 # 슈퍼관리자가 직접 설정

#### 앱/서비스 상태

class ShopService\_\_MainStatus(IntegerChoices): 구독없음 = 100 프로덕트온보딩중 = 200 # 설치 진행 중 라이브 = 300 # 서비스 운영 중 제거중 = 400 서비스중단 = 500 class ShopService\_\_SubStatus\_\_Key(Enum): 재설치여부 = "재설치여부" 이탈유형 = "이탈유형" 라이브유형 = "라이브유형" class ShopService\_\_SubStatus\_\_Value: class 재설치여부(Enum): 최초설치 = 101 재설치 = 102 class 이탈유형(Enum): 과금중이탈 = 201 # 유료 구독 중 이탈 과금전이탈 = 202 # 체험/무료 중 이탈 class 라이브유형(Enum): 과금중 = 301 체험중 = 302 무료구독중 = 303 계약구독중 = 304

#### 서비스 설치 요청 상태

class ShopServiceInstallationRequest\_\_MainStatus(IntegerChoices): 상태없음 = 0 접수전 = 10 요청접수 = 20 접수취소 = 40 서비스개시 = 100 class ShopServiceInstallationRequest\_\_SubStatus\_\_Key(Enum): 설치유형 = "설치유형" 직접설치상태 = "직접설치상태" class ShopServiceInstallationRequest\_\_SubStatus\_\_Value: class 설치방식(Enum): 설치요청 = 100 # CX팀 요청 직접설치 = 200 # 업체 직접 자동설치 = 300 # 시스템 자동 class 직접설치상태(Enum): 직접설치중 = 201 직접설치완료 = 210

#### 월간 시스템 주기 상태

class MonthlySystemCycle\_\_MainStatus(IntegerChoices): 대기 = 100 진행중 = 200 완료 = 300 class MonthlySystemCycle\_\_SubStatus\_\_Key(Enum): 플랜한도옵션변경상태 = "플랜한도옵션변경상태" class MonthlySystemCycle\_\_SubStatus\_\_Value: class 플랜한도옵션변경상태(IntegerChoices): 기본 = 100 FROM\_일반\_TO\_안전\_IN\_초과\_BY\_Shop = 200 # 초과로 인해 자동 전환

#### 청구서 상태

class CustomBill\_\_MainStatus(IntegerChoices): 대기 = 100 진행중 = 200 완료 = 300 실패 = 400 class AssistantBill\_\_MainStatus(IntegerChoices): 대기 = 100 결제성공 = 101 # 결제 완료, 처리 대기 결제실패 = 102 # 결제 실패, 재시도 필요 진행중 = 200 # 후속 처리 중 (설치/제거 등) 완료 = 300 실패 = 400 # 후속 처리 실패 취소 = 500

#### 메시지포인트 상태

class MessagePoint\_\_MainStatus(IntegerChoices): 정상 = 100 결제실패 = 200 # 자동 충전 결제 실패 중지 = 400 # 포인트 사용 중지

#### 알림 메시지 상태

class AlarmMessage\_\_MainStatus(IntegerChoices): 대기 = 100 진행중 = 200 완료 = 300 실패 = 400

#### 설치/제거 요청 상태

class InstallRemoveRequest\_\_MainStatus(IntegerChoices): 대기 = 100 진행중 = 200 완료 = 300 취소 = 400 제거 = 500 # 요청 자체가 제거됨 실패 = 600

#### 마이그레이션 상태

class ShopApp\_\_MigrateStatus(IntegerChoices): 이관전 = 100 이관중 = 200 이관후 = 300 class ShopMigrationInfo\_\_MainStatus(IntegerChoices): 대기 = 100 진행중 = 200 완료 = 300 실패 = 400 기타 = 0

#### 긴급 기능 이력 액션

\# 긴급 상황 시 스크립트를 강제 ON/OFF하는 이력 class EmergencyFeatureHistory\_\_Action(TextChoices): 업셀스크립트 = "업셀스크립트" 푸시스크립트 = "푸시스크립트"

#### 티켓 상태

class Ticket\_\_Status(TextChoices): 등록 = "등록" 접수 = "접수" 확인필요 = "확인필요" 완료 = "완료" 보류 = "보류" 보류취소 = "보류취소" 아카이브 = "아카이브" 종료 = "종료" # 티켓 내 스레드의 유형 class Ticket\_\_ThreadStatus(TextChoices): 등록 = "등록" 스레드 = "스레드" # 일반 댓글 상태변경 = "상태변경" # 상태 변경 기록 티켓내용수정 = "티켓내용수정" 푸시알람 = "푸시알람" # 슬랙 푸시 기록

#### 웹훅 활성화 상태

class ShopDetailWebhookActive\_\_Status(IntegerChoices): 비활성화 = 100 활성화 = 200 부분활성화 = 300 # 일부 웹훅만 활성화 (블랙리스트 등)

#### 등록 상태

\# 발신번호, 수신거부번호 등의 등록 상태 # 비즈엠 API 매핑: R/I→REVIEWING, A→REGISTERED, C→REJECTED class Registration\_\_Status(IntegerChoices): NOT\_REGISTERED = 100 REVIEWING = 200 REGISTERED = 300 REJECTED = 400