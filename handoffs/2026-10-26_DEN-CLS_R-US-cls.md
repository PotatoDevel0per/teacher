# Handoff → DEN·CLS: R-US 잡음 제거기의 분류 효과 (A: UniqueShip → B: DeepShip)

- 작성: 2026-10-26 (Teacher). 사용자 결정(2026-10-26):
  - R-US 잡음 제거기의 성능(분류 효과)을 먼저 확인한다. 잡음 제거기를 파이프라인에 넣게 되면 E1-AE 등 뒤 단계의 입력이 바뀌기 때문이다.
  - **E1-AE는 일시정지한다**(22/30).
  - 순서는 A(UniqueShip) → B(DeepShip)다.
- 잡음 제거기: DEN `runs/rus/ckpt/stage2_best.pt`. UniqueShip 공식 fold1 train 선박 + train 배경으로 학습했다. test 혼합 SDRi 8.46 dB. **입력은 5 s 클립 단위 DC 제거가 전제다.**

## A. UniqueShip fold1 분류 (누출 없음)

- 누출 근거: 잡음 제거기는 fold1 train 선박(MMSI)과 train 배경만 보았다. 그래서 **fold1에서만** 누출이 없다. 다른 fold는 잡음 제거기를 다시 학습해야 하므로 이번에는 fold1만 한다.

### DEN

1. UniqueShip 5C-Bal 153,595 클립 전부(fold1의 train·val·test가 모든 클립을 덮는다)를 처리한다. 순서: 16 kHz soxr VHQ → 클립별 DC 제거 → `denoise()`(3 s 창 50% overlap-add, 5 s 클립 단위).
2. 출력: `outputs/uniqueship_denoised/<class>/<fname>.wav`(16 kHz float32, 5 s)와 manifest, README("fold1에서만 누출 없음"). 길이 일치, NaN·Inf 없음을 확인한다.
3. 실녹음 진단 요약(클래스별 지운 에너지, tonal, LTAS)은 R-US 평가와 같으므로 전체 기준으로만 다시 낸다.
4. GPU: GEN이 비운 GPU를 쓴다. 끝나면 경로를 보고한다.

### CLS

1. 레지스트리에 `uniqueship_den`을 추가한다. 클립 정의와 공식 fold1 분할은 원본과 같다. 원본 UniqueShip 경로는 int16 캐시를 쓰지 않는 core 방식이고, 이 결과물은 이미 16 kHz·DC 제거된 상태다. 이 차이를 편차로 기록한다.
2. MEL 캐시 생성 후 점검한다.
3. 학습은 E1-rep 단계 A(UniqueShip 회귀)와 같은 설정이다(SwinV2, lr 1e-6, best-val, patience 8, DDP 2장).
   - 원본: fold1 × seed 0, 1, 2. 기존 회귀 run(seed 1, regress_MEL_fold1_seed1)과 seed가 겹치면 재사용하고, 나머지만 새로 돌린다.
   - 잡음 제거: fold1 × seed 0, 1, 2
   - run당 약 70–80분이다.
4. 판정(사전 등록, `exp/R3_us/summarize.py` 먼저 커밋):
   - Δ_s = F1(잡음 제거, seed s) − F1(원본, seed s)
   - "도움": 평균 > +1.1 pp & seed 3개 모두 > 0
   - "해로움": 평균 < −1.1 & 모두 < 0
   - 그 외 "불명확"
   - fold 하나 결과라는 한계를 명시한다(R3-DS 교훈: fold 하나는 방향까지 틀릴 수 있다).
   - 보조: acc, 클래스별 F1(background 포함), 선박별 정답 증감(상위 1·2척 몫).

## B. DeepShip 적용 (A 다음, 먼저 CPU로 누출 확인)

### DEN (지금 CPU로)

1. 선박 중복 확인: UniqueShip `metadata_5s_*.csv`(fold_1, 선박명·MMSI)의 **fold1 train 선박**과 DeepShip `ship_id.csv`의 선박명을 대조한다. 정규화(대문자, 영숫자만)하고, 잘린 이름("QUEEN OF")은 접두 일치까지 본다. 출력은 겹치는 선박 목록, DeepShip 쪽 녹음·클립 수, DeepShip 5 fold의 test에 들어가는 몫이다.
2. 배경 날짜 확인: R-US train 배경 날짜와 DeepShip 녹음 날짜(녹음 ID의 YYYYMMDD)가 겹치는 수.
3. 결과를 보고한다. 겹침이 있으면 "겹치는 선박을 뺀 R-US 재학습"이 필요한지 Teacher가 정한다.
