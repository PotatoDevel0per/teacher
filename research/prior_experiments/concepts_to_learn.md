# 이전 실험을 남에게 설명하려면 필요한 개념

- 작성일: 2026-09-30
- **이 목록은 사용자의 이해 수준을 나타내지 않는다.** 이전 실험에 이 개념들이 쓰였다는 사실만으로 사용자가 이해했다고 판단하지 않는다(사용자 요청). 실제 수준은 개념별로 확인한 뒤 `profile/learning_status.md`에 기록한다.
- 우선순위: 기초부터 다시 할 때의 학습 순서 제안이다(`inferred`). CLAUDE.md §11 최소 파이프라인 순서를 따랐다.

## P1. UATR baseline과 평가 설계 (최소 파이프라인 1단계)

| 개념 | 쓰인 폴더 |
|---|---|
| 데이터 누수 3계층 (클립·세그먼트 / 녹음 / 선박) | 전체 |
| group-disjoint 분할, 층화, 소수 선박 문제 | UATR_SLM, preprocessing, DGM |
| shortcut learning (녹음 환경·센서·레벨 지름길) | UATR_SLM, DGM |
| 실효 표본 수와 CI (세그먼트 CI vs 선박 CI), bootstrap | analysis, ot-cfm, PG-MCLDM |
| seed 분산, 유의성, 다중 비교 보정(Holm) | 전체 |
| 사전 등록(preregistration)과 사후 기준 변경의 문제 | 전체 |
| macro vs weighted F1, 클립 vs 녹음 단위 평가 | UATR_SLM, PG-MCLDM |
| early stopping과 val 기반 모델 선택의 잡음 | UATR_SLM, PG-MCLDM |
| log-Mel fbank, CMVN, LFR, CQT | UATR_SLM, PG-MCLDM |
| 사전학습 모델 전이(SenseVoice, full fine-tuning, mean pooling) | UATR_SLM |

## P2. 선박 소음 신호처리 (최소 파이프라인 3–4단계의 전제)

| 개념 | 쓰인 폴더 |
|---|---|
| DC 오프셋, 고역통과, FIR/IIR(sos), 데시메이션과 에일리어싱 | analysis, preprocessing |
| STFT 해상도 트레이드오프 (Δf = fs/n_fft, 창 길이), 주기도 평균과 dB 분산 | analysis, preprocessing, ot-cfm |
| 협대역 토널과 광대역, 하모닉(콤) 구조, 블레이드율 | analysis, UATR_SLM, ot-cfm |
| LOFAR, TPSW 배경 추정, CFAR와 오경보율 | analysis, preprocessing, UATR_SLM |
| DEMON (포락선 복조, 축 회전수, 날개 수), 캐비테이션 | DGM, ot-cfm, PG-MCLDM |
| CPA, AIS 거리, 전파손실(구면·원통 확산, 흡수), Lloyd mirror | analysis, preprocessing, PG-MCLDM |
| 정규모드, TL (coherent vs incoherent), PINN | PG-MCLDM |

## P3. WAV 복원 (최소 파이프라인 3단계)

| 개념 | 쓰인 폴더 |
|---|---|
| 위상 복원: Griffin-Lim, SPSI | DGM, analysis, preprocessing, ot-cfm |
| mel 스케일의 저역 해상도 한계 | analysis |
| 신경 보코더 (HiFi-GAN)와 fine-tuning | analysis |
| 2-stream(저역·고역 분리) 표현과 접합 | preprocessing, ot-cfm, PG-MCLDM |
| LSD의 한계, peak-N 일치율, 우연 바닥과 skill score | analysis, preprocessing |

## P4. 생성 모델 (지금 당장은 필요 없음)

| 개념 | 쓰인 폴더 |
|---|---|
| Flow matching / CFM, 선형 경로, 독립 커플링 vs 미니배치 OT | DGM, ot-cfm, PG-MCLDM |
| SB-CFM, ReFlow | DGM |
| DDPM/DDIM, ε/v-예측, x̂₀ clamp, zero-terminal-SNR, VE-SDE | DGM, ot-cfm, PG-MCLDM |
| CFG, 무조건부 dropout, EMA, NFE와 ODE 적분기 | DGM, ot-cfm, PG-MCLDM |
| VAE, KL 붕괴, latent 생성과 AE 병목 | PG-MCLDM |
| 기억(memorization) vs 모드 축소 | ot-cfm |

## P5. 생성 평가 (최소 파이프라인 4–5단계)

| 개념 | 쓰인 폴더 |
|---|---|
| FAD, KAD(MMD, median heuristic), FAD가 실패하는 조건 | DGM, ot-cfm, PG-MCLDM |
| 임베더 의존성 (PANNs의 저주파 맹점, 레벨 민감성) | ot-cfm, DGM |
| real↔real 귀무 기준선 | DGM, ot-cfm |
| Density/Coverage (PRDC), IS, KL | DGM, ot-cfm, PG-MCLDM |
| TRTR / TSTR / 증강 평가와 그 교란(학습량 차이) | DGM, PG-MCLDM |
