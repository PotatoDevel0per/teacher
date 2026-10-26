# 세미나 발표안 — 논문 흐름, 슬라이드별 (2026-10-26 재정리)

- 가정: 연구실 세미나 25분 + 질의 10분, 본문 16장 + 부록, 서론 약 7분 / 결과 약 12분 / 계획·논의 3분. 발표 시간·청중이 다르면 조정한다.
- 표시: 슬라이드마다 [완료] / [진행 중] / [계획]. 이전 실험은 [미검증].
- 용어: tonal, broadband, window, beating, Rec-disjoint(녹음 단위 분할), Ships-disjoint(선박 단위 분할).
- 10-26 오후 수정: 서론(2–5번)을 논문 서론 흐름으로 다시 씀(연구 필요성 → 데이터 병목 → 누출 → 생성 모델 필요성), 참고문헌 표 추가. 재현 슬라이드는 4번에, "왜 게이트부터인가"는 7번에 합침.
- 10-20판과 달라진 점: E1-rep·E1-src 판정 완료, E1-src-CQT 추가, 잡음 제거 앞단 실험(FocuS-MN 재현 → R3-DS → R-US) 추가, E1-AE 중간 결과 추가. tonal·DEMON 평가기는 한 장으로 합쳤다.
- 발표 전날 채울 것: R3-US(UniqueShip fold1) 판정, E1-AE 재개 여부.

---

## 1. 제목 (0.5분)

- 국문: 선박 분리 조건의 수중 표적 인식을 위한 물리 특징 조건부 잠재 확산 증강
- 영문: Physics-Conditioned Latent Diffusion Augmentation for Ships-disjoint UATR
- 부제: 연구 진행 보고 — 프로토콜·평가기·기준선, 그리고 입력 표현 점검

> 서론 흐름(2–6번, 약 7분): **왜 수중 선박 소음 인식인가 → 왜 어려운가(데이터) → 지금 평가는 믿을 만한가(누출) → 기존 증강으로 충분한가 → 왜 생성 모델인가.** 슬라이드마다 근거 등급을 작게 적는다(참고문헌 표는 이 문서 끝).

## 2. 서론 ① 왜 수중 선박 소음 인식인가 [문헌] (1.5분)

- 핵심 메시지: **선박 소음은 해양 환경 문제이자 해양 감시의 핵심 신호다. 이를 자동으로 듣고 구별하는 기술(UATR)이 필요하다.**
- 근거:
  - 산업혁명 이후 인위적 해양 소음이 늘었고, 해양 생물의 행동·생리에 영향을 준다. 해운이 주요 원인이다 [R1 Duarte 2021, Science]
  - 국제 규제 흐름: IMO 선박 수중 방사소음 저감 지침 2014(MEPC.1/Circ.833) → 2023 개정(MEPC.1/Circ.906, 신조선·기존선 모두 대상, 소음 관리 계획 도입) → 2024 Rev.1. 2026년까지 "경험 축적 단계" [R2 IMO]. 비강제 지침이다
  - 소음을 줄이고 관리하려면 먼저 "어떤 선박이 어떤 소리를 내는지" 측정·식별해야 한다 → 수동 소나 기반 표적 인식(UATR) [R3 Feng 2024, R4 Muller 2024 서베이]
- 응용(민간·방어·교육): 해양 소음 모니터링, 해상 교통 감시, 소나 운용자·선원 교육용 음향 자료
- 발표 노트: "왜 이 분야를 연구해야 하는가"에 대한 답이다. 근거는 환경(R1)과 제도(R2), 기술 동향(R3·R4) 세 갈래다.

## 3. 서론 ② 왜 어려운가: 데이터가 작고 비싸다 [문헌 + 재현] (1.5분)

- 핵심 메시지: **딥러닝 UATR은 데이터가 병목이다. 공개 데이터는 선박 수가 적고, 새로 모으기도 어렵다.**
- 표: 공개 데이터 규모

| 데이터 | 규모 | 출처 |
|---|---|---|
| ShipsEar | 90 녹음, 11 선종, 약 3 h(스페인 대서양 연안 2012–2014) | R5 Santos-Domínguez 2016 |
| DeepShip | 약 47 h, 265척, 4클래스(Strait of Georgia) | R6 Irfan 2021 |
| UniqueShip(프리프린트) | 2,460 h, 4,218척 — 대규모로 모으면 성능이 오른다 | R7 Hashemi 2026 |

- 수집이 어려운 이유: 하이드로폰 장기 운용 비용, AIS 대조 라벨링, 거리·해황·다른 선박 간섭, 비공개 데이터
- 서베이도 "제한된 표본·클래스 불균형·저 SNR"을 핵심 문제로 들고, 해결책으로 데이터 증강·전이학습을 꼽는다 [R8 Domingos 2022, R9 Yan 2026(초록)]
- 연결: UniqueShip에서 **선박 수 2배 +2.4–2.6 pp, 같은 선박 녹음 시간 2배 +0.8–1.3 pp** [R7 Fig. 4] → 필요한 것은 "더 많은 선박"이다

## 4. 서론 ③ 지금의 평가는 믿을 만한가: 누출 [선행연구 + 재현] (1.5분)

- 핵심 메시지: **같은 선박이 train과 test에 함께 있으면 정확도가 약 12 pp 부풀려진다. 분류기는 클래스가 아니라 개별 선박·녹음을 외운다.**
- 그림: 막대 3개 — DeepShip Swin Mel Rec-disjoint 0.710 / Ships-disjoint 0.588 [R7 Table II] / 우리 재현 Ships-disjoint 0.593(F1 58.18 ↔ 원문 0.563)
- 보강 근거: 사전학습 오디오 임베딩 16종의 공간은 선박 종류보다 **녹음 ID**로 묶인다(NMI 0.62 vs 0.13) [R10 Hummel 2026]
- 서베이도 "성능이 분할 방식에 매우 민감하다"고 정리한다 [R9 초록]
- 우리 재현: 코드 회귀 UniqueShip acc 68.40 ± 2.46(원문 범위 안), 이전 실험과 비트 단위 일치 → 이후 모든 결과는 Ships-disjoint로 판정한다
- 가설 H-SC-1: Rec-disjoint에서 분류기는 선박 고유 단서를 쓴다

## 5. 서론 ④ 기존 증강으로 충분한가 → 왜 생성 모델인가 [문헌] (2분)

- 핵심 메시지: **기존 증강은 "같은 선박의 변형"이고 대부분 누출 분할에서 평가됐다. 새 선박 같은 변이를 만들려면 데이터 분포를 배우는 생성 모델이 필요하다.**
- 기존 증강의 현황 [R11 자체 문헌 조사 21편, 분할 확인 9편]:
  - 분할: 세그먼트·샘플 무작위 5, 녹음 단위 3, 시간순 1, **선박 단위 0**
  - 보고 이득: 무작위 분할의 GAN 증강 +6–12 pp vs 녹음 단위 분할의 생성 증강 +0.5–1.3 pp. 백색잡음 증강은 효과 없거나 악화 [R12 Xu 2023]
  - 해석(inferred): 누출이 줄수록 증강 이득도 줄어든다. 선박 단위에서의 효과는 아직 아무도 재지 않았다 → **연구 공백**
- 왜 생성 모델인가(논리):
  1. 필요한 것은 선박 수(3번) → 기존 녹음을 자르고 섞는 증강은 선박 수를 늘리지 못한다
  2. 생성 모델은 클래스 분포를 배우고, 조건을 바꿔 학습에 없던 조합을 만들 수 있다(가설 — 이 연구가 검증할 것)
  3. 물리 조건(tonal, DEMON, broadband 모양)을 주면 "그럴듯하지만 새로운" 선박을 통제해서 만들고, 물리 평가기로 확인할 수 있다
- 기술 동향:
  - LDM: AE로 압축한 latent에서 diffusion, cross-attention 조건화 → 고해상도 생성을 낮은 비용으로 [R13 Rombach 2022]
  - 오디오에서도 LDM 계열이 표준이 됨(예: AudioLDM) [R14, 서지 확인 필요]
  - 인접 분야: 확산 모델 합성 데이터로 ImageNet 분류가 좋아졌다는 보고 [R15, 서지 확인 필요]
  - 수중음향: JASA·JASA-EL 공동 특집 "Generative and Physics-Informed AI for Acoustics"(2026, 수중음향 포함) [R16]. 같은 흐름의 생성 증강 논문(LR-VAE, few-shot, 녹음 단위 분할) [R17 Huang 2026]
- 발표 노트: 동향은 "생성 모델이 유행이다"가 아니라 "물리 정보를 넣은 생성이 음향 분야의 공식 의제가 됐다"는 근거로 쓴다. 근거 등급: 1·3번은 직접 근거 있음, 2번은 가설, R15는 인접 분야 근거.

## 6. 연구 질문과 기여 (1분)

- 연구 질문: **물리 조건부 생성 모델로 만든 "새 선박 같은" 샘플이 Ships-disjoint UATR 성능을 올리는가?**

| | 기여 | 상태 |
|---|---|---|
| C1 | DeepShip·ShipsEar의 검증된 Ships-disjoint 5-fold 프로토콜 | 완료 |
| C2 | 생성물 평가용 물리 평가기 검증(tonal, DEMON의 beating 문제와 CPW) | 완료 |
| C3 | Ships-disjoint에서 클래스 정보는 어디에 있는가(broadband vs tonal) | 완료(일부 보류) |
| C4 | 고정 잡음 제거 앞단이 Ships-disjoint 인식에 주는 효과 | 진행 중 |
| C5 | 물리 조건부 LDM 증강의 Ships-disjoint 효과 | 계획 |

- 발표 노트: 오늘 결과는 C1–C4다. C5가 최종 주장이고 아직 결과가 없다. C3·C4는 "생성 모델이 무엇을 정확히 만들어야 하는가"와 "무엇을 입력으로 쓸 것인가"를 정하는 사전 실험이다.

## 7. 방법 개요: 게이트가 있는 파이프라인 [설계 완료] (1.5분)

- 그림: 6단계 흐름도와 각 단계의 게이트, 그리고 앞단의 "입력 표현 점검" 상자
  - 입력 점검: 특징 도메인(E1-rep) / 단서 위치(E1-src) / 잡음 제거 앞단(R3)
  - 0 평가기 검증 → 1 AE 보존 → 2 무조건 LDM → 3 조건부(c_LOFAR → c_DEMON) → 4 조건 조작(새 선박 변이) → 5 UATR 판정
- 왜 게이트부터인가: **LDM의 생성 품질 상한은 AE 복원이다**(diffusion은 E(x)만 학습하고 출력은 고정 디코더를 거침 [R13]). 이전 시도 PG-MCLDM [미검증]은 생성물 tonal F1 0.2(실데이터 0.66), 증강 +0.66 pp(seed 1, 누출 분할)로 이 순서를 건너뛰어 실패했다
- 원칙: 한 단계에 한 변수만 바꾼다. 판정 규칙은 결과를 보기 전에 코드로 커밋한다

## 8. 실험 설정 [완료] (1분)

- 데이터: DeepShip 33,644 클립 / 244척(이름 병합 후), ShipsEar 2,223 클립 / 57척. 5 s, 16 kHz. UniqueShip은 보조(정식 게재 전 arXiv)
- 분할: Ships-disjoint 5-fold(공유 선박 0, 공유 녹음 0, 모든 클립이 test에 1회). 비교용 Rec-disjoint
- 분류기: SwinV2-Tiny(ImageNet), MEL 256×256, UniqueShip 원문 설정. ShipsEar는 학습량 부족으로 상수 lr 3e-5·200 epoch(D안)
- 판정: fold paired Δ macro-F1, seed 3, run 잡음 약 1.1 pp

## 9. 결과 1: 어느 특징 도메인에서 생성할 것인가(E1-rep) [완료] (1.5분)

- 핵심 메시지: **MEL보다 나은 도메인이 없다.**
- 표(평균 Δ vs MEL): DeepShip STFT −1.89 / CQT −1.74 / MFCC −3.97(모두 5 fold 중 1개만 양수), ShipsEar STFT +0.86 / CQT +0.42 / MFCC +0.26(양수는 fold3 하나에서 나옴)
- 판정: 상위 2개 = MEL + STFT(STFT·CQT 차 0.15 pp, tie 규칙). 이후 CQT도 AE 대상에 추가(생성물 tonal 평가 때문, D-2026-10-21-01)
- 한계: ShipsEar seed sd 최대 8.7 → 검출력 낮음

## 10. 결과 2: 물리 평가기 [완료] (1.5분)

- tonal: 1 s window, TPSW, 6 dB, 절반 이상 지속. AUC DeepShip 0.998 / ShipsEar 0.937 → 사용
- DEMON 핵심 메시지: **가까운 tonal 두 개가 만드는 beating을 프로펠러 박자로 착각한다. CPW 백색화(X/|X|)가 이를 지운다.**
  - 합성: beating 신뢰비 14.7 → 1.39, 날개 변조 23.5 → 20.5
  - AUC V1 / CPW / 하모닉 검출: DeepShip 0.713 / **0.762** / 0.513, ShipsEar 0.720 / 0.683 / 0.540
  - 결정: CPW 통일, DeepShip 사용, ShipsEar 보류(사후 결정임을 명시)
  - 하모닉 검출은 실제 5 s 클립의 90–97%에서 0개 → 검출력 없음
- 근거 등급: CPW는 베어링 진단 포락선 분석의 방법(인접 분야 근거)
- 원칙: 생성 조건 c와 평가 e는 서로 다른 추출기(순환 논증 방지)

## 11. 결과 3: 클래스 정보는 어디에 있나(E1-src, E1-src-CQT) [완료, 판정 보류] (2.5분)

- 그림: 같은 클립의 O_rp(원본 크기) / B(broadband만) / T(tonal만) — MEL과 CQT로
- 설계: 입력 3종 × Rec-/Ships-disjoint, D = drop(B) − drop(T). 판정 D = +3.20 pp, CI [−1.54, +7.84] → 보류
- 핵심 메시지: **Ships-disjoint에서 클래스 정보는 대부분 broadband 장기 스펙트럼 모양에 있다.**
  - Ships-disjoint F1(MEL): B 53.16 ≈ O_rp 52.20 > T 41.87
  - CQT로 그려도 같다: B − T 격차 CQT +11.02 / MEL +11.29. T의 CQT 이득 ΔT +0.34(보류)
- 해석 범위: SwinV2 + 이미지 표현에서 쓸 수 있는 정보에 한정(H-SC-3, inferred). 20 Hz median 분리는 D를 양(+) 쪽으로 치우치게 한다
- 함의: 생성 모델이 가장 정확히 맞춰야 할 것은 broadband 모양(LTAS) → 조건 후보 c_LTAS(H-LDM-5)

## 12. 결과 4: 잡음 제거 앞단 ① FocuS-MN 재현과 DeepShip 적용 [완료] (2.5분)

- 동기: 녹음 조건(배경 잡음) 단서를 지우면 Ships-disjoint가 좋아질까(H-PRE-4)
- 원칙: **잡음 제거기도 분류기의 test 선박을 보면 안 된다**(누출 없는 일관성) → ShipsEar 적용(R3-SE)은 취소
- 재현: ShipsEar test SDRi **8.68 dB**(원문 8.61). "편차 27건을 둔 재현" — 단계 잔차와 2단계 결합 손실(크기 MSE + SI-SNR)을 넣어야 재현됨
- 부수 발견: 결합형 L2(Adam weight decay)가 약 7k step 뒤 가중치 norm을 51.5 → 4.5로 무너뜨림 → AdamW로 해결
- DeepShip 적용(R3-DS): **해로움.** macro-F1 58.18 → 53.35(Δ −4.83, 4/5 fold 음수)
  - DeepShip 실녹음 에너지 87% 제거, 2–8 kHz −16…−19 dB
  - fold1만 보면 +7.24("도움 신호")였고, 이는 큰 선박 두 척이 만든 예외였다
- 교훈 슬라이드 문구: **fold 하나의 예비 결과는 방향까지 틀릴 수 있다.**

## 13. 결과 5: 잡음 제거 앞단 ② 같은 해역 데이터로 학습(R-US) [진행 중] (2분)

- UniqueShip: DeepShip과 같은 ONC 해역 실제 배경 녹음 42.7 h → 실제 배경을 잡음으로 학습
- 전처리 발견: 클립 대부분이 DC(|평균|/RMS 0.96–0.99) → 클립별 DC 제거 필수. 제거 전에는 스펙트럼 차감만으로 SDRi 6.83 dB(허상)
- 잡음 제거 성능: SDRi **8.46 dB → 쓸 만함**. tonal 15.46 → 15.44(보존), 전 대역을 고르게 −6…−9 dB
- 한계: 선박 78.6% vs 배경 87.5% 제거 → 선박 소리도 많이 지움
- 누출 문제: R-US 학습 선박과 DeepShip이 정확 일치 140척(DeepShip 클립 71%), 같은 MMSI·같은 날짜 녹음 180개 → **DeepShip에 그대로 쓰면 누출** → 기간 분리 재학습(R-US-T, 2018-11 이후 데이터만, 겹침 0 확인)
- 분류 효과(R3-US, UniqueShip fold1, seed 3) — 발표 전 선택:
  - 도움(Δ > +1.1, 3/3): "같은 해역에서 학습한 잡음 제거기는 도움이 될 수 있다. fold 하나라 예비 결과다 → DeepShip 5 fold(R-US-T)로 확인"
  - 해로움(Δ < −1.1, 3/3): "broadband를 지우는 앞단은 Ships-disjoint 인식에 해롭다는 것이 두 데이터셋에서 반복됐다(C3과 일관)"
  - 불명확: "효과를 구별할 수 없다"

## 14. 결과 6: AE 보존 게이트 중간 결과(E1-AE) [진행 중, 22/30에서 일시정지] (1.5분)

- 질문: AE로 압축했다 복원한 스펙트로그램을 실데이터 분류기가 여전히 맞히는가(F1 비율 ≥ 0.95)
- 중간 결과(F1 비율):
  - ShipsEar: 세 도메인 대부분 0.9–1.07
  - DeepShip MEL: fold 1–4 = 0.964 / 0.990 / 0.885 / 0.849(평균 0.922, 기준 미달)
  - DeepShip STFT 0.36–0.72, CQT 0.71–0.85(tonal 보존 F1 약 0.97)
- 진단: L1 손실만 쓴 AE가 주파수 방향 질감을 뭉갠다. SwinV2는 그 질감에 민감해 예측이 한 클래스로 쏠린다(STFT → Tanker, CQT → Passenger)
- 핵심 메시지: **tonal은 남았지만 분류기가 쓰는 질감이 사라졌다. 원문 LDM처럼 adversarial·지각 손실이 필요하다는 신호다(inferred).**
- 일시정지 이유: 잡음 제거 앞단이 채택되면 AE 입력이 바뀐다 → C4 결론 후 재개

## 15. 다음 계획과 일정 [계획] (1.5분)

- 바로 다음: R3-US 판정 → R-US-T 학습 → DeepShip 5 fold 분류
- 그다음: 잡음 제거 채택 여부에 맞춰 E1-AE 재개(남은 8개) → 필요하면 patch adversarial 손실을 넣은 AE
- 이후: 무조건 LDM → 조건부(c_LTAS, c_LOFAR, c_DEMON[DeepShip]) → 조건 조작 → UATR 판정
- 일정: 약 33주, 2027년 6월 중순(`research/thesis_timeline_draft.md`). 잡음 제거 분기로 약 1–2주 밀림
- 대체 경로: AE 게이트 2회 실패 시 LDM 보류 → 비생성 물리 증강 + 평가 방법론 + 음성 결과

## 16. 한계와 논의 (1.5분)

- 한계:
  - DeepShip 선박 이름 매칭 휴리스틱, ShipsEar test fold의 클래스당 선박 1–2척
  - 5 s 클립의 DEMON 한계, 데이터셋별 학습 프로토콜 차이(ShipsEar는 상수 lr, 마지막 epoch)
  - E1-src·E1-src-CQT는 seed 0만
  - UniqueShip–DeepShip 선박 중복 → UniqueShip을 DeepShip 관련 실험에 쓸 때는 기간 분리 필수
- 지도교수께 확인받을 것:
  1. 생성 모델을 "증강 성능(Ships-disjoint UATR)"으로 평가하는 방향
  2. 주 데이터 DeepShip·ShipsEar, UniqueShip은 보조(잡음 제거 재료로도 사용)
  3. 잡음 제거 앞단 검증을 AE 이전에 하는 순서
  4. DEMON 조건은 DeepShip에서만

## 부록

- A1 용어: tonal, broadband, beating, CPW, Rec-disjoint, Ships-disjoint, AUC, paired Δ, SDRi
- A2 broadband와 tonal을 나누는 방법(20 Hz median, 폭 기준)
- A3 분할 통계(fold × 클래스별 선박·녹음·클립 수)
- A4 G0 그림 전체, 하모닉 규칙 비교표
- A5 E1-rep fold × 도메인 전체 표
- A6 FocuS-MN 재현 시도 표(시도 1–3a, 2b), 편차 목록
- A7 잡음 제거 전후 스펙트로그램(방법별 비교 페이지)
- A8 UniqueShip–DeepShip 중복 표, R-US-T 학습 풀

---

## 예상 질문과 답

| 질문 | 답의 요지 |
|---|---|
| 왜 아직 생성 결과가 없나? | 생성 품질의 상한은 AE이고, 평가기와 입력 표현이 정해지지 않으면 생성 결과를 믿을 수 없다. 이전 시도가 그 순서를 건너뛰어 실패했다(7번 슬라이드) |
| 생성 연구인데 왜 잡음 제거를 하나? | 잡음 제거가 채택되면 AE·LDM의 입력이 바뀐다. 입력을 먼저 정해야 뒤 단계를 다시 하지 않는다 |
| 잡음 제거가 해로운 이유는? | Ships-disjoint 클래스 정보가 broadband에 있는데(11번), 잡음 제거는 broadband를 지운다. DeepShip에는 깨끗한 기준이 없어 선박 broadband와 배경 broadband를 구별할 정답이 없다(inferred) |
| 왜 UniqueShip을 주 데이터로 안 쓰나? | 정식 게재 전 arXiv 프리프린트다. 코드 회귀, 잡음 제거 재료, 보조 실험에만 쓴다 |
| 선박 분리 성능 58%는 너무 낮지 않나? | 공개된 같은 조건 값(0.588)과 같다. 낮은 값 자체가 연구 문제이고, 판정은 증강 전후 차이(Δ)로 한다 |
| 더 좋은 분류기를 쓰면 되지 않나? | test로 분류기를 고르면 결과가 부풀려진다. 분류기 비교는 val 기준으로 최종 확인 단계에서 한다 |
| 왜 CQT가 tonal을 잘 보는데 분류는 안 좋나? | CQT로 tonal만 그려도 broadband와의 격차(11 pp)가 그대로였다. 표현 문제가 아니라 정보가 broadband에 있다는 쪽이다(SwinV2 한정) |
| fold 하나로 먼저 보는 이유는? | 빠른 신호 확인용이다. R3-DS에서 fold1과 5 fold의 방향이 반대였으므로, 예비 결과로는 결정하지 않는다 |
| 이전 실험 결과는 왜 안 쓰나? | 분할이 폴더마다 다르고 누출이 있어 비교할 수 없다. 교훈으로만 쓴다 |

---

## 참고문헌 (서론용, 확인 수준 표시)

| # | 서지 | 쓰는 곳 | 확인 수준 |
|---|---|---|---|
| R1 | Duarte C. M. et al. (2021). The soundscape of the Anthropocene ocean. *Science* 371, eaba4658. doi:10.1126/science.aba4658 | 2번 해양 소음 증가·생물 영향 | 서지·요지(검색). 본문 미확인 |
| R2 | IMO MEPC.1/Circ.833 (2014); MEPC.1/Circ.906 (2023, MEPC 80 승인); MEPC.1/Circ.906/Rev.1 (2024) — Guidelines for the reduction of underwater radiated noise from shipping | 2번 규제 흐름 | 공식 문서 링크와 해설(AMSA) 확인. 본문 미확인 |
| R3 | Feng et al. (2024). Artificial intelligence-based underwater acoustic target recognition: A survey. *Remote Sensing* 16(17), 3333. doi:10.3390/rs16173333 | 2번 동향 | 초록 |
| R4 | Muller et al. (2024). Navigating the depths: A comprehensive survey of deep learning for passive UATR. *IEEE Access*. doi:10.1109/ACCESS.2024.3480788 | 2번 동향 | 검색 결과. 저자 전체 미확인 |
| R5 | Santos-Domínguez D. et al. (2016). ShipsEar: An underwater vessel noise database. *Applied Acoustics* 113, 64–69. doi:10.1016/j.apacoust.2016.06.008 | 3번 | 서지·초록 |
| R6 | Irfan M. et al. (2021). DeepShip: An underwater acoustic benchmark dataset and a separable convolution based autoencoder for classification. *Expert Systems with Applications* 183, 115270. doi:10.1016/j.eswa.2021.115270 | 3번 | 서지·초록. 47 h·265척은 원문 대조 필요 |
| R7 | Hashemi et al. (2026). UniqueShip. arXiv:2609.13659 | 3·4번 | **원문 전체 읽음**(`papers/notes/2026_hashemi_uniqueship.md`) |
| R8 | Domingos L. C. F. et al. (2022). A survey of underwater acoustic data classification methods using deep learning for shoreline surveillance. *Sensors* 22(6), 2181 | 3번 | 검색 결과(PMC8954367). 권·호 확인 필요 |
| R9 | Yan et al. (2026). 수중 표적 인식 리뷰(중문). *Digital Ocean & Underwater Warfare*. doi:10.19838/j.issn.2096-5753.2026.02.001 | 3·4번 | 영문 초록만. 쓰지 않아도 됨 |
| R10 | Hummel H. I. et al. (2026). 사전학습 오디오 임베딩 linear probing | 4번 녹음 ID 군집 | 원문(에이전트)(`papers/notes/2026_hummel_linear_probing.md`) |
| R11 | 자체 문헌 조사 `research/literature/uatr_augmentation_survey.md` | 5번 | 9편 분할 확인, 나머지 초록·검색 |
| R12 | Xu J. et al. (2023). LMR. *Ocean Engineering*. doi:10.1016/j.oceaneng.2023.114926 | 5번 | 원문(에이전트) + 우리 재현(EXP-002-PC) |
| R13 | Rombach R. et al. (2022). High-resolution image synthesis with latent diffusion models. CVPR | 5·7번 | 핵심 절 원문 대조 |
| R14 | Liu H. et al. (2023). AudioLDM: Text-to-audio generation with latent diffusion models. ICML | 5번 | Claude 기억. **발표 전 서지 확인** |
| R15 | Azizi S. et al. (2023). Synthetic data from diffusion models improves ImageNet classification. TMLR | 5번(인접 분야) | Claude 기억. **발표 전 서지 확인** |
| R16 | JASA·JASA-EL 공동 특집 Generative and Physics-Informed AI for Acoustics (마감 2026-03-02) | 5번 | 공모 페이지(검색) |
| R17 | Huang W. et al. (2026). LR-VAE. *JASA* 159(5), 3773–3791. doi:10.1121/10.0043727 | 5번 | 원문(에이전트)(`papers/notes/2026_huang_lrvae_fewshot.md`) |

- 주의: 서론 근거는 "연구 동기"를 받치는 용도다. 서론 수치 중 우리 실험에 쓰는 것은 R7(원문 확인)뿐이다. R14·R15는 서지를 확인하기 전까지 슬라이드에 "예" 수준으로만 쓴다.
