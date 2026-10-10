# UATR 데이터 증강 문헌 목록 (1차 조사)

- 조사일: 2026-10-06. Claude 조사 에이전트가 웹 검색과 원문 조회로 작성했다.
- **이 목록의 수치는 이 세션이 직접 원문으로 검증하지 않았다.** 검증 수준 열을 반드시 확인한다.
  - 원문: 조사 에이전트가 본문을 읽음 (arXiv, PMC, Frontiers)
  - 초록: Crossref 또는 출판사 초록만 봄
  - 검색: 검색 결과 요약만 봄
- ScienceDirect, MDPI, AIP 본문은 접근 차단(403, 캡차) → 해당 논문은 분할 방식이 unknown이다.
- SCI 여부는 저널 등급에 대한 에이전트의 기억이다. **미검증**이다.

## 목록

| # | 논문 | 증강 | 데이터 | 분할 | 보고된 개선 | 검증 |
|---|---|---|---|---|---|---|
| 1 | Xu J. 2023, *Ocean Engineering*, 10.1016/j.oceaneng.2023.114926 (arXiv 2306.06945) | LMR(국소 마스킹·복제). 비교군: 백색잡음, GAN, mixup | ShipsEar, DeepShip, DTIL | **녹음 단위** (30 s, 같은 트랙 분리, 분할 공개). 선박 분리는 미보장 | DeepShip STFT 74.68 → 78.40. 잡음 추가는 효과가 불일치하거나 악화 | 원문 |
| 2 | Xie Y. 2023, arXiv 2304.11907 (게재처 미확인) | 비교군: 잡음, GAN | ShipsEar, DeepShip | 기재 없음 | Mel DeepShip 74.85 → 75.27 / 75.79 | 원문 |
| 3 | Xie Z. 2023, *Front. Mar. Sci.*, 10.3389/fmars.2023.1113224 | 1-D DCGAN 파형 | ShipsEar 4종 | 샘플 무작위 | CNN 79 → 90% | 원문 |
| 4 | Jiang Z. 2022, *Sensors*, 10.3390/s22062293 | 개량 DCGAN | 비공개 | 이미지 무작위 7:3 | 86 → 92% | 원문 |
| 5 | Li J. 2022, *Entropy*, 10.3390/e24111657 | SpecAugment | DeepShip, ShipsEar | 세그먼트 무작위 | ablation 없음 (99.0%) | 원문 |
| 6 | Mohammadi A. 2025, OCEANS 2025 (학회), arXiv 2409.13878 | SpecAugment + mixup | DeepShip | 녹음 단위 | ablation 없음 | 원문 |
| 7 | Hummel H.I. 2026, *Applied Acoustics*, 10.1016/j.apacoust.2025.111103 | 대조학습용 증강 | DeepShip 외 | 시간순 (선박 중복 미확인) | 증강 종류별 52.5–55.9% | 원문 |
| 8 | Xie Y. 2024, *JASA* 계열, arXiv 2411.02848 | LMR 상시 적용 | ShipsEar | 녹음 단위 | ablation 없음 | 원문 |
| 9 | Mahmud N.-A. 2025, *Sci. Rep.*, 10.1038/s41598-025-32401-3 | mixup 계열 | DeepShip 외 | 클립 무작위 70/30 | 90.40 → 97.53% | 원문 |
| 10 | Qian P. 2025, *Remote Sensing*, 10.3390/rs17172961 (DS3500) | BELLHOP 심해 채널 통과 | ShipsEar 기반 합성 | 세그먼트 단위, test도 합성 | 95.93% | 데이터셋 카드 |
| 11 | Li D. 2023, *Applied Acoustics* 208, 10.1016/j.apacoust.2023.109344 | 수중 채널 모델링 + 전이학습 | 미확인 | unknown | 미확인 | 초록 |
| 12 | Xu Y. 2023, *Applied Acoustics* 211, 10.1016/j.apacoust.2023.109468 | 하모닉을 고려한 pitch shift / time stretch | DeepShip, ShipsEar | unknown | +1.67 / +2.25 %p | 초록 |
| 13 | Liu F. 2021, *Applied Acoustics* 178, 10.1016/j.apacoust.2021.107989 | SpecAugment + 3-D Mel | ShipsEar | unknown | 94.3% | 검색 |
| 14 | Zhao L. 2024, *DSP*, 10.1016/j.dsp.2024.104504 | 시간 마스킹, 속도 섭동, 잡음 | 미확인 | unknown | 미확인 | 검색 |
| 15 | Yao Q. 2023, *Electronics*, 10.3390/electronics12051206 | 증강 + 잔차 CNN | 미확인 | unknown | 미확인 | 검색 |
| 16 | Lyu Y. 2025, *IMTS*, 10.1007/s44295-025-00059-2 (SCI 미확인) | AS-DCGAN | DeepShip, ShipsEar | unknown | 81.14 / 86.11% | 초록 |
| 17 | Huang W. 2026, *JASA* 159(5), 10.1121/10.0043727 | LR-VAE 생성 (few-shot) | 미확인 | unknown | 미확인 | 초록 |
| 18 | Gao W. 2026, *JASA* 160(1), 10.1121/10.0044413 | 지식 기반 스펙트럼 분해 증강 | ShipsEar, DanShip | unknown | 미확인 | 초록 |
| 19 | (관련) Hashemi 2026, UniqueShip, arXiv 2609.13659 | 없음 | — | MMSI 단위 | 누출 효과 측정 | 원문(이 KB에서도 확인) |
| 20 | (관련) Tyagi 2026, SKANN, arXiv 2609.07399 | 채널·잡음·다중경로 섭동(tonal 보존) | IARA | 선체 단위 (재식별 과제) | ablation 없음 | 초록 |
| 21 | (관련) MBAT 2025, *JASA* 157(5):3508, 10.1121/10.0036456 | 개별 선박 정보 적대 학습(증강 아님) | DeepShip, ShipsEar | unknown ("unseen 개별 선박" 주장) | 미확인 | 검색 |

## 요약 (에이전트 결론, `inferred`)

- 분할을 확인한 9편의 분포: 세그먼트·샘플 무작위 5, 녹음 단위 3, 시간순 1, **선박(MMSI) 단위 0**
- 선박 단위 분리 조건에서 증강 효과를 ablation한 UATR 연구는 찾지 못했다.
- 물리·시뮬레이션 기반 증강: #10(BELLHOP, 누출 있음, 합성 test), #11(분할 미확인), #12(반물리적, 분할 미확인)
- 녹음 단위 분할에서 백색잡음 증강은 효과가 없거나 오히려 해로웠다(#1). 생성 증강도 +0.5–1.3 %p 수준이었다(#1, #2). 무작위 분할에서는 +6–12 %p로 보고됐다(#3, #4).
- **"없다"고 확정할 수는 없다.** #11, #12, #21의 원문을 확인해야 한다.

## 원문 확인 우선순위

1. #11 Li 2023 (채널 모델링 증강): 신규성 주장 범위를 정한다.
2. #12 Xu Y. 2023 (하모닉 고려 pitch/time): 회전수 증강과 가장 가깝다.
3. #1 Xu J. 2023: 녹음 단위 분할이 공개돼 있고, 잡음 증강의 부정적 효과를 보고했다.
4. #10 Qian 2025 (BELLHOP): 구현 참고 + 비판 대상
5. #21 MBAT 2025: unseen 선박 평가 프로토콜을 확인한다.

## 논문별 증강 종류와 효과 정리 (2026-10-10)

"유의미" 판정 기준 (Claude 제안):
- **A**: 증강만 뺀 비교(ablation)가 있고, 녹음 단위 이상의 분할에서 개선이 보고됨
- **B**: ablation은 있지만 무작위 분할이거나 분할 방식 미확인 → 개선 폭이 부풀려졌을 수 있음
- **C**: ablation 없음(증강을 썼다는 기록만 있음)
- **–**: 효과 없음 또는 악화가 보고됨

| 논문 | 증강 종류 | 등급 | 근거 |
|---|---|---|---|
| #1 Xu J. 2023 (Ocean Eng.) | LMR(국소 마스킹 + 다른 샘플 패치 복제) | **A** | DeepShip STFT 74.68 → 78.40, ShipsEar 75.24 → 82.76 (녹음 단위) |
| | mixup | A(작음) | DeepShip 74.83(+0.15), ShipsEar 79.31(+4.07) |
| | GAN 합성 | A(작음) | DeepShip 75.98(+1.30) |
| | 가우시안 백색잡음 5–30 dB | **–** | 일관되지 않음. DeepShip Bark에서는 75.15 → 74.18로 악화 |
| #2 Xie Y. 2023 (arXiv) | 백색잡음, GAN | B(작음) | Mel DeepShip 74.85 → 75.27 / 75.79. 분할 기재 없음 |
| #3 Xie Z. 2023 (Front. Mar. Sci.) | 1-D DCGAN 파형 생성 | B | CNN 79 → 90%. 샘플 무작위 |
| #4 Jiang 2022 (Sensors) | 개량 DCGAN(시간-주파수 이미지) | B | 86 → 92%. 이미지 무작위 |
| #5 Li J. 2022 (Entropy) | SpecAugment | C | ablation 없음 |
| #6 Mohammadi 2025 (OCEANS) | SpecAugment, mixup | C | ablation 없음 (녹음 단위) |
| #7 Hummel 2026 (Appl. Acoust.) | 저역통과, 잡음, mixup, gain, reverb, pitch, polarity (대조학습용) | B / – | 증강별 52.5–55.9%. 음성용 증강(reverb, pitch)은 성능을 낮춤. 시간순 분할 |
| #8 Xie Y. 2024 (JASA 계열) | LMR 상시 적용 | C | ablation 없음 |
| #9 Mahmud 2025 (Sci. Rep.) | mixup 계열("CutMix") | B | 90.40 → 97.53%. 클립 무작위 |
| #10 Qian 2025 (Remote Sens.) | BELLHOP 심해 채널 통과(거리·깊이 36개 위치) | B(불확실) | 95.93%. 증강 전 기준값 미확인, test도 합성 |
| #11 Li D. 2023 (Appl. Acoust.) | 수중 채널 모델링 + 랜덤 잡음 | 미확인 | 초록만 봄 |
| #12 Xu Y. 2023 (Appl. Acoust.) | 하모닉을 고려한 pitch shift, time stretch | B(분할 미확인) | DeepShip +1.67, ShipsEar +2.25 %p (초록) |
| #13 Liu F. 2021 (Appl. Acoust.) | SpecAugment | 미확인 | 검색 결과만 봄 |
| #14 Zhao 2024 (DSP) | 시간 마스킹, 속도 섭동, 잡음 | 미확인 | 검색 결과만 봄 |
| #16 Lyu 2025 (IMTS) | AS-DCGAN | 미확인 | 기준값 미확인 |
| #17 Huang 2026 (JASA) | LR-VAE 생성 | 미확인 | 초록만 봄 |
| #18 Gao W. 2026 (JASA) | 지식 기반 스펙트럼 분해 증강 | 미확인 | 초록만 봄 |
| #20 SKANN 2026 (arXiv) | 녹음 체인·주변 잡음·다중경로 섭동, tonal 보존 | C | 재식별 과제, ablation 없음 |

## 최신 SCI 후보 확인 (2026-10-10, 이 세션 웹 검색, 초록 수준)

| 논문 | 서지 (검색으로 확인) | 내용 (초록·검색 요약) | 상태 |
|---|---|---|---|
| Gao W. et al. 2026 | *JASA* 160(1):603–618, DOI 10.1121/10.0044413, PubMed 42461020 | 지식 기반 스펙트럼 분해 증강(spatial-frequency 영역에서 거친 구조는 유지하고 잡음에 민감한 세부 texture는 억제한 여러 view) + cross-feature recalibration. **few-shot** 설정. ShipsEar + 교차 도메인 DanShip. 저 SNR·교차 도메인 강건성 주장 | 초록만. 분할 unknown |
| Huang W. et al. 2026 | *JASA* 159(5):3773–3791, DOI 10.1121/10.0043727, PubMed 42065402 | LR-VAE(latent reconstruction VAE)로 클래스 내 분포를 확장하는 생성 증강. 3단계 파이프라인. **few-shot** 설정. ShipsEar | 초록만. 분할 unknown |

- 두 논문 모두 JASA 특집호 **"Generative and Physics-Informed Artificial Intelligence for Acoustics"** 소속이다(검색 결과 기준). 지도교수가 준 생성 모델 방향과 연결되는 게재처 근거다.
- 주의: 두 논문 모두 few-shot 설정이라, 전체 데이터 증강(UniqueShip 5C-Bal)과는 문제 설정이 다르다. ShipsEar는 57척 규모라 선박 단위 분할이 어렵다.
- 단서 (정정 2026-10-10): "Yu (2025)"를 인용한 것은 Huang 2026이 아니라 **Gao 2026**이다. 서지: Yu, Du, Chen, Bian (2025), "Enhancing underwater acoustic target recognition with diffusion models and AST: A few-shot learning approach", NNICE 2025 (IEEE 학회), pp. 986–990. DOI 미확인. SCI 저널 아님

## 원문 분석 반영 (2026-10-10, 에이전트가 원문 전체를 읽음)

| # | 논문 | 수정·추가된 사실 | 노트 |
|---|---|---|---|
| 1 | Xu J. 2023 LMR | 녹음 단위 분할 확인. LMR은 사실상 spectrogram CutMix(p=0.5)이고, CutMix와 비교하지 않음. DeepShip Mel에서 +0.53 pp로 가장 작고, 같은 조건에서 mixup(75.42)이 LMR(75.38)보다 높음. 단일 실행, α를 test로 선택한 의심 | `papers/notes/2023_xu_lmr_smoothness.md` |
| 18 | Gao 2026 | 2D-FFT로 스펙트로그램을 블러/잡음화(SDA). 저자도 "물리적 분해 아님"이라고 씀. "sample generation"은 생성 모델이 아님. 3 s 세그먼트 단위 분리. −15 dB에서는 SpecAugment보다 좋고, clean에서는 낮음 | `papers/notes/2026_gao_knowledge_spectral_aug.md` |
| 17 | Huang 2026 | 녹음 단위 80/20. VAE 재구성(prior 샘플링 아님), 소수 클래스만. 생성을 빼면 −4.8/−4.9 pp. 오버샘플링 대조군 없음. 생성기의 test 데이터 사용 여부 불명. 수치 불일치 다수 | `papers/notes/2026_huang_lrvae_fewshot.md` |
| 7 | Hummel 2025 | DeepShip 날짜 분할로, test의 약 40%가 기존 선박. 지도 ResNet18에서는 음성용 증강이 +4.7–9.1 pp, 비지도에서는 대부분 악화. 단일 실행 | `papers/notes/2025_hummel_contrastive_uatr.md` |
| — | Hummel 2026 linear probing | 16개 임베딩. BEATs DeepShip 65.4%. 임베딩은 선박 종류보다 녹음 ID로 군집(NMI 0.62 vs 0.13). UniqueShip은 평가하지 않음 | `papers/notes/2026_hummel_linear_probing.md` |

- 요약 (`inferred`): 원문을 읽은 5편 중 **선박 단위 분할은 0편**이다. "물리 기반"을 표방하는 Gao 2026도 실제로는 범용 증강이었다.
- 주의: Hummel 2025의 사전학습 데이터(ONC SCVIP 2019–2020)는 UniqueShip과 해역·기간이 겹칠 수 있다. 그 가중치를 쓰면 누출이 생길 수 있다.
