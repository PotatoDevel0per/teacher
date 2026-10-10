# Hummel et al. 대조학습 일반화 임베딩 (2025, arXiv:2505.12904v1)

- 원문: `papers/pdf/2025_hummel_contrastive_uatr.pdf` (arXiv v1, 23쪽, 2026-10-10 전체 읽음). 게재본은 Applied Acoustics 243 (2026) 111103이다(후속 논문 참고문헌으로 확인). 게재본 PDF는 읽지 않았으므로 수치가 다를 수 있다.
- 기록 규칙: "확인한 내용"은 원문에서 직접 확인한 것(`confirmed`)이다. "해석"은 Claude의 추론(`inferred`)이다. 그림에서 눈으로 읽은 값은 `≈`로 표시한다.

## 연구 분류

- [x] 증강 설계 근거 (증강 종류별 비교표)
- [x] 평가 방법 (DeepShip 시간순 분할)
- [ ] 누출 없는 baseline (선박 단위 분할이 아니다)

## 한 문장 요약

ONC 하이드로폰 1대의 무라벨 녹음으로 Conformer를 VICReg 대조학습한 뒤, frozen 임베딩 + 로지스틱 회귀로 DeepShip·ShipsEar·Watkins를 분류한 논문이다. 대조학습의 positive pair를 만드는 증강(저역통과, Gaussian noise, 대역 mixup, 음성용 증강)을 비교한다.

## 확인한 내용 (`confirmed`)

### 데이터와 분할 (§2.1)

- **무라벨 학습 데이터**: ONC SCVIP 하이드로폰 1대 (49.04 N, -123.43 W, 수심 298 m). DeepShip과 같은 장소를 일부러 골랐다. 2019-09 ~ 2020-12의 5분 녹음을 월·시간대(아침/오후/저녁/밤)가 고르게 되도록 뽑았다. 30 GB. 내용 정보는 없다 (§2.1.1).
- **DeepShip** (47 h 3 m, 4 클래스): 시간순 분할. 원문: *"The recordings until November 2017 were used as training data and the recordings from December 2017 onward as test set. ... due to this split, almost 60% of the data samples in the test set are newly seen ships."* (§2.1.2)
  - 단위: **녹음 파일의 날짜 기준 분할**. 선박 단위 분할이 아니다. 테스트 샘플의 약 40%는 학습에 나온 선박이다.
- **ShipsEar** (3 h 8 m, 5 클래스)와 **Watkins** (45 클래스): 원문: *"The remaining labeled datasets had no available time information and therefore were divided into 80% training data and 20% test data."* (§2.1.2)
  - 단위: **명시되지 않음**. 녹음 단위인지 2초 window 단위인지 알 수 없다.
- **DeepShip 무작위 분할(비교 실험)**: 원문: *"randomly splitting the individual Deepship recordings into a training set (80%) and a test set (20%), ensuring that no individual recordings were present in both sets."* (§3.3.2) → 녹음 단위 분할. 선박 중복은 통제하지 않는다.
- 전처리: 분할 후 16 kHz 다운샘플, 겹치지 않는 2초 window (§2.1.3). Mel 128 bin (§2.3).

### 모델과 학습 (§2.4–2.7)

- 인코더: Conformer 블록 4개 (MHSA 4 head, conv kernel 31) → flatten 2,048 → linear. Expander: 2층 MLP, 8,196 차원. 파라미터 101M (Table 5).
- 손실: VICReg. 가중치 λ=5, µ=5, ν=1. 30 epoch, batch 2,048, LARS lr 0.01 (정체 시 1/10).
- 하류 분류기: 임베딩 위의 로지스틱 회귀. 지표: 정확도, 가중 F1.
- 비교 기준: ResNet-18 (16.7M) + 2층 MLP 128 projector, supervised contrastive loss, **라벨된 DeepShip으로 학습**. Adam(lr 5e-4) 또는 LARS(lr 0.01).

### 증강 설정 (§2.2, §3.3.1)

positive pair는 한 2초 조각에 증강 family에서 무작위로 고른 두 함수를 각각 적용해 만든다 (시간 영역).

| 증강 | 원문 설정 | 저자가 밝힌 의도 |
|---|---|---|
| No augmentation | 원본 유지 | – |
| Gaussian noise | 출력 SNR을 0.3–0.5 dB로 제한 | 더 시끄러운 해양 환경 모사 |
| Low-pass | "a maximum of 1 kHz as the cutoff frequency" | 선박 종류 판별 정보가 50 Hz–1 kHz에 있다는 저자 survey(Hummel 2024) 근거 |
| MixUp | 원본을 1 kHz 저역통과 + 같은 녹음에서 N(중심 시각, σ=50 s)로 뽑은 다른 2초 조각을 1–8 kHz 고역통과 → 더함 | 저역 = 선박 고유 특성, 고역 = 관련 있지만 다른 특성. Temporal Neighborhood Coding에서 착안 |
| (확장) gain, reverb, pitch, polarity inversion | **파라미터 없음**. "speech-based augmentation functions"라고만 씀 | – |

- 원문에 없는 것: Low-pass cutoff를 무작위로 뽑는지 1 kHz 고정인지, 필터 종류·차수, 단일 증강 실험에서 family가 {없음, 해당 증강}인지 {해당 증강}뿐인지.

### 결과표

**Table 1. 다중 데이터셋 분류 (원래 증강 family)**

| 모델 | DeepShip Acc / F1 | ShipsEar Acc / F1 | Watkins Acc / F1 |
|---|---|---|---|
| Sup. CL ResNet18 (Adam) | 53.94% / 0.49 | 21.40% / 0.08 | 54.54% / 0.54 |
| Sup. CL ResNet18 (LARS) | **56.51%** / 0.55 | 43.94% / 0.42 | 80.46% / 0.77 |
| Sup. Conformer (LARS) | 55.16% / 0.54 | 48.47% / 0.49 | **87.10%** / 0.85 |
| Unsup. ResNet18 (LARS) | 50.34% / 0.49 | 42.25% / 0.37 | 71.80% / 0.63 |
| Unsup. Conformer (LARS) | 54.87% / 0.54 | **57.42%** / 0.57 | 86.10% / 0.84 |

**Table 2. VICReg 가중치 (선박 종류, DeepShip으로 추정)**: (1,1,1) 55.35%, (5,5,1) 55.61%, (25,25,1) 23.81%. VICReg 원 논문 권장값(25,25,1)은 붕괴에 가깝다.

**Table 3. 증강 함수별 (비지도 Conformer로 추정. 표 제목은 모델을 명시하지 않음)**

| 증강 | DeepShip Acc / F1 | ShipsEar Acc / F1 | Watkins Acc / F1 |
|---|---|---|---|
| LowPass | **55.93%** / 0.54 | 49.42% / 0.44 | **87.00%** / 0.83 |
| Noise | 52.54% / 0.52 | 50.19% / 0.48 | 85.21% / 0.83 |
| MixUp | 55.25% / 0.54 | 51.86% / 0.51 | 86.03% / 0.84 |
| Combined | 55.61% / 0.55 | **52.14%** / 0.50 | 87.00% / 0.83 |

**Table 4. 음성용 증강을 추가한 확장 family**

| 모델 | DeepShip | ShipsEar | Watkins | Table 1 대비 (DeepShip / ShipsEar / Watkins, pp) |
|---|---|---|---|---|
| Sup. CL ResNet18 (Adam) | 63.07% | 45.91% | 75.73% | +9.13 / +24.51 / +21.19 |
| Sup. CL ResNet18 (LARS) | 61.17% | 52.64% | 86.33% | +4.66 / +8.70 / +5.87 |
| Sup. CL Conformer (LARS) | 56.55% | 45.41% | 86.94% | +1.39 / −3.06 / −0.16 |
| Unsup. ResNet18 (LARS) | 42.48% | 38.24% | 69.66% | −7.86 / −4.01 / −2.14 |
| Unsup. Conformer (LARS) | 57.78% | 50.47% | 86.14% | +2.91 / −6.95 / +0.04 |

(차이 열은 Claude가 Table 1과 빼서 계산한 값이다.)

**Fig. 5. DeepShip 시간순 vs 녹음 단위 무작위 분할 (지도 모델, 확장 증강, 그림에서 읽은 값)**

| 모델 | DeepShip 시간순 → 무작위 | ShipsEar 전이 | Watkins 전이 |
|---|---|---|---|
| ResNet (Adam) | ≈63 → ≈72 | ≈46 → ≈21 | ≈76 → ≈58 |
| ResNet (LARS) | ≈61 → ≈65 | ≈53 → ≈46 | ≈86 → ≈81 |
| Conformer (LARS) | ≈55 → ≈60 | ≈48 → ≈52 | ≈87 → ≈88 |

**Fig. 7. 라벨 비율 (DeepShip, 10/25/50/100%)**: 비지도 Conformer ≈43.5 / 50 / 55 / 55.5. 10%에서는 지도 Conformer(≈49)와 ResNet Adam(≈45)이 더 높다. 25%에서 ResNet Adam은 ≈24로 급락. 저자는 10% 부분집합의 "개별 선박 중복" 때문이라고 설명한다 (§3.4).

**기타**: 임베딩 크기 512까지 정확도 상승, 이후 소폭 (Fig. 8). 추론 2초 샘플당 ResNet 2.8 ms, Conformer 5.3 ms (A100).

### 저자 해석 (원문 주장, §3.3, §4)

- LowPass 단독이 DeepShip·Watkins에서 최고이며 전체 family와 비슷하다. 저자 설명: 판별 정보가 저주파 대역에 몰려 있어서 모델이 가장 정보가 많은 대역에 집중한다.
- 그러나 LowPass 단독은 ShipsEar에서 떨어진다 → cross-dataset 안정성에는 전체 조합이 필요하다.
- 음성용 증강 추가: 비지도에서는 개선되지 않는다("representative augmentation functions"가 중요). 지도에서는 라벨이 있으므로 추가 변이성의 이득을 본다.
- 무작위(녹음 단위) 분할은 DeepShip 정확도를 올리지만 다른 데이터셋으로의 일반화를 떨어뜨릴 수 있다. 이유: 새 선박이 적고 계절 영향이 줄어든다.
- 클래스 정의(AIS 1차 분류)가 음향적으로 겹친다. 블레이드 수, 크기, 엔진 종류 기반 클래스를 제안한다 (§4).

### 원문 내부 불일치 (`confirmed`)

- 같은 "비지도 Conformer + 원래 family + (5,5,1)" 설정으로 보이는데 Table 1은 DeepShip 54.87% / ShipsEar 57.42%, Table 2·3은 55.61% / 52.14%다. 실행이 다르거나 설정이 다른 것으로 보이나 원문에 설명이 없다.
- 반복 실행과 표준편차가 전혀 없다.

## 해석 (`inferred`)

### 증강 수치를 얼마나 믿을 수 있나

- Table 3의 증강 간 차이는 DeepShip에서 최대 3.4 pp, ShipsEar 2.7 pp, Watkins 1.8 pp다. Table 1과 Table 3의 같은 설정 차이(DeepShip 0.7 pp, ShipsEar 5.3 pp)가 이 범위와 비슷하거나 더 크다. **따라서 Table 3의 증강 순위는 실행 간 변동과 구분되지 않는다.** "LowPass가 가장 좋다"는 근거로 쓰기 어렵다.
- UniqueShip 논문(2026_hashemi_uniqueship)에서 DeepShip 누출 없는 조건의 표준편차가 ±7.7 pp였다. 이 논문의 DeepShip 테스트도 단일 시간 분할이라 비슷한 불확실성이 있을 수 있다.
- 확실하게 큰 효과는 두 가지다. (1) 지도 ResNet18에서 음성용 증강 확장이 DeepShip +4.7–9.1 pp. (2) VICReg 가중치 (25,25,1)의 붕괴. (1)도 단일 실행이다.

### 이 논문의 증강은 사용자의 증강과 역할이 다르다

- 여기서 증강은 **대조학습에서 "같은 것"을 정의하는 수단**이다. 증강이 없애는 정보에 대해 임베딩이 불변해진다. 예: Low-pass를 positive로 쓰면 "1 kHz 위 정보는 무시해도 된다"를 가르친다.
- 사용자는 **지도 분류기의 학습 분포를 넓히는 증강**을 설계한다. 원리는 비슷하지만(라벨을 보존하는 변환이어야 함) 수치가 그대로 옮겨지지는 않는다. Table 4의 "지도" 행만 사용자 설정에 가깝다. 그것도 supervised contrastive loss + logistic regression이지 cross-entropy 분류기가 아니다.

### 물리 기반 증강 설계에 주는 근거

- **gain, reverb, pitch, polarity 같은 비물리 증강도 지도 학습에서는 시간순 분할 DeepShip을 올렸다** (Table 4, 직접 근거, 단일 실행). 물리 기반 증강을 제안하려면 이 "일반 오디오 증강 묶음"을 반드시 비교 기준에 넣어야 한다. 그렇지 않으면 "물리성"의 기여와 "아무 변이성"의 기여를 구분할 수 없다.
- **pitch 증강은 tonal 선 성분의 주파수를 옮긴다.** 같은 선박 종류 안에서 회전수 변화(shaft rate, blade rate 변화)를 흉내 내는 면이 있다. 그러나 균일 pitch shift는 모든 주파수를 같은 비율로 옮기므로 broadband 스펙트럼 형태와 전파 효과까지 함께 옮긴다. 물리적으로는 "회전수만 바꾸는 tonal 이동"과 "전파·환경은 유지" 분리가 필요하다 → 사용자의 물리 기반 증강이 차별화할 수 있는 지점이다. (합리적인 가설이지만 직접 근거가 부족함)
- **reverb는 다중경로 전파를 대충 흉내 낸다.** 음성용 reverb는 실내 임펄스 응답이라 수중 다중경로(해면·해저 반사, 수 ms–수백 ms 지연)와 다르다. 수중 채널 모델(예: 거리·수심에 따른 전달손실, 다중경로 지연)을 쓰는 증강과 비교할 가치가 있다. (인접 분야의 근거를 적용하는 것임)
- **Gaussian noise SNR 0.3–0.5 dB는 매우 공격적이다.** 백색잡음이라 해양 배경잡음(저주파에 몰린 colored noise, Wenz 곡선 형태)과 스펙트럼이 다르다. 사용자 연구에서는 실제 배경 녹음(UniqueShip은 배경 클래스 제공)이나 Wenz형 colored noise로 SNR 범위를 넓게 두는 쪽이 물리적으로 더 타당하다. (구현 휴리스틱임)
- **Low-pass 결과는 "1 kHz 아래에 정보가 많다"를 지지하지만 증명하지는 않는다.** 이 논문은 16 kHz 다운샘플, 2초 window를 썼다. 2초 window의 주파수 해상도에서 저주파 tonal을 얼마나 분해했는지는 알 수 없다.
- **대역 MixUp(저역 원본 + 고역 다른 시점)은 "저주파 선박 서명은 유지하고 고주파 환경을 바꾼다"는 생각이다.** 같은 녹음 안 ±50 s에서 고역을 가져오므로 같은 선박일 가능성이 높다. 사용자 설정에서는 **다른 선박·다른 배경의 고역**을 섞는 변형을 생각할 수 있다. 다만 라벨 보존 여부를 확인해야 한다. (논문에서 영감을 받은 가설임)

### 분할과 누출

- DeepShip 시간순 분할은 녹음 무작위 분할보다 엄격하지만 **선박 단위 분리가 아니다** (테스트 약 40% 기존 선박). 이 논문의 DeepShip 수치는 UniqueShip MMSI 분할 수치와 직접 비교하면 안 된다.
- ShipsEar 80/20의 단위가 불명이다. window 단위라면 같은 녹음이 학습·테스트에 모두 들어간다. 녹음 단위라도 ShipsEar에는 같은 선박의 녹음이 여러 개 있으므로 선박 누출 가능성이 있다. (ShipsEar의 선박 중복 여부는 ShipsEar 원문으로 확인 필요, `unknown`)
- 무라벨 사전학습 데이터(SCVIP, 2019-09 ~ 2020-12)는 DeepShip(2016-05 ~ 2018-10)과 기간이 겹치지 않는다. 그러나 **UniqueShip(2016-05 ~ 2023-11, ONC 같은 해역)과는 기간·해역이 겹친다.** 이 논문의 사전학습 가중치를 UniqueShip에 쓰면 테스트 선박의 녹음을 무라벨로 본 상태일 수 있다. (UniqueShip 하이드로폰이 SCVIP와 같은 장비인지는 미확인, `unknown`)

## 사용자 연구와의 관계 (`inferred`)

- **직접 쓸 수 있는 것**: 증강 후보 목록과 "비물리 일반 오디오 증강이 지도 학습에서 이득을 줄 수 있다"는 경고. 물리 기반 증강 실험의 비교군에 (a) 증강 없음, (b) 일반 오디오 증강 묶음(gain, pitch, reverb, polarity, Gaussian noise), (c) 물리 기반 증강을 반드시 둔다.
- **쓰면 안 되는 것**: Table 3의 증강 순위를 "어떤 증강이 효과적인가"의 근거로 쓰는 것. 단일 실행, 대조학습 설정, 분할 단위 문제 때문이다.
- **분류기 선택**: 지도 ResNet18(17M)이 시간순 DeepShip에서 Conformer(101M)보다 좋았다. 저자도 "DeepShip은 큰 모델을 학습시키기에 작다"고 본다. 작은 데이터에서 ResNet-18 후보를 유지할 근거가 된다(약한 근거).
- 저자의 "클래스가 음향적으로 겹친다" 지적은 UniqueShip의 Cargo–Tanker 혼동과 일치한다. 물리 기반 증강이 클래스 간 혼동을 줄이는지 혼동행렬로 볼 필요가 있다.

## 이해 확인 질문 (사용자용)

1. 대조학습에서 positive pair를 만들 때 Low-pass 증강을 쓰면, 학습된 임베딩은 어떤 정보에 대해 "불변"해지는가? 이것이 지도 분류기의 학습 데이터 증강으로 Low-pass를 쓰는 것과 어떻게 다른가?
2. Table 3에서 LowPass가 DeepShip 55.93%, Combined가 55.61%다. 이 0.32 pp 차이로 "LowPass가 더 낫다"고 말할 수 없는 이유를 이 논문 안의 다른 수치를 들어 설명하라. (힌트: Table 1과 Table 3의 같은 설정)

## 상태

- [x] 원문 확보 (arXiv v1)
- [x] 원문 읽기
- [ ] 게재본(Applied Acoustics 2026) 수치 차이 확인
- [ ] 공식 코드에서 증강 파라미터(gain/reverb/pitch, low-pass cutoff 분포) 확인
- [ ] 최소 재현
