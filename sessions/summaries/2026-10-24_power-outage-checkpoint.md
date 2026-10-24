# 세션 요약: 정전 전 진행 상황 기록 (2026-10-24)

- 기간: 2026-10-19 ~ 2026-10-24 (Teacher 세션, 실행 세션 CLS·GEN·DEN)
- 작성 이유: 정전 예정. 재개할 때 이 문서와 `handoffs/current_context.md`부터 읽는다.

## 1. 방향 결정 (이 기간)

| 결정 | 내용 |
|---|---|
| D-2026-10-19-01 | 학위논문. 지도교수 1순위는 생성 모델. 주 방법 = **증강용 생성 모델**(조건부 LDM). 판정은 Ships-disjoint UATR. WAV는 후순위 |
| D-2026-10-19-02 | 주 데이터 **DeepShip·ShipsEar**(선박 단위 5-fold 새로 고정). UniqueShip은 보조(코드 회귀 확인, 최종 보조 일반화, 잡음 재료) |
| D-2026-10-20-01 | DEMON 평가기는 **CPW 백색화(W)로 통일**. DeepShip 사용, ShipsEar 보류(사후 결정) |
| D-2026-10-21-01 | E1-AE 대상 도메인 MEL + STFT + CQT(CQT는 생성물 tonal 평가 가능성 때문에 추가) |
| 우선순위(10-21) | FocuS-MN 재현을 E1-AE보다 먼저 → 재현 후 E1-AE 재개 |
| 원칙(10-22) | **잡음 제거기도 분류기의 test 선박을 보면 안 된다**(누출 없는 일관성) |
| 용어(10-20) | tonal / window / narrow·broad / **beating** / **Rec-disjoint**(녹음 단위) · **Ships-disjoint**(선박 단위) |

## 2. 끝난 실험과 결론

| 실험 | 결론 | 상태 |
|---|---|---|
| 단계 A 회귀 | 공유 코드(core)가 EXP-002 A0와 비트 단위 일치. UniqueShip acc 68.40 ± 2.46 | confirmed |
| 분할 | DeepShip 33,644 클립·244 선박, ShipsEar 2,223 클립·57척 Ships-disjoint 5-fold, 공유 선박·녹음 0(Teacher 독립 검증) | confirmed |
| E1-rep | 상위 2개 = MEL + STFT(tie 규칙). MEL보다 나은 도메인 없음. DeepShip MEL F1 58.18(UniqueShip 원문 0.563과 일치) | 판정 완료 |
| E0-G0 v1·v2 | tonal 평가기 AUC 0.998 / 0.937 사용. DEMON: beating 문제 → CPW로 DeepShip 0.762. 하모닉 검출은 5 s에서 검출력 없음 | 판정 완료 |
| E1-src (MEL) | D = +3.20 pp, CI [−1.54, +7.84] → 보류. B(broadband만) 53.16 ≈ O_rp 52.20 > T 41.87 | 보류 |
| E1-src-CQT | ΔT +0.34 → 보류. B − T 격차가 MEL·CQT에서 같음(11 pp) → H-SC-3이 MEL에만 한정되지 않음 | 보류 |
| FocuS-MN R2 (ShipsEar 재현) | 시도 2b(단계 잔차 + 2단계 결합 손실)로 **SDRi 8.68 dB**(원문 8.61). 편차 27건을 둔 재현 | 통과 |
| R2b (ShipsEar 모델 → DeepShip 혼합) | SDRi 5.86 → 미달. 실녹음 에너지 87% 제거, 2–8 kHz −16…−19 dB | 미달 |
| R3-DS (ShipsEar 모델을 DeepShip 분류 앞단에) | **해로움**: F1 58.18 → 53.35(−4.83, 4/5 fold). fold1 +7.24는 두 척이 만든 예외 | 판정 완료 |
| R2c 원인 진단 | **결합형 L2가 원인**(약 7k step 뒤 가중치 51.5 → 4.5, train 손실 상승). AdamW는 정상 | 판정 완료 |
| R-US (UniqueShip 잡음 제거기) | DC 제거(원본 클립 대부분이 DC) 후 학습. **SDRi 8.46 dB → 쓸 만함.** tonal 보존(15.46 → 15.44), 선박 79%·배경 88% 에너지 제거 | 판정 완료 |

방법론 교훈: fold 하나 예비 결과는 방향까지 틀릴 수 있다(R3-DS fold1). L1만 쓴 AE는 주파수 방향 질감을 뭉개고 SwinV2가 그 질감에 민감하다(흐림 진단).

## 3. 진행 중이던 실험 (정전 시 중단될 수 있음)

| 실험 | 세션 | 상태 | 재개 방법 |
|---|---|---|---|
| **E1-AE** (AE 30개, L1만) | GEN | 19/30 완료(fold1–3). fold4·5 남음(11개, GPU 2장 약 19 h). 정전 전 STOP 요청 | GEN REPORT 맨 위의 재개 절차. 중단된 AE는 처음부터 |

E1-AE 3 fold 중간 관찰(F1 비율, 기준 0.95): DeepShip MEL 0.946(경계), STFT 0.556, CQT 0.804(tonal 보존 0.97). ShipsEar는 세 도메인 모두 0.98–1.02.

## 4. 사용자 결정 대기

1. **E1-AE 진행 방식:** Teacher 추천 B(30개 완주 + GEN이 patch adversarial 손실 버전을 CPU로 준비)
2. **R-US 잡음 제거기 다음 단계:** A(UniqueShip 분류에 적용) / B(DeepShip 적용, UniqueShip–DeepShip 선박 중복 확인 먼저) / C(마무리)
3. E1-src 캐시(26.6 GB) 삭제 여부
4. 세미나 슬라이드 제작(발표 시간·형식)

## 5. 위치

- 실험 저장소: `/jhlee/UWShipNoise/thesis`(CLS·GEN), `/jhlee/UWShipNoise/denoising/FocuS-MN`(DEN). 둘 다 로컬 git, 원격 없음
- 지시서: `handoffs/2026-10-19_*` ~ `2026-10-23_*`
- 기록: `research/experiment_registry.md`, `research/decisions.md`, `research/hypotheses.md`(H-SC-1~4, H-PRE-4, H-LDM-5), `research/datasets/uniqueship.md`
- 논문 노트: `papers/notes/2022_rombach_ldm.md`, `papers/notes/2026_gu_focusmn_denoising.md`
- 세미나 발표안: `research/seminar_outline_draft.md`
- 결과 페이지(비공개): G0 https://claude.ai/artifact/XoXtUnAFsWJ8Rtg8hyL8xo · E1 https://claude.ai/artifact/7FJkFiNfVqHU2514khW7c7 · 잡음 제거 비교 https://claude.ai/artifact/DmbucTLGuF5wDeJBhnydnb
