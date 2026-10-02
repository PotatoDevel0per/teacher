# 이전 실험 아카이브 (Prior Experiments, 2026-08 ~ 2026-09)

- 작성일: 2026-09-30
- 조사 방법: Claude 서브에이전트 5개가 각 폴더를 **읽기 전용**으로 조사(문서·config·코드·로그·결과 json). 재실행·재계산 없음.
- 대상: `/jhlee/DGM`, `/jhlee/deepship_analysis`, `/jhlee/UATR_SLM`, `/jhlee/deepship_preprocessing`, `/jhlee/ot-cfm`, `/jhlee/PG-MCLDM`

## 0. 이 아카이브를 읽는 규칙 (중요)

1. **모든 실험은 사용자가 Claude Code와 함께 약식으로 진행했고, 타당성이 검증되지 않았다.** (사용자 발언, 2026-09-30)
2. **사용자가 이 실험들에 쓰인 개념을 이해했다고 판단하지 않는다.** `profile/learning_status.md`의 등급 근거로 쓰지 않는다. (사용자 요청)
3. 이 아카이브의 기록 등급:
   - `[문서]`: 해당 폴더 문서에 적힌 주장. 문서 자체도 Claude가 작성했다. → 상태 `hypothesis`
   - `[확인]`: 조사 에이전트가 코드·로그·json에서 직접 확인한 값. **"그 파일에 그 값이 있다"는 뜻이지, 실험이 타당하다는 뜻이 아니다.** → 상태 `confirmed(기록 존재)`
   - `[추론]`: 조사 에이전트 또는 이번 세션 Claude의 해석. → 상태 `inferred`
4. 여기 적힌 결론을 새 연구의 **전제**로 쓰지 않는다. 재검증 후보 또는 반면교사로만 쓴다.

## 1. 시간 순서와 계보

| 순서 | 폴더 | 기간 (mtime) | 성격 | 상세 |
|---|---|---|---|---|
| 1 | `DGM` | 08-19 ~ 09-01 | 생성: 8 kHz·4 s dB STFT, 생성 프레임워크 6종 비교 ("라운드 1") | [DGM.md](DGM.md) |
| 2 | `deepship_analysis` | 09-04 ~ 09-09 | 데이터 분석: CPA·거리, 톤 검출 임계, 보코더 왕복 | [deepship_analysis.md](deepship_analysis.md) |
| 3 | `UATR_SLM` | 09-05, 09-08 | 인식: UATR-SLM(ICASSP 2026) 재현 + 분할 누수 측정 | [UATR_SLM.md](UATR_SLM.md) |
| 4 | `deepship_preprocessing` | 09-08 ~ 09-09 | 전처리: 9-stage 파이프라인, 2-stream STFT + GL 복원 결정 | [deepship_preprocessing.md](deepship_preprocessing.md) |
| 5 | `ot-cfm` | 09-10 ~ 09-29 | 생성: 30 s 2-stream, CFM(R0) vs DDIM(D0) ("라운드 2") | [ot-cfm.md](ot-cfm.md) |
| 6 | `PG-MCLDM` | 09-28 ~ 09-30 | 생성: 물리 조건 latent OT-CFM + 증강 검증 (중단 상태) | [PG-MCLDM.md](PG-MCLDM.md) |

의존 관계 `[확인]`:

```
/jhlee/data/deepship (609 녹음, 32 kHz) + ship_id.csv (출처 불명의 휴리스틱 매칭)
 ├─ DGM ── (/jhlee/Underwater_Acoustic/.../deepship_split4) ──┐ physmetrics, cfm.py 등 재사용
 ├─ UATR_SLM ── deepship_split/manifest.csv (ship_id) ──┐     │
 │                                                        ▼     ▼
 ├─ deepship_preprocessing ── ship_disjoint split, 2-stream repr ──▶ ot-cfm (코드 복사 + 산출물 소비)
 │                                     │                                  │
 │                                     └──▶ PG-MCLDM (src import, conditions.parquet) ◀── R0/D0 외부 비교
 └─ deepship_analysis (보코더·톤 결론을 preprocessing/PG-MCLDM이 문서로 인용)
```

폴더 밖 의존성: `/jhlee/Workspace/src`(FAD 구현 `urn.eval.fad`, ot-cfm과 PG-MCLDM이 import), `/jhlee/Underwater_Acoustic/`(DGM의 데이터·보코더), `/jhlee/hifigan`(PG-MCLDM).

## 2. 가장 중요한 공통 경고: 분할이 최소 4개다

| 분할 | 사용처 | 단위 | 선박 누수 | 비고 |
|---|---|---|---|---|
| split4 | DGM | 4 s 조각 / 선박 group | 없음 `[확인]` | test Tug 2척, Passenger 4척 |
| `UATR_SLM/deepship_split` (seed 42) | UATR_SLM (학습에는 미사용) | 5 s 클립, 254척 | 없음 | 학습은 `data/splits/S{0,1,2}`로 함 |
| `ship_disjoint` (split_seed 42) | deepship_preprocessing, ot-cfm | 30 s 세그먼트, 220척 | 없음 | test Tug 2척 |
| DEMONet Table 10 | PG-MCLDM | recording-disjoint | **test 73.9%가 train과 같은 선박** `[확인]` | 논문 분할 재사용 |

- `ship_disjoint`와 `UATR_SLM/deepship_split`은 공통 선박 220척 중 fold가 일치하는 것이 121척뿐이다 `[확인]`.
- ot-cfm test 537 세그먼트 중 366개가 PG-MCLDM의 train에 들어 있다 `[확인]`.
- **폴더 사이에서 수치를 비교하거나, 한 폴더의 모델·분류기를 다른 폴더의 test에 쓰면 안 된다.**

## 3. 폴더를 가로질러 반복된 관찰 (재검증 대상 후보)

모두 `hypothesis` 상태다. 여러 폴더에서 비슷한 결과가 나왔지만, 모두 Claude가 설계·실행·해석했고 독립 재현은 없다.

| # | 관찰 | 근거 폴더 | 신뢰 판단 |
|---|---|---|---|
| O1 | DeepShip 클립 단위 무작위 분할은 인식 성능을 크게 부풀린다 (SLM macro-F1 97.7 → 선박 분리 50.0) | UATR_SLM | 3 seed 있음. 다만 S1/S2 하이퍼파라미터 재조정 없음 |
| O2 | 녹음별 정적 스펙트럼 형상(센서·경로·배경)이 지름길(shortcut)일 수 있다 | UATR_SLM(D1, D3), DGM(gate1: KAD의 61–67%가 세션 차이) | 방향은 일관, 기제는 미확인 |
| O3 | mel + HiFi-GAN 왕복은 저역 토널 피크를 거의 보존하지 못한다 (top-20 일치 22.6%, 우연 21.9%) | deepship_analysis, PG-MCLDM 인용 | 16 kHz, 특정 mel 규약 한정 |
| O4 | 선형 STFT n_fft 16384 + GL이면 저역 피크 위치 일치 93–95% | deepship_analysis, deepship_preprocessing | "피크 위치"만 봄. 청취 품질·고역 미보장 |
| O5 | LSD는 톤 보존의 대리지표가 아니다 (GL 반복을 늘리면 LSD는 좋아지고 톤은 나빠짐) | deepship_preprocessing | 40 세그먼트 |
| O6 | PANNs 기반 FAD/KAD는 저주파 토널에 둔감하고 준위(레벨)에 민감하다 | ot-cfm, DGM | 문서 인정. 대안 임베더 미구현 |
| O7 | 같은 설정에서 CFM 계열이 DDPM/DDIM보다 좋게 나왔다 | DGM, ot-cfm | **불공정 비교**(clamp, ε-예측, NFE, seed 1). 결론으로 쓰면 안 됨 |
| O8 | 생성기는 토널 선 구조와 DEMON 변조를 잘 만들지 못한다 | ot-cfm(안정 톤 bin 실 9.2 vs R0 1.6), PG-MCLDM(DEMON 신뢰비 0.007–0.018) | 여러 폴더에서 반복 |
| O9 | 증강 없는 소표본(수천 개)에서는 분포 학습보다 모드 축소·기억이 먼저 온다 | ot-cfm | seed 1 |
| O10 | 생성 데이터의 UATR 기여는 **한 번도 제대로 측정되지 않았다** | 전체 (PG-MCLDM만 seed 1회, 선박 누수 분할) | 연구 목표의 핵심이 공백 |

## 4. 반복된 방법론 문제 (다음 연구에서 피할 것)

1. **seed 1개**: DGM, ot-cfm, PG-MCLDM의 생성기는 모두 seed 1개다. 차이의 유의성을 알 수 없다.
2. **판정 기준을 결과를 본 뒤 바꿈**: DGM(K 기준 3회 변경, D·L 임계를 pilot 결과로 설정), ot-cfm(09-12 규칙 변경으로 9 체크포인트 중 6곳 판정 변화), PG-MCLDM(G0 best-val → last epoch, Phase 3 판정을 val 대신 test로). 이름은 "사전 등록"이었지만 실제로는 사후 조정이었다.
3. **비교 조건이 다름**: 학습 step(DGM 200k vs 100k), config 버전(ot-cfm R0/D0 sha 다름, PG-MCLDM 코드 버전 혼재), 대역(DGM lf2k), 증강 시 학습량(PG-MCLDM n_train 증가).
4. **test 선박이 너무 적음**: 선박 분리 분할에서 Tug test가 2–5척이다. 클래스별 수치의 신뢰구간이 매우 넓다.
5. **복원 비대칭**: 생성물만 GL을 거치고 참조는 원본 파형인 경우가 있었다(DGM). ot-cfm은 실데이터도 GL 왕복을 거치게 해서 이 문제를 고쳤다.
6. **baseline 부재**: 기존 feature-space 증강 재현이나 외부 생성 연구 재현이 없다. CLAUDE.md §11의 최소 파이프라인 1–2단계를 건너뛰고 생성 모델부터 시작했다.
7. **이름과 실제가 다름**: "ot-cfm"은 미니배치 OT를 쓰지 않았다. "PG-MCLDM"은 diffusion이 아니라 OT-CFM이고, PINN은 하류에 쓰이지 않았다.

## 5. 재사용 가치가 있는 자산 (색인)

아래는 "쓸 수 있을지도 모르는 것"이다. 쓰기 전에 각각 검증해야 한다.

| 범주 | 자산 | 경로 | 주의 |
|---|---|---|---|
| 메타데이터 | 609 파일 인벤토리(선박, AIS 거리, DC, 클리핑) | `/jhlee/deepship_analysis/deepship_analysis/file_manifest.csv` | ship_id는 휴리스틱 매칭, 잘린 선박명 있음 |
| 메타데이터 | 녹음·세그먼트·조건 표 | `/jhlee/deepship_preprocessing/deepship_pipeline/{recordings,segments,conditions}.parquet` | 거리 보간 45%가 비정상해 |
| 분할 | 누수 검사 포함 S0/S1/S2 (3 seed) | `/jhlee/UATR_SLM/data/splits/` | |
| 분할 | 선박 분리 30 s | `/jhlee/deepship_preprocessing/deepship_pipeline/splits/ship_disjoint.json` | test Tug 2척 |
| 분할 | 논문 분할 전사 (Xie2024 track, DEMONet Table 10) | `/jhlee/ot-cfm/data/splits/xie2024_*.json`, `/jhlee/PG-MCLDM/splits/deepship_table10.json` | 논문 분할 자체에 선박 누수 있음(59%, 74%) |
| 코드 | 3계층 누수 검사, 그룹 분할 | `/jhlee/UATR_SLM/src/split.py` | |
| 코드 | 정적 특징 82차원 + MLP 지름길 baseline | `/jhlee/UATR_SLM/src/diag_d1.py` | 모든 UATR 결과의 대조군 후보 |
| 코드 | 분류기 (CQT/STFT/Mel + ResNet-18, TRTR/TSTR/few-shot) | `/jhlee/PG-MCLDM/pg_mcldm/classifier/train.py` | G0 재현 미통과(72.2 vs 77.15) |
| 코드 | DSP(FIR 데시메이션, sos HPF), TPSW/CFAR, CPA 기하 | `/jhlee/deepship_preprocessing/src/deepship_prep/` | |
| 코드 | 토널 분석 (TPSW, 해석적 CFAR, 하모닉 콤 검증) | `/jhlee/UATR_SLM/deepship_repr/tonal_analysis.py` | analysis 폴더와 방법이 다름 |
| 코드 | DEMON 구현 (합성 신호 검증 포함) | `/jhlee/ot-cfm/src/features/demon.py`, `/jhlee/PG-MCLDM/pg_mcldm/features/demon.py` | |
| 코드 | FAD/KAD, 귀무 분포, 선박 bootstrap, 기억 게이트 | `/jhlee/ot-cfm/src/deepship_cfm/metrics.py`, `/jhlee/DGM/scripts/eval_gen.py` | PANNs 맹점 |
| 코드 | 톤 보존 평가: peak-N 일치율 + 우연 바닥 | `/jhlee/deepship_analysis/.../scripts/tv_common.py` | |
| 코드 | 스케일 불변 URN 지표 (prominence, peak ratio) | `/jhlee/ot-cfm/experiments/urn_protocol_eval.py` | |
| 코드 | 물리 지표 (선밀도, 동적범위 등) | `/jhlee/DGM/scripts/physmetrics.py` | **LTAS 대역 버그 있음** |
| 코드 | 정규모드 solver (Pekeris 대비 0.03%) | `/jhlee/PG-MCLDM/pg_mcldm/physics/modes.py` | 경험 보정 필요했음 |
| 코드 | 생성 프레임워크 (CFM, SB-CFM, DDPM/DDIM, ReFlow, UNet) | `/jhlee/DGM/scripts/` | |
| 캐시 | 학습된 체크포인트 | 각 폴더 `runs/`, `ckpt/` (총 수십 GB) | 분할이 폴더마다 다름 |

## 6. 이 아카이브의 다른 파일

- 폴더별 상세: `DGM.md`, `deepship_analysis.md`, `UATR_SLM.md`, `deepship_preprocessing.md`, `ot-cfm.md`, `PG-MCLDM.md`
- 이 실험들을 남에게 설명하려면 먼저 배워야 할 개념: [concepts_to_learn.md](concepts_to_learn.md)

## 7. 기초부터 다시 시작할 때 참고할 점 (Claude의 제안, `inferred`)

- CLAUDE.md §11 최소 파이프라인 1단계(UATR baseline)부터 시작한다. 이전 실험에서 가장 탄탄했던 것이 UATR_SLM의 분할 누수 측정이었다. 이를 사용자가 직접 이해하고 재현하는 것이 좋은 출발점이다.
- 먼저 **단일 공식 분할**을 하나 정하고 모든 실험에 고정한다. 이전 실험의 가장 큰 구조적 문제는 분할이 여러 개였다는 점이다.
- 이전 수치는 "재현해 볼 목표값"으로만 쓰고, 연구 결론으로 인용하지 않는다.
