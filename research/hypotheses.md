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
