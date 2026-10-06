# Session Summary

- 날짜: 2026-10-02 ~ 2026-10-06
- 세션 주제: 연구 목표 전환(WAV 생성 → 물리 기반 증강), UniqueShip 확보, DEMON/LOFAR 개념 학습
- 관련 프로젝트: `/jhlee/UATR_SLM` (다른 세션 `UATR_SLM_REPLAY`), `/jhlee/data/uniqueship`

## 확정한 내용

- D-2026-10-06-02: 1순위는 물리 기반 증강으로 UATR의 누출 없는 일반화를 개선하는 것이다. WAV 생성은 후순위다. 지도교수 승인은 미확인이다.
- D-2026-10-06-01: 생성 트랙은 LDM을 먼저 하고 LFM을 나중에 한다.
- D-2026-10-02-01: obsolete 처리했다.
- 용어 표기 규칙: tonal / window / narrow·broad (`profile/preferences.md`)

## 논문 근거 (원문 확인)

- UniqueShip (arXiv:2609.13659)
  - 누출 없는 baseline: Swin Mel 0.665 ± 0.012
  - 선박 수 2배 = +2.4–2.6 pp, 시간 2배 = +0.8–1.3 pp
- Hashmi & Raza 2023 (JEET)
  - PSD를 보고 샘플마다 band-pass를 수동 선택한다
  - DEMON에서 SRPM·NOB·NOS를 추출한다
  - NOB 정확도는 보고하지 않았다
- DEMONet: 백본은 ResNet-18, baseline은 CQT 77.15%(누출 분할)
- Gao 2024 서베이: 사용자가 잘못 준 파일이었다. 잡음 제거 서베이이고, EWT 같은 적응 대역 방법을 소개한다.

## 데이터

UniqueShip 12C-5h(26 GB)와 5C-Balanced(93 GB)를 받고 무결성을 확인했다. 기록은 `research/datasets/uniqueship.md`에 있다.

## 다른 세션에서 받은 결과

`handoffs/2026-10-05_from_UATR_SLM_REPLAY.md`
- 분할 연구: DeepShip 98.02 → 52.80
- UniqueShip 분류기 비교: 누출이 없는 조건에서 모델 간 차이가 유의하지 않다
- FunASR seed 버그

## 새롭게 이해한 개념

DEMON의 포락선(변조) 개념: exposed → basic. 근거는 `profile/learning_status.md`에 있다.

## 아직 이해하지 못한 개념

- DEMON band-pass의 역할
- LOFAR 주파수 분해능(Δf와 window length)

## 새 가설

H-AUG-1/2/3, H-PRE-1/2/3 (`research/hypotheses.md`)

## 다음 세션에서 할 일

- EXP-001(UniqueShip Swin 재현) 결과 판정
- 분류기 3종 계획 확정
- 물리 기반 증강 문헌 조사
- 지도교수 확인용 1쪽 요약(제안함, 미작성)
- 이해 확인 질문: 5 s 클립에서 0.25 Hz 떨어진 tonal을 구분할 수 있는가
