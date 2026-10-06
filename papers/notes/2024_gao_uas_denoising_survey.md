# UAS Denoising Survey (Gao et al., 2024, arXiv:2407.13264)

- 원문: `papers/pdf/2024_gao_uas_denoising_survey.pdf` (16쪽, 2026-10-06 본문 전체 읽음)

## 논문 성격 (`confirmed`)

**서베이 논문이다.** 방법을 제안하거나 실험하지 않는다. 수중음향 신호 잡음 제거 방법을 네 갈래로 분류한다.
1. 기존 방법 (wavelet thresholding, 선형 필터)
2. 신호 분해 (DWT, EWT, EMD/EEMD/CEEMDAN, VMD) + 성분 선별 + thresholding
3. 딥러닝 (autoencoder, GAN, attention)
4. 하이브리드

## 사용자 질문과 관련된 내용 (`confirmed`)

- 원문에서 "PSD"라는 단어는 쓰이지 않는다. "PSD로 band-pass를 수동 설정한다"는 서술도 찾지 못했다(텍스트 검색 기준).
- **EWT**(Gilles 2013, 원문 ref [13]/[64]): FFT 스펙트럼을 데이터 기반으로 분할해 band-pass 필터 뱅크를 만든다. 경계 ωn은 스펙트럼에서 자동으로 정해진다(§IV-B, 식 6–8). 즉 신호마다 적응적인 대역 분할이다.
- Table I: 분해 기반 연구 대부분이 하이퍼파라미터(분해 수준, 임계값 등)를 "Manually" 설정한다. 일부는 진화 알고리즘(Grey Wolf, Sand cat swarm)을 쓰거나 분해 수준을 기준으로 정한다.
- §IV-G: 분해 수준이 작으면 mode mixing이 생기고, 크면 가짜 주파수 성분이 생긴다.
- §X-5: 하이퍼파라미터를 수동으로 선택하는 문제를 미해결 과제로 꼽는다. "environment-agnostic automatic learning framework"가 필요하다고 한다.
- §X-3: 전처리(정규화, 샘플레이트, 창 길이)가 연구마다 달라서 결론이 달라진다고 지적한다.
- 평가: SNR, PSNR, SDR, SI-SNR, MSE. 주로 **깨끗한 기준 신호가 있는 합성 데이터**(Lorenz, Chen 등 혼돈 신호)를 쓴다. 실데이터에는 깨끗한 기준이 없다.

## 사용자 연구와의 관계 (`inferred`)

- 선박 소음에서 "잡음"과 "신호"의 경계는 모호하다. 광대역 캐비테이션 잡음은 선박 신호의 일부다. SNR 기반 평가를 그대로 적용하기 어렵다.
- 자동 대역 선택에는 이미 계열별 선행 방법이 있다: EWT, VMD 자동 K, kurtogram(DEMON 대역 선택) 등. kurtogram은 이 서베이에 나오지 않는다(Claude 기억, 원문 미확인).
- 현재 연구 방향(누출 없는 UATR 증강)에서 잡음 제거는 전처리 변수다. 도입하려면 baseline 대비 단일 변수 실험으로 다뤄야 한다.
