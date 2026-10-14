# ot-cfm — 30 s 2-stream 스펙트로그램 조건부 생성, CFM vs DDIM ("라운드 2")

- 경로: `/jhlee/UWShipNoise/generation/ot-cfm` (6.0 GB, git init만 되고 커밋 0)
- 기간: 2026-09-10 ~ 09-29. 주요 라운드는 09-11 ~ 09-13, URN 감사는 09-23(외부 감사자 `/jhlee/UWShipNoise/legacy/Workspace`)
- 전체 상태: `hypothesis`. 표기 규칙은 [README.md](README.md) §0.

## 1. 문제 정의

deepship_preprocessing의 30 s 2-stream 선형 dB 스펙트로그램을 클래스와 연속 조건(`level_rel_framemax_db`, `level_slope_db_per_s`)으로 조건부 생성했다. 생성기는 CFM(R0)과 DDPM/DDIM(D0) 두 가지이고, GL로 WAV를 복원해 사전 등록 지표로 판정했다. **UATR 증강 기여 검증은 수행하지 않았다.**

## 2. 데이터

- `/jhlee/UWShipNoise/data_analysis/deepship_preprocessing/deepship_pipeline`을 읽기 전용으로 소비한다. 전처리 코드는 복사본이다(`src/deepship_prep`, 일부 파일은 원본과 다름).
- 분할 `ship_disjoint`: train 4,288 / 171척, val 535 / 18척, test 537 / 31척. 누수 0. test Tug 2척
- 학습 232 프레임(29.568 s), per-bin z 정규화(train에서만 산출)

## 3. 방법

- **R0**: 선형 경로 x_t=(1−t)x₀+t·x₁, σ_min=0, uniform t, **coupling = independent** `[확인]` (`src/deepship_cfm/cfm.py`)
  - 이름은 "OT-CFM"이지만 Tong et al.의 미니배치 OT-CFM이 아니다. Lipman et al.의 OT 경로 CFM(rectified-flow 형태)이다 `[추론]`.
  - 미니배치 OT를 뺀 근거: `experiments/probe_ot_coupling.py`, "효과 0.2% 미만"
- **D0**: ε-예측, cosine 1000 스텝, DDIM η=0, x̂₀ clamp ±6
- 공통: 2-분기 UNet 24.77M, CFG dropout 0.1, 100k step, 유효 배치 8, lr 2e-4, EMA. 샘플링은 midpoint NFE 50, cfg 1.0만. 복원은 SPSI + GL. 증강 금지.

## 4. 결과

| 실험 | 결과 | 출처 |
|---|---|---|
| R0 궤적 | FAD 20.17(10k) → 10.66(100k), 귀무 2.81. 톤 분류기 Acc 0.711(실데이터 0.616). 30k부터 "기억 확정" → 사전 규칙상 `discard_run` | `runs/R0/eval/`, `docs/RESULTS.md` §2 |
| D0 | FAD 63.27, Acc 0.384, Coverage/Density 0 | `runs/D0/eval/` |
| NFE 100 | R0 FAD 9.89, D0 44.30 | RESULTS §2-3 |
| 톤 구조 | 안정 톤 bin: 실 9.2, R0 1.6, D0 0. 콤 초과분: 실 +0.029, R0 −0.005 | RESULTS §4-2 |
| STFT 도메인 비교(보코더 분리) | FD 귀무배수: GL 바닥 12.75, R0 8.68, D0 1038 | `data/eval_cache/stft_domain_compare.json` |
| DDIM 기제 | 첫 스텝 x̂₀ 증폭 641.7배, 24% 클램프 → D0 약점의 주원인은 설정 | `ddim_*.json`, `docs/URN_PROTOCOL_AUDIT.md` |
| URN 스케일 불변 재평가 | peak ratio: 실 5.72, R0 5.30, D0 3.51. 하모닉 초과분: R0 ≈ D0 (0.076 vs 0.079) | `urn_protocol_eval.json` |
| Xie2024 Table 10 분할 전사 | 논문 분할에서 **test 선박 59.3%가 train과 겹침** | `data/splits/xie2024_track_overlap.json` |
| DEMON 구현 검증 | 합성 AM 신호에서 피크 오차 0 Hz | `demon_validate.json` |

- 문서 결론: 통과한 체크포인트가 없다. "CFM > DDIM"이라고 썼지만, 격차의 기제는 DDIM 설정에 있다고 스스로 한정했다. 톤 구조 결손은 프레임워크와 무관하다고 결론냈다.
- 미실행 항목: R0′(시드 반복), R1(logit-normal), CFG 스윕, guidance.

## 5. 문제·의심점

1. **판정 규칙을 결과를 본 뒤 변경했다**(09-12). 9 체크포인트 중 6곳의 판정이 바뀐다. 문서에 투명하게 기록돼 있다.
2. seed 1개 → run 간 분산을 모른다.
3. R0/D0 비교가 불공정하다(clamp 6, ε-예측, ZTSNR·v-예측 미적용). "DDIM 성능"으로 인용하면 안 된다.
4. config 해시 드리프트: R0 학습 `f7c6…`, 평가 `c233…`, D0 `eed6…` `[확인]`
5. **"Acc가 실데이터의 80% 이상이면 통과" 규칙은 생성 Acc가 실데이터보다 높은 경우(0.71 > 0.62)도 통과시킨다.** 모드 축소를 성공으로 읽을 수 있다 `[추론]`.
6. PANNs(fmin 50 Hz)는 저주파 톤에 둔감하다. 주 지표가 모두 레벨에 반응한다.
7. 증강 없이 4,288 표본 → 30k step에서 모드 축소(다양성 139배 감소 `[문서]`)
8. 연속 조건값을 test 세그먼트에서 가져와 test와 비교한다(`cond_source: test`).
9. 3 Hz HPF 때문에 bin 0–3은 필터 롤오프를 학습한다(수정 보류).

## 6. 재사용 가치

- 코드: `src/deepship_cfm/metrics.py`(FAD·KAD·귀무·선박 bootstrap·기억 게이트), `src/features/demon.py`(DEMONet 구현, 논문 모호점 주석 포함), `experiments/urn_protocol_eval.py`, `experiments/stable_tones.py`
- 분할: `data/splits/xie2024_track.json`, `xie2024_shipsear_track.json`(원본 wav가 없어 로컬 적용 불가)
- 캐시: `data/eval_cache/`(GL 왕복 PANNs 임베딩 5360×2048, 톤 분류기)
- 체크포인트: `runs/{R0,D0}/ckpt/` 각 10개, 합계 5.6 GB
- 좋은 설계 요소: 실데이터도 같은 GL 왕복을 거치게 한 점, 귀무 분포, 선박 단위 bootstrap
