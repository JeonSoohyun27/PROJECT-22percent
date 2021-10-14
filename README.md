# [에잇퍼센트](https://8percent.kr/) Clone Project

## 프로젝트 소개
- React, Django를 이용한 [에잇퍼센트](https://8percent.kr/) 홈페이지 클론 프로젝트
- 두번째 협업 프로젝트로서, 데이터베이스 모델들의 관계를 활용할 수 있는 금융사이트 중 에잇퍼센트를 선정했습니다.
- 짧은 프로젝트 기간, 개발에 집중하기 위하여 디자인 및 기능의 기획 부분만 클론했습니다.
- 개발은 초기 세팅부터 전부 직접 구현하였습니다.

## 데모영상
(이미지 클릭시 유튜브 링크로 이동)

[![](https://img.youtube.com/vi/w6lc-QAqR7E/0.jpg)](https://www.youtube.com/watch?v=w6lc-QAqR7E)

## 프로젝트 참여자
- front-end: [황소미](https://github.com/somangoi), [정빛열음](https://github.com/kylee817), [장운서](https://github.com/unseoJang)
- back-end: [이동명](https://github.com/dom-lee), [이준영](https://github.com/Pratiable), [전수현](https://github.com/JeonSoohyun27)

## 프로젝트 기간
- 2021.7.19 - 2021.7.30

## 기술스택
- Front-End : JavaScript, React.js, sass, Styled-Components, Hooks
- Back-End : Python, Django, MySQL, Bcrypt, PyJWT
 
## API 문서
- https://documenter.getpostman.com/view/12180757/TzmChsx9

## ERD
![22percent_20210730_59_28](https://user-images.githubusercontent.com/46280353/127621262-b8a486d9-0ee2-4181-9847-dedd1a2c133f.png)

## 팀원별 역할
### 공통
- 프로젝트 초기 세팅
- Database 모델링 및 ERD 작성

### 이동명
* 회원가입 & 로그인
  - 비밀번호 BCRYPT 암호화
  - JWT ACCESS TOKEN 전송
  - SNS(카카오톡) 로그인
* 유저인증
  - JWT ACCESS TOKEN 유효성 검토
* 투자요약
  - 사용자 투자 한도에 따른 잔여한도
  - 투자 상품들의 원금회수 상태에 따른 투자 중 원금 DATA
  - 투자상품의 등급/카테고리/수익률별 분류
* 투자하기
  - 투자상품 투자하기

### 이준영

* 투자상품 List
  - 상품 상태(모집중, 모집예정, 모집완료 등)별 분류
  - 상품 카테고리(부동산, 개인신용 등)별 분류
  - 모집 중 상품의 진행상태(%), 모집금액 제공
* 메인페이지 누적투자액
  - 사이트에 등록된 총 상품의 누적 투자금액 DATA
* 투자이력
  - 투자 상품들의 원금 상태에 따른 투자 내역 DATA
  - 투자 상품의 현재 상환회차, 예상수익률, 투자시작일 DATA
  - 투자 상품 검색 기능 제공
  - 투자 전체 내역 EXCEL 다운로드

### 전수현

* 투자상품 상세페이지
  - 투자상품의 담보 안정성 DATA
  - 대출신청자의 신용 history 제공
  - 부동산 위치, 이미지 등 상세 DATA
  - 해당 상품에 투자시, 투자 금액별 예상 수익/세금/이용료 DATA
  - 기투자 여부 확인(로그인 시)
* 투자하기 페이지
  - 투자상품별 투자가능 금액 DATA
  - 사용자의 예치금 DATA

## Reference
- 이 프로젝트는 [에잇퍼센트](https://8percent.kr/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
