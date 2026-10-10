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
| 2024_xie_demonet | DEMONet: multi-expert UATR + cross-temporal VAE | `/jhlee/ot-cfm/docs/DEMONet.pdf` | 부분 읽음 | DEMON, UATR, 분할 | `papers/notes/2024_xie_demonet.md` |

## 찾는 중

- DEMON에서 블레이드 수(또는 축 회전수)를 **정답 라벨과 비교해** 추정하는 논문. 사용자가 탐색 중이다 (2026-10-02).
  - 2026-10-06: Hashmi & Raza 2023을 확인했다. NOB 추출 규칙은 있지만 NOB 정확도와 공개 정답 라벨은 없다.
  - 후보로 원문을 확인할 것: Chung et al. 2011, Pollara et al. 2016 (포락선 SNR 기반 자동 대역 선택)
