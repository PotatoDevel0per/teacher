# ICASSP 형식 서론 초안 (2026-10-26)

- 가정: 본문 4쪽 + 참고문헌 1쪽. 서론은 약 0.7단(450–600 단어). 현재 약 830 단어로 ICASSP에는 길다 → 줄이는 안은 끝에 적었다. 학위논문 1장에는 그대로 쓸 수 있다.
- 사용자 요청 요소: (A) UATR 배경, (B) 분류 연구의 분할 한계, (C) 증강 연구의 분할 한계, (D) WAV 복원 가능한 생성 모델의 부재, (E) 목표 변경 서사(사용자 요청 2026-10-26: WAV 생성 → 누출·선박 암기 발견 → 클래스 특징 분류기 먼저, LDM 물리 기반 증강).
- (E)의 수치는 우리 실험(E1-src, DeepShip MEL 입력 O_rp/B/T, seed 0, 5 fold)이다. 본문 §분석 절에 같은 수치가 있어야 한다.
- [TBD]는 실험 결과가 나와야 채울 수 있는 부분이다.
- 문단 순서: A → B → C → D → 기여. B(평가 문제)를 먼저 세워야 C의 "증강 이득이 부풀려졌다"와 D의 "새 선박 변이를 만들 생성기가 없다"가 자연스럽게 이어진다.

---

## 1. INTRODUCTION

**(A) Background.** Underwater acoustic target recognition (UATR) aims to identify vessel classes from ship-radiated noise recorded by passive hydrophones. Beyond its role in maritime surveillance and traffic monitoring, UATR has gained importance as anthropogenic noise, dominated by shipping, has become a recognized stressor on marine ecosystems [1], prompting the International Maritime Organization to issue and revise guidelines for reducing underwater radiated noise from ships [2]. Deep learning has become the dominant approach to UATR [3], [4], yet its progress is constrained by data: public corpora such as ShipsEar [5] (90 recordings, about 3 h) and DeepShip [6] (about 47 h from 265 vessels) cover only a few hundred vessels, and collecting new labeled recordings requires long-term hydrophone deployment and AIS-based annotation.

**(B) Partition bias in classification studies.** The reported accuracy of UATR models is further inflated by how the data are partitioned. Recordings of the same vessel are strongly correlated, and when clips of one vessel appear in both the training and test sets, a classifier can rely on vessel-specific cues rather than class-level characteristics. Hashemi et al. [7] showed that enforcing vessel-disjoint partitions reduces accuracy by 10–48 percentage points (pp) across benchmarks; on DeepShip, a Swin Transformer drops from 0.710 to 0.588. Hummel et al. [8] further observed that pretrained audio embeddings of ship noise cluster by recording rather than by vessel class. Nevertheless, neither ShipsEar nor DeepShip provides an official vessel-disjoint partition, and segment-, file-, or recording-level splits remain common practice [9].

**(C) Partition bias in augmentation studies.** Data augmentation is a natural remedy for data scarcity, and both generic transforms (SpecAugment, mixup, local masking and replicating) and generative models (GANs, VAEs) have been applied to UATR [10]–[13]. However, among the augmentation studies whose partition protocol we could verify, none was evaluated on vessel-disjoint splits. The gains of GAN-based augmentation reported under random sample-level splits (+6 to +12 pp [12], [13]) shrink to +0.5 to +1.3 pp under recording-level splits [10], where noise injection also showed no consistent benefit [10]. Meanwhile, doubling the number of vessels improves vessel-disjoint accuracy roughly two to three times more than doubling the recording time per vessel [7]. Effective augmentation should therefore synthesize vessel-level variation, which cropping and mixing existing recordings cannot provide. Whether any augmentation delivers such variation under vessel-disjoint evaluation has not been tested.

**(D) Lack of waveform-recoverable generative models.** Generative models are a natural candidate for producing vessel-level variation, and a waveform-recoverable generator would further allow generated samples to be listened to, re-analyzed with other front-ends, and checked against the physical signatures of ship noise: tonal lines from machinery and propeller-induced amplitude modulation revealed by DEMON analysis. Existing generators for ship-radiated noise, however, mostly operate on normalized spectrogram features; the LR-VAE of Huang et al. [11], for example, explicitly operates at the feature level and is not intended to synthesize physically faithful waveforms, while waveform-domain GANs [12] were assessed under random sample-level splits. In general audio, by contrast, latent diffusion models [14] combined with neural vocoders have made waveform-recoverable generation routine [15].

**(E) From waveform generation to class-level recognition.** This work originally set out to build such a waveform-recoverable generator. In doing so, we found that the bottleneck lies one step earlier, in what the classifier learns. On DeepShip, the macro-F1 of the same classifier drops from 69.2% under recording-disjoint splits to 57.8% under vessel-disjoint splits, indicating that much of the reported accuracy comes from memorizing individual vessels rather than learning class-level characteristics. Moreover, under vessel-disjoint evaluation, a classifier given only the broadband long-term spectrum retains almost all of its accuracy (53.2%), whereas one given only tonal lines falls to 41.9%. A generator judged by such a classifier would be rewarded for reproducing vessel identity and broadband texture, not for producing new, physically plausible vessels. We therefore reorder the problem: we first establish a classifier and evaluation protocol that measure class-level recognition on unseen vessels, and then use a latent diffusion model for physics-based augmentation under this protocol. Waveform recovery is retained as the final stage, which the physics-based evaluators already support because they operate on waveforms.

**Contributions.** In this paper, we address these gaps as follows:
(1) We establish vessel-disjoint five-fold protocols for DeepShip and ShipsEar, verified to share no vessel or recording between training and test sets, and show that recording-disjoint evaluation inflates macro-F1 by about 11 pp.
(2) We analyze where class-discriminative information resides under vessel-disjoint evaluation by separating broadband and tonal components, finding that it lies mainly in the broadband long-term spectrum.
(3) We build physics-based evaluators for generated samples: tonal-line detection, and a DEMON detector with cepstral pre-whitening that suppresses spurious modulation peaks caused by beating between closely spaced tonal lines.
(4) We propose a physically conditioned latent diffusion model for augmentation and evaluate it under vessel-disjoint protocols [TBD: 클래스 특징 중심 분류기 설계, 증강 결과].

---

## 참고문헌 (번호는 위 본문 기준)

| # | 서지 | 본문에서 받치는 주장 | 확인 수준 |
|---|---|---|---|
| [1] | Duarte et al., "The soundscape of the Anthropocene ocean," *Science*, 371, eaba4658, 2021 | 해운 소음이 해양 생태계 스트레스 요인 | 서지·요지(검색) |
| [2] | IMO, MEPC.1/Circ.906 (2023), Rev.1 (2024) | 수중 방사소음 저감 지침 발행·개정 | 공식 문서 링크 |
| [3] | Feng et al., "AI-based UATR: A survey," *Remote Sens.*, 16(17), 3333, 2024 | 딥러닝이 주류 | 초록 |
| [4] | Muller et al., *IEEE Access*, 2024 | 같음 | 검색. 저자·제목 원문 확인 필요 |
| [5] | Santos-Domínguez et al., "ShipsEar," *Appl. Acoust.*, 113, 64–69, 2016 | 90 녹음, 약 3 h | 서지·초록 |
| [6] | Irfan et al., "DeepShip," *Expert Syst. Appl.*, 115270, 2021 | 약 47 h, 265척 | 서지·초록. **수치 원문 대조 필요**(인용 논문마다 47.07–47.22 h) |
| [7] | Hashemi et al., "UniqueShip," arXiv:2609.13659, 2026 | 10–48 pp 하락, 0.710 → 0.588, 선박 수 vs 시간 ablation | **원문 전체 읽음** |
| [8] | Hummel et al., linear probing, 2026 | 임베딩이 녹음 ID로 군집 | 원문(에이전트) |
| [9] | Yan et al., *Digital Ocean & Underwater Warfare*, 2026 (중문) | 분할 방식에 민감, 세그먼트·녹음 분할이 흔함 | 영문 초록만. **대체 근거 권장**(아래 위험 1) |
| [10] | Xu J. et al., LMR, *Ocean Eng.*, 2023 | 녹음 단위 분할에서 생성 증강 +0.5–1.3, 잡음 증강 효과 없음 | 원문(에이전트) + 우리 재현 |
| [11] | Huang et al., LR-VAE, *JASA*, 159(5), 2026 | feature level, 물리적으로 충실한 파형이 목표 아님(저자 문장) | 원문(에이전트) |
| [12] | Xie Z. et al., 1-D DCGAN, *Front. Mar. Sci.*, 2023 | 파형 GAN, 샘플 무작위 분할, 79 → 90% | 원문(에이전트) |
| [13] | Jiang et al., DCGAN, *Sensors*, 2022 | 이미지 무작위 7:3, 86 → 92% | 원문(에이전트) |
| [14] | Rombach et al., LDM, CVPR 2022 | latent diffusion | 핵심 절 원문 대조 |
| [15] | Liu et al., AudioLDM, ICML 2023 | 일반 오디오에서 LDM + 보코더로 파형 생성 | **Claude 기억. 서지 확인 필요** |

## 주장별 위험

1. (B) "segment-, file-, or recording-level splits remain common practice": 지금 근거는 증강 논문 9편의 분할 분포(`research/literature/uatr_augmentation_survey.md`)와 중문 리뷰 초록뿐이다. 분류 논문 5–10편의 분할을 확인해 표로 만들면 [9]를 대체할 수 있다.
2. (C) "none was evaluated on vessel-disjoint splits": 근거는 분할을 확인한 9편이다. 그래서 "among the studies whose partition protocol we could verify"라는 한정어를 붙였다. 이 한정어는 빼지 않는다. MBAT(JASA 2025)는 "unseen 개별 선박"을 주장하므로, 원문을 확인하기 전에는 반례 후보로 남긴다.
3. (D) "To our knowledge, no generative model ...": 세 조건(파형 복원, 물리 특징 보존 검증, 선박 단위 UATR 개선)을 모두 만족하는 연구가 없다는 주장이다. 각 조건 하나만 보면 반례가 있을 수 있다. 예: [12]는 파형을 생성한다. 그래서 세 조건을 묶어 썼다. 투고 전에 "ship noise waveform generation diffusion" 계열을 다시 검색해야 한다.
4. **(해결됨, 2026-10-26: (E) 문단으로 WAV를 최종 단계로 명시)** (D)와 현재 연구 결정의 충돌. D-2026-10-19-01에서 WAV 생성은 후순위로 두었다. 서론에서 WAV 부재를 공백으로 내세우면, 본문에서 WAV를 실제로 복원하고 물리 평가기로 확인한 결과가 있어야 한다. 선택지:
   - (가) WAV 복원(보코더 또는 Griffin–Lim)과 파형 기반 tonal·DEMON 평가를 논문 범위에 넣는다. 평가기 e는 이미 파형 기반이라 바로 쓸 수 있다.
   - (나) (D)를 "물리 특징 보존을 검증한 생성 모델의 부재"로 약하게 쓰고, WAV는 future work로 둔다.
5. (A) [6]의 DeepShip 수치는 원문으로 확인한다. 우리 분할 기준 수치(244 그룹, 33,644 클립)와는 다르다. 이름 병합과 Tanker 10 녹음 제외 때문이며, 본문 §데이터에 적는다.

## 줄이는 안 (약 450 단어로)

- (A)에서 IMO 문장을 [1]에 붙여 한 절로 줄인다.
- (B)의 Hummel 문장을 뺀다. 핵심 근거는 [7] 하나로 충분하다.
- (C)의 수치 괄호(+6 to +12, +0.5 to +1.3)를 남기고, 잡음 증강 절은 뺀다.

## (E) 문단 주의 (2026-10-26)

- (E)의 근거 수준:
  - "Rec-disjoint 69.2 → Ships-disjoint 57.8": 원본 MEL, seed 0, 5 fold(thesis `exp/E1_src/summary.md`, 하락 +11.40). Rec-disjoint는 E1-src용 recrand 분할(fold별 공유 선박 39–47척)이다. 투고 전 seed 3으로 늘린다.
  - "broadband만 53.2%, tonal만 41.9%": seed 0, 5 fold. SwinV2 + MEL 표현에서 쓸 수 있는 정보에 한정된다(H-SC-3, inferred). 20 Hz median 분리는 넓은 narrow 성분을 B에 남긴다.
  - **broadband가 정확도를 부풀린다는 것은 확인되지 않았다.** E1-src의 D = drop(B) − drop(T) = +3.20, CI [−1.54, +7.84]로 보류다. 확인된 것은 (1) Rec-disjoint의 부풀림, (2) Ships-disjoint 클래스 정보가 broadband에 있다는 것 두 가지다. 그래서 (E)는 "선박 암기"와 "broadband 의존"을 따로 썼다.
- 기여 (4)의 "클래스 특징 중심 분류기"는 아직 설계가 없다. 투고 전까지 무엇을 하는지 정해야 한다(예: 선박 ID 적대 학습, 선박 균형 샘플링, broadband 정규화). 정하지 못하면 (E)의 "first establish a classifier"를 "first establish an evaluation protocol"로 줄인다.
- ICASSP에서는 "originally set out to" 같은 연구 이력 서술이 드물다. 분량이 모자라면 (E)의 첫 두 문장을 "A generator, however, can only be as meaningful as the classifier used to judge it."로 바꾼다. 학위논문 1장에는 이력 서술을 그대로 둔다.
