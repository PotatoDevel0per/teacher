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
| EXP-002 | 범용 증강의 효과 (H-AUG-1) | EXP-001과 동일 + arm 하나씩: A1 CutMix(LMR 근사), A2 mixup, A3 SpecAugment, A4 일반 오디오 묶음(pitch shift / time stretch, polarity는 no-op이라 제외). 지시서: `research/experiments/EXP-002_generic_augmentation.md` | fold별 paired Δ macro-F1, 사전 등록 판정 규칙(지시서 §7) | 사용자 승인(2026-10-10). sanity check에서 헤드 초기화 비시드를 발견해 ②를 채택했다(2026-10-12): 시드를 모델 생성 전으로 옮기고 A0 5 fold를 재실행한다. A1은 원문 LMR로 바꾼다. EXP-002-PC(a) 이후 재개한다 **보류 유지(2026-10-14).** 재개 시 EXP-003-LDM 단계 5의 A-gen arm으로 재검토한다. |
| EXP-002-PC (제안) | 양성 대조군: 증강 구현이 논문의 이득을 재현하는지, 그리고 이득이 분할 단위에 따라 달라지는지 | (a) 논문 재현: Xu J. 2023 LMR. DeepShip 녹음 단위 분할(원문 Table 9), ResNet-18+MHA, STFT. 논문값 baseline 74.68 → LMR 78.40 (+3.72, 단일 실행). seed 3개. Mel은 +0.53으로 run 잡음(~1 pp)보다 작아 재현 대상에서 제외한다. (b) 같은 데이터 대조: UniqueShip naive 분할 vs MMSI 분할, SwinV2 Mel, A0 vs A1 | (a) LMR Δ > 0이 seed 3개 모두에서 나오고 평균 Δ ≥ 2 pp면 구현 재현으로 본다(사전 등록 예정). (b) split × augmentation 상호작용 | (a) **판정: 재현됨 (2026-10-12)**. Δ +2.34 ± 1.97 pp (+2.91/+3.97/+0.16, 원문 +3.72). 기준을 근소하게 넘었다. last epoch 기준으로는 −7.1로 뒤집히고, Passenger는 −4.79. 상세는 지시서 기록. 지시서: `research/experiments/EXP-002-PC_lmr_positive_control.md`. 단계 2(baseline 70% 재현): D2(segment 단위 val, 원문 segment 수와 일치) 채택. 3 seed: last 68.00 ± 3.37(사전 등록 기준 70% 미달), best-val 70.37 ± 0.75(보조). D4(dB + 샘플별 정규화) −1.65로 미채택. D 시리즈 중단(단계 비교가 test 선택이 되는 문제를 Teacher가 정정). 사용자 (B) 선택: D6 블록 val(겹침 0): best-val 67.92 ± 0.30, 미달. epoch 최고도 69.81. **baseline 절대값 재현하지 못함.** 다음 경로 사용자 결정 대기. (b) 미승인 **종료(2026-10-14, 사용자 결정).** 결론: LMR 증강 이득 Δ는 재현, baseline 절대값 70%는 재현하지 못함. 추가 run 없음. |
| EXP-DEMON-001 | DEMON 대역 자동 선택(H-PRE-3) 검증. Wang 2026 JMSE 일부 모듈 재현 | 합성 신호(원문 모델: f_s 8 Hz, B 5, 20 s). 비교: 고정 BP 2개 / EEMD-ENV / EEMD-TCDS-FFT / SBL 계열 / WANG 전체 / ORACLE(200–1000 Hz). 판독: HPS(K=5)+LS. 실행: `DEMON` 세션, `/jhlee/DEMON/results/` | 정답 기반 지표(f_s 정답률 ±0.1 Hz, 하모닉 비율). 사전 등록은 노트에 있음 | 2a 완료(2026-10-12): 잡음 없음 → 천장 효과(BP 없이도 100%). TCDS +5.7/+8.6 pp 개선, SBL은 정답 지표 악화(SHLSNR만 부풀림). 원문 경향 2/3 일치. **2b-1: H-PRE-3 불지지(합성 모델 한정)**. 사후 추가 BP-MID(100–2000 Hz)가 −15 dB에서 EEMD보다 +35 pp. SBL은 잡음 조건에서도 악화. 다음: 실패 분석 → SNR 보강(사후), 2b-2 보류. 노트: `papers/notes/2026_wang_noise_robust_demon.md` **종료(2026-10-14, 사용자 결정).** 합성 단계에서 마무리. 2b-2·실데이터 단계는 하지 않는다. 결론: 원문 EEMD 선택은 잡음에 취약하고, 분산 정규화로 고정 저역 수준까지 회복(아이디어 기반 변형). LDM 조건은 고정 대역 DEMON으로 시작. |
| EXP-LOFAR-001 | Cho & Ha 2024(Hough + CNN, LOFARgram) 재현 → 누수 없는 분할에서 HT 이득 유지 여부 | R1 원문 분할(이미지 7:3 무작위) / R2a 녹음 단위 / R2b 선박 단위. DeepShip 4클래스 + ShipsEar Passenger, 3-layer CNN·ResNet18·DenseNet121 × 원본/HT × seed 3. 실행: `LOFAR` 세션 | R1: ResNet18 원본 81.85 ± 5 pp, HT 이득 ≥ +2 pp(2/3 seed 이상 양수). R2b에서 같은 기준으로 "유지" 여부 판정 | 사용자 결정(2026-10-12). **R1: 부분 재현.** CNN3 HT 이득 +5.22(3/3), DenseNet121 +2.37(2/3), ResNet18 −4.98(1/3, 마지막 epoch 불안정). **R2b(선박 분할): CNN3 이득 +5.18(3/3) '유지', ResNet18·DenseNet121 '유지되지 않음'.** 선박 분할에서 절대 정확도는 25–30 pp 하락. R2c(DEMONet 분할): CNN3 +7.15(3/3) PASS, 사전학습 둘은 FAIL. 원본 정확도 하락(R1→R2c→R2b): CNN3 70→45→44, ResNet18 80→66→54, DenseNet121 74→63→52. 결합 분류기는 결론 보류. seed 8개(사후): R2b CNN3 이득 +2.53 ± 3.05(6/8)로 축소, 사전학습 모델은 부호 판단 불가. **종료(2026-10-13).** CNN3 seed 8개 이득: R1 +4.67(8/8), R2c +7.52(8/8), R2a +4.40(7/8), R2b +2.53(6/8). LDM 조건 지침: LOFARgram은 조건부로 사용 가능, Hough 선 목록은 사용 불가. 지시: `handoffs/2026-10-12_to_LOFAR.md` |
| EXP-003 | 물리 기반 증강 1종 (H-AUG-2/3) | 문헌 조사 후 1종 선택 | EXP-002 대비 | 미정 |
| EXP-003-LDM (초안) | 조건부 LDM 증강 (D-2026-10-13-02, H-LDM-2, H-AUG-2) | 단계 0 특징·독립 평가기 → 1 AE 복원 게이트 → 2 무조건 LDM → 3 조건부(c_LOFAR, c_DEMON 하나씩) → 4 조건 조작 → 5 UATR 선박 분리 판정(A0/A-gen/A-phys/A-ldm-real/A-ldm-manip) | 단계별 게이트. 임계값은 실행 전 사전 등록 | **초안, 미승인.** 사용자 결정 D1–D5 대기. 문서: `research/experiments/EXP-003-LDM_conditional_aug_design.md` |

