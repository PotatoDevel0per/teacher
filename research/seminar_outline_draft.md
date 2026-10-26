# 세미나 발표안 v3 — 진행한 실험 중심 (2026-10-26)

- 사용자 방향(2026-10-26): 논문 형식이 아니라 "지금까지 진행한 실험"을 순서대로 보여 준다.
  - 순서: ① 분류 SOTA의 분할 누출 → ② 증강 논문 재현과 분할 → ③ 분류기가 학습한 특징 → ④ 물리 평가기 → ⑤ 잡음 제거
- 가정: 25–30분 + 질의, 슬라이드 약 18장.
- 표시:
  - [Teacher 검증]: 이 KB에서 판정 규칙과 함께 확인한 실험
  - [이전 세션]: 다른 세션 실험, Teacher가 재검증하지 않음. 슬라이드에 작게 표시한다.
- 용어: tonal, broadband, window, beating, Rec-disjoint, Ships-disjoint
- 이전 판(v2, 논문 서론형): `research/seminar_outline_v2_paperflow.md`

---

## 0. 도입 (2장, 2분)

### S1. 제목
- 수중 선박 소음 생성·인식 연구 진행 보고 — 분할 누출, 학습 특징, 물리 평가, 잡음 제거

### S2. 연구 출발점과 방향 전환
- 원래 목표: WAV로 복원 가능한 선박 소음 생성 모델 → UATR 데이터 부족 완화
- 연구 중 발견: 분류 정확도가 분할 방식에 따라 크게 바뀐다. 생성물을 평가할 분류기 자체가 선박 개체를 외우고 있었다.
- 그래서 순서를 바꿨다:
  1. 분할과 분류기 점검
  2. 물리 평가기
  3. 입력 전처리 점검
  4. LDM 물리 기반 증강
  5. WAV 복원
- 오늘 발표: 이 순서로 진행한 실험 5묶음

---

## 1부. 기존 UATR 분류 연구의 분할 누출 (3장, 5분)

### S3. UATR-SLM(ICASSP 2026) 재현: 분할만 바꾸기 [이전 세션, 결과 그대로 사용(사용자 결정 2026-10-26)]
- 실험: 분류기는 UATR-SLM 하나로 고정하고 분할 방식만 바꿈. 2 데이터셋 × 4 분할 × seed 3 = 24 run
- 표(macro-F1, 평균 ± sd):

| 분할 | DeepShip | ShipsEar |
|---|---|---|
| 논문 보고치(분할 단위 미기재) | 99.32 | 99.00 |
| 무작위(클립) | 98.02 ± 0.07 | 96.40 ± 1.87 |
| 녹음 분리 | 65.06 ± 4.26 | 73.12 ± 13.06 |
| 선박 분리 | **52.80 ± 6.04** | **71.80 ± 6.79** |

- 핵심 메시지: **SOTA 99%는 클립 무작위 분할의 수치다. 선박을 나누면 DeepShip은 45 pp 떨어진다.**
- 하락 분해(DeepShip):
  - 무작위 → 녹음 분리 −33.0 pp(녹음·채널 서명)
  - 녹음 분리 → 선박 분리 −12.3 pp(선박 개체 서명)
- ShipsEar는 녹음 수와 선박 수가 거의 같아 녹음 분리와 선박 분리의 차이가 작다(공유 6척). sd가 커서 둘을 구분할 수 없다.
- 그림: t-SNE(`UATR_SLM_split_study/03_tsne/tsne_deepship_seed0.png`). 분할이 엄격해질수록 군집이 깨진다. 보조 그림이고, 정량값은 표를 본다.
- 한계: 무작위 분할 재현치가 논문보다 1.3–2.6 pp 낮다(원인 미특정)
- 출처: `/jhlee/UWShipNoise/recognition/UATR_SLM/UATR_SLM_split_study/README.md`

### S4. UniqueShip 기준선 재현: 누출 vs 선박(MMSI) 분할 (EXP-001) [Teacher 검증]
- 실험: UniqueShip 5C-Bal, SwinV2-Tiny + Mel, 5 fold
- 결과(acc):

| 분할 | 우리 재현 | 원문 |
|---|---|---|
| naive(누출) | 86.01 ± 0.34 | 82.6 |
| official(MMSI 분리) | **67.30 ± 2.45** | 66.5 ± 1.2 |

- 판정: 재현됨. 편차 3건(16 kHz, batch 64, best-val ckpt)
- 핵심 메시지: **대규모(4,218척) 데이터에서도 선박을 나누면 19 pp 떨어진다.**

### S5. 우리 프로토콜: DeepShip·ShipsEar Ships-disjoint 5-fold [Teacher 검증]
- 분할: DeepShip 33,644 클립 / 244 그룹, ShipsEar 2,223 클립 / 57척. 공유 선박 0, 공유 녹음 0
- DeepShip MEL(SwinV2): acc 59.25 / F1 58.18 ↔ UniqueShip 원문이 보고한 DeepShip 선박 분할 0.588 / 0.563
- 코드 회귀: UniqueShip acc 68.40 ± 2.46, 이전 실험과 비트 단위 일치
- 메시지: **이후 모든 실험은 이 분할에서 판정한다.**

---

## 2부. 기존 증강 연구의 재현과 분할 (2장, 4분)

### S6. LMR 증강 재현 (EXP-002-PC, Xu 2023) [Teacher 검증]
- 원문: DeepShip 녹음 단위 분할, ResNet-18+MHA, STFT. 74.68 → 78.40(+3.72, 단일 실행)
- 우리 재현(seed 3, best-val):

| seed | 증강 없음 | LMR | Δ |
|---|---|---|---|
| 0 | 66.90 | 69.81 | +2.91 |
| 1 | 65.10 | 69.06 | +3.97 |
| 2 | 66.86 | 67.02 | +0.16 |
| 평균 | 66.29 | 68.63 | **+2.34 ± 1.97** |

- 판정: 증강 이득 Δ는 재현됨. 기준(≥ 2 pp)을 0.34 pp 차이로 넘었다. baseline 절대값(74.68)은 재현하지 못함.
- 주의: last epoch 기준이면 Δ가 −8.40 pp로 뒤집힌다(seed별 −9.82 / −10.95 / −4.43). 체크포인트 선택 규칙에 따라 결론이 바뀐다.
- **원문 분할의 누출 규모(CLS 확인, 3ceb496):** test 녹음 153개(선박 103척). train+val segment의 **64.6%(5,126/7,932)가 test 선박의 녹음**이다 → 녹음 단위 분할이어도 학습 데이터의 2/3가 test와 같은 선박
- 선박 분할 비교(EXP-E2-LMR-ships, 12 run, 자원 빌 때): ship arm(test 선박 제거) vs R arm(같은 양을 무작위 제거, 선박 공유 유지). 결과가 없으면 "진행 중"으로 표시

### S7. LOFAR + Hough 증강 재현 (EXP-LOFAR-001, Cho & Ha 2024) [Teacher 검증]
- 실험: DeepShip 4클래스 + ShipsEar Passenger, 분할 4종(무작위 / 녹음 / DEMONet / 선박) × 모델 3종 × 원본·HT
- 표 1, 원본 정확도(%):

| 모델 | 무작위 | DEMONet 분할 | 선박 분할 |
|---|---|---|---|
| CNN3 | 70 | 45 | 44 |
| ResNet18 | 80 | 66 | 54 |
| DenseNet121 | 74 | 63 | 52 |

- 표 2, HT 이득(CNN3, seed 8개): 무작위 +4.67(8/8), 녹음 +4.40(7/8), DEMONet +7.52(8/8), **선박 +2.53(6/8)**
- 사전학습 모델(ResNet18, DenseNet121)은 선박 분할에서 이득이 유지되지 않음
- 핵심 메시지(1–2부 종합): **분할이 엄격해질수록 절대 정확도는 25–30 pp 떨어지고, 증강 이득도 작아지거나 불안정해진다.**

---

## 3부. 분류기는 무엇을 학습했나 (3장, 5분)

### S8. 어떤 특징 도메인이 좋은가 (E1-rep) [Teacher 검증]
- 실험: MEL / STFT / CQT / MFCC × DeepShip·ShipsEar × 5 fold × seed 3 = 120 run
- 결과(평균 Δ vs MEL):
  - DeepShip: STFT −1.89 / CQT −1.74 / MFCC −3.97
  - ShipsEar: STFT +0.86 / CQT +0.42 / MFCC +0.26 (seed sd가 최대 8.7로 큼)
- 메시지: **MEL보다 나은 도메인은 없었다.** tonal이 잘 보이는 CQT도 분류는 좋아지지 않았다. 그러면 분류기는 무엇을 보는가?

### S9. broadband와 tonal 분리 실험 설계 (E1-src)
- 그림: 같은 클립의 O_rp(원본 크기) / B(broadband만) / T(tonal만), MEL·CQT 각각(E1 결과 페이지 그림)
- 분리 방법: |X|²를 20 Hz median으로 평활한 것이 B, |X| ÷ 평활이 T(부록에 설명)
- 설계: 입력 3종 × Rec-disjoint·Ships-disjoint

### S10. 결과: 분류기는 선박을 외우고, 클래스 정보는 broadband에 있다 (E1-src, E1-src-CQT) [Teacher 검증]
- Rec-disjoint → Ships-disjoint(원본 MEL): 69.17 → 57.77(−11.4 pp)
- Ships-disjoint F1(MEL): B 53.16 ≈ O_rp 52.20 > T 41.87. CQT로 그려도 B − T 격차는 같다(+11.02 vs +11.29)
- 하락폭 비교 D = drop(B) − drop(T) = +3.20, CI [−1.54, +7.84] → **선박 고유 단서가 어느 쪽에 더 있는지는 보류**
- 확인된 것 두 가지:
  1. 녹음 단위 정확도에는 선박 암기가 섞여 있다
  2. Ships-disjoint 클래스 정보는 broadband 장기 스펙트럼 모양에 있다(SwinV2 + 이미지 표현 한정)
- 한계: seed 0만

---

## 4부. 물리 평가기: 실제 선박과 대조군을 구별하는가 (2장, 3분)

### S11. tonal 평가기 (E0-G0) [Teacher 검증]
- 대조군: 같은 클립의 PSD를 평활해 tonal만 지운 잡음
- 결과: AUC DeepShip 0.998, ShipsEar 0.937 → 사용
- 그림: 클래스별 tonal 수 분포(실제 10–16개 vs 대조군 거의 0), 합성 검증

### S12. DEMON 평가기와 beating (E0-G0, G0v2) [Teacher 검증]
- 대조군: 위상 무작위화(진폭 변조를 지움)
- 문제: 위상을 섞어도 가까운 tonal 두 개의 beating이 41.4 Hz 피크를 남긴다 → 가짜 프로펠러 변조
- 개선안 3종: CPW 백색화 / 하모닉 검출 / 둘의 결합

| | V1 | CPW | 하모닉 |
|---|---|---|---|
| DeepShip AUC | 0.713 | **0.762** | 0.513 |
| ShipsEar AUC | 0.720 | 0.683 | 0.540 |

- 합성 검증: beating 신뢰비 14.7 → 1.39, 날개 변조는 23.5 → 20.5로 유지
- 결정: CPW로 통일하고 DeepShip만 사용(사후 결정임을 명시). 하모닉 검출은 5 s 클립에서 검출력 없음

---

## 5부. 잡음 제거 앞단 (5장, 7분)

### S13. 논문 소개: FocuS-MN (Gu 2026, JMSE 14:621)
- 동기: 배경 잡음(녹음 조건 단서)을 지우면 Ships-disjoint 인식이 좋아질까?
- 방법: STFT 크기^0.3 + 위상 → dilated DenseNet 인코더 → 학습형 리샘플링 + FSMN(M = 6, N = 6) → 학습형 sigmoid 마스크. 0.34 M 파라미터
- 데이터: ShipsEar 선박 + 배경을 −5 dB로 섞음. test는 처음 보는 선박 종류 4개
- 원문 결과: SDR 3.77 / SDRi 8.61 dB

### S14. 재현 결과 (DEN-R) [Teacher 검증]
- 시도별 SDRi:
  - 시도 1(원문대로) 6.58
  - 시도 2(+잔차) 5.16
  - 시도 3a(AdamW) 5.98
  - **시도 2b(잔차 + 2단계 결합 손실) 8.68 → 통과**
- 표기: 편차 27건을 둔 재현
- 부수 발견: 결합형 L2(Adam weight decay)가 약 7k step 뒤 가중치를 무너뜨림 → AdamW로 해결

### S15. DeepShip에 적용하면 잘 안 된다 (R2b, R3-DS) [Teacher 검증]
- 그림: `research/figures/seminar_S15_den_methods_deepship.png`. 같은 DeepShip 클립의 방법별 MEL과 LTAS. 시도 2b는 2–8 kHz를 거의 지운다.
- 잡음 제거 성능: DeepShip 혼합 SDRi 5.86 dB(기준 6.9 미달). 실녹음 에너지 87% 제거, 2–4 kHz −16 dB, 4–8 kHz −19 dB
- 분류 앞단(5 fold): **F1 58.18 → 53.35(−4.83, 4/5 fold 음수)**
- **2026-10-26 발견: DeepShip 클립 에너지의 98%가 DC였고, 잡음 제거기에 DC를 빼지 않고 넣었다.** DC를 빼면 ShipsEar 모델의 DeepShip 혼합 SDRi는 7.07(통과). DC를 뺀 입력으로 분류 5 fold를 다시 하는 중(R3-DS-DC) → 발표 전 결과로 이 슬라이드를 고친다
- 교훈: fold1만 봤을 때는 +7.24였다(큰 선박 두 척의 효과). fold 하나는 방향까지 틀릴 수 있다.
- 연결: 3부에서 클래스 정보는 broadband에 있었다. broadband를 지우면 해롭다는 결과와 일관된다.

### S16. 같은 해역 데이터로 학습: R-US [Teacher 검증]
- UniqueShip: DeepShip과 같은 ONC 해역, 실제 배경 녹음 42.7 h
- 전처리 발견: 클립 대부분이 DC(|평균|/RMS 0.96–0.99) → 클립별 DC 제거 필수
- 결과: SDRi **8.46 dB**(쓸 만함). tonal 15.46 → 15.44로 보존, 전 대역을 고르게 −6…−9 dB
- 한계: 선박 소리도 78.6% 지움(배경 87.5%)
- 누출 주의: 학습 선박이 DeepShip과 140척 겹친다(DeepShip 클립의 71%). DeepShip 분류에는 기간 분리 재학습(R-US-T)이 필요하다.

### S17. R-US 잡음 제거 결과를 세 데이터셋에서 비교 [그림 완성: `research/figures/seminar_S17_rus_3datasets.png`]
- 구성: 행 = UniqueShip cargo(fold1 test) / DeepShip Cargo(R-US 학습 선박과 겹치지 않는 SPRING QUEEN) / ShipsEar tugboat(두 모델 모두 학습에 없음) / UniqueShip background. 열 = 원본(DC 제거) / ShipsEar 모델(시도 2b) / R-US / LTAS
- 클립 선택 규칙(미리 고정): 후보 풀에서 seed 0으로 20개를 뽑아 원본 tonal 수가 중앙값인 클립
- 숫자(지운 에너지, tonal 수 원본 → ShipsEar 모델 → R-US):

| 클립 | ShipsEar 모델 | R-US |
|---|---|---|
| UniqueShip cargo | −5%, 11 → 8 | 90%, 11 → 13 |
| DeepShip Cargo | 38%, 10 → 7 | 69%, 10 → 10 |
| ShipsEar tug | 78%, 20 → 17 | 91%, 20 → 18 |
| UniqueShip 배경 | 91%, 9 → 6 | 88%, 9 → 9 |

- 읽는 법:
  - ShipsEar 모델은 데이터셋과 관계없이 2–8 kHz를 크게 깎는다(LTAS의 파란 선).
  - R-US는 스펙트로그램 모양을 거의 유지하면서 전체 레벨을 낮춘다. 지운 에너지의 대부분은 에너지가 몰린 저주파(< 100 Hz)에서 나온다(LTAS의 주황 선).
  - tonal 수는 R-US에서 유지되고, ShipsEar 모델에서는 2–3개 줄어든다.
- 주의: 클립 하나씩이다. 전체 통계는 S16 숫자(UniqueShip test 전체)를 쓴다. 지운 에너지 %는 저주파 레벨에 지배된다.
- 분류 효과: R3-US(UniqueShip fold1, seed 3) 결과를 발표 전에 채운다. 문구 3종(도움 / 해로움 / 불명확)을 준비해 둔다.

---

## 6부. 정리와 다음 (1장, 2분)

### S18. 정리와 다음 단계
- 정리:
  - 분할을 엄격하게 하면 분류 정확도(−12…−45 pp)와 증강 이득이 모두 줄어든다
  - Ships-disjoint 클래스 정보는 broadband에 있다
  - 물리 평가기: tonal은 사용, DEMON은 CPW로 DeepShip만 사용
  - ShipsEar로 학습한 잡음 제거는 DeepShip에서 해롭다
- 다음 단계:
  1. R3-US
  2. R-US-T(DeepShip 5 fold)
  3. 잡음 제거 채택 여부 결정
  4. AE 게이트(E1-AE 22/30에서 일시정지, L1 AE의 질감 손실 진단)
  5. LDM 물리 기반 증강
  6. WAV 복원
- 지도교수 확인: 방향 전환(생성 전에 분할·분류기·입력 점검), 주 데이터 DeepShip·ShipsEar

---

## 부록
- A1 용어
- A2 broadband/tonal 분리 방법
- A3 분할 통계
- A4 UATR-SLM 클래스별 F1
- A5 E1-rep 전체 표
- A6 FocuS-MN 편차 목록
- A7 UniqueShip–DeepShip 중복 표

## 예상 질문
| 질문 | 답의 요지 |
|---|---|
| UATR-SLM 수치는 믿을 만한가? | 이전 세션 실험이고 무작위 분할 재현치가 1.3–2.6 pp 낮다. 분할 간 차이(33–45 pp)는 이 오차보다 훨씬 크다 |
| LMR은 선박 분할에서 어떤가? | 측정하지 않았다. 필요하면 Ships-disjoint로 6 run을 추가할 수 있다 |
| 왜 생성 결과가 없나? | 생성물을 평가할 분류기와 평가기가 먼저 검증돼야 했다. 그 과정이 오늘 발표 내용이다 |
| 잡음 제거가 왜 해로운가? | 클래스 정보가 broadband에 있는데 잡음 제거가 broadband를 지운다(inferred). R-US로 다시 확인 중이다 |
