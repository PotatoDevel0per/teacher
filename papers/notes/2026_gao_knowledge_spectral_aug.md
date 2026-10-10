# SDA_CFM: Knowledge-inspired spectral augmentation for few-shot UATR (Gao et al., 2026, JASA 160(1):603–618)

- 원문: `papers/pdf/2026_gao_knowledge_spectral_aug.pdf` (17쪽, 2026-10-10 전체 읽음)
- 기록 규칙: 아래 "확인한 내용"은 원문에서 직접 확인한 것(`confirmed`)이다. "해석"은 Claude의 추론(`inferred`)이다.

## 연구 분류

- [ ] 반드시 읽어야 하는 논문
- [x] 비교 기준 (범용 스펙트로그램 증강과의 비교 프로토콜 사례)
- [ ] 평가 방법 (few-shot 프로토콜이라 사용자 설정과 다름)
- [x] "물리 기반 증강"이라는 이름에 주의해야 하는 사례

## 한 문장 요약

스펙트로그램 이미지에 2D FFT를 적용해 중앙 저공간주파수만 남긴 "smooth" view와 바깥 고공간주파수를 가우시안 잡음으로 바꾼 "perturbed" view를 만들고, 이를 ProtoNet 계열 few-shot 모델의 multi-view 학습과 테스트 시 support set 증강(PSG)에 쓴 논문이다. ShipsEar(클래스 단위 base/novel 분할)와 DanShip(교차 도메인)에서, 학습·테스트 모두 잡음을 주입한 저 SNR 조건의 이득을 보고한다.

## 확인한 내용 (`confirmed`)

### "knowledge-inspired"의 정체 (§I, §II.A, §II.C, §II.D)
- SDA는 STFT 스펙트로그램 X(C×H×W)를 **2D 이미지로 보고 FFT**한다. 원문: "the FFT is applied to the STFT spectrogram as a 2D feature matrix rather than to the raw time-domain waveform … coordinates in F(X) correspond to spatial frequencies of the spectrogram pattern, rather than the acoustic low- and high-frequency components" (§II.A).
- 마스크 M은 중앙 직사각형(가로·세로 비율 r = 0.2)이다 (식 1).
  - smooth view: Y_zero = F(X)⊙M (식 2). 스펙트로그램 이미지의 저역 통과(블러)와 같다.
  - perturbed view: Y_randn = F(X)⊙M + N⊙(1−M), N ~ N(0, σ²). σ는 바깥 계수의 표준편차로 정한다 (식 3).
  - IFFT로 되돌린다. 원문: "not intended to reconstruct physically meaningful time-domain waveforms" (§II.A).
- 저자가 직접 물리 분해가 아니라고 쓴다: "Although this design is motivated by domain knowledge in underwater acoustics, it is not intended as a physically exact decomposition of target and noise components … but rather as a representation-level prior" (§II.A). perturbed view에 대해서도 "The goal is not to simulate a specific physical noise source directly"라고 쓴다.
- 논문에 나오는 "도메인 지식"은 다음 세 가지 정성적 가정뿐이다.
  1. 선박 표적은 "relatively stable and repeatable line-spectrum-related patterns"(tonal)을 가지고, 잡음은 비정상(non-stationary)이다. 이것은 CFM 게이팅의 동기다 (§II.C).
  2. 전파 거리·해상 상태가 진폭을 크게 바꾼다. 그래서 Euclidean 대신 cosine 거리를 쓴다 (§II.D).
  3. 미세 텍스처는 잡음에 민감하고 거친 구조가 표적 정보다 (§II.A).
- 이 가정을 정량 모델(전파 모델, tonal 주파수, 도플러, 채널 등)로 쓰지 않는다. 다중경로·전파손실은 서론에서 동기로만 언급된다.

### "sample generation"의 정체 (§II.F, §III.B.2, §IV.D.5)
- **생성 모델이 아니다.** PSG는 테스트 시 support 샘플마다 "a stochastic, label-preserving perturbation function A(·)"로 pseudo-sample M개를 만든다 (식 13). 원문: "A(·) denotes a representation-level perturbation applied to spectrogram features … It is not intended as a physically exact acoustic transformation model."
- **A(·)의 구체적 형태(어떤 perturbation인지)는 원문에 없다.** pseudo-sample 수는 75개다 (§III.B.2, Table IX). 그 뒤 support set으로 50 epoch, lr 0.005 미세조정하고 에피소드마다 θ_init으로 초기화한다 (§II.F, §IV.D.5).
- GAN·diffusion은 관련연구로만 인용된다 (§I). 이 논문은 생성망을 학습하지 않는다.

### 모델·입력 (§II.B–E, §III.B)
- 입력: 16 kHz 리샘플, 3 s 세그먼트, STFT window 40 ms, overlap 20 ms, "128 filters"(STFT인데 128 filters라고 쓴 이유는 불명확함).
- ResNet + TFA(주파수축·시간축 평균 → MLP → sigmoid attention, 식 5–7)로 된 Siamese(가중치 공유) 3-stream 구조다.
- CFM: Weight = σ(f_ori ⊙ f_aug), f̃_aug = f_aug ⊙ (1+Weight) (식 8–9).
- 손실: 세 view 각각의 cosine-ProtoNet CE의 합 (식 12). 명시적 일관성 손실은 없다.
- 4.91 M 파라미터, 219.69 GFLOPs (Table X).

### 데이터 분할 (§III.A, §III.B.3–4)
- **ShipsEar (in-domain)**: 배경을 뺀 11 클래스를 쓴다 (Table I). base/novel을 "strictly mutually exclusive at the class level"로 나누고, 3개 split을 쓴다 (Table II: base 6 / novel 5 클래스).
  - 예: split 1 base = {0,1,3,5,8,10}, novel = {2,4,6,7,9}.
- **DanShip (cross-domain)**: 3 클래스(fishing, cargo, motorboats)다. 원문: "the full ShipsEar dataset serves as the source domain … DanShip serves as the unseen target domain (novel set)". "No DanShip data are used during pre-training" (§IV.C).
- **에피소드 구성**: N개 클래스를 균등 확률로 뽑는다. 그 다음 "K support samples and a fixed number of query samples are independently and uniformly drawn from the candidate pool of each selected class, with no overlap between the two sets" (§III.B.3). **N 값과 query 수는 숫자로 쓰여 있지 않다.**
- **녹음 단위·선박 단위 분리에 관한 기술은 원문 어디에도 없다.** "no overlap"은 샘플(3 s 세그먼트) 단위 중복 없음이다. support/query가 같은 녹음(같은 선박)의 다른 세그먼트일 수 있다. 이것은 ShipsEar, DanShip 모두 같다.
- **잡음 프로토콜**: 학습 시 base set에 "Natural ocean noise"를 SNR U[−15, 7] dB로 무작위 주입한다. 테스트는 clean, −5, −10, −15 dB다 (§III.A). 잡음 녹음의 출처와 학습/테스트 잡음의 분리 여부는 미기재다.
- **보고 방식**: 200 에피소드 평균 ± 95% CI를 3개 split에 걸쳐 평균한다 (§III.B.4). **seed 수와 독립 학습 반복은 기재되지 않았다.** 학습 epoch, batch, base 학습 lr도 없다.

### 주요 결과 (ShipsEar, 5-shot, ACC %)
| 설정 | −15 dB | −10 dB | −5 dB | clean |
|---|---|---|---|---|
| SDA_CFM (전체) | 51.00 ± 0.87 | 60.05 | 66.86 | 78.54 ± 0.75 |
| DAATF (2위 비교법) | 43.64 | 54.88 | 62.77 | 74.67 |
| ProtoNet | 28.57 | 37.76 | 43.21 | 54.81 |
(Table III, IV). 1-shot clean 53.82, 3-shot 71.03. DanShip 5-shot clean 80.29, −5 dB 67.59 (Table V, VI).

### 증강만의 ablation
- **Table VII (모두 PSG 포함, 5-shot)**:
  | 구성 | −15 | −10 | −5 | clean |
  |---|---|---|---|---|
  | Baseline (PSG만) | 37.28 | 50.81 | 58.89 | 76.99 |
  | +SDA (Config 3) | 49.65 | 59.42 | 64.83 | **76.19** |
  | TFA+CFM, SDA 없음 (Config 7) | 37.03 | 50.56 | 58.82 | 76.96 |
  | 전체 | 51.00 | 60.05 | 66.86 | 78.54 |
  | 전체 − PSG (Config 8) | 39.43 | 42.83 | 44.39 | **52.01** |
  - SDA 단독 효과: −15 dB에서 +12.37 pp, clean에서 −0.80 pp.
  - PSG 제거: clean −26.5 pp. 테스트 시 미세조정이 가장 큰 요인이다.
- **Fig. 6 (증강 비교, 수치는 본문 §IV.D.2)**:
  - −15 dB: 무증강 36.78, random freq masking 47.59, SpecAugment 46.16, Mixup 41.38, SDA 51.00.
  - clean: SpecAugment 80.36, Mixup 80.94, SDA 78.54. **clean에서는 범용 증강이 더 좋다.** 저자는 "general-purpose methods prioritize sample diversity rather than noise robustness"라고 설명한다.
- **Fig. 8 (multi-view)**: 단일 view 77.50 clean / 36.78 (−15 dB). smooth나 perturbed view를 CFM 없이 추가하면 오히려 하락한다(+smooth −15 dB 23.92). 전체는 −15 dB에서 +14.22 pp다.
- **Table VIII (r)**: r = 0.1–0.8 범위에서 −15 dB 47.48–51.00, clean 77.65–78.54로 민감도가 낮다.
- **Fig. 9 (마스크 형태)**: central > band_prior(−15 dB에서 −1.03) > random/circular/high-frequency. 평균 64.11%.
- **Fig. 10**: −15 dB에서 "signal-domain" 증강보다 +2.89, "frequency-band-domain" 증강보다 +5.31. **두 비교 증강의 구체적 정의는 원문에 없다.**
- 저자가 밝힌 한계: closed-set 설정이다. open-set 확장은 향후 과제다 (§V).

## 해석 (`inferred`)

### 물리 기반 증강인가? → 아니다
- SDA는 **스펙트로그램 이미지의 공간주파수 저역 통과 + 고역 계수 잡음 치환**이다. 신호처리로 보면 2D 블러와 텍스처 잡음에 가깝다. 음원·전파·센서 중 어떤 물리 과정도 모델링하지 않는다. 저자 스스로도 그렇게 쓴다(§II.A). 사용자 연구의 분류로는 **범용(표현 수준) 증강**에 넣어야 한다. "knowledge-inspired"는 동기 서술일 뿐이다.
- tonal과 충돌할 가능성: 시간 방향으로 일정한 tonal 선은 시간축 공간주파수로는 낮지만, 주파수축 폭이 좁아 **주파수축 공간주파수로는 높다.** 주파수축에서도 r = 0.2만 남기면 tonal 선이 주파수 방향으로 번진다(narrow → broad 쪽으로). 즉 SDA는 tonal을 보존하기보다 흐리게 만들 가능성이 있다. 실제로 clean 성능이 오르지 않은 것과 맞는다. 원문이 검증한 내용은 아니다. 직접 확인하려면 Fig. 7 또는 재현이 필요하다.
- 저 SNR 이득의 상당 부분은 "학습 때 해양 잡음 주입 + 테스트 때 같은 방식으로 잡음 주입"이라는 일치된 조건에서 블러 view가 잡음 텍스처에 대한 불변성을 준 결과로 보인다. 실제 원거리·저 SNR 녹음(도메인 시프트)에서도 같은 이득이 나는지는 검증되지 않았다.

### 분할과 누출
- ShipsEar의 클래스 단위 분할은 novel 클래스의 선박을 학습에서 보지 않는다는 점에서 base↔novel 사이 누출은 없다. 하지만 **평가 에피소드 안에서** support/query가 같은 녹음의 세그먼트일 수 있다. 그러면 "같은 선박의 다른 3 s 구간 맞추기"가 된다. ShipsEar는 클래스당 녹음 수가 적어 이럴 가능성이 높다. 정확도가 부풀려졌을 수 있다 (UniqueShip 논문의 누출 논지와 같은 종류).
- PSG가 빠지면 clean 정확도가 26.5 pp 떨어진다. support 샘플을 변형해 미세조정하는 것이 큰 효과를 내는 것은, query가 support와 같은 녹음에서 왔다면 자연스럽게 설명된다. 증명된 것은 아니며 가설이다.
- DanShip 교차 도메인은 데이터셋(해역·장비)이 다르다는 의미의 교차이고, 클래스 의미는 소스와 겹친다(fishing, motorboats).

### 사용자 연구와의 관계
- **UniqueShip 전체 데이터 설정으로 이식: SDA만은 가능하다.** SDA는 입력 스펙트로그램에 대한 결정적·확률적 변환일 뿐이므로 SwinV2+Mel 지도학습 파이프라인에 학습 증강으로 넣을 수 있다. 단 다음은 이식하지 않는 것이 맞다.
  - CFM·multi-view 3-stream: 메타러닝 구조에 묶여 있다.
  - PSG: 테스트 시 support 미세조정이라 일반 분류 설정에는 support set이 없다.
  - 그대로 넣으면 "논문의 일부 모듈(SDA)을 기반으로 변형함"이라고 표기해야 한다.
- **기대 효과는 낮다** (인접 근거 적용). 논문 안에서도 SDA의 이득은 저 SNR 잡음 주입 조건에 한정된다. clean에서는 SpecAugment·Mixup보다 낮았다. UniqueShip은 잡음 주입 프로토콜이 없는 실측 녹음이고 선박 단위 분리 일반화가 목표라서, 이 논문의 근거가 직접 적용되지 않는다.
- **범용 증강 비교군으로 쓸 수 있다.** 이 경우 "스펙트로그램 이미지 수준 텍스처 불변성" 대표 방법으로 둔다. SpecAugment·Mixup·freq masking과 함께 범용 증강 군에 넣고, 물리 기반 증강(채널·거리·tonal 변형)이 이것보다 나은지를 묻는 구도가 가능하다. 구현이 단순하다(2D FFT 마스크 몇 줄). 코드 미공개라 식 1–3대로 재구현해야 한다.
- 인용 문헌 중 사용자에게 더 직접적인 것: D. Li et al. (2023, Appl. Acoust. 208) "underwater acoustic channel modeling" 기반 증강이 있다. 이것이 물리 기반 증강 선행연구 후보다. 이 논문은 이것을 비교하지 않았다. J. Xu et al. (2023) smoothness 정규화는 이미 `papers/metadata/2023_xu_lmr_smoothness.yml`에 있다.
- 지도교수의 생성 모델 방향과는 연결이 약하다. "sample generation"은 생성 모델이 아니다.

## 이해 확인 질문 (사용자용)

1. SDA의 FFT 좌표 (u, v)는 음향 주파수(Hz)인가? 그렇지 않다면, 시간 방향으로 일정한 좁은 tonal 선은 (u, v) 평면 어디에 에너지를 가지는가? r = 0.2 중앙 마스크가 그 선에 무엇을 하는가?
2. Table VII에서 SDA를 넣으면 −15 dB는 +12.4 pp, clean은 −0.8 pp다. 이 차이를 학습·테스트 잡음 주입 프로토콜(§III.A)과 연결해 설명해 보라. UniqueShip 설정에서는 어느 쪽 숫자가 더 관련 있는가?
3. 이 논문의 "support/query no overlap"(§III.B.3)은 어떤 단위의 중복을 막는가? UniqueShip의 MMSI 분리와 비교하면 무엇이 빠져 있는가?

## 상태

- [x] 원문 확보
- [x] 원문 읽기
- [ ] 공식 코드 확인 (원문에 코드 링크 없음)
- [ ] 최소 재현 (필요 시 SDA만 범용 증강 비교군으로)
