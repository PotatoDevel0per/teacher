# 2022_rombach_ldm — Latent Diffusion Models (Rombach et al., CVPR 2022)

- 원문: `papers/pdf/2022_rombach_ldm.pdf` (arXiv 2112.10752v2)
- 읽은 범위: §3.1–3.3, §4.1, 부록 D.1·G (Claude, 2026-10-14). 사용자는 별도로 원문을 공부했다.
- 사용 목적: EXP-003-LDM의 기반 방법. 이 연구에서는 "LDM 논문의 아이디어를 기반으로 변형"으로 표기한다.

## 원문에서 확인한 사실 (confirmed)

| 항목 | 원문 내용 | 위치 |
|---|---|---|
| 2단계 구조 | AE(E, D)를 먼저 학습하고 고정한다. 그다음 diffusion을 latent z = E(x)에서 학습한다. 샘플은 D 한 번으로 디코딩한다 | §3, §3.2 |
| AE 손실 | perceptual loss(LPIPS) + patch 기반 adversarial loss + 약한 정규화. "L1/L2 픽셀 손실만 쓰면 흐려진다" | §3.1, 식 25 |
| 정규화 | KL-reg.(가중치 약 10⁻⁶) 또는 VQ-reg.(큰 codebook). "임의로 큰 분산의 latent를 피하기 위해" | §3.1, 부록 G |
| 다운샘플 f | f = H/h ∈ {1,…,32}. f가 작으면(1, 2) 학습이 느리다. f가 크면 정보 손실로 품질 상한이 막힌다. LDM-4~16이 균형, 4·8이 최선 | §4.1 |
| latent 재스케일 | KL-reg.는 첫 배치에서 σ̂를 추정해 z ← z/σ̂로 단위 분산을 맞춘다. latent 분산이 SNR(Var(z)/σ_t²)을 바꿔 결과에 크게 영향을 준다 | 부록 G, D.1 |
| 목적함수 | ε-예측 L2: ‖ε − ε_θ(z_t, t)‖², t 균등 샘플 | 식 2 |
| 조건화 (cross-attention) | 도메인 전용 인코더 τ_θ(y) ∈ R^{M×d_τ}. Q = UNet 중간 특징, K·V = τ_θ(y). τ_θ와 ε_θ를 함께 학습한다 | §3.3, 식 3 |
| 조건화 (concat) | 공간 정렬된 조건(semantic map, 저해상도 영상)은 ε_θ 입력에 concat한다 | Fig. 3, §4.3.2 |
| guidance | 실험에 classifier-free guidance를 쓴다(ImageNet s = 1.5, text s = 10). 원문의 제안이 아니라 [32]를 인용한 것이다 | §4.3.1, 표 18 |
| 암기 확인 | 작은 데이터셋 모델은 VGG 특징 공간 최근접 이웃을 보였다 | 부록 H |

## 해석 (inferred, Claude)

- §3.2의 "high-frequency, imperceptible details are abstracted away"는 영상 기준이다. 선박 소음의 tonal은 주파수 축에서 1–2 bin 폭의 가는 선이다. 이것이 "버려지는 세부"에 해당할 위험이 있다. 그래서 AE 복원 게이트(G1)가 필요하다.
- FiLM은 이 원문에 없다. 사용하면 인접 근거를 쓰는 것이다.
- v-예측, ZTSNR 등은 원문 이후의 변형이다(D-2026-10-06-01).

## 사용자 연구와의 차이

- 입력: RGB 영상 → 로그 스펙트로그램(축 의미가 다르고, 주파수 축은 이동 불변이 아니다).
- 지각 손실: LPIPS(ImageNet VGG)는 스펙트로그램에 대한 근거가 없다.
- 데이터 규모: ImageNet 1.28M장 ↔ UniqueShip 5C-Bal train 선박 일부.
- 평가: FID(영상 임베더) ↔ tonal·DEMON 보존과 UATR 기여.
