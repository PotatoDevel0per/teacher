# Smoothness-inducing Regularization + LMR (Xu, Xie, Wang, 2023, arXiv:2306.06945v3)

- 원문: `papers/pdf/2023_xu_lmr_smoothness.pdf` (13쪽, 2026-10-10 본문·부록 전체 읽음)
- 게재: Ocean Engineering 2023 (PDF에는 "Preprint submitted to Elsevier"만 있음. 권·DOI는 PDF로 확인하지 못함)
- 코드: 원문 각주 2의 GitHub 저장소 (`xy980523/SmoothReg-LMR-DataPrune–underwater-acoustic-recognition`). **저장소 내용은 아직 확인하지 않음**
- 기록 규칙: 아래 "확인한 내용"은 원문에서 직접 확인한 것(`confirmed`)이다. "해석"은 Claude의 추론(`inferred`)이다.

## 연구 분류

- [x] 비교 기준 (범용 증강 baseline 후보: LMR)
- [x] 학습 방식 비교군 (증강 샘플을 정규화 항으로만 쓰는 방식)
- [ ] 평가 방법 (분할이 선박 단위가 아니므로 평가 프로토콜로는 쓰지 않음)

## 한 문장 요약

spectrogram 패치를 다른 샘플의 같은 위치 패치로 바꾸는 증강(LMR)과, 잡음 샘플을 CE에 넣지 않고 clean/noisy 예측의 대칭 KL로만 쓰는 정규화(smooth reg)를 제안하고, ShipsEar·DeepShip·DTIL에서 noise aug·GAN aug·mixup보다 낫다고 보고한 논문이다.

## 확인한 내용 (`confirmed`)

### 데이터 (§3.1, Table 1, 2)
- ShipsEar: 11 클래스 중 9 클래스 사용(dredger, fish boat, motorboat, mussel boat, natural noise, ocean liner, passenger ship, ro-ro ship, sailboat). 2.94 h, SR 52,734 Hz.
- DeepShip: 4 클래스(cargo, passenger ship, tanker, tug), 265척, 47.07 h, SR 32,000 Hz.
- DTIL: 비공개(천도호, speedboat 330 min + experimental vessel 285 min), SR 17,067 Hz.
- 30 s segment, 15 s overlap. segment 수(train/val/test): ShipsEar 400/71/116, DTIL 1655/292/354, DeepShip 6742/1190/2547.

### 데이터 분할 (§3.2, 부록 B, Table 8, 9)
- 원문: *"we make sure that segments in the training set and the test set must not belong to the same audio track."*
- 즉 **녹음 파일(audio track) 단위** 분리다. 클립(segment) 단위 무작위 분할은 아니다. **선박 단위 분리라는 언급은 없다.**
- train/test 파일 ID를 공개했다. ShipsEar는 Table 8(클래스별 train/test WAV ID), DeepShip은 Table 9(test ID만 나열, 나머지 "Else"는 train).
- validation: *"we randomly take 15% of the data in the training set as the validation set."* 무엇을 단위로 15%를 뽑는지(파일인지 segment인지)는 적혀 있지 않다.
- 평가는 segment(30 s) 단위 정확도. 파일 단위 정확도는 test 파일 수가 적어 값이 겹치므로 보고하지 않았다고 밝힌다 (§4).

### 특징과 전처리 (§2.1, §3.3, §3.4, 부록 A, C)
- 특징 4종: STFT, Mel, Bark, CQT spectrogram. frame 50 ms / shift 25 ms (부록 C, Table 10에서 선택). Mel·Bark filter 300개, CQT octave 해상도 30.
- "effective frequency band": ShipsEar 100–26,367 Hz, DTIL 100–2,000 Hz, DeepShip 100–8,000 Hz (Table 2). STFT·baseline으로 band를 비교해 고른 것이다 (부록 A, Table 7). 목적 중 하나는 LMR이 복사하는 영역에 유효 정보가 들어가게 하는 것이다 (§3.3).
- 입력 크기 예: DeepShip Mel 1199×300, STFT 1199×400 (Table 2).
- §2.1에 beamforming이 전처리로 적혀 있지만, 공개 데이터셋에 실제로 무엇을 했는지는 기술되지 않는다.

### 모델과 학습 설정 (§2.2, §3.4, 부록 D)
- ResNet-18 + multi-head attention pooling ("QKV" 방식). 11.8 M 파라미터 (Table 11). 사전학습 언급 없음.
- AdamW, lr 5e-4, batch 64, weight decay 1e-5, 100 epoch, A40 1장. 모든 실험 동일.
- **seed 수, 반복 횟수, 표준편차는 어디에도 보고되지 않는다.** 모든 표가 단일 수치다.
- validation set을 어디에 썼는지(early stopping, checkpoint 선택, α 선택)는 적혀 있지 않다.

### LMR 알고리즘 (§2.4, Fig. 4, Eq. 5)
1. batch 안에서 클래스와 무관하게 spectrogram 두 개 x_i, x_j를 무작위로 고른다.
2. x_i에서 a×b 패치를 지우고, x_j의 **같은 크기·같은 위치** 패치를 그 자리에 복사한다. 결과는 x̃_ij.
3. a ∈ (0, W), b ∈ (0, H)는 샘플마다 무작위로 바뀐다. 분포(균등 여부)는 적혀 있지 않다.
4. 혼합 비율 λ = 1 − ab/(HW). 손실 L_LMR = λ·CE(ŷ_ij, y_i) + (1−λ)·CE(ŷ_ij, y_j).
5. **batch마다 50% 확률로 LMR을 켠다.** 나머지 50%는 원본 batch를 그대로 쓴다.
6. 적용 domain: effective band로 자른 2D spectrogram(특징 domain). 학습 중에만 쓴다. WAV로 되돌리지 않는다.
7. 훈련 샘플 수를 늘리지 않는다 (batch 내 on-the-fly 교체). 학습 시간 27.6 → 28.0 min (Table 11).
- 마스킹 "비율"은 고정값이 아니라 a·b가 무작위라서 매번 달라진다. 패치 위치 분포와 패치 개수(본문은 "patches" 복수형, 수식은 a×b 하나)는 명시되지 않는다.

### Smoothness-inducing regularization (§2.3, Eq. 3–4, §4.1)
- clean 특징 x_i와 잡음 특징 x̃_i를 동시에 넣어 logit z_i, z̃_i를 얻는다.
- L = CE(z_i, y_i) + α·[KL(p_i‖p̃_i) + KL(p̃_i‖p_i)]. **잡음 샘플은 CE에 들어가지 않는다.** 대칭 KL로 두 예측을 가깝게 만들 뿐이다. SMART(Jiang et al., 2019)에서 영감을 받았다고 밝힌다.
- 잡음 샘플은 "noise aug"와 같은 설정으로 만든다: Gaussian white noise, SNR 5–30 dB. Fig. 1상 잡음은 신호(WAV) 단계에서 더한 뒤 특징을 뽑는다.
- 공정 비교를 위해 noise aug, GAN aug, smooth reg는 모두 원본과 같은 수의 잡음 샘플을 만든다 (훈련 샘플 2배).
- 두 기법을 함께 쓸 때 L = L_LMR + α·Reg (Eq. 6). LMR이 켜진 batch에서 Reg 항의 z_i가 혼합 샘플인지 원본인지는 명확하지 않다.
- α ∈ {0, 0.5, 1, 2}를 비교 (Table 5). 저자 권고는 "0.5, 1, 2 중에서 데이터·특징마다 실험으로 고른다" (§4.4).

### 비교한 증강과 결과 (Table 3, ResNet-18+MHA, segment 정확도 %)

| 특징 | 방법 | ShipsEar | DTIL | DeepShip |
|---|---|---|---|---|
| STFT | baseline | 75.24 | 95.93 | 74.68 |
| | + noise aug | 78.45 | 96.05 | 75.07 |
| | + GAN aug | 76.05 | 96.14 | 75.98 |
| | + smooth reg | 81.90 | 97.74 | 76.38 |
| | + LMR | 82.76 | 96.61 | 78.40 |
| | + smooth reg + LMR | 82.97 | 97.80 | 78.56 |
| Mel | baseline | 77.14 | 95.48 | 74.85 |
| | + noise aug | 78.72 | 95.58 | 75.27 |
| | + GAN aug | 79.68 | 95.45 | 75.79 |
| | + smooth reg | 82.76 | 95.76 | 77.05 |
| | + LMR | 82.76 | 96.33 | 75.38 |
| | + smooth reg + LMR | 83.45 | 96.50 | 77.12 |
| Bark | baseline | 72.86 | 96.30 | 75.15 |
| | + noise aug | 75.86 | 96.33 | **74.18** |
| | + GAN aug | 74.59 | 96.65 | **75.08** |
| | + LMR | 79.31 | 96.61 | 77.46 |
| | + smooth reg + LMR | 79.25 | 96.93 | 77.80 |
| CQT | baseline | 73.33 | 96.48 | 77.82 |
| | + GAN aug | 74.43 | 96.89 | **77.12** |
| | + LMR | 81.03 | 97.18 | 78.97 |
| | + smooth reg + LMR | 82.76 | 97.56 | 80.05 |

(Bark·CQT의 noise aug·smooth reg 줄은 일부 생략. 굵은 값은 baseline보다 낮음.)

- LMR 단독 이득: ShipsEar +5.62(Mel) ~ +7.70(CQT) pp, DeepShip +0.53(Mel) ~ +3.72(STFT) pp, DTIL +0.31 ~ +0.85 pp.
- noise aug는 Bark/DeepShip에서 −0.97 pp, GAN aug는 Bark/DeepShip −0.07, CQT/DeepShip −0.70 pp. 저자는 이것을 "시뮬레이션 샘플이 실제와 어긋나면 성능이 떨어질 수 있다"의 근거로 쓴다.
- GAN은 "vanilla GAN"이라는 말 외에 구조·입력·학습 정보가 없다.

### 분리 가능성 ablation
- Table 3 하단이 사실상 2×2 ablation이다 (없음 / smooth reg / LMR / 둘 다). 두 효과를 따로 볼 수 있다.
- Table 4, 5는 "LMR을 쓰지 않고", Table 6은 "정규화를 쓰지 않고" 측정했다고 명시한다.
- 조합이 항상 더 좋지는 않다: Bark/ShipsEar에서 둘 다 79.25 < LMR 단독 79.31.

### LMR vs mixup (Table 6, 정규화 없음)

| 특징 | baseline | mixup | LMR (ShipsEar / DTIL / DeepShip) |
|---|---|---|---|
| STFT | 75.24 / 95.93 / 74.68 | 79.31 / 95.76 / 74.83 | 82.76 / 96.61 / 78.40 |
| Mel | 77.14 / 95.48 / 74.85 | 76.72 / 96.05 / 75.42 | 82.76 / 96.33 / 75.38 |
| Bark | 72.86 / 96.30 / 75.15 | 75.86 / 96.51 / 73.77 | 79.31 / 96.61 / 77.46 |
| CQT | 73.33 / 96.48 / 77.82 | 79.31 / 97.18 / 78.48 | 81.03 / 97.18 / 78.97 |

- 저자 주장: LMR이 네 특징 모두에서 mixup보다 이득이 크다. **그러나 Mel/DeepShip에서는 mixup 75.42 > LMR 75.38이다.** 이 칸은 주장과 맞지 않는다(차이는 0.04 pp).
- 저자는 mixup이 선 스펙트럼(tonal)과 주기 변조 줄무늬를 선형으로 겹쳐 "aliasing·왜곡"을 만든다고 설명한다 (§4.5). **이 설명을 직접 검증한 실험은 없다.**
- CutMix는 영감으로 인용했지만 비교하지 않았다.

### 잡음 강건성 (Table 4, Mel, LMR 없음)
- test에 Gaussian 잡음을 더했을 때, SNR −15~10 dB에서 noise aug는 78.72 → 71.69(DeepShip 75.27 → 68.67), smooth reg는 82.76 → 79.69(DeepShip 77.05 → 73.03).

### 저자가 밝힌 한계 (§5)
- smooth reg는 데이터가 많은 DeepShip에서 이득이 제한적이다. 과적합을 줄일 뿐 성능 상한을 올리지는 못한다고 본다.
- LMR은 detection 같은 다른 작업에서는 해가 될 수 있다.

## 해석 (`inferred`)

### 분할과 누출
- 파일 단위 분리는 segment 무작위 분할보다는 낫지만 **선박 단위 분리는 아니다.** ShipsEar는 같은 선박(예: 항구를 오가는 같은 여객선)을 여러 번 녹음한 파일이 있고, DeepShip도 265척에 비해 녹음 파일 수가 훨씬 많아서 한 선박에 여러 녹음이 있다. 따라서 같은 선박이 train과 test에 함께 있을 가능성이 높다. Table 8·9의 ID로 실제 중복을 확인하지는 않았다.
- UniqueShip 논문의 결과(누출 분할에서 DeepShip 정확도가 크게 부풀려짐)를 적용하면, 이 논문의 절대 정확도와 **증강 이득의 크기 모두** 선박 단위 분할에서 유지된다는 보장이 없다. 특히 LMR·mixup처럼 "같은 선박의 다른 녹음 패턴을 섞는" 증강은 선박 기억을 도울 수도 있다. 이것은 가설이다.
- validation 15%가 segment 단위 무작위라면 15 s overlap 때문에 train과 겹치는 segment가 validation에 들어간다. 이 경우 validation은 model selection에 거의 정보를 주지 않는다.

### 수치 신뢰도
- **Table 3의 smooth reg 12칸은 모두 Table 5에서 α별 값 중 최댓값과 일치한다** (예: STFT는 ShipsEar α=0.5, DTIL·DeepShip α=2; Mel은 ShipsEar α=2, DTIL·DeepShip α=0.5). Table 5가 test 정확도라면 α를 test로 고른 것이다. smooth reg 수치는 낙관적으로 보아야 한다. LMR에는 조정 가능한 하이퍼파라미터가 거의 없어서 이 문제가 상대적으로 작다.
- ShipsEar test는 116 segment이고, overlap 때문에 실제 독립 정보는 더 적다. 1 segment = 0.86 pp다. 82.76% = 96/116이 여러 칸에 반복된다. seed 분산이 없으므로 ShipsEar의 1–3 pp 차이는 잡음과 구분할 수 없다.
- DeepShip test 2,547 segment에서 LMR 이득 +0.53(Mel) ~ +3.72(STFT) pp. 단일 seed라서 Mel의 +0.53은 유의하다고 보기 어렵다. 사용자의 주 조건(Mel)에서 이득이 가장 작다는 점에 주의해야 한다.

### 방법의 성격
- LMR은 실질적으로 **CutMix를 spectrogram에 적용하고 batch 단위 50% 확률을 더한 것**에 가깝다. 차이는 (1) a, b를 직접 무작위로 뽑음(CutMix는 Beta 분포 λ에서 상자 크기를 정함), (2) effective band로 자른 입력에 적용, (3) batch 50% 적용이다. 저자는 CutMix와 비교하지 않았다. 따라서 "LMR 고유의 효과"와 "CutMix류 패치 혼합 일반의 효과"는 구분되지 않는다.
- LMR은 물리적으로 의미 있는 샘플을 만들지 않는다. 패치 경계에서 tonal 선이 끊기고, 두 선박의 broadband 배경 레벨이 다르면 경계에서 계단이 생긴다. WAV 복원 가능성도 고려하지 않는다. 사용자 연구에서는 "물리적 타당성 없는 범용 정규화형 증강" baseline 역할로 적합하다.
- smooth reg는 사용자 연구에서 별도로 쓸모가 있다. 물리 증강 샘플이 실제 분포에서 벗어날 위험이 있을 때, 그 샘플을 CE 대신 일관성 항(대칭 KL)에만 쓰는 방식은 "물리 증강 + CE"와 비교할 만한 대안이다. 이것도 논문이 검증한 것은 아니다. 논문의 잡음은 Gaussian white noise뿐이다.

## 사용자 연구와의 관계 (`inferred`)

### UniqueShip에서 LMR을 범용 증강 baseline으로 재현할 때 필요한 세부사항
- 원문에서 가져올 수 있는 것: 쌍 선택(batch 내, 클래스 무관), 같은 위치 패치 복사, λ = 1 − ab/(HW), 혼합 CE 손실, batch 50% 적용, 샘플 수 증가 없음.
- 사용자 설정과 다른 점: 입력이 5 s(UniqueShip) vs 30 s, SR 20 kHz vs 32 kHz, SwinV2 ImageNet 사전학습 + lr 1e-6 vs ResNet-18 scratch + lr 5e-4, Mel 해상도·dB 범위가 다르다. 5 s Mel에서 LMR 패치는 시간 방향으로 훨씬 짧아진다.
- effective band: 논문은 DeepShip에 100–8,000 Hz를 썼다. UniqueShip(20 kHz → 최대 10 kHz)에서는 band를 바꾸지 않고 baseline 전처리 그대로 LMR만 추가하는 것이 "한 번에 하나의 변경" 원칙에 맞다.
- 정확한 표현: UniqueShip에서 쓰면 "논문의 LMR 모듈을 재현함(다른 backbone·데이터에 적용)"이다. "논문 방법을 그대로 재현했다"고 쓰면 안 된다.

### 원문에서 빠진 정보 (코드 저장소에서 확인 필요)
1. a, b의 분포(균등 여부, 최소·최대 크기 제한)와 패치 위치 분포.
2. 패치 개수(1개인지 여러 개인지).
3. 짝을 고르는 방식(batch를 shuffle한 순열인지, 독립 추출인지).
4. LMR 적용 시점(정규화 전/후, dB 변환 전/후).
5. validation 분할 단위와 사용 목적(checkpoint 선택 여부).
6. seed 수와 분산. 재현 시에는 UniqueShip 5 fold로 평균 ± 표준편차를 직접 내야 한다.
7. smooth reg와 LMR을 함께 쓸 때 KL 항의 입력.
8. GAN aug 구조와 학습 정보 (GAN을 비교군으로 재현하는 것은 정보 부족으로 어렵다).

### 지금 할 일 / 하지 않아도 되는 일
- 할 일: 코드 저장소에서 위 1–5 확인 → SwinV2+Mel baseline(67.3%)에 LMR만 추가해 5 fold 비교.
- 하지 않아도 되는 일: GAN aug 재현, 4종 특징 비교, smooth reg α 탐색. 범용 증강 baseline에는 LMR(그리고 필요하면 SpecAugment·mixup) 정도면 충분하다.

## 이해 확인 질문 (사용자용)

1. 이 논문의 분할은 어떤 단위인가? 같은 단위로 UniqueShip을 분할하면 어떤 종류의 누출이 남는가?
2. LMR 손실에서 λ는 무엇으로 정해지며, mixup의 λ와 무엇이 다른가? 같은 위치 패치를 복사한다는 조건은 tonal 성분에 어떤 영향을 주는가?
3. smooth reg가 noise aug와 같은 잡음 샘플을 쓰는데도 Bark/DeepShip에서 성능이 떨어지지 않은 이유를 손실 함수 관점에서 설명하라. 그리고 Table 3의 smooth reg 수치를 그대로 믿기 어려운 이유는 무엇인가?

## 상태

- [x] 원문 확보
- [x] 원문 읽기
- [ ] 공식 코드 확인 (LMR 세부: a·b 분포, 패치 위치·개수, 짝 선택)
- [ ] ShipsEar·DeepShip 분할(Table 8, 9)의 선박 중복 확인 (선택)
- [ ] UniqueShip에서 LMR 최소 재현
