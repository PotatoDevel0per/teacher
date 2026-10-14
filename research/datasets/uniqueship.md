# UniqueShip 로컬 사본

- 위치: `/jhlee/UWShipNoise/data/uniqueship/`
- 받은 날짜: 2026-10-05. 받은 방법: rclone(`jhlee_remote`, 공유 폴더 `--drive-root-folder-id`). 원본은 Dataset Version 1.0
- 무결성: rclone check 차이 0건, `unzip -t` 오류 없음
- 논문 노트: `papers/notes/2026_hashemi_uniqueship.md`

## 12 Class - 5h Each (`12class_5h/stage/allclass_5hours/`, 26 GB) — `confirmed` (직접 집계)

- 구성: `audio/<class>/*.wav`(5 s), `fold_1..5/metadata_5s_{train,validation,test}.csv`(42열)
- 오디오: **32 kHz**, mono, PCM_32, 5.0 s (논문 본문의 "20 kHz 리샘플"과 다름 → baseline을 재현할 때 확인 필요)
- 클래스 12개, 각 약 3,600 클립. 총 43,208 클립
- 누수 검사 (5 fold 모두):
  - train/val/test 사이 MMSI 겹침 0
  - 배경 날짜 겹침 0
  - 5 fold의 test 선박 1,864척이 모두 서로 다름
  - test CSV의 경로는 전부 존재
- **주의: 이 부분집합은 클래스별 평가에 부적합하다.**
  - dredger와 pilotvessel은 fold마다 test 선박이 0–1척이다.
  - fold 2 test는 pilotvessel 1척이 3,565클립으로, test의 63%를 차지한다.
  - passengership test 선박은 fold마다 5–13척이다.
  - 용도는 형식 확인과 빠른 디버깅으로 한정한다.

## 5 Class - Balanced (`5class_balanced/`) — 다운로드 중 (2026-10-05)

- 위치: `5class_balanced/stage/main5_balanced/` (93 GB). 압축 해제 확인 후 zip 삭제
- 오디오: 32 kHz, PCM_32, 5.0 s. 클래스 5개, 각 약 30,720 클립. 총 153,595 클립
- 누수 검사 (5 fold 모두):
  - MMSI 겹침 0
  - 배경 날짜 겹침 0
  - 누락 경로 0
  - 5 fold의 test 선박 1,734척이 모두 서로 다름
- fold당 train 약 2,540척, val 245–359척, test 274–389척. 합계 3,175척으로 논문 Table I과 일치
- test 클래스별 선박 수 (fold 1–5):
  - cargo 215–316
  - tug 27–42
  - tanker 20–25
  - **passengership 7–11**
- test 클래스별 클립 수가 fold마다 다르다(passengership 1,968–3,383). 클래스 균형은 train 전체 기준이다.
- 주의(`inferred`):
  - passengership은 test 선박이 약 10척이라, 이 클래스의 정확도는 선박 몇 척에 좌우된다.
  - DeepShip(2016-05 ~ 2018-10)과 기간·하이드로폰이 겹친다. 두 데이터셋을 섞어 쓰면 선박 중복을 확인해야 한다.
