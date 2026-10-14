# UATR_SLM — UATR-SLM 재현과 분할 누수 측정

- 경로: `/jhlee/UWShipNoise/recognition/UATR_SLM` (27 GB, git 없음)
- 기간: 2026-09-05 (본 실험), 09-08 (`deepship_split/`, `deepship_repr/` 추가)
- 성격: **인식(분류)** 재평가 연구. 생성 모델은 없다.
- 전체 상태: `hypothesis` (Claude와 약식으로 진행, 미검증). 표기 규칙은 [README.md](README.md) §0.

## 1. 문제 정의

Huang et al., "From Human Speech to Ocean Signals: Transferring Speech Large Models for UATR" (ICASSP 2026, UATR-SLM)를 DeepShip에서 재현했다. 같은 파이프라인에서 분할 단위만 클립 → 녹음 → 선박으로 바꿔 누수가 성능을 얼마나 부풀렸는지 측정했다. SLM = Speech Large Model이고, 실제 모델은 SenseVoiceSmall이다 `[확인]` (원문 PDF `docs/paper_ICASSP2026_Huang_UATR-SLM.pdf`, `docs/paper_notes.md`).

## 2. 데이터

- 원천: `/jhlee/UWShipNoise/data/deepship`, 609 녹음 / 47.22 h / 32 kHz `[문서]`
- 5 s 비중첩 클립 33,770개. 논문은 33,693개(+0.23%) `[문서]`
- 입력: 16 kHz(soxr VHQ) → kaldi fbank 80 mel(25/10 ms) → LFR(m=7, n=6) → (83, 560) → SenseVoice `am.mvn` CMVN. FunASR 원본과 max|Δ| = 0 `[문서]`
- 캐시: `data/clips/feats.f16`, `feats_rmsnorm.f16` (각 3.1 GB)
- 선박 ID: `ship_id.csv`로 599/609 매칭, 미매칭 10개는 각각 고유 선박으로 처리. 총 254척 `[문서]`
- 분할 `[확인]` (`src/split.py`, `data/splits/*.json`, seed 0/1/2)
  - **S0** 클립 무작위 (논문 Table 1 재구성): train↔test 녹음 494–504개, 선박 219–222척 공유 → 누수
  - **S1** 녹음 분리: 녹음 겹침 0, 선박 겹침 38–42척
  - **S2** 선박 분리: 모든 겹침 0
- `deepship_split/` (09-08, seed 42): 149/46/59척, 누수 0, test Tug 3척. **이 분할로 학습한 run은 없다** `[확인]`. ot-cfm과 deepship_preprocessing은 이 manifest의 ship_id만 가져다 쓴다.

## 3. 방법

- SenseVoiceSmall 인코더 전체 미세조정(234M) → masked mean pooling → Linear(512, 4) → CE `[확인]` (`src/model.py`)
- batch 60, lr 2e-4, AdamW wd 0.01, warmup 10% + 선형 감쇠, bf16, 최대 20 epoch, patience 3, best-val macro-F1, 증강 없음 `[확인]` (`runs/*/args.json`)
- 논문 미기재 항목 G1–G26은 추정값으로 채웠다 → **"논문 방법을 재현함(미기재 항목은 재구성)"**. 결과는 부분 재현이다.

## 4. 실험과 결과

출처: `reports/final_report.md`, `reports/summary.md`, `runs/*/result.json`. 수치는 macro-F1이고, 명시가 없으면 3 seed 평균 ± sd다.

| 실험 | 결과 | 비고 |
|---|---|---|
| S0 재현 | 97.74 ± 0.42 (논문 99.32, Δ −1.58) | 부분 재현. gap 원인 미해결 |
| S1 full / matched | 65.81 ± 5.64 / 67.32 ± 3.80 | |
| S2 full / matched | 50.01 ± 3.47 / 50.28 ± 3.16 | |
| 누수 분해 | 녹음 +30.43 pp, 선박 +17.04 pp | `[문서]` 계산 |
| D1 정적 특징 82차원 + MLP | S0 95.48 / S1 63.88 / S2 48.28 | SLM의 증분은 +2–4 pp |
| D2 레벨 십분위 (seed 0) | 최저 레벨 십분위 정확도 S0 97.04 vs S2 37.87 | |
| D3 RMS 정규화 재학습 | S0 97.59, S2 52.83 | 문서 결론: 레벨이 아니라 스펙트럼 형상이 지름길 |
| 가변 길이 zero-shot (seed 0) | S0 1 s 83.7 → 10 s 98.0 / S2 50.8 → 49.4 (평탄) | |
| 탐침 C1/C2/C6 (seed 0) | 97.75 / 96.83 / 89.24 | gap 원인 특정 실패 |
| deepship_repr Task A | 하모닉 간격 5%ile ≈ 7 Hz, 9.5–16 kHz 협대역 군집이 녹음 17%에만 존재 | 신호처리 분석 |

- 문서 스스로 사전 등록 예측 6개 중 4개가 빗나갔다고 기록했다.

## 5. 문제·의심점

1. **matched 통제가 무의미했다**: 그리디 분할이 이미 8:1:1이어서 matched와 full의 train 수가 거의 같다. S1 seed 2는 두 결과가 완전히 같다 `[확인]`.
2. **S1/S2에서 조기 종료**: best epoch가 1–4다. S0에 맞춘 하이퍼파라미터를 그대로 썼다 → S2 50점이 도달 가능한 상한은 아닐 수 있다 `[추론]`.
3. D2, 가변 길이, C1/C2/C6은 seed 1개다. C6은 두 요인을 동시에 바꿨다.
4. S2 test Tug가 2–5척이다.
5. 평가는 클립 단위뿐이다. 녹음·선박 단위 집계는 없다.
6. D1(MLP)과 SLM의 모델 선택 절차가 다르다.
7. ShipsEar cross-domain(원 논문의 일부)은 재현하지 않았다.

## 6. 재사용 가치

- `src/split.py` (`leakage_check`, 그룹 그리디 분할), `src/metrics.py`, `src/eval_varlen.py`
- `src/diag_d1.py`: **지름길 하한 대조군**. 모든 UATR 결과 옆에 둘 가치가 있다.
- `deepship_repr/tonal_analysis.py`, `tone_lines.parquet` (251k 라인), `cache/verified_combs_2k.csv`
- `runs/*/best.pt` 24개 (각 885 MB)

## 7. 이 폴더가 이후 연구에 주는 의미 (`inferred`)

6개 폴더 중 문제 정의가 가장 좁고, 3 seed와 대조군을 갖춘 실험이다. "분할 단위가 결과를 지배한다"는 주장은 이후 모든 폴더가 인용했다. 기초부터 다시 시작할 때 사용자가 **직접 재현하고 설명할 수 있어야 할 첫 실험**으로 적합하다.

## 8. 후속: 분할 방식별 재실험 (2026-10-05, 다른 세션)

- `handoffs/2026-10-05_from_UATR_SLM_REPLAY.md` 참조. DeepShip ①98.02 → ②65.06 → ④52.80, ShipsEar ①96.40 → ②73.12 → ④71.80
- FunASR가 seed를 0으로 덮어쓰는 버그가 발견됐다. 위 §4의 9월 run이 영향을 받았는지는 `unknown`이다.
