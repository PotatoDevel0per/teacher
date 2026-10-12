# Experiment Registry

## 이전 실험 (2026-08 ~ 2026-09, 타당성 미검증)

사용자가 Claude Code와 함께 약식으로 진행했다. 모든 결론은 `hypothesis` 상태다. 상세는 `research/prior_experiments/`에 있다.

| ID | 폴더 | 기간 | 유형 | 핵심 결과 (문서상) | 분할 | seed | 상태 |
|---|---|---|---|---|---|---|---|
| PRIOR-DGM | `/jhlee/DGM` | 08-19 ~ 09-01 | 생성 (8 kHz 4 s dB STFT, 6 프레임워크) | 최선 OT-CFM 200k, KAD 판정선의 1.28× | split4 (선박 분리) | 1 | hypothesis |
| PRIOR-DSA | `/jhlee/deepship_analysis` | 09-04 ~ 09-09 | 데이터 분석, 보코더 왕복 | mel+HiFi-GAN 톤 피크 일치 22.6% ≈ 우연 | 해당 없음 | - | hypothesis |
| PRIOR-SLM | `/jhlee/UATR_SLM` | 09-05, 09-08 | 인식 재현 + 누수 측정 | macro-F1 S0 97.7 / S1 65.8 / S2 50.0 | S0/S1/S2 | 3 | hypothesis (가장 탄탄함) |
| PRIOR-DSP | `/jhlee/deepship_preprocessing` | 09-08 ~ 09-09 | 전처리 파이프라인, 복원 설정 결정 | n_fft 16384 + GL로 저역 피크 일치 95% | ship_disjoint | - | hypothesis |
| PRIOR-OTCFM | `/jhlee/ot-cfm` | 09-10 ~ 09-29 | 생성 (30 s 2-stream, CFM vs DDIM) | 통과 체크포인트 없음, 30k부터 모드 축소 | ship_disjoint | 1 | hypothesis |
| PRIOR-PGMCLDM | `/jhlee/PG-MCLDM` | 09-28 ~ 09-30 | 물리 조건 latent 생성 + 증강 | 증강 +0.66%p (유의성 없음), G0 재현 미통과 | DEMONet Table 10 (선박 누수 74%) | 1 | hypothesis, 중단 |
| PRIOR-SLM-R2 | `/jhlee/UATR_SLM/UATR_SLM_split_study` | 10-05 | 분할 방식별 재실험 (DeepShip + ShipsEar, 24 run) | DeepShip macro-F1 98.02 → 52.80, ShipsEar 96.40 → 71.80 | 무작위 / 녹음 / DEMONet / 선박 | 3 | hypothesis (다른 세션) |

**주의**: 분할이 폴더마다 다르므로 폴더 사이에서 수치를 비교하면 안 된다 (`research/prior_experiments/README.md` §2).

## 새 실험 (1차 목표: 물리 기반 증강, D-2026-10-06-02)

| ID | 목적 | 설정 | 판정 기준 | 상태 |
|---|---|---|---|---|
| EXP-001 | UniqueShip baseline 재현 | 5C-Bal 5 fold, SwinV2-Tiny + Mel, 20 kHz 리샘플(논문 §III-A, 배포본은 32 kHz), DC 제거, 90 dB 범위, AdamW lr 1e-6, 30 epoch. fold당 seed 1, 가능하면 3 | 정확도 평균이 0.665 ± 0.024(2 sd) 안이면 재현 | **판정: 재현됨 (2026-10-06)**. 실행: `UATR_SLM_REPLAY`. official acc 67.30 ± 2.45 (fold: 67.25/70.40/67.54/67.77/63.56), F1 65.81 (논문 65.6). naive acc 86.01 ± 0.34 (논문 82.6). 편차: 16 kHz(논문 20 kHz), batch 64(미기재), best-val 체크포인트(논문은 30 epoch 고정으로 추정). 표현: "논문 방법을 재현함(편차 3건)". 산출물: `/jhlee/UATR_SLM/uniqueship_clf/runs/uniqueship_*` |
| EXP-001b (제안) | 분류기 3종 baseline: UATR-SLM(SenseVoiceSmall 234M, 음성 사전학습), SwinV2-Tiny(27.6M, ImageNet), ResNet-18(약 11M, DEMONet 백본) | 같은 UniqueShip 5C-Bal fold. 각 모델은 원 논문의 입력 표현을 따른다(fbank-LFR / Mel 256 90 dB / CQT). ResNet-18 설정은 DEMONet §4.3을 차용하되 5 s 클립에 맞게 변형 | 모델별 5 fold 평균 ± sd. Swin만 논문 수치와 대조 가능 | 사용자 제안 (2026-10-06). 개발은 1개 모델, 최종 확인은 3개 모델로 하는 안을 권고 |
| EXP-002 | 범용 증강의 효과 (H-AUG-1) | EXP-001과 동일 + arm 하나씩: A1 CutMix(LMR 근사), A2 mixup, A3 SpecAugment, A4 일반 오디오 묶음(pitch shift / time stretch, polarity는 no-op이라 제외). 지시서: `research/experiments/EXP-002_generic_augmentation.md` | fold별 paired Δ macro-F1, 사전 등록 판정 규칙(지시서 §7) | 사용자 승인(2026-10-10), `UATR_SLM_REPLAY`에 전달 |
| EXP-003 | 물리 기반 증강 1종 (H-AUG-2/3) | 문헌 조사 후 1종 선택 | EXP-002 대비 | 미정 |

