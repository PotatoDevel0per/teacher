# deepship_analysis — DeepShip 원본 분석과 보코더 왕복 검증

- 경로: `/jhlee/UWShipNoise/data_analysis/deepship_analysis` (962 MB, git 없음)
- 기간: 2026-09-04 ~ 09-09. 요청서는 `docs/deepship_analysis_prompt.md`다.
- 성격: 데이터 특성 분석. 분류·생성 학습은 하지 않았다(HiFi-GAN fine-tune만 예외).
- 전체 상태: `hypothesis`. 핵심 수치는 Claude가 계산했고 교차 재현이 없다. 표기 규칙은 [README.md](README.md) §0.

## 1. 데이터 인벤토리 `[확인]` (`deepship_analysis/file_manifest.csv`, 609행)

- sr 32000, mono. FLOAT 605, PCM_24 4
- 길이: min 6 s, median 263 s, max 1887 s(문헌 1530 s)
- 고유 ship_id 244척(문헌 265), 미매칭 10개. 클래스별 선박 수: Cargo 62, Passenger 43, Tanker 123, Tug 16
- AIS 거리 가용 571개
- **DC 파워 비율 중앙값 0.968.** 474개 파일에서 DC가 파워의 90%를 넘는다. DC를 제거하지 않으면 분석 결과가 아티팩트가 된다.
- ship_id는 날짜·시각 휴리스틱 매칭이다(`/jhlee/UWShipNoise/data/deepship/ship_id.csv`, 출처 불명). "QUEEN OF"(35 녹음)처럼 잘린 선박명이 있다.

## 2. 분석 목록 `[문서]`

| Task | 내용 | 결과 |
|---|---|---|
| A. CPA/거리 (`01_cpa_analysis.md`) | 클래스와 무관한 거리 축이 있는가 | 지지: 레벨차와 AIS 거리비의 r=0.823. "파일 = 완전한 통과, CPA가 중앙" 전제는 기각(CPA 위치가 U자형, 양끝 5%에 44.6%). "원거리 = 저역통과"도 반대 방향으로 기각. 원거리에서도 톤 prominence는 유지됨 |
| 톤 검출 교정 (`04_*addendum.md`) | 요청서의 3 dB 임계 검증 | 순수 잡음에서 프레임당 779개 오경보 → 몬테카를로로 임계 교정. 블레이드율 간격을 복원하려면 Δf ≤ 0.49 Hz, 8 s 적분이 필요 |
| B. 세그먼트 길이 (`02_*.md`) | 30 s 안의 거리 변화 영향 | 레벨 변동 3.4 dB 중 거리 몫 0.18 dB. 판정 보류 |
| C. 누수 3계층 | 미실행 (source-disjoint로 가기로 결정) | 분할 실현 가능성만 측정: 무작위 선박 분할의 5%에서 test에 빠지는 클래스가 생김. 세그먼트 기준 명목 CI가 실효 CI보다 약 4배 좁음 |
| V. 보코더 왕복 (`05_*.md`, 180 세그먼트) | 복원 경로별 저역 top-20 피크 일치 | mel+HiFi-GAN 22.6% (우연 21.88%, 구별 불가), mel+GL 27.5%, 선형+GL(n_fft 1024) 54.0%, 선형 n_fft 16384+GL 93–95% |
| V-8. HiFi-GAN fine-tune (30k step) | 재학습하면 톤이 회복되는가 | recall 19.8–20.4%로 회복되지 않음 `[확인]` (`cache/ft_eval_summary.csv`). 판별기 포화를 문서가 인정 |

## 3. 문제·의심점

- 검출기 결함으로 문서가 여러 번 정정됐다(rev2, "결론 21 철회"). 결론이 방법 파라미터에 민감하다는 신호다.
- 보코더 결론은 16 kHz와 특정 mel 규약에 한정된다. 일반 신경 보코더 전체에 대한 결론이 아니다.
- 청취 평가는 없다.

## 4. 재사용 가치

- `file_manifest.csv`, `per_file_cpa.csv`, `cache/metafile_parsed.csv`
- **peak-N 일치율 + 우연 바닥(null) + skill score**로 톤 보존을 평가하는 방식(`scripts/tv_common.py`). 토널 평가 지표 정의의 출발점 후보다.
- 전처리 원칙 "DC 제거 + 3 Hz HPF"의 근거
- 보코더 손실 분해 설계(A/P/B/L/C/D 경로): 무엇이 톤을 잃게 하는지 단계별로 분리하는 방법

## 5. 연구 목표와의 연결 (`inferred`)

"Mel 기반 생성 결과를 WAV로 복원하면 토널 구조가 손상될 수 있다"는 현재 가설(`handoffs/current_context.md`)에 대해, 방향이 같은 예비 증거를 준다. 다만 이것은 방향을 맞추는 증거일 뿐이다. 설정을 바꿔 재현하기 전까지는 `hypothesis`로 둔다.
