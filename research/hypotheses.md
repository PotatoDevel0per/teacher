# Hypotheses

## 후보 연구 주제: 물리 조건부 latent Flow Matching (2026-09-30 검토)

출처: 사용자가 가져온 외부 AI 답변. 원문 논문(LDM, AudioLDM, AudioLDM 2, Flow Matching)은 이 지식베이스에서 아직 원문 확인을 하지 않았다 → 인용 내용은 `unknown`.

| ID | 가설 | 상태 | Claude 평가 (`inferred`) |
|---|---|---|---|
| H-LFM-1 | latent 생성이 waveform 생성보다 같은 계산량에서 스펙트럼 오차가 낮다 | hypothesis | 인접 분야 근거가 있다. UATR 기여와는 거리가 멀다 |
| H-LFM-2 | 같은 latent에서 CFM이 diffusion보다 적은 step으로 비슷한 품질을 낸다 | hypothesis | 일반 생성 분야의 질문이다. 이전 실험에서는 CFM과 DDPM-v의 차이가 CI 안이었다(PG-MCLDM E2 vs E6) |
| H-LFM-3 | RPM·블레이드 수 조건을 추가하면 DEMON peak 오차가 줄어든다 | hypothesis | **DeepShip에는 RPM·블레이드 정답 라벨이 없다.** 신호에서 추정한 조건으로 같은 신호 특성을 평가하면 순환 논증이 된다. PG-MCLDM에서 생성물의 DEMON 신뢰비는 0.007–0.018이었다. DEMONet(2411.02758)은 블레이드 수를 추정·평가하는 논문이 아니다(원문 부분 확인, 2026-10-02) |
| H-LFM-4 | 물리 조건부 생성 데이터가 unseen-vessel UATR을 더 개선한다 | hypothesis | 연구 목표와 가장 직접 연결된다. 전제로 선박 분리 분할, UATR baseline, 비생성 증강 baseline이 필요하다 |

## 판단 보류 사유

- 이 설계는 PG-MCLDM(`research/prior_experiments/PG-MCLDM.md`)에서 이미 약식으로 시도됐다. 실패 원인이 생성기 선택(FM vs diffusion)에 있다는 증거는 없다.
- H-LFM-3과 H-LFM-4를 판정할 지표(DEMON peak error, LOFAR similarity, tonal F1)가 검증되지 않았다 (`research/open_problems.md` OP6).

## 후보 연구 주제: 물리 특성을 반영한 데이터 증강 (2026-10-05 검토, 사용자 제안)

| ID | 가설 | 근거 등급 | 상태 |
|---|---|---|---|
| H-AUG-1 | 누출 없는 분할에서 범용 증강(SpecAugment, mixup 등)의 효과는 작다 | 인접 근거: UniqueShip의 "시간 2배 = +0.8–1.3 pp". PG-MCLDM의 SpecAugment+mixup +0.3 pp(누출 분할, seed 1) | hypothesis |
| H-AUG-2 | 선박 간 변이(새 선박처럼 보이는 변이)를 만드는 물리 기반 증강은 범용 증강보다 unseen-vessel 정확도를 더 높인다 | UniqueShip의 "선박 2배 = +2.4–2.6 pp"에서 영감을 받은 가설. 직접 근거 없음 | hypothesis |
| H-AUG-3 | 클립별 레벨 정규화(절대 레벨 제거)가 선박 분리 조건의 일반화를 돕는다. 즉 절대 레벨은 녹음·거리 지름길이다 | 이전 실험 근거: UATR_SLM D3 +2.83 pp (seed 3), UniqueShip clf 비교(교란 있음, 유의하지 않음) | hypothesis |

- 판정 전제: UniqueShip 5C-Bal 누출 없는 분할과 Swin Mel baseline(0.665 ± 0.012)을 재현해야 한다.
- 어떤 증강이 "물리 특성을 반영"하는지는 아직 정의되지 않았다. 문헌 조사가 필요하다.

## 전처리 후보: 샘플별 적응형 대역 선택 (2026-10-06 검토, 사용자 제안)

- 정정 (2026-10-06): 사용자가 처음 준 논문(서베이)은 잘못된 파일이었다. 의도한 논문은 Hashmi & Raza 2023이다. 이 논문은 **샘플마다 다른 대역**을 PSD를 보고 **수동으로** 정한다. 목적은 LOFAR 토널 보존이 아니라 DEMON용 캐비테이션 대역 분리다.
- H-PRE-3 (hypothesis): DEMON용 band-pass 대역을 자동으로 정할 수 있다(포락선 SNR 최대화, spectral kurtosis 등). 사람이 PSD를 보고 정한 대역과 비슷하거나 더 나은 SRPM 추정을 낸다. 근거: Chung 2011, Pollara 2016(원문 미확인). 검증: UniqueShip background + 합성 AM 신호(fm·NOB를 알고 있음)로 fm 오차를 잰다.

| ID | 가설 | 근거 등급 | 상태 |
|---|---|---|---|
| H-PRE-1 | 모든 샘플에 같은 고정 band-pass를 쓰면 일부 선박의 토널·고조파가 대역 밖에서 손실된다 | 합리적 가설. 손실 정도는 대역 설정에 따라 다르다. 직접 측정 없음 | hypothesis |
| H-PRE-2 | 샘플별 적응형 대역 선택(EWT 등)이 고정 대역보다 누출 없는 UATR 성능 또는 토널 보존을 개선한다 | 인접 분야 근거(서베이: 분해 기반 잡음 제거). 선박 분리 조건의 직접 근거 없음 | hypothesis |

- 위험: 샘플별 필터 경계가 녹음 환경 정보를 담으면 새로운 지름길이 될 수 있다(H-AUG-3과 같은 계열).
- 검증 방법 후보: UniqueShip background 클래스 + 알려진 합성 토널을 섞은 준합성 데이터로 토널 회수율을 측정한다.
