# 2026_gu_focusmn_denoising — FocuS-MN (Gu, Li, Tang, JMSE 2026)

- 원문: `papers/pdf/2026_gu_focusmn_denoising.pdf`. 읽은 범위: §1, §3(구조), §4(데이터·학습·지표), §5(결과), §6–7 (Claude, 2026-10-21, PDF 텍스트 대조)
- 사용 목적(사용자): 분류기 앞단 잡음 제거(H-PRE-4) 후보

## 원문에서 확인한 사실 (confirmed)

| 항목 | 내용 | 위치 |
|---|---|---|
| 과제 | 지도학습 잡음 제거(음성 향상 방식). STFT 크기·위상을 2채널로 입력 → encoder(Dilated DenseNet) → 학습형 down/up-sampling + FSMN → **크기 마스크** decoder → ISTFT | §3, Fig. 1 |
| "깨끗한" 정답 | ShipsEar 선박 녹음 자체. 녹음 안의 잔여 배경은 무시하고 "근사적으로 깨끗하다"고 가정 | §4.1 |
| 잡음 | ShipsEar 배경 녹음(바람, 해류, 비)을 선박 녹음에 **−5 dB SNR로 더함**(합성 혼합) | §4.1 |
| 데이터 | 16 kHz, 3 s 구간. test = 선박 종류 4개(준설선, 예인선, 트롤선, 파일럿선, 미관측 종류). 나머지 7종류를 무작위로 train/val. 비율 약 7:2:1 | §4.1 |
| 학습 | 2단계: 크기 MSE → SI-SNR. Adam lr 5e-5, cosine, batch 16, 최대 200 epoch, early stopping 20 | §4.2 |
| 결과 | SDR 3.77 dB, SDRi 8.61 dB, SSNR 3.83 dB(−5 dB 입력). 비교: DCCRN 2.38, FullSubNet 2.02, SEGAN −3.06 | §5, Table 2 |
| 파라미터 | 0.34 M, 18.73 GFLOPs(3 s 입력) | Table 3 |
| 미기재 | STFT n_fft·hop, 압축 지수 p의 수치(텍스트 기준). 코드는 요청 시 제공 | §3.1, Data Availability |
| 하류 과제 | 분류 성능 평가는 없다. PSD 그림으로 line spectrum 보존을 정성적으로 보여 준다 | §4.2.3, §5 |

## 해석 (inferred, Claude)

- "latent space"는 마스크 추정 네트워크의 중간 특징이다. 표본을 뽑는 생성 latent(VAE·LDM)가 아니다.
- 이 모델의 "깨끗한 신호"는 **실제 ShipsEar 선박 녹음 그대로**다. 그러므로 실제 녹음(추가 잡음 없음)에 적용하면 이상적으로는 거의 항등 변환이어야 한다. 학습 때 더한 종류의 배경(바람·해류·비)을 닮은 성분만 줄인다.
- DeepShip은 다른 해역·하이드로폰이다. 분포 밖 적용이 된다.
- 공개 사전학습 모델을 쓰면 ShipsEar의 우리 test fold 선박을 이미 본 모델이 된다(누출).
- 데이터 구성 방식(선박 녹음 + 실제 배경 녹음을 SNR로 혼합)은 그 자체로 물리적 증강 후보다(A-phys, D4).

## 재현 결과 (2026-10-21, DEN 세션, `/jhlee/UWShipNoise/denoising/FocuS-MN`)

- 판정: **편차 27건을 둔 재현.** test SDR 3.677 / SDRi 8.677 / SSNR 3.833 dB(원문 3.773 / 8.611 / 3.828). 파라미터 0.341 M(원문 0.34 M).
- 원문대로 구현한 시도 1은 학습 부족으로 미달(SDRi 6.58)이었다. 통과에 필요했던 변경 두 가지:
  1. 단계 잔차 x + up(FSMN(down(x))) 추가 — 원문에 없음. 학습 부족을 풀었다(1단계 val MSE 0.0305 → 0.0159).
  2. 2단계 손실 = 압축 크기 MSE + SI-SNR — 원문 제목 'Joint Magnitude and Waveform Modeling'에 따른 해석(본문은 SI-SNR만). SI-SNR만 쓰면 출력 크기가 묶이지 않아 SDR이 떨어졌다(출력 에너지 +2.9 dB).
- 원인이 아니었던 것: 결합형 L2 weight decay(decoupled AdamW로 바꿔도 학습 부족 그대로), 출력 위상 규칙(상한 6.18 dB).
- 시사점(inferred): 원문 그림·본문만으로는 재현되지 않았다. 생략된 구조 요소(잔차)와 손실 정의가 있을 가능성이 크다.
