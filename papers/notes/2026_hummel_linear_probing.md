# Hummel et al. 사전학습 오디오 임베딩 + linear probe (2026, arXiv:2601.08358v2)

- 원문: `papers/pdf/2026_hummel_linear_probing.pdf` (arXiv v2, 26쪽, 2026-10-10 전체 읽음. 23–26쪽은 참고문헌, 부록 없음)
- 기록 규칙: "확인한 내용"은 원문에서 직접 확인한 것(`confirmed`)이다. "해석"은 Claude의 추론(`inferred`)이다.
- 선행 논문: `papers/notes/2025_hummel_contrastive_uatr.md` (같은 1저자, DeepShip 시간순 분할을 그대로 가져옴)

## 연구 분류

- [x] 비교 기준 후보 (값싼 frozen 임베딩 baseline)
- [x] 분류기·백본 선택 근거
- [ ] 증강 근거 (증강 사용 안 함)

## 한 문장 요약

16개 사전학습 오디오 모델(일반 오디오, 음성, 생물음향, 해양생물)을 frozen으로 두고 linear probe로 DeepShip·ShipsEar 선박 종류를 분류하면 BEATs가 가장 좋았고(65.4% / 74.0%), 임베딩 공간의 전역 구조는 선박 종류가 아니라 녹음 ID에 지배된다는 것을 보인 논문이다.

## 확인한 내용 (`confirmed`)

### 데이터와 분할 (§3.1.2)

- **DeepShip** (>45 h, 4 클래스, 2 km inclusion zone): 원문: *"For Deepship, a time-wise split was made as described in [11]. This split ensures that there is no data leakage in the test set and that the test set represents the future relative to the training set."*
  - [11]은 2025_hummel_contrastive_uatr이다. 그 논문에서 분할은 2017-11까지 학습, 2017-12부터 테스트이며 *"almost 60% of the data samples in the test set are newly seen ships"*라고 썼다.
  - 단위: **날짜 기준 녹음 분할.** 이 논문은 "no data leakage"라고 주장하지만, 선행 논문의 수치대로라면 테스트 샘플의 약 40%는 학습에 나온 선박이다. **선박 단위 분리가 아니다.**
- **ShipsEar** (이 논문은 "eight hours", 5 클래스, 스페인 북서부 대서양 연안): 원문: *"For ShipsEar, this information is not present to make such a split. Therefore, 80% of the individual recordings were utilized for training, and the remaining recordings for testing."*
  - 단위: **녹음 단위 80/20.** 선박 단위 통제는 언급 없음.
  - Fig. 2 범례의 ShipsEar 클래스: Cargo, Passenger, Tanker, Tug, Background. 원래 ShipsEar의 A–E 분류와 다른 재구성으로 보인다(재구성 규칙은 원문에 없음).
  - 테스트 녹음 수: ShipsEar 21개, DeepShip 237개 (§4.1.3, 녹음 ID 클러스터 수).
- 전체 길이 불일치: ShipsEar를 2025 논문은 3 h 8 m, 이 논문은 8 h라고 썼다.
- **UniqueShip, VTUAD 등 다른 데이터는 평가하지 않았다.**

### 사전학습 모델 (Table 2, §3.2)

모두 frozen. 크기가 여러 개면 base 크기를 썼다.

| 도메인 | 모델 | 구조 / 파라미터 | 사전학습 데이터 | 입력 | SR | window | 임베딩 | 학습 |
|---|---|---|---|---|---|---|---|---|
| 일반 오디오 | AudioMAE | Transformer 86M | AudioSet | Mel | 16 kHz | 10 s | 768 | SSL |
| 일반 오디오 | BEATs | Transformer 90M | AudioSet | Spectrogram | 16 kHz | 10 s | 768 | SSL |
| 일반 오디오 | HuBERT AS | (Table 2에 없음, §3.2.1) | AudioSet | – | – | – | – | SSL |
| 음성 | Wav2Vec2.0 | Transformer 95M | LibriSpeech | raw | 16 kHz | 10 s | 768 | SSL |
| 음성 | Data2Vec | Transformer 95M | LibriSpeech | raw | 16 kHz | 10 s | 768 | SSL |
| 음성 | WavLM | CNN+Transformer 94.7M | LibriSpeech | raw | 16 kHz | 10 s | 768 | SSL |
| 음성 | HuBERT Base | CNN+Transformer 95M | LibriSpeech | raw | 16 kHz | 10 s | 768 | SSL |
| 생물음향 | BirdMAE | Transformer 86M | BirdSet | Spectrogram | 32 kHz | 10 s | 1,280 | SSL |
| 생물음향 | BirdNET | ResNet 27M | XC, eBird, Macaulay | Spectrogram | 48 kHz | 3 s | 1,024 | SL |
| 생물음향 | AvesEcho | PaSST 85M | – | Mel | 16 kHz | 1 s | 768 | SL |
| 생물음향 | Animal2Vec MK | Transformer 315M | MeerKAT | raw | 8 kHz | 10 s | 1,024 | SSL |
| 생물음향 | Perch | EfficientNet 7.8M | XC | raw | 32 kHz | 5 s | 1,280 | SL |
| 생물음향 | Perch 2.0 | EfficientNet 12M | XC, iNat, Tierstimmen, FSD50K | log Mel | 32 kHz | 5 s | 1,536 | SL |
| 생물음향 | AVES | CNN+Transformer 95M | FSD50K, AS 20k, VGGSound | raw | 16 kHz | 1 s | 768 | SSL |
| 해양생물 | Google Whale | EfficientNet | NOAA | Spectrogram | 24 kHz | 5 s | 1,280 | SL |
| 해양생물 | SurfPerch | EfficientNet | ReefSet | Spectrogram | 32 kHz | 5 s | 1,280 | SL |

- **PANNs와 CLAP은 평가하지 않았다.**
- Baseline: log Mel(128 bin, n_fft 1,024, hop 512) → 시간 평균 → 로지스틱 회귀 (§3.2.5).

### 평가 방법 (§3.3)

1. K-Means(클러스터 수 = 클래스 수) + NMI.
2. 테스트 샘플끼리 cosine similarity 순위 → 같은 클래스를 positive로 한 ROC-AUC.
3. frozen 임베딩 + linear probe 선박 종류 분류 정확도.

- **원문에 없는 것**: linear probe의 최적화 설정(optimizer, epoch, 정규화), 입력 clip 길이와 각 모델 window보다 긴 녹음의 처리, 시간 pooling 방식, 사용한 층(최종 층으로 추정), 반복 실행 수와 표준편차.

### 결과

**Table 6. linear probe 정확도 (단일 값)**

| 모델 | DeepShip | ShipsEar |
|---|---|---|
| AudioMAE | 61.9% | 67.2% |
| **BEATs** | **65.4%** | 74.0% |
| HuBERT AS | 54.2% | 42.7% |
| **Wav2Vec2.0** | 56.8% | **78.0%** |
| Data2Vec | 56.8% | 53.1% |
| WavLM | 49.7% | 45.0% |
| HuBERT | 50.1% | 32.8% |
| BirdMAE | 63.4% | 67.2% |
| BirdNET | 58.6% | 57.5% |
| AvesEcho | 57.22% | 64.26% |
| Animal2Vec MK | 64.0% | 61.0% |
| Perch | 55.0% | 64.3% |
| Perch 2.0 | 61.4% | 73.2% |
| AVES | 56.4% | 59.1% |
| Google Whale | 45.9% | 50.6% |
| SurfPerch | 57.8% | 58.9% |
| Baseline (Mel 평균 + LR) | 56.4% | 48.6% |

- Attentive probing도 시도했으나 linear probe보다 못했다(수치 미제시, §4.2.1).
- 저자 해석: WavLM이 baseline보다 낮은 것은 denoising 사전학습 목표가 선박의 잡음 특성을 지우기 때문일 수 있다. 해양생물 모델은 지도 학습된 좁은 도메인이라 전이가 나쁘다. Animal2Vec은 8 kHz인데도 64.0%.

**Table 3, 4. 비지도 지표 (DeepShip / ShipsEar)**

- NMI: 대부분 0.03–0.18 / 0.13–0.39. Mel baseline 0.00 / 0.16. 최고 Data2Vec 0.18(DeepShip), AvesEcho 0.39(ShipsEar). BEATs 0.13 / 0.22.
- 유사도 ROC-AUC: BEATs 0.61 / 0.72, Mel baseline 0.62 / 0.71. **어떤 사전학습 모델도 Mel baseline을 뚜렷이 넘지 못했다.**

**녹음 ID 분석 (§4.1.3, §4.2.2)**

- BEATs 임베딩을 녹음 ID로 평가하면 NMI 0.62 / 0.66, ROC-AUC 0.90 / 0.93 (Table 5). 선박 종류 기준(0.13 / 0.22, 0.61 / 0.72)보다 훨씬 높다. 다른 모델도 같은 현상이라고 저자가 씀(수치 미제시).
- 라벨 셔플 대조 실험(BEATs): **녹음 단위로** 라벨을 섞어 재학습 → DeepShip 22.9%, ShipsEar 44.6%.
- linear probe의 logit 공간 클러스터링: NMI 0.36 / 0.42 (원 임베딩의 약 2배). PCA 축소만으로는 0.14 / 0.27.
- 특징 하나씩 0으로 만들기: 대부분 특징은 정확도에 영향이 없고 일부만 크게 영향 (Fig. 3, ShipsEar).
- HuBERT 3종(음성 / AudioSet / AVES 생물음향) 비교: 음성 사전학습이 가장 나쁘고, 생물음향이 일반 오디오보다 약간 좋다 (Fig. 4).

### 증강

- **증강을 전혀 쓰지 않았다.** 원문에 augmentation 언급 없음.

## 해석 (`inferred`)

### 누출 없는 조건의 성능은 아직 모른다

- 이 논문의 "누출 없음"은 날짜 기준 분할이다. 선박 단위가 아니다. 따라서 **MMSI 분리 조건에서의 BEATs + linear probe 성능은 `unknown`이다.**
- 참고로 UniqueShip 논문의 DeepShip 결과: SwinV2 Mel, MMSI 분리 58.8 ± 7.7%, 파일 무작위 71.0 ± 2.9%. 이 논문의 DeepShip 시간순 분할 BEATs 65.4%는 그 사이에 있다. 분할 정의, 테스트 집합, 클립 길이가 모두 달라서 **직접 비교는 할 수 없다.**
- 단일 실행이고 표준편차가 없다. DeepShip 테스트 녹음이 237개, ShipsEar는 21개뿐이다. ShipsEar에서 녹음 하나가 정확도를 수 pp 움직일 수 있다. Wav2Vec2.0 78.0% vs BEATs 74.0% 같은 순위는 믿기 어렵다.

### 녹음 ID 지배 현상의 의미

- 저자는 라벨 셔플에서 정확도가 떨어졌으니 "녹음 ID에 의존하지 않는다"고 결론낸다. 하지만 이 실험은 **선박 ID 지름길**을 배제하지 못한다. 학습과 테스트에 같은 선박이 있으면, 선박 고유 특성(특정 tonal 주파수)을 외워서 종류를 맞힐 수 있다. 그 경우 라벨 셔플에서도 정확도는 떨어진다. 즉 셔플 실험은 "녹음 ID 지름길"과 "선박 ID 지름길"을 구분하지 않는다.
- ShipsEar 라벨 셔플 후 44.6%는 5 클래스 우연 수준(20%)보다 꽤 높다. 클래스 불균형이나 녹음 단위 셔플의 특성 때문일 수 있으나 원문 설명은 없다.
- 녹음 ID가 임베딩을 지배한다는 결과는 **녹음 조건(거리, 배경, 장비, 계절)이 선박 종류보다 큰 분산을 만든다**는 뜻이다. 이것은 사용자의 물리 기반 증강 동기와 직접 연결된다. 녹음 조건 변이를 증강으로 만들어 분류기가 그것에 불변하도록 하는 것이 목표가 될 수 있다. (합리적인 가설이지만 직접 근거가 부족함)

### 모델 간 비교에서 통제되지 않은 변수

- 샘플링레이트가 8–48 kHz, window가 1–10 s로 다르다. 저주파 tonal 분해능은 window 길이에 직결된다. BEATs·AudioMAE·BirdMAE(10 s)가 상위인 것이 사전학습 데이터 때문인지 긴 window 때문인지 이 논문으로는 구분할 수 없다.

## 사용자 연구와의 관계 (`inferred`)

- **baseline 추가 후보**: "frozen BEATs(또는 Perch 2.0) + linear probe"는 GPU 비용이 작고, 증강과 무관한 강한 비교 기준이다. 사용자 연구에서 SwinV2 + Mel 67.3%(UniqueShip) 옆에 두면 "증강으로 얻은 이득이 단순히 좋은 사전학습 표현으로도 얻어지는가"를 확인할 수 있다. (직접적인 선행연구 근거가 있음: DeepShip·ShipsEar에서 Mel baseline을 넘음. 단 UniqueShip 근거는 없음)
- **분류기 선택에 대한 함의**: 이 논문은 fine-tuning을 하지 않았고, SwinV2·ResNet-18·UATR-SLM과 비교하지도 않았다. 따라서 "linear probe가 지도 분류기보다 낫다"는 근거는 **없다.** 이 논문이 주는 것은 "frozen 일반 오디오 임베딩이 Mel 평균 + LR보다 낫다"까지다.
- **증강 실험 설계에 대한 함의**: frozen 임베딩 + linear probe 위에서 증강 효과를 보면, 증강이 백본 표현을 바꾸지 않으므로 효과가 작게 나올 수 있다. 증강 연구의 주 실험은 학습 가능한 분류기(SwinV2, ResNet-18)에서 하고, BEATs probe는 고정 비교 기준으로만 쓰는 것이 단순하다. (구현 휴리스틱임)
- **누출 점검 도구로 쓸 수 있음**: 녹음 ID / MMSI로 임베딩 NMI를 재는 이 논문의 방법을 그대로 써서, 사용자의 분할에서 테스트 임베딩이 선박 ID로 얼마나 뭉치는지 확인할 수 있다. 증강 후 선박 ID NMI가 내려가고 선박 종류 정확도가 유지되면 "선박 고유 지름길을 줄였다"는 보조 증거가 된다. (논문에서 영감을 받은 가설임)
- **주의**: BEATs 등은 AudioSet으로 사전학습되었다. ONC 데이터가 AudioSet에 들어 있을 가능성은 낮지만 확인된 것은 아니다(`unknown`).

## 이해 확인 질문 (사용자용)

1. 이 논문의 라벨 셔플 실험은 "분류가 녹음 ID에 의존하지 않는다"는 것을 보였다. 그런데 학습·테스트에 같은 선박이 있을 때 생기는 "선박 ID 지름길"은 왜 이 실험으로 배제되지 않는가?
2. BEATs(16 kHz, 10 s window)와 BirdNET(48 kHz, 3 s window)의 DeepShip 정확도 차이를 "사전학습 데이터 도메인의 차이"로만 해석하면 안 되는 이유를 tonal 분해능 관점에서 설명하라.

## 상태

- [x] 원문 확보 (arXiv v2)
- [x] 원문 읽기
- [ ] 공식 코드에서 probe 설정, clip 길이, pooling 확인
- [ ] UniqueShip MMSI 분할에서 frozen BEATs + linear probe 최소 재현
