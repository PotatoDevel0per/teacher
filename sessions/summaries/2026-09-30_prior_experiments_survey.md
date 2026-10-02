# Session Summary

- 날짜: 2026-09-30
- 세션 주제: 이전 실험 폴더 6개 조사·정리
- 관련 프로젝트: `/jhlee/{DGM, deepship_analysis, UATR_SLM, deepship_preprocessing, ot-cfm, PG-MCLDM}`
- 관련 파일: `research/prior_experiments/`

## 사용자 질문

이전 실험 폴더들을 조사해 정리해 달라. 이 실험들은 Claude Code와 약식으로 진행해 타당성이 미검증이다. 사용자가 이해했다고 판단하지 말 것. 기초부터 다시 할 때 도움이 될 것을 남기는 것이 목적이다.

## 이번 세션에서 확정한 내용

- 이전 실험은 미검증 참고 자료로만 취급한다 (D-2026-09-30-01).
- 조사는 읽기 전용으로 했고 재실행하지 않았다.

## 새롭게 이해한 개념

없음. 이 세션은 조사만 했고, 사용자의 이해 수준은 평가하지 않았다.

## 아직 이해하지 못한 개념

`research/prior_experiments/concepts_to_learn.md` 전체 (수준 미확인)

## 실패 또는 문제

- 폴더마다 DeepShip 분할이 최소 4개다. 서로 호환되지 않는다.
- 생성기 실험이 모두 seed 1개다. 판정 기준을 사후에 바꾼 사례가 반복됐다.
- 생성 데이터의 UATR 기여는 선박 분리 조건에서 측정된 적이 없다.

## 새로 생성하거나 갱신한 파일

- 생성: `research/prior_experiments/{README, DGM, deepship_analysis, UATR_SLM, deepship_preprocessing, ot-cfm, PG-MCLDM, concepts_to_learn}.md`
- 갱신: `research/experiment_registry.md`, `research/open_problems.md`, `research/decisions.md`, `profile/learning_status.md`(주의 문구만), `handoffs/current_context.md`

## 다음 세션에서 할 일

- 단일 공식 분할과 ship_id 신뢰성 문제(OP1, OP2)를 어떻게 다룰지 논의한다.
- 최소 파이프라인 1단계(UATR baseline)를 설계한다. 출발점 후보는 UATR_SLM의 분할 누수 실험을 사용자가 직접 이해하고 재현하는 것이다.
- concepts_to_learn P1 개념부터 이해 수준을 확인한다.
