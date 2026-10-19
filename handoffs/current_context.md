# Current Research Context

## 연구 목표

WAV 파형으로 복원 가능한 수중 표적 선박 소음 생성 및 평가 파이프라인을 연구한다.

## 1차 목표 (2026-10-06 결정)

물리 기반 증강으로 UATR의 누출 없는 일반화를 개선한다. WAV 생성은 후순위다 (`research/decisions.md` D-2026-10-06-02).
조건부 LDM 생성(DEMON·LOFAR 조건)은 물리 기반 증강의 후보 방법 중 하나로 본다 (D-2026-10-13-02). 순서: AE 복원 상한 → 무조건 LDM → 조건부 LDM → 조건 조작 증강 → UATR 평가.

## 현재 핵심 질문

선박 분리 조건에서, 기존 녹음의 변형(범용 증강)이 아니라 "새 선박처럼 보이는" 물리 기반 변이를 만드는 증강이 UATR 일반화를 개선하는가?

## 확정된 사실

- 기존 UATR 생성 연구 상당수는 feature-space 또는 Mel-space 합성을 사용한다.
- 일반 오디오 임베더 기반 FAD/KAD를 수중음향에 그대로 적용하는 것은 검증이 필요하다.
- 선박 소음에서는 협대역 토널 성분과 광대역 성분을 분리해 평가해야 한다.
- 데이터셋 분할에서 선박 또는 passage 단위 누수를 방지해야 한다.

## 현재 가설

- 수중음향 도메인 특화 임베더가 범용 오디오 임베더보다 생성 품질 평가에 더 적합할 가능성이 있다.
- UATR 성능 향상만으로는 WAV 생성 품질을 입증할 수 없다.
- Mel 기반 생성 결과를 WAV로 복원할 때 토널 구조가 손상될 가능성이 있다.

## 현재 상태

- [ ] 데이터셋 최종 선정
- [x] UATR baseline (EXP-001, UniqueShip SwinV2)
- [ ] feature-space augmentation 재현 (EXP-002-PC(a) 진행 중)
- [ ] WAV 복원 baseline
- [ ] 토널 평가 지표
- [ ] 도메인 특화 임베더
- [ ] 통합 실험

## 이전 실험 (2026-08 ~ 09, 미검증)

- 6개 폴더의 조사 결과: `research/prior_experiments/README.md`
- 모두 `hypothesis` 상태이며 사용자의 이해 근거로 쓰지 않는다 (`research/decisions.md` D-2026-09-30-01).
- 폴더마다 DeepShip 분할이 달라 수치를 서로 비교하면 안 된다.

## 현재 진행 (2026-10-12 갱신)

실험 전체 목록과 상태: `research/experiment_registry.md`. 실행은 모두 `UATR_SLM_REPLAY` 세션이 한다.

| 실험 | 상태 | 문서 |
|---|---|---|
| EXP-001 UniqueShip baseline (SwinV2 + Mel) | 재현됨: acc 67.30 ± 2.45 | `research/experiment_registry.md` |
| EXP-002-PC(a) LMR 양성 대조군 (DeepShip, Xu J. 2023 재현) | **종료(2026-10-14).** Δ 재현됨(+2.34). 단계 2: baseline 70% 재현 시도. D2 분할 채택. B0 3 seed: last 68.00(기준 미달), best-val 70.37. D4 미채택. D6(누수 없는 val) best-val 67.92, 미달. baseline 절대값 재현하지 못함 | `research/experiments/EXP-002-PC_lmr_positive_control.md` |
| EXP-002 범용 증강 A1–A4 (UniqueShip MMSI 분할) | 보류. PC(a) 결과를 보고 재개한다. ② 반영(헤드 초기화 시드, A0 5 fold 재실행) | `research/experiments/EXP-002_generic_augmentation.md` (하단 편차·결정 기록) |
| EXP-002-PC(b) naive vs MMSI 분할 | 미승인 | registry |
| EXP-003 물리 기반 증강 | 미정 | — |

- 실험 폴더는 2026-10-14부터 `/jhlee/UWShipNoise/` 아래에 있다. 색인: `/jhlee/UWShipNoise/README.md`. 체크포인트와 캐시는 정리됐다(D-2026-10-14-02).
- UniqueShip 로컬 사본: `/jhlee/UWShipNoise/data/uniqueship/` (`research/datasets/uniqueship.md`)
- 측정된 실행 잡음: 같은 설정을 다시 돌렸을 때 acc +1.12 pp (1표본, 헤드 초기화 비시드)

## 현재 막힌 문제

1. 단일 공식 DeepShip 분할이 없다. ship_id 매칭의 신뢰성도 불확실하다 (`research/open_problems.md` OP1, OP2).
2. 선박 분리 조건의 UATR baseline 상한을 모른다 (OP4).
3. 토널 보존 평가 지표가 검증되지 않았다 (OP6). "음향학적 타당성"의 정의도 없다 (OP11).
4. 블레이드 수 정답 라벨이 없다. 사용자가 DEMON 기반 블레이드 수 추정 논문을 탐색 중이다 (OP12).

## 다른 프로젝트 세션에 요청할 것

- 논문 원문 분석:
- 코드 재현:
- 신호처리 검토:
- 실험 설계 검토:

## 참고 파일

- `research/research_overview.md`
- `research/open_problems.md`
- `research/decisions.md`
- `papers/index.md`
## 대기 상태와 다음 할 일 (2026-10-14: 병렬 실험 모두 종료)
| 세션 | 상태 | 다음 |
|---|---|---|
| LOFAR | **EXP-LOFAR-001 종료**(2026-10-13). 부분 재현. CNN3 HT 이득은 선박 분할에서 +2.53 ± 3.05(6/8)로 작다 | 없음. LDM 조건: TPSW LOFARgram은 조건부 사용, Hough 선 목록은 사용 불가(`papers/notes/2024_cho_lofar_hough_cnn.md`) |
| DEMON | **EXP-DEMON-001 종료**(2026-10-14). 합성 단계에서 마무리 | 없음. LDM 조건: 고정 대역 DEMON 스펙트럼 |
| UATR_SLM_REPLAY | **EXP-002-PC 종료**(2026-10-14). Δ 재현, baseline 절대값 미재현. EXP-002는 보류 유지 | 없음 |

- **조건부 LDM 설계 초안 작성됨 (2026-10-13):** `research/experiments/EXP-003-LDM_conditional_aug_design.md`. 사용자가 LDM 원문을 공부한 뒤 D1–D5(데이터, 표현, 조건 주입, A-phys, 실행 세션)를 정한다.
- **설계 때 반드시 반영할 이전 교훈** (PG-MCLDM, 미검증):
  - 생성물 tonal F1은 0.2다(실데이터 0.66).
  - DEMON 변조를 만들지 못했다(신뢰비 0.007–0.018).
  - 물리 손실(Phase 3)은 기각됐다.
  - 증강 이득은 +0.66 pp로 유의하지 않았다(seed 1개, 선박 누수 분할).
  - 따라서 AE 복원본의 tonal·DEMON 보존을 첫 게이트로 둔다.

## 2026-10-19 갱신

- 학위논문 주 방법 = 증강용 생성 모델 (D-2026-10-19-01). 판정은 선박 분리 UATR.
- 실험 저장소: `/jhlee/UWShipNoise/thesis` (git, core/ 공유 코드 + exp/). 세션: CLS(분류·판정), GEN(AE·LDM, E1-rep 이후).
- 진행: EXP-E1-rep 승인. 지시서 `handoffs/2026-10-19_to_CLS_E1-rep.md`. CLS 세션 개설 대기.
- 일정 초안: `research/thesis_timeline_draft.md` (약 33주, 2027-06 중순).
