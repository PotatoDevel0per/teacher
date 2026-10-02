# deepship_preprocessing — 조건부 생성용 9-stage 전처리 파이프라인

- 경로: `/jhlee/deepship_preprocessing` (29 GB, git 없음)
- 기간: 2026-09-08(코드) ~ 09-09(산출물·실험). `DECISIONS.md` "복원 방식 확정 (2026-09-09)"
- config sha256 c66591420b44…, seed 20260908, python 3.11.9 / scipy 1.17.1 / librosa 0.11.0 `[확인]`
- 전체 상태: `hypothesis`. 표기 규칙은 [README.md](README.md) §0.

## 1. 파이프라인 `[확인]` (`config.yaml`)

| Stage | 내용 | 산출물 |
|---|---|---|
| 1 | 32 → 16 kHz Kaiser FIR polyphase(1301탭), 3 Hz 4차 sos zero-phase HPF | `stage1/` 11 GB |
| 2 | 30 s 비중첩 세그먼트. 30 s 미만 파일과 선박 미매칭 파일 제외 → 510 녹음, 5,360 세그먼트 | `segments.parquet` |
| 3 | 조건 변수 후보: 레벨, 스펙트럼 기울기, AIS 쌍곡선 거리 보간(`r_interp_m`, `r_cpa_m`, `v_ms`) | `conditions.parquet` (보간 해가 서는 경우 54.2%) |
| 4 | 선박 분리 분할(아래) | `splits/` |
| 5 | train 전용 bin별 dB 정규화 통계 | `norm_stats/` |
| 6 | 2-stream: 저역 0–2 kHz(n_fft 16384, hop 2048, 2048×235), 고역 1937.5–8 kHz(n_fft 512, hop 256, 194×1876). 복원은 SPSI 초기 위상 + 스트림별 GL 128 + 공동 GL 32 | `repr/` |
| 7 | 4096 Hz LOFAR 톤 텐서 [2000×15], TPSW + 해석적 CFAR | `tonal/` |
| 8 | 5 s 판정자 클립 32,160개(부모 분할 상속) | `judge_clips/` 9.7 GB |
| 9 | 무결성 16항목 PASS | `stage9_integrity.json` |

## 2. 분할 (`deepship_pipeline/splits/`)

- `ship_disjoint.json`: 클래스별 8:1:1, 클래스당 test/val 최소 2척, 재시작 4000회, split_seed 42. val 18척, test 31척. **test Tug 2척/7녹음** `[확인]`
- `segment_random.json`: 누수 대조군(녹음 276, 선박 150 공유)
- **UATR_SLM 분할과 다르다**: 공통 선박 220척 중 fold 일치 121척. 이 파이프라인의 train 선박 62척이 UATR_SLM에서는 val/test다 `[확인]`.

## 3. 부속 실험 (40 세그먼트 층화 표본) `[문서]`

| 로그 | 실제 내용 | 결과 |
|---|---|---|
| `exp_gl` | GL 반복 수, 저역 hop | LSD 32회 5.37 → 1024회 3.68 dB, 256회 이후 평탄 |
| `exp_judge` | **이름과 달리 GL 설정 6종 비교** (로그 태그 `exp.gl`) | 반복을 128 → 512로 늘리면 LSD는 좋아지고 톤 지표는 나빠짐 → "LSD는 톤 보존의 대리지표가 아니다" |
| `exp_repr` | SPSI 대 랜덤 초기화, 조합 순서, hop | SPSI 이득 없음(p > 0.38). 공동 GL은 필수(빼면 경계 편차 2.63 → 3.99 dB) |
| `exp_power` | 트랙 길이 지표 W1의 판별력 | 절대 기준 ≤ 1 프레임은 판별력 없음. 기준 재설정 미결 |
| `exp_bnd` | 대역 접합부(1.8–2.2 kHz) 편차 | 2.633 dB, 대조 대역과 구별 불가(p = 0.25). 원인은 접합이 아니라 고역 GL 오차 |
| `exp_peak` | 저역 5–250 Hz top-20 피크 일치 | 중앙값 0.95 (우연 0.15). 95%는 거의 전부 n_fft 16384 덕분이고 대역 분할 기여는 +0.1%p |

## 4. 문제·의심점

- test Tug 2척 → 실효 CI ±14%p `[문서]`
- AIS 매칭 커버리지가 폴더마다 다르다(599 대 571). 거리 보간의 45%는 비정상해다.
- 조건 변수 중 무엇을 primary로 쓸지 정하지 않았다. `v_ms`는 클래스와 교락돼 있다(MI가 H(class)의 15%).
- "95% 톤 일치"는 피크 위치 일치일 뿐이다. 고역 품질과 청취 품질은 미보장이다(청취 평가는 "양호(주관)"뿐).
- 9.5–16 kHz 대역이 데시메이션으로 제거됐다. 174 녹음에서 이 대역 파워가 1%를 넘는다.

## 5. 재사용 가치

- `src/deepship_prep/`: `dsp.py`(FIR 데시메이션, sos HPF), `tones.py`(TPSW, CFAR, 트랙), `geometry.py`(CPA 보간), `stage4_splits.py`(제약 붙은 선박 분할), `spsi.py`, `stage6_repr.py`
- `recordings.parquet`, `segments.parquet`, `conditions.parquet`, `stage1_audio_stats.csv`, `norm_stats/`
- `DECISIONS.md`: 복원 설정과 그 근거
- ot-cfm은 이 산출물을 읽기 전용으로 소비한다. PG-MCLDM은 `src`를 import한다.
