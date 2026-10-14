# DGM — 8 kHz·4 s 스펙트로그램 생성, 프레임워크 6종 비교 ("라운드 1")

- 경로: `/jhlee/UWShipNoise/generation/DGM` (31 GB, git 없음)
- 기간: 2026-08-19 ~ 09-01. 보고서 `docs/01_EXPERIMENT_REPORT.md`는 08-29에 작성됐고, 그 뒤의 band50 최종 평가와 lf2k 결과는 반영되지 않았다.
- 이름: DGM의 정의는 어디에도 없다. Deep Generative Model(s)로 추정한다 `[추론]`.
- 전체 상태: `hypothesis`. 표기 규칙은 [README.md](README.md) §0.

## 1. 문제 정의

DeepShip 4클래스를 조건으로 8 kHz·4 s STFT dB 스펙트로그램을 생성하고, 같은 UNet으로 생성 프레임워크 6종(OT-CFM, SB-CFM, DDPM, DDIM, VE-SDE, ReFlow)을 비교했다. 평가 프로토콜(KAD + 물리 지표 판정축)도 함께 정의했다. 설계 출발점은 외부에서 작성된 것으로 보이는 가이드 `docs/DEEPSHIP_GEN_EXPERIMENT_GUIDE.md`다.

## 2. 데이터

- 원천: `/jhlee/UWShipNoise/legacy/Underwater_Acoustic/Datasets/deepship`의 32 kHz 30 s 세그먼트 5,378개. **다른 폴더와 원천 경로가 다르다.**
- 8 kHz로 리샘플하고 4 s 비중첩 조각 7개로 잘랐다 → 37,646개, `wav8k.npy` 4.8 GB `[확인]` (`scripts/build_wav8k.py`)
- 표현 A: STFT n_fft 1024 / hop 256, 20log10|S|를 [−120, 25] dB로 clip, 모델 입력 512×128. A0는 전역 정규화, A1은 per-bin whitening. 복소 표현 B는 코드만 있다.
- 분할 split4 `[확인]` (`cache/chunks.csv`): train 23,198 / train_dev 3,164 / dev 5,642 / test 5,642.
  - 선박 group 겹침 0, 녹음 겹침 0.
  - train_dev는 train과 같은 선박의 다른 녹음이다(암기 진단용).
  - test Tug 2척, Passenger 4척.
- 복원: SPSI + GL200.

## 3. 방법

- 2D UNet 22.66M, FiLM(t, class), CFG null class(p_uncond 0.1), bs 32, lr 2e-4, EMA 0.9999, **seed 0 하나**
- OT-CFM: σ_min=0 직선 경로, midpoint NFE 50. SB-CFM은 σ_sb>0이고 t를 clamp한 변형이다(참조 구현과 다름).
- 논문 방법 그대로가 아니라 **아이디어를 기반으로 스펙트로그램 도메인에 맞게 변형**했다.

## 4. 결과

KAD 판정선은 train↔dev 0.00879(n=900)다 (`results/kad_baseline.json`). 판정선 대비 배수로 적는다.

| 실험 | 결과 `[확인]` | 문서 결론 |
|---|---|---|
| gate1 세션 상관 | 같은 선박 L2/L4 = 61–67% | KAD의 상당 부분이 세션 차이를 잰다 |
| A0 vs A1 (H1) | whitening 효과 +0.4~6.6% | dB 도메인에서 whitening 무의미 |
| H2 (복소 도메인) | 미실행 | 공백 |
| A0 OT-CFM 100k / 200k | 1.44× / 1.28× (cfg3) | 최선 결과, PARTIAL 3/4 |
| SB-CFM 100k | 1.72× | |
| ReFlow 100k | 2.30× | 교사보다 나쁨 |
| DDIM / DDPM 100k | KAD 0.063 / 0.068 | 문서 결론: CFM이 5.6배 좋음 |
| VE-SDE | σ 오설정 2회, 20k에서 중단 | 기각 |
| band50 (저역 loss 가중) | 1.89× | 가설 반증. 100k 최종값은 미문서화 |
| lf2k (0–2 kHz만) | f257 판정선 대비 1.06× | 대역을 줄인 효과이지 개선이 아님 `[추론]` |
| 분류기 v1 (TSTR 심판 후보) | dev 0.497, test 0.579 | 심판으로 쓰기엔 약함 |
| DEMON rpm | 4 s 창으로는 개별 판정 불가 | |

## 5. 문제·의심점

1. seed 1개, CI 없음. KAD 판정선도 점추정이다.
2. 판정 임계를 pilot 결과를 본 뒤 정했다. K 기준은 0.408 → 0.01002 → 0.00879로 바뀌었다. D·L 축이 단측이라 과증폭(DDPM 동적범위 149%)도 통과한다.
3. 생성물만 GL을 거치고 참조는 원본이다. GL 오차(+0.0012)는 판정선의 약 14%다 `[추론]`.
4. n=256과 n=900 결과를 같은 표에 섞었다.
5. **`physmetrics.compare()` LTAS 버그**: FMAX_BIN을 적용하지 않아 lf2k LTAS L1이 41 dB로 나온다 `[확인]`.
6. 학습 예산이 다르다: OT-CFM만 200k, 나머지는 100k.
7. downstream(TSTR/증강) 기여는 측정하지 않았다.
8. 보고서 스스로 관측 함정 5건을 인정했다(EMA 진폭 억제, 사다리 오선택 등). 무효 결과는 `results/invalid/`에 격리돼 있다.

## 6. 재사용 가치

- 분할: `cache/chunks.csv` (선박 분리 + train_dev 암기 진단 세트라는 설계 아이디어)
- 코드: `scripts/{repr,cfm,diffusion,reflow,model,eval_gen,kad_baseline,physmetrics,verdict,phase_recon,demon_rpm}.py`, `scripts/lofar_lig/`
- 교훈 `[문서]`:
  - real↔real 기준선 위에서만 지표를 해석한다.
  - 학습 초기 판정은 EMA가 아니라 raw 가중치로 한다.
  - 물리 지표 통과와 KAD 실패가 괴리될 수 있다.
  - 산출물 파일명에 step을 넣는다.
- 체크포인트: `ckpt/` 14 GB, `band/` 2.1 GB, `lf2k/` 2.7 GB
