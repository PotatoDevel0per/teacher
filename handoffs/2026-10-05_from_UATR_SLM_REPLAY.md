# Handoff 수신: UATR-SLM 분할 방식별 성능 연구 (UATR_SLM_REPLAY 세션)

- 수신일: 2026-10-05
- 보낸 곳: 다른 Claude 세션 `UATR_SLM_REPLAY` (이 세션이 직접 검증하지 않음)
- 산출물: `/jhlee/UATR_SLM/UATR_SLM_split_study/` (README, `01_conditions/CONDITIONS.md`, `02_results`, `03_tsne`, `04_splits/SPLITS.md`), 압축본 `/jhlee/UATR_SLM/UATR_SLM_split_study.zip` (1.8 MB). 폴더 존재와 README 표가 메시지와 일치하는 것만 확인했다.
- 상태: `hypothesis` (Claude 주도, 사용자 검증 전). `research/decisions.md` D-2026-09-30-01 규칙을 적용한다.

## 설계

- 분류기 고정: UATR-SLM (SenseVoiceSmall 234M 전체 미세조정 + mean-pool + Linear)
- 변수: 분할 방식만. 2 데이터셋 × 4 분할 × 3 seed = 24 run
- 전처리: 16 kHz, 5 s 비중첩, fbank80 → LFR(7,6) → CMVN
- 하이퍼파라미터: 논문 명시값을 따르고, 미기재 항목은 세션이 채움

## 결과 (test macro-F1, 3 seed 평균 ± sd)

| 분할 | DeepShip | ShipsEar |
|---|---|---|
| 논문 보고치 | 99.32 | 99.00 |
| ① 무작위 클립 8:1:1 | 98.02 ± 0.07 | 96.40 ± 1.87 |
| ② 녹음 분리 8:1:1 | 65.06 ± 4.26 | 73.12 ± 13.06 |
| ③ 녹음 분리 (DEMONet 원본 비율) | 67.33 ± 1.33 | 65.42 ± 7.86 |
| ④ 선박 분리 8:1:1 | 52.80 ± 6.04 | 71.80 ± 6.79 |

- 분해 (①②④만 사용): 녹음 서명 기여 DeepShip −32.97 / ShipsEar −23.28 pp, 선박 서명 기여 −12.26 / −1.32 pp
- ShipsEar는 녹음 수와 선박 수가 비슷하다(90 / 57). 녹음을 분리하면 선박도 거의 분리되므로, 선박 서명을 따로 측정할 수 있는 것은 DeepShip뿐이다.

## 세션이 밝힌 한계

1. DEMONet 조건(③)은 8:1:1이 아니므로 직접 비교할 수 없다.
2. ShipsEar는 sd가 크다(test 213–429 클립, 클래스당 1–2척). ②와 ④는 구분되지 않는다.
3. 무작위 분할 재현치가 논문보다 −1.30 / −2.60 pp 낮다. 원인 미상.
4. t-SNE는 정성 자료일 뿐이다.

## 부수 발견 (재사용 가치 높음)

- **ShipsEar 선박 ID 복원**: 원본 90 녹음 파일명에서 57 선박 그룹을 만들었다. A/B 클래스(보트, 요트)는 일반명사라 모호해서 번호가 다르면 다른 배로 간주했다. 규칙: `04_splits/code/shipsear_inventory.py`
- **ShipsEar 사본 검증**: 클래스별 클립 수 843/486/369/301/224 = 2,223으로 논문 Table 2와 일치한다. `/jhlee/data/shipsear/DATASET_INFO.md`의 "무음 제거" 기재는 틀렸다.
- **FunASR seed 버그**: `funasr/auto/auto_model.py:555`의 `set_all_random_seed(kwargs.get("seed", 0))`가 모델 생성 직전에 seed를 0으로 덮어쓴다. DistributedSampler의 기본 seed=0과 겹치면 run이 비트 단위로 같아진다. 위 표는 교정본이다.

## 이 지식베이스에 주는 의미 (`inferred`)

- 9월의 UATR_SLM 결과(S0 97.74 / S1 65.81 / S2 50.01)와 방향·크기가 비슷하다. 다만 **9월 run에도 FunASR seed 버그가 있었는지는 미확인(`unknown`)**이다. 9월 결과의 seed 간 분산이 실제 분산인지 재확인해야 한다.
- UniqueShip 논문(DeepShip 누출 없음 Swin 0.588)과 같은 방향이다. 분할 정의, 지표(정확도 vs macro-F1), 모델이 모두 달라 수치를 직접 비교할 수는 없다.
- 증강 연구로 전환할 경우, DeepShip 선박 분리 조건의 sd ±6.04는 몇 pp 수준의 증강 효과를 검출하기 어렵다는 것을 다시 보여 준다. 주 벤치마크는 UniqueShip이 적절하다는 판단을 지지한다.

---

# 추가 수신 (2026-10-06): UniqueShip 분류기 비교

- 산출물: `/jhlee/UATR_SLM/uniqueship_clf/COMPARE.md`, `runs/` 24개 (존재 확인)
- 설계: UniqueShip 논문 §IV의 분류기(SwinV2-Tiny, Mel 256, 90 dB 동적범위, lr 1e-6)를 같은 클립·24 분할·seed에서 학습했다.
- **논문 그대로가 아니다.** 30 epoch 대신 epoch 상한을 올리고 조기 종료를 썼다(미수렴 문제 때문). batch 64는 논문 미기재 → "논문의 일부 모듈을 재현함(변형)".

## DeepShip test macro-F1 (3 seed)

| 분할 | UATR-SLM | UniqueShip clf | 차이 | Welch p (이 세션 계산) |
|---|---|---|---|---|
| 무작위 | 98.02 ± 0.07 | 94.69 ± 0.43 | −3.33 | 0.005 |
| 녹음 분리 | 65.06 ± 4.26 | 69.78 ± 2.12 | +4.72 | 0.19 |
| 선박 분리 | 52.80 ± 6.04 | 56.19 ± 2.72 | +3.39 | 0.45 |

- ShipsEar는 sd가 최대 16이라 모델 간 차이를 해석할 수 없다.
- 보낸 세션의 주장: "누출을 제거하면 순위가 뒤집힌다."
- **이 세션의 평가 (`inferred`)**: 누출 조건에서 UATR-SLM이 앞선다는 것은 유의하다. 그러나 녹음·선박 분리 조건에서 UniqueShip이 앞선다는 것은 seed 3개로는 유의하지 않다(p 0.19, 0.45). 지지되는 것은 "순위 역전"이 아니라 **"누출 없는 조건에서는 234M 음성 모델의 우위가 사라진다"**는 데까지다.
- 레벨 정규화 설명: 9월 D3(+2.83 pp)와 방향이 같다. 하지만 모델·특징·lr이 동시에 다르다(보낸 세션도 인정). 증강 연구와 관련 있는 가설로 기록해 둔다. 레벨(절대 음압) 정보는 녹음·거리 지름길일 수 있다.
- 다음 계획(보낸 세션): `/jhlee/data/uniqueship/5class_balanced`로 논문 Table III(0.665 ± 0.012)를 직접 대조한다. 이 세션이 받은 데이터를 쓴다.
