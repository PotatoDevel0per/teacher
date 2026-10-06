# Learning Status

> **주의 (2026-09-30)**: 이전 실험 폴더(`research/prior_experiments/`)에 쓰인 개념은 이해 수준의 근거로 쓰지 않는다. 그 실험들은 Claude Code와 약식으로 진행한 것이다. 사용자는 설명할 수 없는 공백이 많다고 직접 밝혔다. 필요한 개념 목록은 `research/prior_experiments/concepts_to_learn.md`에 있다. 등급은 개념별로 직접 확인한 뒤에만 올린다.

## 상태 등급

- unknown: 아직 접하지 않음
- exposed: 용어를 봤지만 설명하기 어려움
- basic: 기본 개념을 설명할 수 있음
- working: 간단한 실험을 수행할 수 있음
- research-ready: 비판적 비교와 변형이 가능함

## 수중음향

| 개념 | 현재 수준 | 근거 | 다음 학습 |
|---|---|---|---|
| 선박 방사소음 | exposed | 기본 용어 확인 | 발생 원인과 성분 구분 |
| broadband 소음 | unknown |  |  |
| tonal | exposed |  | tonal 추적 실험 |
| 캐비테이션 | unknown |  |  |
| PSD | basic | 신호처리 경험 | URN 분석 적용 |
| LOFARgram | exposed | 2026-10-06: 시간-주파수 표현이라는 점은 안다 | 긴 window와 Δf, 배경 정규화 |
| DEMON 분석 | basic | 2026-10-06 질문 1: 시간 집계 차이로 오해했다. 질문 2: "세기가 일정하면 포락선이 평평하다"를 스스로 설명했다 → 포락선(변조) 개념을 획득했다. band-pass의 역할(대역 밖 tonal 제거, 제곱에 의한 가짜 tonal 방지)은 아직 설명하지 못했다 | band-pass 대역 선택, 실제 DeepShip/UniqueShip 클립에 적용 |
| 다중경로 | unknown |  |  |

## 생성모델

| 개념 | 현재 수준 | 근거 | 다음 학습 |
|---|---|---|---|
| GAN | working | 기존 딥러닝 경험 | 오디오 GAN |
| Diffusion | working | 생성모델 연구 | waveform diffusion |
| Flow Matching | exposed | 연구 관심 | 수식과 학습 절차 |
| Vocoder | exposed | 관련 논문 조사 | 수중음향 보코더 |
| FAD | exposed | 생성 평가 조사 | 임베더 의존성 |
| KAD | unknown |  | 분포 가정 비교 |

## 실험 능력

- 데이터 전처리: working
- PyTorch 학습: working
- UATR baseline: 미확인
- 오디오 waveform 분석: basic
- STFT 분석: basic
- 생성 모델 재현: exposed