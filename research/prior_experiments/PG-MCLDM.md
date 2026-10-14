# PG-MCLDM — 물리 조건 latent 생성 + 증강 검증 (중단 상태)

- 경로: `/jhlee/UWShipNoise/generation/PG-MCLDM` (89 GB, `.git`은 있으나 커밋 0)
- 기간: 2026-09-28 ~ 09-30 (약 2일). 사용자 요청으로 중단(pause)됐다 `[문서: CLAUDE.md]`.
- 이름: **Physics-Guided Multi-Condition Latent Diffusion Model**. 실제 생성기는 diffusion이 아니라 OT-CFM이다(DDPM-v는 ablation). **PINN은 학습됐지만 하류에 쓰이지 않았다** `[문서: docs/PROGRESS.md 09-30 정정]`.
- 전체 상태: `hypothesis`. 표기 규칙은 [README.md](README.md) §0.

## 1. 문제 정의

DeepShip 30 s WAV를 물리 조건(축 주파수, 날개 수, DEMON, 토널, 캐비테이션, 속도·거리·레벨)으로 조건부 생성한다. 수신음은 음원 S × 채널 H로 분해한다. 생성 데이터로 분류기를 증강해 H3(UATR 기여)도 검증하려 했다.

## 2. 데이터

- `/jhlee/UWShipNoise/data/deepship`, 16 kHz, 10 Hz HPF (`cache/audio16k` 11 GB)
- **분할: DEMONet(arXiv 2411.02758) Table 10 recording-disjoint**. test ID는 하드코딩돼 있다 `[확인]` (`scripts/make_deepship_table10_split.py`).
  - 녹음 수 train 387 / val 69 / test 153. 세그먼트는 30 s 창·15 s hop으로 6,785 / 1,213 / 2,575
  - **test 녹음의 73.9%, val의 62%가 train과 같은 선박** `[확인]`. 문서는 "미관측 선박 일반화가 아님"이라고 명시했다.
- 생성 표현: 2-stream STFT(deepship_preprocessing 방식), GL 128 + 공동 32, random 초기화
- 분류기 입력: 근사 CQT(STFT에 constant-Q 삼각 커널) 290×1190
- CPA 거리 궤적은 `/jhlee/UWShipNoise/data_analysis/deepship_preprocessing/.../conditions.parquet`에서 가져왔다.

## 3. 방법 파이프라인 `[확인]`

1. CT-VAE(DEMONet §3.2 변형)로 DEMON 정제 → 축 주파수·날개 수 추정
2. 자체 정규모드 solver로 15개 환경 TL 계산 → `down_mudA15` 선택. 관측 감쇠가 모델보다 1.7–3.5배 가팔라 경험 보정 k(f) = 1.7–2.4를 적용했다 → "물리 채널"보다 경험적 TL 보정에 가깝다 `[추론]`.
3. 채널 보상된 음원 공간에서 2-stream AE 학습(8k step에서 G2 통과 즉시 고정)
4. latent 조건부 UNet(27.5M, cross-attention) + OT-CFM(미니배치 OT, Hungarian). 50k step, CFG 4, **seed 0 하나**
5. 샘플링: latent → AE → S × incoherent H → GL
- Phase 3 물리 손실(L_inv, L_DEMON, L_tonal) → **기각**
- P4 AM 계층: 재학습 없이 축 주파수로 AM 포락선을 곱하는 후처리
- 원안 명세서(mel-VAE LDM + HiFi-GAN + Helmholtz 잔차)에서 7개 항목이 바뀌었다 → **"논문 아이디어를 기반으로 변형"**

## 4. 결과 (`docs/RESULTS.md`, `runs/**/metrics.json`)

**G0 분류기 재현: 미통과.** last epoch 72.23%(3 seed: 72.47 / 72.39 / 71.84), 논문은 77.15%다. 원인은 미해결이다.

생성 (test 900개, CFG 4):

| 모델 | FAD | KAD×100 | tonal F1 |
|---|---|---|---|
| E0 실데이터 train vs test | 2.23 | 0.25 | 0.658 |
| E1 class-only | 34.6 | 31.7 | 0.117 |
| E2 `pg_otcfm` 50k | 29.3 | 22.9 [21.3, 25.2] | 0.215 |
| E3 +10k, 물리 없음 | 33.2 | 28.0 | 0.200 |
| E4 Phase 3 | 99.0 | 44.2 | 0.117 |
| E5 E3 + AM 계층 | 30.5 | 25.4 | 0.200 |
| E6 DDPM-v | 28.9 | 21.1 [19.7, 23.3] | 0.207 |

- 생성물의 DEMON 신뢰 비율은 0.007–0.018로, 변조를 만들지 못한다.

증강 H3 (전부 seed 123, 1회):

| 조건 | 정확도 |
|---|---|
| TRTR | 72.47% |
| SpecAugment + mixup | 72.78% |
| E3 증강 | 72.54% |
| E4 증강 | 70.87% |
| E5 증강 | 73.13% |

- 문서 결론은 "판정 보류"다. E5의 +0.66%p는 seed 간 범위(0.63%p) 수준이라 유의하지 않다 `[추론]`.
- 학습했지만 평가하지 않은 것: A1b, B2, A4 ×3. OOM으로 실패한 것: A3, P4 spatial ×2.

## 5. 문제·의심점

1. **선박 누수 분할**: 증강 이득이 선박 암기일 수 있다(문서 인정). KAD 판정선 0.25도 이 때문에 인위적으로 낮다.
2. seed 1개. E2 vs E6은 CI가 겹치고, 같은 모델을 10k step 더 학습하면 22.9 → 28.0으로 나빠진다 → 체크포인트 간 변동이 모델 간 차이보다 크다.
3. 코드 버전 혼재: E2/E6은 구 코드(무조건부 분기가 거의 학습 안 됨)로 학습했는데, CFG 4는 새 코드에서 선택했다. CFG sweep이 단조 감소라 탐색 경계에서 선택된 셈이다.
4. 증강하면 n_train이 6,785 → 8,785로 늘어 총 학습량이 달라진다. 실데이터 증가 대조군이 없다.
5. 계획 불이행: 짧은 세그먼트 제외 미적용. Phase 3는 val이 아니라 test로 판정했다. G0 기준을 best-val에서 last epoch로 사후 변경했다.
6. G1/G2 게이트에 맞춘 선택 편향. G1 cosine과 G2 DEMON cosine은 붕괴를 구별하지 못한다.
7. IS/KL/Acc: E1 Acc 97.0% > 실데이터 74.9%. 클래스 원형을 과장하는 생성물이 높게 나오는 구조다.

## 6. 재사용 가치

- 분류기: `pg_mcldm/classifier/train.py` (CQT/STFT/Mel + ResNet-18, TRTR/TSTR/few-shot/SpecAugment/mixup). baseline 72.2 ± 0.3%(Table 10, last epoch)
- 분할: `splits/deepship_table10.json` (ship_id.csv와 결합하면 ship-disjoint 부분집합 test 40 녹음을 만들 수 있다)
- DEMON / CT-VAE: `pg_mcldm/features/{demon,shaft}.py`, `models/ctvae.py`. 교훈: β = 1은 붕괴하고, cosine으로는 붕괴를 판별할 수 없다.
- 정규모드 solver `pg_mcldm/physics/modes.py`, 평가 `pipelines/p50_eval.py`(녹음 bootstrap KAD), `p52_tonal_metrics.py`(tonal P/R/F1)
- 사전등록 형식 예시: `configs/verdict.yaml`
- GL 복원 바닥값: FAD 2.79 / KAD 1.12 (`runs/gl_ref/metrics.json`)
- 캐시: cache 47 GB, runs 43 GB

## 7. 연구 범위 관점 (`inferred`)

CLAUDE.md §11이 "한 번에 모두 구현하지 말라"고 한 요소(latent 생성, flow matching, 물리 기반 합성, 복잡한 조건부 생성, 다중 평가 지표)를 2일 안에 동시에 도입했다. 그 결과 어떤 요소가 결과에 기여했는지 분리할 수 없다. 기초부터 다시 할 때는 이 폴더를 **요소별 아이디어 목록**으로만 쓰는 것이 적절하다.
