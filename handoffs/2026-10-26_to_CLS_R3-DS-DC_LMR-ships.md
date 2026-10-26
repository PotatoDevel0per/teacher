# Handoff → CLS: R3-DS-DC 분류, LMR Ships-disjoint (2026-10-26)

- 작성: Teacher.
- 우선순위: R3-US(진행 중) → **1. R3-DS-DC** → **2. LMR-ships**(자원이 빌 때)
- 사용자 결정(2026-10-26): R3-DS를 DC 제거 입력으로 다시 한다. LMR 선박 분할은 자원이 빌 때 돌린다.

## 1. R3-DS-DC: ShipsEar 모델 잡음 제거(DC 제거 입력) → DeepShip 분류 5 fold

- **배경:** DeepShip 클립 에너지의 98%가 DC다. R3-DS에서는 DC를 빼지 않고 잡음 제거기에 넣었다.
  - DC를 빼면 ShipsEar 모델의 DeepShip 혼합 SDRi는 7.07 dB다(기준 6.9 통과, DEN 89f4c15).
  - 그래서 R3-DS의 "해로움"(−4.83)은 DC가 섞인 조건에 한정된 결과다.
- **입력:** DEN `outputs/deepship_denoised_dc/`. DEN이 완료를 알리면 시작한다.
- **설정:** R3-DS와 같다. `deepship_den_dc` 데이터셋을 등록하고, MEL, E1-rep DeepShip v2 설정, 5 fold × seed 0–2 = 15 run.
- **비교:** E1-rep DeepShip MEL(58.18)과 paired Δ macro-F1. R3-DS(DC 미제거) 결과도 함께 표에 넣는다.
- **판정(사전 등록, summarize를 먼저 커밋):** R3-DS와 같은 규칙이다.
  - 평균 Δ > 0이고 4/5 fold 양수: 도움
  - 평균 Δ < 0이고 4/5 fold 음수: 해로움
  - 그 외: 판단 불가
- 보조로 낼 것: acc, 클래스별 F1, 선박별 정답 증감(상위 2척이 차지하는 몫).
- 중간 보고: fold별 결과가 나올 때 숫자만 보고한다. fold 하나로 방향을 단정하지 않는다(R3-DS 교훈).

## 2. LMR-ships: LMR 증강 이득이 선박 분할에서도 유지되는가 (EXP-002-PC 확장)

- **목적:** 세미나 2부 "분할 방식에 따른 증강 이득 차이"에 쓴다. EXP-002-PC는 원문의 녹음 단위 분할에서만 쟀다(Δ +2.34).
- **바꾸는 변수는 하나다: train·val과 test 사이의 선박 공유.**
  - test 녹음은 EXP-002-PC(원문 Table 9)와 같게 둔다.
  - train·val에서 test 선박과 같은 선박의 녹음을 뺀다.
  - 선박 판정은 `/jhlee/UWShipNoise/data/deepship/ship_id.csv`의 선박명을 쓰고, thesis core/splits와 같은 정규화 규칙을 적용한다. "QUEEN OF" 같은 잘린 이름은 병합한다.
- **혼입 요인:** 학습 녹음 수가 줄어든다. 뺀 녹음 수와 segment 수를 보고한다.
- **코드:** `/jhlee/UWShipNoise/recognition/UATR_SLM/deepship_lmr_pc/`(train.py, lmr.py, model.py)를 thesis `exp/E2_lmr_ships/`로 복사한다.
  - 원본 폴더는 수정하지 않는다.
  - 설정은 EXP-002-PC 판정 run과 같다: best-val 기준, val-mode recording, feature log1p.
  - EXP-002-PC의 B0·B1 run 6개는 그대로 비교 기준으로 쓴다. 다시 돌리지 않는다.
- **run:** B0·B1 × seed 0–2 = 6 run. run당 약 57분이다. GPU가 빌 때 돌린다.
- **판정(사전 등록):**
  - 주 지표: Δ_s = acc(B1) − acc(B0), test segment 정확도, best-val 기준. EXP-002-PC와 같다.
  - "유지": Δ > 0이 3/3 seed이고 평균 ≥ 2 pp
  - "사라짐": 평균 ≤ 0 또는 양수가 1/3 이하
  - 그 외: "약해짐"
  - 보조: last epoch 기준 Δ도 보고한다(EXP-002-PC에서는 −7.1로 뒤집혔다).
- **사전 점검(학습 전):** test 선박이 train·val에 0척인지 확인한다. 녹음 단위 분할에서 test 선박과 겹쳤던 train 녹음 수도 낸다. 이것이 원래 분할의 누출 규모다.
