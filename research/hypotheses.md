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
  - **2026-10-12 EXP-DEMON-001 2b-1**: Wang 2026의 EEMD 대역 선택은 원문 합성 모델 + 백색잡음에서 **불지지**다. 고정 저역 대역(100–2000 Hz)보다 −15 dB 정답률이 35 pp 낮았다. 한계: 합성 모델 하나, 판정이 SNR 한 단계에 의존한다. 다른 자동 선택 기준(포락선 SNR 최대화, spectral kurtosis; Chung 2011, Pollara 2016)은 아직 검증하지 않았다.
  - **2026-10-13 변형 (d)**: R_j를 IMF 분산으로 정규화하면(Wang 아이디어 기반 변형) 새 seed에서 −15 dB 정답률이 BP-MID·ORACLE 수준까지 회복됐다(a=3 40%, a=6 90%; 원문 EEMD 대비 +30 pp, McNemar p = 0.031). 고정 대역보다 낫다는 근거는 없다. 따라서 H-PRE-3은 "자동 선택 = 고정 저역과 같은 수준"까지만 지지된다. 합성 모델 하나에서의 결과다.

| ID | 가설 | 근거 등급 | 상태 |
|---|---|---|---|
| H-PRE-1 | 모든 샘플에 같은 고정 band-pass를 쓰면 일부 선박의 토널·고조파가 대역 밖에서 손실된다 | 합리적 가설. 손실 정도는 대역 설정에 따라 다르다. 직접 측정 없음 | hypothesis |
| H-PRE-2 | 샘플별 적응형 대역 선택(EWT 등)이 고정 대역보다 누출 없는 UATR 성능 또는 토널 보존을 개선한다 | 인접 분야 근거(서베이: 분해 기반 잡음 제거). 선박 분리 조건의 직접 근거 없음 | hypothesis |

- 위험: 샘플별 필터 경계가 녹음 환경 정보를 담으면 새로운 지름길이 될 수 있다(H-AUG-3과 같은 계열).
- 검증 방법 후보: UniqueShip background 클래스 + 알려진 합성 토널을 섞은 준합성 데이터로 토널 회수율을 측정한다.

## LDM에 물리 특징(DEMON·LOFAR) 반영 (2026-10-13, 사용자 질문에서 나옴)

사용자 질문: "인코더 latent에서 DDPM을 돌릴 때 DEMON spec과 LOFAR를 함께 추출해, 광대역·협대역 특징을 노이즈 제거 과정에 반영하고 싶다. 목적함수를 추가해야 하나?"

반영 위치는 네 곳으로 나눈다. 각 위치는 서로 다른 가설이다.

| ID | 반영 위치 | 가설 | 근거 등급 | 상태 |
|---|---|---|---|---|
| H-LDM-1 | 오토인코더 손실 | AE 학습에 LOFAR(tonal)·DEMON(포락선) 복원 손실을 더하면, latent가 협대역·광대역 구조를 더 잘 보존한다 | 합리적 가설. LDM 원문의 AE는 LPIPS + patch adversarial + 약한 KL/VQ 손실이다(원문 §3.1·부록 G 확인). 수중음향 근거 없음 | hypothesis |
| H-LDM-2 | 조건 입력 | DEMON·LOFAR 요약 벡터를 ε_θ(z_t, t, c)의 조건 c로 넣으면(cross-attention 또는 FiLM), 생성물의 해당 특징이 조건을 따른다(제어 가능성) | LDM의 cross-attention 조건화를 쓰는 것이다(원문 §3.3 확인). FiLM은 원문에 없다(인접 근거). 목적함수 변경이 필요 없다 | hypothesis |
| H-LDM-3 | 학습 보조 손실 | x̂₀를 디코딩해 DEMON·LOFAR를 계산하고 목표와 맞추는 보조 손실을 더하면 H-LDM-2보다 조건 준수가 좋아진다 | 구현 휴리스틱. 디코더와 특징 추출의 미분 가능성이 필요하다. 비용과 불안정성 위험이 있다 | hypothesis |
| H-LDM-4 | 샘플링 guidance | 학습은 바꾸지 않는다. 샘플링 때 특징 거리의 gradient로 z_t를 유도한다(classifier/universal guidance 계열) | 인접 분야 근거. 원문 미확인 | hypothesis |

- **순환 논증 위험 (H-LFM-3과 같음):** 신호에서 뽑은 특징으로 조건을 주고 같은 특징으로 평가하면, "조건을 따른다"는 것만 보인다. 물리적 타당성은 보이지 않는다.
- **지름길 위험:** LOFAR·DEMON 특징에는 녹음·선박 정체성이 담긴다(EXP-LOFAR-001 R2: Passenger 출처 지름길). 조건 생성이 기존 선박을 복제할 수 있다.
- **새 선박 같은 변이(H-AUG-2)와의 연결:** 조건 c를 물리 손잡이(f_s 이동, 하모닉 수, tonal 위치)로 조작해야 증강이 된다. 실제 샘플의 c를 그대로 쓰면 재현일 뿐이다.
- **이전 시도:** PG-MCLDM(미검증)이 물리 조건 latent 생성을 했다. 생성물의 DEMON 신뢰비는 0.007–0.018이었다.
- **특징 재현 실험이 준 정보 (2026-10-13):**
  - DEMON: 정교한 자동 대역 선택(Wang)은 고정 저역보다 낫지 않다. SBL은 지표만 부풀린다.
  - LOFAR: Hough 선 검출은 가장자리 가짜 선, 두 줄 검출, 도플러 선 누락이 있다.
  - → 조건·손실용 특징은 처음에는 단순하고 미분 가능한 형태가 맞다. 예: 고정 대역 DEMON 스펙트럼, TPSW 정규화 LOFAR(`inferred`).
- **제안 순서 (Teacher 추천):**
  1. AE 복원 상한을 tonal·DEMON 지표로 잰다. 이것은 D-2026-10-06-01의 재검토 조건이다.
  2. 무조건 LDM baseline을 만든다.
  3. H-LDM-2 조건화를 적용한다.
  4. 필요할 때만 H-LDM-1이나 H-LDM-3을 적용한다.
  - 한 번에 하나만 바꾼다.
- **우선순위:** 사용자가 결정했다(D-2026-10-13-02). 조건부 LDM 생성을 물리 기반 증강의 한 방법으로 본다.

## 지름길(shortcut) 학습 가설 (2026-10-20, 사용자 제기)

| ID | 가설 | 근거 | 상태 |
|---|---|---|---|
| H-SC-1 | 누출 분할에서 분류기는 클래스 공통 특징 대신 **개별 선박·녹음 고유의 단서**를 학습한다. 선박 분리 분할의 정확도 하락폭이 그 의존도다 | UniqueShip 원문: 선박 분리 시 10–48 pp 하락, DeepShip Swin Mel 0.710 → 0.588(Table II, `confirmed`). 원문 해석과 같다 | 직접 근거 있음 (해석 수준) |
| H-SC-2 | 그 고유 단서는 주로 **broadband** 성분(녹음 조건, 거리, 배경, broadband 모양)에 있다 | 사용자 제기. 반대 가능성: 정확한 tonal 주파수(축 회전수)는 선박 고유성이 매우 높다. 어느 쪽인지 직접 근거 없음 | **보류 (E1-src, 2026-10-21): D = +3.20 pp, CI [−1.54, +7.84].** 상대 하락은 B 16.6% vs T 15.0%로 비슷하다. 대신 Ships-disjoint 클래스 정보는 broadband만으로 원본(위상 무작위)과 같은 수준(B 53.16 vs O_rp 52.20, T 41.87)이다 |
| H-SC-3 | Ships-disjoint에서 클래스 변별 정보는 주로 broadband 장기 스펙트럼 모양에 있고, tonal의 추가 기여는 작다. **(2026-10-21 범위 정정: MEL 표현 + SwinV2에서 쓸 수 있는 정보에 한정. MEL은 이미지 window 주엽 ±31 Hz로 tonal이 약 9칸에 번지므로 T 입력이 불리했다. CQT로 그린 T에서는 달라질 수 있다 — 사용자 지적)** **E1-src-CQT(2026-10-21): 사전 판정은 보류(ΔT +0.34, 3/5)지만, B − T 격차가 CQT +11.02 / MEL +11.29로 표현과 거의 무관했다. 클래스별로는 Cargo·Passenger에서 CQT-T가 오르고 Tanker·Tug에서 내린다** | E1-src: B 53.16 ≈ O_rp 52.20 > T 41.87(seed 0, 5 fold). E1-rep: tonal이 잘 보이는 CQT가 MEL보다 낫지 않음. 한계: B에 넓은 narrow 성분이 일부 남음 | inferred (직접 검증 전) |
| H-LDM-5 | broadband 장기 스펙트럼(LTAS, 시간 평균 MEL 프로파일)을 조건 c_LTAS로 주고, 같은 클래스 안에서 조작(선박 간 보간, 기울기 변경)하면 '새 선박 같은' 변이를 만들 수 있다 | E1-src: 클래스 정보는 broadband 모양에 있고(H-SC-3), 그 안에도 선박 고유 단서가 있다(상대 하락 16.6%). 사용자 질문(2026-10-21)에서 나옴. DEMON은 변조 주파수 축이라 broadband 모양을 담지 않는다(CPW는 모양을 일부러 지운다) | hypothesis |

## 잡음 제거 전처리 (2026-10-21, 사용자 질문)

| ID | 가설 | 근거 | 상태 |
|---|---|---|---|
| H-PRE-4 (**R3-DS 5 fold: 해로움, −4.83 pp, 2026-10-22.** ShipsEar 학습 FocuS-MN 고정 앞단 조건에서 불지지) | 앞단에 잡음 제거를 두면 녹음 조건(배경 소음) 단서가 줄어 Ships-disjoint 일반화가 좋아진다 | 찬성: Rec-disjoint → Ships-disjoint 하락에 녹음 조건 단서가 섞여 있을 수 있다(H-SC-1). 반대: E1-src에서 Ships-disjoint 클래스 정보는 broadband에 있었고(B 53.16 > T 41.87, H-SC-3), 일반적인 잡음 제거는 broadband를 줄인다. 선박 broadband(캐비테이션)와 배경 broadband를 구별할 기준 신호가 DeepShip에 없다. 서베이(Gao 2024)도 실데이터에는 깨끗한 기준이 없고 "잡음과 신호의 경계가 모호"하다고 정리한다 | hypothesis. 지금은 검증하지 않는다. 검증안: E1-rep 형식의 단일 arm(고정·비학습 잡음 제거 + MEL), Rec-/Ships-disjoint 둘 다 |
| H-SC-4 | 고주파(약 2 kHz 이상) broadband에는 클래스 정보보다 녹음 조건·선박 고유 단서가 많고, 저주파(<1 kHz) broadband 모양이 클래스 정보를 담는다 | R3-DS fold1: 잡음 제거가 2–8 kHz를 −16…−19 dB 줄이고 0–1 kHz는 −1…−4 dB만 줄였는데 F1 +7.2 pp. E1-src B(broadband 전체 유지)는 원본 수준. 직접 검증 전이며 효과가 두 척에 몰려 있음 | hypothesis **(약화, 2026-10-22: R3-DS fold1의 상승이 5 fold에서 재현되지 않음. 고주파 broadband 제거는 평균적으로 분류를 해쳤다)** |
