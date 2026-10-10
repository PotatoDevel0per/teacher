# VAE-BL / LR-VAE (Huang et al., 2026, JASA 159(5):3773–3791)

- 원문: `papers/pdf/2026_huang_lrvae_fewshot.pdf` (20쪽, 1쪽은 AIP 표지. 2026-10-10 전체 읽음. Fig. 5–9의 수치는 PDF에서 추출한 그림 이미지로 읽음)
- DOI: 10.1121/10.0043727. JASA 특집호 "Generative and Physics-Informed Artificial Intelligence for Acoustics" 소속 (p.3773 각주 a)
- 기록 규칙: 아래 "확인한 내용"은 원문에서 직접 확인한 것(`confirmed`)이다. "해석"은 Claude의 추론(`inferred`)이다. 절 번호는 원문 표기(II.C.2 등)를 따른다.

## 연구 분류

- [x] 생성 증강 선행연구 (UATR + VAE)
- [x] 평가 프로토콜 일부 차용 후보 (증강 비율 ablation)
- [ ] 비교 기준 (누출 없는 baseline으로는 쓸 수 없음. 분할 단위가 녹음)

## 한 문장 요약

5 s 클립의 128×128 log-Mel을 skip connection이 있는 VAE(LR-VAE)로 재구성해서 소수 클래스를 2배로 늘리고, 원본+재구성 샘플을 frozen BEATs 임베딩 + LightGBM으로 분류해서 ShipsEar 95.56%, DeepShip 90.6%를 보고한 논문이다. 분할은 녹음(file) 단위다.

## 확인한 내용 (`confirmed`)

### 3단계 파이프라인 (§II.A, Fig. 1)
1. **ACcut** (전처리, §II.B): 16 kHz 리샘플(식 1) → 5 s window, 1 s hop(80% 겹침, 식 3) → 에너지 임계값 `η = E_avg − 2σ(E)`로 저에너지 구간 제거(식 5) → 구간별 최대 절댓값 정규화(식 6). 에너지 통계는 **train 데이터에서만** 추정하고 val/test에 고정 적용한다고 명시.
2. **LR-VAE** (생성, §II.C): 아래 참조.
3. **AIM** (분류, §II.D): frozen BEATs(ref 26, Chen 2022. 본문은 "BEATs-v2"라고도 부름) → 768차원 평균 pooling 임베딩(식 34) → LightGBM(learning rate 0.1, 식 35). "fivefold stratified cross-validation across the 12 vessel classes"로 학습한다고 씀(§II.D).

### LR-VAE 구조 (§II.C, Fig. 2)
- 입력: STFT(window 1024, hop 512, Hann, 식 7) → 128 Mel → log → **구간 단위 min–max 정규화**(식 11) → 시간축을 128 frame으로 맞춤(부족하면 zero padding, 넘치면 균등 sampling). 결과 128×128 ∈ [0,1].
- 인코더: 4단계 2D conv downsampling(Enc1–Enc4), 마지막 특징 256×8×8 → flatten 16384(식 12) → FC 두 개로 μ, log σ² → reparameterization(식 13).
- 디코더: z(본문 1024차원, 식 14) → 256×8×8 → transposed conv 4단계(8→16→32→64→128) → sigmoid(식 16). U-Net식 skip concat 4개(downsampling 배율 16/8/4/2, 식 15).
- 손실: `L = L_rec(MSE, 식 17) + 0.1·L_KL(식 18)` (식 19). validation loss로 early stopping.
- 파형 복원(§II.C.3): 저장한 (M_min, M_max)로 역정규화(식 20) → exp(식 21) → 역 Mel(식 22) → √ (식 23) → **Griffin–Lim 50–60회**(식 24–27).

### 생성 대상 공간과 생성 방식
- 생성 공간은 **정규화된 log-Mel (feature level)**이다. 저자가 직접 "LR-VAE-based data augmentation operates at the feature level rather than the waveform level"이라고 씀(§III.B).
- 생성 방식은 prior에서 sampling하는 것이 아니라 **기존 segment 각각을 인코딩·재구성**하는 것이다: "By applying the previously-noted reconstruction procedure to all spectrogram segments from each class, the resulting audio retains the general scale of the original data while introducing additional variability through latent-space perturbations" (§II.C.3 끝). 조건부 생성(클래스 조건)은 없다.
- 분류기 입력 경로: 재구성 Mel → Griffin–Lim 파형 → 다시 log-Mel 128×128 → BEATs (§II.C.3, §II.D.1.a).

### 생성물 품질 평가
- **정량 평가 지표가 없다.** FAD, LSD, 스펙트럼 거리, 청취 평가 모두 없다.
- 유일한 직접 증거는 Fig. 8의 원본/재구성 log-Mel 시각화다. 저자 스스로 "not intended to be perceptually realistic reconstructions", "the objective of LR-VAE is not to synthesize physically faithful waveforms or fine-grained harmonic structures"라고 쓴다(§III.C.4.d). 성능 향상은 "intra-class consistency and feature space regularization" 때문이라고 주장한다.

### 데이터와 분할 (§III.A, Table I–II)
- ShipsEar 12 클래스 전부(NaturalAmbientNoise 포함), DeepShip 4 클래스(Cargo, PassengerShip, Tanker, Tug).
- 분할 단위 원문: "The dataset is first partitioned at the original recording (file) level, such that all segments extracted from the same raw audio recording are assigned exclusively to either the training set or the test set" (ShipsEar). DeepShip도 "first split at the original recording level prior to segmentation". 최종 "80%/20% training and test split is applied at the recording level rather than at the segment level".
- **선박(ship/MMSI) 단위 분리는 원문 어디에도 없다.**
- 증강 대상: ShipsEar는 500 샘플 미만 클래스, DeepShip은 1000 미만인 Tug만 생성으로 2배. 그다음 클래스당 500(ShipsEar) / 1000(DeepShip) 샘플만 골라 400/100, 800/200으로 나눈다(Table I, II).
- few-shot 설정: episodic N-way K-shot이 아니다. test를 고정하고 클래스당 학습 샘플을 400→300/200/100/50(ShipsEar), 800→600/400/200/100(DeepShip)으로 줄인다(§III.B, Table VI).
- 생성 모델(LR-VAE) 학습 데이터의 범위: **명시 없음.** ACcut 통계는 train only라고 명시했지만, LR-VAE가 train split만으로 학습됐다는 문장은 없다. LR-VAE early stopping의 validation set이 어디서 왔는지도 쓰지 않았다.
- 코드·데이터: 비공개, 교신저자에게 요청 (Data Availability).

### 결과
| 설정 | ShipsEar Acc | DeepShip Acc | 출처 |
|---|---|---|---|
| ECAPA-TDNN | 90.2 | 86.3 | Table III |
| CAM++ | 92.3 | 88.6 | Table III |
| ResNet-SE | 88.3 | 84.5 | Table III |
| Transformer | 85.15 | 87.24 | Table III |
| VAE-BL | **95.56** | **90.6** | Table III |

few-shot (Table VI): ShipsEar 400→50/클래스에서 95.56 → 90.48, DeepShip 800→100에서 90.6 → 85.5.

### 증강만의 ablation (§III.C.4, Fig. 5–7, 9)
| 구성 | ShipsEar Acc / F1 | DeepShip Acc / F1 |
|---|---|---|
| VAE-BL-Full | 92.3 / 91.8 | 88.8 / 87.4 |
| w/o LR-VAE (생성 없음) | 87.5 / 86.2 | 83.9 / 82.5 |
| w/o BEATs-v2 (log-Mel 직접) | 86.2 / 84.8 | 82.6 / 81.1 |
| w/o AIM (FC 헤드) | 88.9 / 87.1 | 84.3 / 83.1 |
| Baseline ("w/o All") | 82.2 / 80.1 | 78.4 / 76.8 |
(Fig. 9 heatmap 수치. Fig. 5 막대와 일치)

- 생성 없음 → 있음: **ShipsEar +4.8 pp, DeepShip +4.9 pp** (본문 "approximately 4%–5%").
- 증강 비율(DeepShip, Fig. 7): 0% ≈ 82.7 → 100% ≈ 88.8 (본문 +6.12 pp, Macro-F1 +0.063, EER 18.42% → 11.92%). 150%, 200%에서 약간 하락. 학습 시간 1.2 h(0%) → 2.8 h(100%) → 4.9 h(200%).
- LR-VAE 구조(ShipsEar, Fig. 6): Full 92.35, w/o skip 89.72, latent 64 90.84, latent 256 91.93, β=0.1 91.27, β=1.0 90.45. 본문은 "standard 128-dimensional bottleneck", "β = 0.5 yields optimal"이라고 씀.
- **다른 생성 모델과의 비교 실험은 없다.** GAN(ref 21–23)은 서론에서 "training instability and pattern collapse"로 비판만 하고, SpecAugment는 §III.C.5에서 말로만 대비한다. plain VAE(skip 없음)는 "w/o Skip" 변형이 사실상 유일한 생성 모델 대조군이다.
- 반복 실행 횟수, seed, 표준편차는 보고하지 않는다.

### 원문 내부 불일치 (확인한 사실)
1. Full 성능: Table III 95.56 / 90.6 vs Fig. 5·9 92.3 / 88.8. 어느 설정 차이인지 설명이 없다.
2. latent 차원: §II.C(식 14) 1024 vs §III.C.4.b "standard 128-dimensional".
3. KL 가중치: 식 19는 0.1 vs ablation은 β=0.5가 최적이고 β=0.1은 Full보다 낮은 변형(Fig. 6).
4. 분류기 학습: §II.D "fivefold stratified cross-validation across the 12 vessel classes" vs §III.A 고정 80/20 split. DeepShip은 4 클래스다.
5. DeepShip 생성 없음 성능: Fig. 7 0% ≈ 82.7 vs Fig. 9 w/o LR-VAE 83.9.
6. 참고문헌: ECAPA-TDNN을 ref 30으로 인용하는데 ref 30은 QiandaoEar22 데이터셋 논문이다.

### 인용한 생성 증강 선행연구 (참고문헌 확인)
- ref 21 Liu et al. 2021, Appl. Acoust. 178, 107989 (3-D Mel + 증강, GAN 언급)
- ref 22 Jiang, Zhao, Wang 2022, Sensors 22(6), 2293 (modified DCGAN + S-ResNet)
- ref 23 Yao, Wang, Yang 2023, Electronics 12(5), 1206 (DCGAN + MFCC + ResNet18)
- **diffusion 기반 선행연구는 이 논문에 인용되지 않는다.** 참고문헌 32개 전부 확인. "Yu 2025"는 이 논문이 아니라 **Gao et al. 2026 (JASA 160(1):603–618, DOI 10.1121/10.0044413)**이 인용한 것이다. Gao 2026 원문 텍스트 추출본의 서지:
  - Yu, B., Du, S., Chen, Y., and Bian, Z. (2025). "Enhancing underwater acoustic target recognition with diffusion models and AST: A few-shot learning approach," in *5th International Conference on Neural Networks, Information and Communication Engineering (NNICE)*, IEEE, pp. 986–990. (Gao 2026 본문: "integrated diffusion models with audio spectrogram transformers ... generating high-quality Mel-spectrogram samples"). DOI는 아직 확인하지 않았다(`unknown`).

## 해석 (`inferred`)

### 분할과 누수
- 녹음 단위 분할은 UniqueShip 기준으로는 "누출 조건"에 가깝다. DeepShip은 한 선박이 여러 녹음을 가지므로 같은 선박이 train/test에 동시에 들어갈 수 있다. UniqueShip 논문에서 DeepShip은 파일 무작위 0.710 vs 선박 분리 0.588이었다(`papers/notes/2026_hashemi_uniqueship.md`). 이 논문의 DeepShip 90.6%는 선박 분리 조건과 비교할 수 없다.
- ShipsEar도 같은 선박(예: 반복 운항하는 여객선)이 여러 녹음에 나온다. 녹음 단위 분할로는 선박 누수를 막지 못한다.
- 생성 샘플이 test에 들어갔을 가능성: Table I은 "Before VAE / After VAE / Training 400 / Test 100" 순서다. Dredger(실제 332)처럼 실제 샘플이 500보다 적은 클래스에서도 500을 맞췄으므로, 증강된 pool에서 500을 뽑았을 수 있다. test 100이 실제 샘플만인지 원문으로 판정할 수 없다(`unknown`). 생성 샘플이 test 녹음의 segment를 재구성한 것이라면 test에 원본의 거의 복사본이 들어가는 셈이다.
- LR-VAE가 test 녹음의 segment로 학습되거나 test segment를 재구성했는지도 `unknown`이다. 이 논문의 증강 효과 수치를 인용할 때는 이 두 가지 불확실성을 같이 적어야 한다.

### 증강 효과의 해석
- "w/o LR-VAE"에서 학습 샘플 수가 통제됐는지 불명확하다. 소수 클래스는 실제 샘플이 400보다 적을 수 있으므로, +4.8 pp가 "생성의 효과"인지 "샘플 수·클래스 균형의 효과"인지 분리되지 않는다. 같은 수만큼 원본을 복제(oversampling)하는 대조군이 필요하다.
- 생성 방식이 per-sample 재구성이므로, 이 증강은 "새로운 선박"을 만드는 것이 아니라 "기존 segment의 smoothing된 사본"에 가깝다. 저자도 smoothing·blob 패턴을 인정한다(§III.C.4.d). UniqueShip 결과(선박 수 2배 +2.4–2.6 pp > 시간 2배 +0.8–1.3 pp)에 비추면, 선박 분리 조건에서는 효과가 줄어들 것이라는 가설을 세울 수 있다. **검증되지 않았다.**
- 구간 단위 min–max 정규화와 128 frame 균등 sampling은 절대 레벨 정보와 시간 해상도를 버린다. STFT 1024점/16 kHz는 bin 간격 15.6 Hz라서 저주파 tonal을 Mel 128 band로 분해하는 능력이 낮다. 저자도 미세 harmonic 구조 재현은 목표가 아니라고 쓴다. → **tonal 보존을 평가하는 사용자 연구의 관점에서는 이 생성물을 "음향학적으로 유사한 WAV"라고 볼 근거가 없다.**
- Griffin–Lim 파형은 128 frame(hop 512 기준 약 4.1 s 분량)으로 압축된 Mel에서 복원되므로 원래 5 s와 길이·시간축이 다를 것이다. 원문은 이 점을 다루지 않는다.
- Fig. 8의 "original" log-Mel은 축이 0–64 bin으로 표시되고 매끄러운 sinusoid 형태의 패턴이라, 실측 선박 소음의 tonal 선 구조로 보이지 않는다. 실제 데이터 그림인지 원문만으로 판단하기 어렵다.
- 성능 대부분은 BEATs 사전학습 임베딩에서 나올 가능성이 있다. w/o BEATs가 가장 큰 하락(−6.1 pp ShipsEar)이다. baseline들은 end-to-end로 처음부터 학습했으므로 Table III은 "생성 증강의 효과"가 아니라 "사전학습 임베더 + 증강 + LightGBM" 묶음의 효과다.

## 사용자 연구와의 관계 (`inferred`)

- **이식 가능성 (전체 데이터·선박 분리 조건)**:
  - 이 논문의 설정은 few-shot(클래스당 50–400), 녹음 분리, 소수 클래스만 2배 증강이다. 사용자 설정은 UniqueShip 5C-Bal(클래스당 42 h 40 m, 3,175척), MMSI 분리, SwinV2+Mel 67.3%다. 데이터 규모, 분할 단위, 분류기 모두 다르다.
  - 5C-Bal은 이미 클래스 균형이 맞으므로 "소수 클래스 2배"라는 이 논문의 증강 규칙이 그대로 적용되지 않는다. 이식하려면 "전 클래스 증강 비율 r ∈ {0, 25, 50, 100}%"로 바꿔야 하고, 이는 **논문의 아이디어를 기반으로 변형한 것**이다.
  - LR-VAE 자체는 단순해서 구현 비용이 낮다(conv VAE + skip + Griffin–Lim). 그러나 생성 공간이 정규화 log-Mel이고 tonal 보존을 보장하지 않으므로, "WAV 복원 가능한 생성" 목표에는 맞지 않는다.
- **LDM 생성 증강 계획과의 비교**:
  - 공통점: 둘 다 Mel/latent 공간에서 생성하고 vocoder/위상 복원으로 WAV를 얻는다.
  - 차이: LR-VAE는 per-sample 재구성(조건 없음, 새 샘플이 원본 근처에 묶임)이고, LDM은 prior에서 sampling하고 클래스·메타데이터 조건을 걸 수 있다. 선박 분리 일반화에는 "새 선박처럼 보이는 변이"가 필요하다는 가설과 LDM이 더 잘 맞는다(합리적인 가설이지만 직접 근거가 부족함).
  - 이 논문은 LDM 실험의 **약한 생성 baseline**으로 쓸 수 있다: (a) 생성 없음, (b) 원본 oversampling, (c) VAE 재구성(이 논문 방식), (d) LDM. (b)를 반드시 넣어야 이 논문이 분리하지 못한 "샘플 수 효과"를 분리할 수 있다.
- **차용할 것**: 증강 비율 sweep(Fig. 7)과 학습 시간 보고. "w/o skip" 같은 생성기 구조 ablation을 downstream 정확도로 평가하는 방식.
- **차용하지 않을 것**: 녹음 단위 분할, 생성물 품질 무평가, 단일 실행 보고.
- 이 논문은 "생성 증강이 선박 분리 조건에서 효과가 있다"는 근거가 **아니다**. 근거가 되는 것은 "녹음 분리 few-shot 조건, 사전학습 임베더 위에서 VAE 재구성 증강이 약 +5 pp"까지다.

## 이해 확인 질문 (사용자용)

1. 이 논문의 LR-VAE는 새 샘플을 어떻게 만드는가? prior N(0, I)에서 sampling하는 것과 무엇이 다르고, 그 차이가 "선박 다양성" 관점에서 왜 중요한가? (힌트: §II.C.3 마지막 문단)
2. "w/o LR-VAE"의 −4.8 pp를 "생성의 효과"라고 말하려면 어떤 대조군이 더 필요한가? 학습 샘플 수와 test 구성 관점에서 답하라. (힌트: Table I의 Dredger 332 → 500)
3. 이 논문의 DeepShip 90.6%를 UniqueShip의 DeepShip 선박 분리 0.588과 직접 비교할 수 없는 이유 두 가지는?

## 상태

- [x] 원문 확보
- [x] 원문 읽기 (전체, 그림 수치 포함)
- [ ] 교신저자에게 코드·분할 요청 여부 결정
- [ ] Yu 2025 (NNICE 2025) 원문 확보
- [ ] 최소 재현 (계획 시: 생성 없음 / oversampling / VAE 재구성 3조건, UniqueShip MMSI 분리)
