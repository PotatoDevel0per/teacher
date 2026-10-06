# Open Problems

## 이전 실험 조사에서 드러난 문제 (2026-09-30)

출처: `research/prior_experiments/`. 모두 미해결이다.

| # | 문제 | 근거 | 상태 |
|---|---|---|---|
| OP1 | **단일 공식 DeepShip 분할이 없다.** 폴더마다 분할이 4개 이상이고 서로 호환되지 않는다. | prior_experiments/README §2 | unknown: 어떤 분할을 쓸지 미결정 |
| OP2 | `ship_id.csv`가 출처 불명의 휴리스틱 매칭이다. 잘린 선박명(예: "QUEEN OF" 35 녹음)이 있다. 선박 수가 244 / 254 / 265로 문서마다 다르다. | deepship_analysis, preprocessing | unknown: 선박 단위 분할의 기반이 불확실 |
| OP3 | 선박 분리 분할에서 소수 클래스(Tug)의 test 선박이 2–5척뿐이다. 클래스별 평가의 CI가 매우 넓다. | UATR_SLM, DGM, preprocessing | unknown |
| OP4 | 선박 분리 조건에서 UATR 성능 상한이 어디인지 모른다. SLM 50%는 하이퍼파라미터를 재조정하지 않은 값이다. | UATR_SLM | hypothesis |
| OP5 | 녹음 환경 지름길(정적 스펙트럼 형상)의 정체를 모른다. | UATR_SLM D1/D3, DGM gate1 | hypothesis |
| OP6 | 토널 구조 보존을 평가할 검증된 지표가 없다. 후보는 peak-N 일치율, tonal F1, 안정 톤 bin, peak ratio 등이지만 서로 비교·검증되지 않았다. | analysis, ot-cfm, PG-MCLDM | unknown |
| OP7 | 범용 임베더(PANNs) 기반 FAD/KAD는 저주파 토널에 둔감하고 레벨에 민감하다. 대안이 없다. | ot-cfm, DGM | hypothesis |
| OP8 | 생성 데이터의 UATR 기여가 선박 분리 조건에서 한 번도 측정되지 않았다. | 전체 | unknown |
| OP9 | 논문 재현 gap이 미해결이다: UATR-SLM −1.58 pp, DEMONet 분류기 −4.9 pp. | UATR_SLM, PG-MCLDM | unknown |
| OP10 | 논문 분할 자체에 선박 누수가 있다(Xie2024 track 59%, DEMONet Table 10 74%). 논문 수치와 선박 분리 결과를 어떻게 비교할지 정해지지 않았다. | ot-cfm, PG-MCLDM | unknown |
| OP11 | "음향학적으로 타당한 WAV"의 정의와 판정 기준이 없다. 어떤 성분(토널, 광대역, DEMON, 시간 변화)을 어떤 지표와 임계로 판정할지 정해야 한다. | D-2026-10-02-01 | unknown: 1차 목표의 선행 과제 |
| OP12 | 블레이드 수·축 회전수의 정답 라벨이 DeepShip에 없다. DEMON 추정값을 조건과 평가에 동시에 쓰면 순환 논증이 된다. | hypotheses.md H-LFM-3, DEMONet 노트 | unknown: Hashmi & Raza 2023을 확인했으나 NOB 정확도와 공개 정답이 없음. Chung 2011, Pollara 2016 원문 확인 필요 |
