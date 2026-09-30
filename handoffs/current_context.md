# Current Research Context

## 연구 목표

WAV 파형으로 복원 가능한 수중 표적 선박 소음 생성 및 평가 파이프라인을 연구한다.

## 현재 핵심 질문

수중 표적 선박 소음을 생성할 때, WAV 파형 복원 가능성·토널 구조 보존·분포 유사성·UATR 성능·도메인 일반화를 함께 검증하려면 어떤 평가 체계가 필요한가?

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
- [ ] UATR baseline
- [ ] feature-space augmentation 재현
- [ ] WAV 복원 baseline
- [ ] 토널 평가 지표
- [ ] 도메인 특화 임베더
- [ ] 통합 실험

## 현재 막힌 문제

1.
2.
3.

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