---
id: b92fcd62-8e75-430b-b5db-d86f912c96b7
category: "[[10_Wiki/🛠️ Projects/SaladLab]]"
confidence_score: 0.96
tags: [알파리뷰, 데이터모델, DB, Backend, SaladLab, 리뷰, 상태관리]
last_reinforced: 2026-04-13
github_commit: ""
---

# [[AI] 리뷰 데이터 모델 및 상태 관리]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 알파리뷰의 Review 모델은 단순 평가 데이터를 넘어, 상태 머신(게시/혜택 상태)과 15개 이상의 하위 테이블을 관장하며, 원본/복사본 메커니즘(`review_origin`)을 통해 데이터 무결성을 추적하는 서비스의 마스터 허브 역할을 한다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** "리뷰 도메인의 허브 구조." 리뷰는 `Shop`, `Product`, `OrderItem`의 핵심 부모를 두고, `Photo`, `Video`, `MediaIndex` 같은 미디어 컴포넌트와 `Reward`, `Log`, `Comment`, `AI` 등의 부가 기능을 1:N으로 주렁주렁 매달고 있는 중앙 집중식 데이터 구조를 취한다.
- **세부 내용:**
    - **핵심 데이터 및 인덱싱:** 기본 필드 외에 GA 트래킹(`ga_event`), CDN 기반 미디어 처리, 숏 URL용 base62 인코딩(`review_no_new`), 다양한 복합 인덱스(조회수/시계열/작성자별/위젯옵션별 정렬) 최적화.
    - **상태 관리 전이 (Machine):** 
        - **게시 상태 (Posting Status):** 게시예정(10) / 게시대기(11, default) / 게시됨(20) / 숨김(21)
        - **혜택 상태 (Reward Status):** 생성 시 지급대기(11) → 조건 달성에 따라 지급예정(10) / 비회원대기(12) / SNS대기(13) → 완료(20, 40) 혹은 예외종료(취소/실패/제한/포인트없음) → 지급 후 취소 시 회수예정/완료(30, 31).
    - **원본-편집본 버전 관리:** 수정을 요청하면 기존 데이터를 파기하지 않는다. 기존 코어의 `creater_type`을 **원본(100)**으로 전환하고, 신규 리뷰를 만든 뒤 OneToOneField(`review_origin`)로 묶어 이력을 보존한다. 보상과 노출의 모든 기준은 가장 최신의 **편집본**이다.
    - **자동화 로직 동작 (`save` & `delete`):** `is_verified` 로직으로 실구매 여부 판별. 저장 훅(`save`)을 통해 별점 클램핑 및 최적화, 자동 평점(`quick_written_rating`) 스토리지 동기화가 이뤄진다. 

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 삭제 로직(`delete`)이 현재는 실제 DB 파기(하드 삭제 및 CASCADE)를 유발하지만, 소프트 삭제(`is_deleted = True`) 체제로 마이그레이션이 주석상에 기재되어 과도기적인 상태. Instagram 연관 데이터는 ORM CASCADE가 아닌 수동 삭제 로직을 타고 있음에 주의. 소셜 로그인 관련 프로바이더 구분이 이메일 suffix(`@k`, `@n`)에 의존해 취약했으며 현재는 deprecated 상태.
- **정책 변화:** 기존의 "리뷰 종류 정리", "알파리뷰 포인트 지급 정책" 등에서 확인하던 '원본/복사본 모델', '상태코드 1x~4x 매핑'의 내부 Backend 구현 구조를 정확히 도식화하여 시스템 지식과 기획 지식을 병합.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects/SaladLab]]
- **Related:** [[알파리뷰 포인트 지급 정책]], [[리뷰 종류 정리]]
- **Raw Source:** [[00_Raw/Clippings/Where teams and agents work together 3.md]]
