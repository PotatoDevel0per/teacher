# Handoff → DEN: FocuS-MN 재현 (R1 구현, R2 재현 확인)

- 작성: 2026-10-21 (Teacher). 받는 곳: `DEN` (`/jhlee/UWShipNoise/denoising/FocuS-MN`)
- 원문: `docs/2026_gu_focusmn_denoising.pdf` (Gu, Li, Tang, JMSE 14:621, 2026). Teacher 노트: `/jhlee/teacher/papers/notes/2026_gu_focusmn_denoising.md`
- 근거: 사용자 결정(2026-10-21). 가설 H-PRE-4: 분류기 앞단에 고정 잡음 제거를 붙이면 Ships-disjoint 일반화가 좋아지는가. 원문 가중치는 공개되지 않았다("요청 시 제공"). 그래서 재현한다.

## 1. 맥락

- 사용자 연구: 수중 선박 소음 인식(UATR), Ships-disjoint(선박 단위 분할) 일반화. 주 데이터 DeepShip·ShipsEar.
- 이 폴더에서 할 일: 모델을 만들고 원문 조건에서 재현되는지 확인한 뒤, **학습 없이 쓰는 고정 앞단 모듈**(추론 함수 + 체크포인트)을 내놓는다.
- 분류기 실험(R3 이후)은 thesis 저장소의 CLS 세션이 한다. 이 폴더에서는 분류기를 학습하지 않는다.

## 2. R1: 구현 (CPU)

원문 §3에서 확인한 구조를 그대로 따른다.

| 부분 | 원문 내용 |
|---|---|
| 입력 | STFT(Hann) → 크기 \|X\|에 거듭제곱 압축 \|X\|^p, 위상 ∠X. 두 개를 채널로 붙인다(식 4–7) |
| Encoder | Conv2D 3×3 stride 1 (2→32ch) + InstanceNorm + PReLU → Dilated DenseNet(시간·주파수 팽창 1, 2, 4, 8, 층마다 IN + PReLU) → Conv2D 3×3 (→32ch) + IN + PReLU. 주파수 축은 줄이지 않음(§3.2) |
| 리샘플링 | Algorithm 1: 채널별 학습 가중치 W ∈ R^{C×2}, softmax → 인접 2칸 가중 평균(½ 곱)으로 1/2. Algorithm 2: 각 칸을 2번 반복해 복원. 시간·주파수 각각에 작용, (T, F) → (T/2, F/2) → (T, F) (§3.3) |
| FSMN | affine 2층(shallow, deep) + ReLU → FSMN basic block N개. basic block = linear → 좌(과거, Lorder)·우(미래) depthwise 1D conv 메모리 → linear, 출력 = X + H_left + H_right (식 8–11, Fig. 3–4) |
| 전체 | M개의 [down → FSMN → up] 단계 + latent FSMN N개. **M = 6, N = 6** (Table 1 최선) |
| Decoder | Dense block → SP ConvTranspose2D + IN + PReLU → point-wise conv → 학습형 sigmoid 마스크 M = β·σ(S ⊙ X), 주파수별 S(식 12) |
| 출력 | 마스크 × 입력 크기 → (입력 위상과 함께) ISTFT |

원문에 수치가 없는 것은 아래 값으로 채우고 **모두 편차로 기록**한다. 근거는 원문이 참고한 MP-SENet(Lu et al. 2023) 관례다.

| 항목 | 채울 값(초안) | 비고 |
|---|---|---|
| n_fft / window / hop | 400 / 400 / 100 (16 kHz) | MP-SENet 관례. 다른 값을 쓰려면 근거를 적는다 |
| 압축 지수 p | 0.3 | MP-SENet |
| β | 2.0 | MP-SENet learnable sigmoid |
| Dense block 층 수 | 4 | MP-SENet |
| FSMN 은닉 차원, Lorder | 파라미터 수가 약 0.34 M이 되도록 정한다 | 원문 Table 3: 0.34 M |
| 리샘플링 축 순서 | 시간과 주파수를 단계마다 함께 1/2 | 원문 "(T/2, F/2)" 서술 |
| 출력 위상 | 입력(잡음 섞인) 위상 | 원문은 크기 마스크만 서술한다 |

- **파라미터 수 0.34 M(±10%)를 맞추는 것이 R1의 완료 조건이다.** 맞추지 못하면 차이와 이유를 보고한다.
- 단위 테스트: shape(3 s, 16 kHz 입력 → 같은 길이 출력), 리샘플링 down/up shape, 마스크 범위 [0, β], 결정적 재현.

## 3. R2: 원문 조건 재현 확인 (GPU 1장)

### 데이터 구성 (원문 §4.1)

- ShipsEar 원본 90 녹음(`CLAUDE.md`의 경로). 선박 녹음은 "깨끗한" 정답이고, 배경 녹음(클래스 E: 바람·해류·비 등)은 잡음이다.
- 16 kHz로 리샘플(soxr VHQ, thesis와 같은 방식), 3 s 구간으로 자른다.
- **−5 dB SNR**로 섞는다. SNR은 3 s 구간 전체 에너지 기준이다(편차로 기록). 잡음 구간은 무작위로 고르고 seed 0으로 고정한다.
- 분할: test = 선박 종류 **준설선, 예인선, 트롤선, 파일럿선**의 모든 구간. 나머지 7종류를 무작위로 train/val로 나눈다(원문). 전체 비율은 약 7:2:1이다. 종류 이름과 inventory의 `vtype` 대응표를 REPORT에 적는다.

### 학습 (원문 §4.2)

- 1단계: 크기 MSE(식 13). 2단계: SI-SNR(식 14–15). Adam, weight decay 0.01, lr 5e-5, cosine, batch 16, 최대 200 epoch, early stopping patience 20.
- 두 단계의 epoch 배분은 원문에 없다. 초안: 1단계를 val 손실이 20 epoch 개선되지 않을 때까지, 그다음 2단계. 편차로 기록한다.

### 판정 (사전 등록, `exp/r2_verdict.py`를 먼저 커밋)

- 지표: SDR, SDRi, SSNR(식 16–18, SSNR 프레임은 20 ms), test 전체 평균.
- **재현 통과: SDR이 3.77 ± 0.5 dB 안 그리고 SDRi ≥ 8.1 dB.** 기준값은 원문 Table 2이고, 허용폭 ±0.5 dB는 구현 휴리스틱이다.
- 미달이면 R3로 넘어가지 않는다. 원인 후보(빠진 설정)를 정리해 보고한다. 설정을 바꿔 다시 돌리려면 먼저 Teacher에게 묻는다(한 번에 하나씩).
- 보조: PSD 그림(원문 Fig. 9와 같은 구성), 원문 비교군 중 쉬운 것 하나(스펙트럼 차감 등) 대비 수치.

## 4. 산출물

- `src/`(모델, 데이터 혼합, 학습, 추론), `configs/`, `exp/`(R1 테스트, R2 결과, REPORT.md)
- **추론 함수:** `denoise(wav_16k: np.ndarray) -> np.ndarray`. 길이가 3 s보다 긴 입력은 3 s 창을 50% 겹쳐 처리하고 Hann 가중 overlap-add로 잇는다(규칙을 REPORT에 고정). CLS가 이 함수를 import해서 DeepShip·ShipsEar에 적용한다.
- 체크포인트 경로와 config를 REPORT에 적는다.
- 보고 시점: R1 완료(파라미터 수), R2 판정. 각각 커밋한 뒤 Teacher에게 메시지로 보고한다.

## 5. 이후 (참고, 이 세션이 직접 하지 않음)

- R3: CLS가 고정 모듈로 DeepShip 전체 → MEL 캐시 → 분류기 15 run → E1-rep MEL과 paired Δ. 원문 분할 모델은 ShipsEar test 선박을 보았으므로 판정은 DeepShip으로 한다.
- R5(선택): ShipsEar fold별 train 선박만으로 DEN이 다시 학습해 같은 비교를 한다.

---

## 6. 추가 지시 (2026-10-21, 사용자 결정): DeepShip에서도 잡음 제거가 되는지 확인

순서: R2(ShipsEar 재현) 통과 → R2b → (필요하면) R2c → (그래도 미달이면) R2d. **R2가 통과해야 R2b를 시작한다.**

### 공통 규칙

- **혼합 데이터:** DeepShip 선박 클립(4클래스: Cargo, Passenger, Tanker, Tug) + ShipsEar 배경 녹음(클래스 E)을 −5 dB로 섞는다(R2와 같은 규칙, 3 s, 16 kHz).
- **배경 녹음도 나눈다(누출 방지).** ShipsEar 배경 12 녹음을 녹음 단위로 train 8 / test 4로 고정한다(seed 0). test 혼합에는 test 배경만 쓴다. R2b의 test에도 같은 test 배경을 쓴다. 분할표를 REPORT에 적는다.
- **DeepShip 선박도 나눈다.** thesis의 Ships-disjoint fold1(`/jhlee/UWShipNoise/thesis/core/splits/deepship_shipcv_fold1.json`)을 쓴다. 잡음 제거 평가는 fold1 test 선박으로 하고, R2c 학습은 fold1 train·val 선박만 쓴다. 나중에 분류기 실험(R3)과 누출 없이 맞추기 위해서다.
- **한계(REPORT에 기록):** DeepShip 선박 녹음은 1.5–2 km 거리의 실해역 녹음이라 바다 소음이 이미 섞여 있다. 그래서 "깨끗한 정답" 자체가 깨끗하지 않다. SDR은 "더한 ShipsEar 배경을 얼마나 지웠는가"만 잰다.
- **실녹음 진단(정답 없음, 모든 단계):** 섞지 않은 원래 DeepShip fold1 test 클립(5 s)에 `denoise()`를 적용하고 다음을 잰다.
  - 지운 에너지 비율
  - tonal 수 변화: thesis `core/evaluate/tonal.py`를 import만 한다
  - LTAS 변화(dB)
  - "거의 항등 변환인지, broadband를 크게 지우는지"를 보는 용도다.

### R2b: ShipsEar로만 학습한 모델로 DeepShip 혼합을 추론

- R2 모델을 그대로 쓴다. 재학습하지 않는다. DeepShip fold1 test 선박 + test 배경 혼합에서 SDR, SDRi, SSNR을 잰다.
- **판정(사전 등록):** SDRi ≥ 6.9 dB(R2 원문 SDRi 8.61의 80%, 구현 휴리스틱)면 "DeepShip에서도 쓸 수 있다"로 보고 R2c를 건너뛸 수 있다. 미달이면 R2c로 간다.

### R2c: DeepShip + ShipsEar 배경으로 새로 학습

- 구조와 학습 설정은 R2와 같다. 데이터만 바꾼다. DeepShip fold1 train 선박 + train 배경으로 학습하고, val은 fold1 val 선박 + train 배경으로 한다.
- 같은 DeepShip test 혼합으로 판정한다. **SDRi ≥ 6.9 dB면 통과.** 미달이면 R2d를 할지 Teacher에게 묻는다.
- R3에서 이 모델을 쓰려면 fold 2–5도 같은 방식으로 학습해야 한다. 그것은 R2c 통과 후에 따로 지시한다.

### R2d: UniqueShip 대용량으로 큰 모델 학습 (마지막 수단, 착수 전 Teacher 승인 필요)

- UniqueShip 배경 녹음은 DeepShip과 **같은 ONC 하이드로폰 해역**이다. 그래서 잡음 분포가 DeepShip에 더 가깝다는 장점이 있다.
- **누출 위험:** UniqueShip(2016–2023)과 DeepShip(2016–2018)은 같은 해역·기간이 겹친다. 같은 선박이 두 데이터에 모두 있을 수 있다. 학습에 쓰기 전에 DeepShip test 선박 이름과 UniqueShip 선박명·MMSI를 대조해 겹치는 선박을 빼야 한다.
- "큰 모델"은 원문 구조를 바꾸는 것이다. 이때부터는 "논문 아이디어 기반 변형"으로 표기한다.
- 착수 조건과 설계는 R2c 결과를 본 뒤 Teacher가 따로 지시한다.
