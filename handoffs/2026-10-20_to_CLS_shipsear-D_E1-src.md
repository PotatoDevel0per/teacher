# Handoff → CLS: (1) E1-rep ShipsEar D안 (2) E1-src 지름길 성분 진단

- 작성: 2026-10-20 (Teacher). 받는 곳: `CLS` (`/jhlee/UWShipNoise/thesis`)
- 사용자 승인 (2026-10-20): ShipsEar 학습 설정 D안, E1-src 진행.
- 순서: DeepShip E1-rep 60 run 완료 → **(1) ShipsEar** → E1-rep 전체 판정 보고 → **(2) E1-src**.
- 공통 규칙은 이전 지시서와 같다. 판정 규칙은 실행 전에 코드로 커밋하고, test로 설정을 고르지 않는다.

---

## (1) E1-rep ShipsEar: D안

배경: lr 1e-6 × epoch당 23 step으로는 학습이 부족했다(train loss 0.95에서 정체). val이 252 클립이라 체크포인트를 val로 고르기도 불안정했다. 이전 pilot 3 run은 판정에서 뺀다.

### 1-a. lr pilot (train loss만 사용)

- MEL, fold1, seed 0. 후보 lr ∈ {1e-6, 1e-5, 3e-5}. 각각 100 epoch(약 2,300 step)을 고정하고, scheduler와 조기 종료는 끈다(상수 lr). 나머지 설정은 v2와 같다.
- **선택 규칙(사전 등록):** 마지막 20% step의 train loss 상대 변화(앞 5% 구간 평균 대비 뒤 5% 구간 평균)가 5% 미만이면 "수렴"이다. 수렴한 후보 중 **가장 작은 lr**을 고른다. 셋 다 수렴하지 않으면 3e-5로 200 epoch을 쓴다.
- val과 test는 이 선택에 쓰지 않는다. 기록만 하고 보고하지 않는다.

### 1-b. 본 실행

- 4 arm × fold 5 × seed 0,1,2 = 60 run. pilot에서 고른 lr을 상수로, 같은 epoch 수로 돌린다.
- **주 지표: 마지막 epoch 체크포인트의 test macro-F1.** best-val 값은 보조로 기록한다.
- 판정 규칙은 v2 §4와 같다(MEL 대비 fold paired Δ, 상위 2개는 두 데이터셋 평균 Δ). 데이터셋마다 프로토콜이 다르다는 점(DeepShip은 best-val + plateau, ShipsEar는 상수 lr + 마지막 epoch)을 REPORT 편차 절에 쓴다. paired Δ는 같은 데이터셋 안에서만 비교하므로 판정 틀은 유지된다.
- 끝나면 `summarize.py`로 E1-rep 전체 판정(상위 2개 도메인)을 보고한다.

---

## (2) E1-src: 선박 고유 단서가 broadband와 tonal 중 어디에 있는가

- 가설: H-SC-2(`research/hypotheses.md`). 누출 분할에서 학습한 선박 고유 단서가 주로 broadband에 있다(사용자 제기). 반대 가능성은 정확한 tonal 주파수가 선박 고유 단서라는 것이다.
- 데이터: **DeepShip만** 쓴다. 특징 도메인은 MEL(E1-rep 설정)이다.

### 2-a. 누출 분할 새로 만들기: 녹음 단위 무작위, 선박 공유 허용

- 같은 33,644 클립(unmatched 제외)을 쓴다. **녹음** 단위로 클래스 층화 5 fold(클립 수 기준 약 20%, 그리디, seed 0)를 만든다. val은 train 녹음의 15%(클립 기준)다.
- 같은 선박의 다른 녹음이 train과 test에 함께 들어가는 것을 **허용**한다. 같은 녹음은 갈라지지 않는다. 그래서 하락폭은 "선박 고유 단서" 의존도를 잰다. 녹음 안의 인접 클립 누출은 섞이지 않는다.
- 출력: `core/splits/deepship_recrand_fold{1..5}.json`. 검증: 녹음 공유 0, 각 클립이 test에 정확히 1회, fold별 train↔test 공유 선박 수(보고).

### 2-b. 입력 3종 (모두 같은 클립에서 만들고, 모두 위상 무작위화로 시간 구조를 같게 맞춘다)

| arm | 진폭 \|X\| | 위상 | 남는 것 |
|---|---|---|---|
| O_rp (기준) | 원본 \|X\| | 무작위 | tonal + broadband (시간 구조 제거) |
| B (broadband 전용) | median 평활 \|X\| (~20 Hz, `core/evaluate/surrogate.py`의 smooth_psd와 같은 평활) | 무작위 | broadband 모양만 |
| T (tonal 전용) | \|X\| ÷ median 평활 \|X\| | 무작위 | 평탄한 broadband 위의 tonal만 |

- 5 s 클립 전체 rfft 기준이다(G0와 같다). 만든 파형으로 E1-rep MEL 파이프라인을 그대로 거친다(dB, 90 dB 범위, 256 × 256).
- 세 arm 모두 위상을 무작위화하므로, B와 T의 차이는 **스펙트럼 모양**에서만 나온다. O_rp와 E1-rep MEL(원본)의 차이는 시간 구조(변조, 과도 성분)의 기여다(참고).
- 캐시 3종 × 약 4.4 GB. 만들기 전에 크기를 보고한다. GEN의 `surrogate.py`는 import만 하고 수정하지 않는다.

### 2-c. 실행

- arm 3 × 분할 2(recrand, shipcv) × fold 5 × seed 0 = 30 run. 학습 설정은 DeepShip E1-rep(v2)과 같다.
- 참고 run: 원본 MEL의 recrand 5 run(seed 0). shipcv 원본은 E1-rep MEL seed 0을 재사용한다.
- 합계 35 run, 약 8–9시간.

### 2-d. 판정 (사전 등록)

- 하락폭 drop_a = 평균 F1(recrand) − 평균 F1(shipcv), arm a마다 5 fold 평균으로 계산한다. 분할 종류가 달라 fold 짝은 없다.
- D = drop_B − drop_T. fold 단위 bootstrap(각 분할에서 fold 재표집, 2000회, seed 0)으로 95% CI를 구한다.
  - CI > 0: **H-SC-2 지지**(선박 고유 단서가 broadband 쪽에 더 많다)
  - CI < 0: **반대**(tonal 쪽에 더 많다)
  - CI가 0을 포함: 결론 보류
- 보조 보고: arm별 shipcv 절대 F1(선박 분리에서 남는 클래스 정보량), recrand fold별 공유 선박 수, 클래스별 F1.

### 산출물

- `exp/E1_src/`: config, 실행 스크립트, results, `summarize.py`(판정 규칙을 먼저 커밋), `REPORT.md`
- 단계(분할 검증, 캐시, 판정)마다 커밋하고 보고한다.
