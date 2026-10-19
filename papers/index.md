# Papers Index

| Paper ID | 제목 (요약) | 원문 | 상태 | 관련 주제 | 노트 |
|---|---|---|---|---|---|
| 2023_xu_lmr_smoothness | LMR(사실상 spectrogram CutMix) + smoothness 정규화 | `papers/pdf/2023_xu_lmr_smoothness.pdf` | 전체 읽음(에이전트) | 범용 증강, 녹음 단위 분할 | `papers/notes/2023_xu_lmr_smoothness.md` |
| 2026_gao_knowledge_spectral_aug | 2D-FFT 스펙트럼 분해 증강(SDA), few-shot. 물리 기반 아님 | `papers/pdf/2026_gao_knowledge_spectral_aug.pdf` | 전체 읽음(에이전트) | 범용 증강, few-shot | `papers/notes/2026_gao_knowledge_spectral_aug.md` |
| 2026_huang_lrvae_fewshot | LR-VAE 재구성 기반 생성 증강, few-shot | `papers/pdf/2026_huang_lrvae_fewshot.pdf` | 전체 읽음(에이전트) | 생성 증강, 녹음 단위 분할 | `papers/notes/2026_huang_lrvae_fewshot.md` |
| 2025_hummel_contrastive_uatr | 대조학습 임베딩, 증강 종류별 비교 | `papers/pdf/2025_hummel_contrastive_uatr.pdf` | 전체 읽음(에이전트) | 증강 비교, 날짜 분할 | `papers/notes/2025_hummel_contrastive_uatr.md` |
| 2026_hummel_linear_probing | 사전학습 오디오 임베딩 16종 + linear probe | `papers/pdf/2026_hummel_linear_probing.pdf` | 전체 읽음(에이전트) | baseline, 녹음 ID 군집 | `papers/notes/2026_hummel_linear_probing.md` |
| 2026_hashemi_uniqueship | UniqueShip: 누출 없는 UATR 벤치마크 (4,218척) | `papers/pdf/2026_hashemi_uniqueship.pdf` | 전체 읽음 | 누출, 벤치마크, baseline | `papers/notes/2026_hashemi_uniqueship.md` |
| 2023_hashmi_demon_classification | DEMON 분석으로 SRPM·NOB·NOS 추출, 규칙 기반 9범주 분류 | `papers/pdf/2023_hashmi_demon_classification.pdf` | 전체 읽음 | DEMON, 블레이드 수, band-pass | `papers/notes/2023_hashmi_demon_classification.md` |
| 2024_gao_uas_denoising_survey | 수중음향 잡음 제거 서베이 (분해·DL) | `papers/pdf/2024_gao_uas_denoising_survey.pdf` | 전체 읽음 | 잡음 제거, EWT, VMD | `papers/notes/2024_gao_uas_denoising_survey.md` |
| 2026_wang_noise_robust_demon | EEMD 적응 대역 선택 + 3차 누적량 + SBL로 잡음에 강한 DEMON 스펙트럼 추출 | `papers/pdf/2026_wang_noise_robust_demon.pdf` | 전체 읽음 (2026-10-12 조건부 확정, 출력은 스펙트럼뿐·f_s/N 추정 없음) | DEMON, 대역 자동 선택, 축 주파수 | `papers/notes/2026_wang_noise_robust_demon.md` |
| 2024_cho_lofar_hough_cnn | Hough 수평선 검출 + CNN 분류 (한국음향학회지 43(1)) | `papers/pdf/2024_cho_lofar_hough_cnn.pdf` | 핵심 절 원문 대조 | LOFAR, tonal, Hough | `papers/notes/2024_cho_lofar_hough_cnn.md` |
| 2020_han_deeplofargram | DeepLofargram: 약하고 흔들리는 tonal 선을 LOFARgram에서 검출·복원 (JASA 148(4)) | 미확보 (arXiv 1912.00605) | 서지만 (LOFAR 연구 잠정 선정 2026-10-12) | LOFAR, tonal 검출 | — |
| 2024_xie_demonet | DEMONet: multi-expert UATR + cross-temporal VAE | `/jhlee/UWShipNoise/generation/ot-cfm/docs/DEMONet.pdf` | 부분 읽음 | DEMON, UATR, 분할 | `papers/notes/2024_xie_demonet.md` |
| 2022_rombach_ldm | LDM: AE 고정 후 latent에서 diffusion, cross-attention 조건화 (CVPR 2022) | `papers/pdf/2022_rombach_ldm.pdf` | 핵심 절 원문 대조 (§3, §4.1, 부록 D.1·G) | 생성, LDM, EXP-003 | `papers/notes/2022_rombach_ldm.md` |

## 찾는 중

- DEMON에서 블레이드 수(또는 축 회전수)를 **정답 라벨과 비교해** 추정하는 논문. 사용자가 탐색 중이다 (2026-10-02).
  - 2026-10-06: Hashmi & Raza 2023을 확인했다. NOB 추출 규칙은 있지만 NOB 정확도와 공개 정답 라벨은 없다.
  - 후보로 원문을 확인할 것: Chung et al. 2011, Pollara et al. 2016 (포락선 SNR 기반 자동 대역 선택)
  - 2026-10-12 SCI 후보 검색 (Crossref 초록 기준):
    - Wang 2026 JMSE (10.3390/jmse14161459): **조건부 확정** (2026-10-12 원문 확인)
    - Yu 2026 JASA-EL (10.1121/10.0044208): block-sparse harmonic dictionary, SWellEx-96 공개 데이터 → 예비
    - Li 2022 JMSE (10.3390/jmse10101565): CRNN F0 추정, 학습 기반
    - Zhou 2024 Appl. Acoust. (10.1016/j.apacoust.2024.110211): 사전정보 없는 약한 변조선 검출, 초록 없음
    - Zhu 2022 JMSE (10.3390/jmse10030328): CPP 선박 1척, 피치별 특성. 정답이 있는 실측 사례

- LOFAR 특징 추출 SCI 후보 (2026-10-12 검색, Crossref 기준)
  - Han 2020 JASA DeepLofargram (10.1121/10.0002172): **잠정 선정**
  - Xiao 2026 JASA Multiple DeepLofargram (10.1121/10.0046669, 160(3):2608–2626): 약지도 다중 선 → 예비
  - Shi 2024 JASA (10.1121/10.0034356): HMM 선 추적. 주파수-방위-시간 공간이 필요해 배열 전제 → 제외
  - Appl. Sci. 2025 (10.3390/app15136952): 해군 비공개 데이터 분류 → 제외
  - Cho & Ha 2024 한국음향학회지 (10.7776/ASK.2024.43.1.019): Hough 수평선 검출 + CNN 분류. 특징 추출을 정량 평가하지 않고, 분할에 누수가 의심된다 → 주 논문 부적합. 비학습 보조 기준선 후보 (사용자 제안 2026-10-12)
