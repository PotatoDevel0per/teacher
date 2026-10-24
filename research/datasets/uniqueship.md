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
  - 배경 날짜 겹침 0 (**2026-10-23 정정: 파일명 UTC 날짜 기준으로 fold1에서 train–val 1일, train–test 2일이 겹친다. 겹친 날도 train과 최소 1 h 10 m 떨어져 있다. 현지 날짜 기준이면 21·25일이 겹친다. 공식 분할의 배경 단위는 날짜가 아닌 다른 기준(녹음 구간 등)으로 보인다. DEN R-US 분할 검증**)
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

## DeepShip과의 분포 차이 (2026-10-23, Teacher 빠른 측정, inferred)

- 녹음 환경(원문 기준, confirmed): 둘 다 ONC Strait of Georgia 하이드로폰. UniqueShip은 device 2523·2556, 2016-05 ~ 2023-11. DeepShip은 2016-05 ~ 2018-10로 기간이 겹친다. UniqueShip은 2 km 안 단일 선박(4 km 안 다른 선박 없음) 조건으로 골랐다.
- 측정: E1-rep MEL 캐시(16 kHz, 클립별 90 dB 정규화)에서 클래스당 400 클립의 시간 평균 프로파일(256칸)을 비교했다.
  - 같은 클래스의 데이터셋 간 평균 프로파일 차이(RMS): Cargo 2.7, Passenger 3.5, Tanker 1.6, Tug 1.3 dB
  - 같은 데이터셋 안의 클래스 간 차이 평균: UniqueShip 3.3, DeepShip 3.9 dB
  - 클립 간 흩어짐(같은 클래스): 7.0–8.2 dB
  - 프로파일만으로 데이터셋을 구별하는 로지스틱 회귀(5-fold CV): acc 0.655(우연 0.5)
- 해석: 데이터셋 간 차이는 클래스 간 차이와 비슷하거나 작고, 클립 간 흩어짐보다 훨씬 작다. Passenger가 가장 다르다(DeepShip Passenger는 BC 페리 "QUEEN OF" 계열이 많다). 절대 레벨은 정규화로 지워졌으므로 비교하지 않았다. 표본이 작고 한 가지 표현(MEL)만 봤다.

## 5C-Bal 클래스별 분포 (2026-10-23, Teacher 직접 집계, confirmed)

| 클래스 | 클립 | 시간 | 선박(MMSI) | 녹음 날짜 수 | 선박당 클립(중앙값 / 최대) | 상위 10척 몫 |
|---|---|---|---|---|---|---|
| cargo | 30,720 | 42.7 h | 2,526 | 1,370 | 12 / 13 | 0.4% |
| passengership | 30,719 | 42.7 h | 112 | 911 | 156 / 1,320 | 39.3% |
| tanker | 30,720 | 42.7 h | 233 | 414 | 84 / 2,880 | 29.1% |
| tug | 30,719 | 42.7 h | 304 | 1,426 | 108 / 108 | 3.5% |
| background | 30,717 | 42.7 h | – | 808 | – | – |

- 시간은 클래스마다 같게 맞췄지만 선박 다양성은 크게 다르다. cargo는 배마다 약 1분(12 클립)으로 잘라 2,526척, passengership은 112척이고 상위 10척이 39%다.
- test fold의 선박 수(fold 1–5): cargo 286 / 272 / 308 / 316 / 215, passengership 10 / 7 / 10 / 9 / 11, tanker 20 / 22 / 25 / 22 / 21, tug 36 / 37 / 38 / 42 / 27, background(날짜) 85 / 84 / 80 / 80 / 81.
- 12 Class - 5h: 12 클래스(tug, tanker, cargo, pilotvessel, sailing, fishing, dredger, other, passengership, rescue, pleasurecraft, background) 각 약 3,600 클립. 오디오는 2026-10-14 정리 때 삭제했고 메타데이터만 남았다.

## DC 성분 (2026-10-23, DEN 측정, confirmed)

- 5C-Bal 원본 클립은 대부분 DC가 지배한다. 3 s 구간의 |평균|/RMS 중앙값: 선박 0.963, 배경 0.996.
- 그대로 쓰면 −5 dB 혼합 같은 SNR 정의가 DC 크기의 비율이 된다. 파형을 직접 쓰는 실험(잡음 제거, 파형 증강)은 클립별 DC 제거가 필요하다. UniqueShip 원문 전처리와 thesis 특징 경로(EXP-001)도 DC를 뺀다.
- DC 제거 후(클립별 평균 빼기): |평균|/RMS 중앙값 선박 0.036, 배경 0.082. 클립 안에 느린 드리프트가 있다(1 s 창 평균의 범위가 RMS의 0.49배(선박), 0.89배(배경)). 그래서 배경 에너지의 34%가 0–20 Hz에 남는다. 0–20 Hz를 쓰는 분석은 고역 통과를 고려해야 한다.
