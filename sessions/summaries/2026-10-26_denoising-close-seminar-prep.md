# 세션 요약: 잡음 제거 분기 종료, 세미나 준비 (2026-10-26)

- 상태: **실험 일시 중지(사용자, 2026-10-26 16:3x UTC).** 사용자는 내일(10-27) 세미나 준비에 집중한다. CLS·DEN·GEN 모두 대기 중이고 GPU 2장은 비어 있다.

## 1. 오늘 결정

| 결정 | 내용 |
|---|---|
| D-2026-10-26-01 | 연구 서사: WAV 생성 목표 → 분할 누출과 선박 암기 발견 → 분할·분류기 점검을 먼저 하고 LDM 물리 기반 증강 → WAV 복원은 마지막 |
| D-2026-10-26-02 | **잡음 제거 앞단을 넣지 않는다. R-US-T는 하지 않는다.** |
| LMR-ships | 사용자 결정으로 중단(16:19 UTC), 결과 없음 |
| R-US-T 판정 정의 | DeepShip DC 발견으로 b1_dc를 결과 보기 전에 수정(커밋은 보존, 취소로 미사용) |

## 2. 오늘 결과

| 실험 | 결과 |
|---|---|
| UniqueShip 전체 잡음 제거(R-US) | 153,595 클립. 지운 에너지 선박 78%, 배경 87%, tonal 보존 |
| R3-US (UniqueShip fold1 분류) | **불명확**: 66.05 → 66.13 (+0.09, seed별 +1.20 / −0.63 / −0.31) |
| DeepShip DC 발견 | 정답 클립 에너지의 98%가 DC. R2b·R2c의 "−5 dB"는 교류 기준으로 약 −22 dB였다. DC를 빼면 ShipsEar 모델의 SDRi는 7.07(통과) |
| R3-DS-DC (DC 제거 입력) | **해로움**: 58.18 → 53.84 (−4.34, 5/5 fold). 클래스별 Passenger −8.8이 가장 큼 |
| DC 미제거 입력의 저주파 인공물 | 그림으로 확인(`research/figures/seminar_S15b_r3ds_vs_r3dsdc.png`) |
| LMR 원문 분할 누출 규모 | train+val segment의 64.6%가 test 선박 녹음 |
| 정정 | EXP-002-PC last-epoch Δ −7.1 → −8.40(Teacher 계산 오류) |

## 3. 세미나 산출물

- 최신 패키지: `scratchpad/seminar_pkg_v2.zip`
  - `PROMPT_for_PPT_session.md`
  - `seminar_slides_v2.md`
  - `figures/` 24개
- KB 사본: `research/seminar_slides_v2.md`, `research/seminar_ppt_prompt_v2.md`, `research/figures/`
- 이전 판: `research/seminar_outline_draft.md`(v3, 실험 중심), `research/seminar_outline_v2_paperflow.md`
- 서론 초안(논문용): `research/paper_drafts/icassp_intro_ko.md`(확인된 사실만), `icassp_intro_draft.md`(영문)

## 4. 다음에 할 일 (세미나 뒤)

1. **E1-AE 재개 방식을 사용자와 상의한다.**
   - 현재 22/30, L1 AE는 DeepShip에서 기준 미달이고 질감이 뭉개진다.
   - Teacher 추천: 남은 8개를 마저 돌리고, 그동안 patch adversarial 손실 버전을 준비한다.
2. **디스크 정리 결정을 받는다.**
   - /jhlee 97% 사용, 여유 247 GB
   - 후보:
     - UniqueShip 잡음 제거 결과 47 GB
     - DEN data_mix 46 GB
     - DeepShip 잡음 제거 결과 11 GB × 2
     - E1-src 캐시 26.6 GB(지워도 된다고 답변함, 사용자 확인 대기)
     - 잡음 제거 분류 캐시(용량 미확인)
3. E1-src를 seed 3개로 늘릴지 정한다(논문용, 선택).
4. 세미나 피드백(지도교수 확인 사항)을 decisions에 반영한다.
