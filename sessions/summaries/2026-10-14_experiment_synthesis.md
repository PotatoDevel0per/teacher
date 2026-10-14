# 2026-10-14 세션별 실험 종합

1차 목표: 물리 기반 증강으로 누수 없는 UATR 일반화(D-2026-10-06-02). 조건부 LDM은 후보 방법 중 하나다(D-2026-10-13-02).

## UATR_SLM_REPLAY

| 실험 | 결과 | 상태 |
|---|---|---|
| EXP-001 UniqueShip baseline (SwinV2 + Mel, MMSI 분할 5 fold) | acc 67.30 ± 2.45, 기준 0.665 ± 0.024 안 | 재현됨 (`confirmed`) |
| EXP-002-PC(a) LMR 양성 대조군 (DeepShip, Xu J. 2023) | 증강 이득 Δ +2.34 재현 | Δ 재현됨 |
| 〃 baseline 절대값 70% | D2 last 68.00 ± 3.37, best-val 70.37 ± 0.75(val이 녹음 누수). 누수 없는 val(D6)에서 best-val 67.92 ± 0.30, epoch 최대 69.81 | **재현하지 못함.** 다음 경로는 사용자 결정 대기 |
| EXP-002 범용 증강 A1–A4 (UniqueShip) | — | 보류 (PC 결과 대기) |

- 교훈: 세그먼트 단위 val은 녹음 누수로 test보다 8–9 pp 높게 나온다. stage 비교를 test로 하면 test 선택이 된다(Teacher 오류, 정정함).

## LOFAR (EXP-LOFAR-001, 종료)

- Cho & Ha 2024(Hough + CNN)의 **일부 모듈을 재현함.**
- 원본 정확도 (이미지 무작위 → DEMONet 분할 → 선박 분할):
  - CNN3: 70.1 → 45.3 → 44.3
  - ResNet18: 80.4 → 65.9 → 54.4
  - DenseNet121: 73.8 → 63.2 → 51.5
- CNN3 HT 이득 (seed 8개): +4.67 → +7.52 → +2.53 ± 3.05. 선박 분할에서 가장 약하다. 사전학습 모델은 이득의 부호를 판단할 수 없다.
- Hough 구현 한계: 10 Hz 미만 가짜 선(이미지 95%), 이중 검출, 도플러로 기운 tonal 누락.
- Passenger 클래스에 출처 지름길이 있다(ShipsEar recall 높음, DeepShip 낮음). `inferred`
- LDM 조건 지침: TPSW LOFAR 스펙트럼은 사용 가능, Hough 선 목록은 사용 불가.

## DEMON (EXP-DEMON-001, 합성 단계 완료)

- Wang 2026의 **일부 모듈을 재현함**(합성 신호만).
- 2a 잡음 없음: 천장 효과. TCDS +5.7/+8.6 pp 개선. SBL은 정답 지표를 악화시키고 SHLSNR만 부풀린다.
- 2b-1 잡음 조건: EEMD 자동 대역 선택은 고정 저역(100–2000 Hz)보다 −15 dB 정답률이 35 pp 낮다 → H-PRE-3 불지지.
- (d) 분산 정규화 변형(아이디어 기반 변형): 원문 대비 +30 pp(McNemar p = 0.031). 고정 대역 수준까지 회복할 뿐, 더 낫지는 않다.
- 다음 단계(2b-2 / 단계 3 실데이터 소규모 / 마무리)는 사용자 결정 대기.

## 종합 판단 (`inferred`)

1. **분할이 결과를 지배한다.** LOFAR는 선박 분리에서 22–31 pp가 떨어진다. DeepShip PC는 val 누수만 없애도 2–3 pp가 떨어진다. 증강 효과는 반드시 선박 분리에서 판정한다.
2. **정교한 특징 추출기가 단순한 것보다 낫다는 근거가 없다.** Hough와 EEMD 선택이 그 예다. LDM 조건은 단순하고 연속값인 특징(TPSW LOFAR, 고정 대역 DEMON)으로 시작한다.
3. **DeepShip baseline 재현은 막혀 있다.** UATR 판정 데이터는 baseline이 재현된 UniqueShip이 유력하다.
4. **실데이터에서 tonal·DEMON 특징이 얼마나 보이는지는 아직 검증되지 않았다.** DEMON은 합성 신호만, LOFAR는 분류 정확도로만 확인했다. EXP-003-LDM 단계 0의 목적이다.

## 대기 중인 사용자 결정

- DeepShip PC 다음 경로
- DEMON 다음 단계
- EXP-003-LDM D1–D5 (LDM 원문 공부 후)
