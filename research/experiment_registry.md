# Experiment Registry

## 이전 실험 (2026-08 ~ 2026-09, 타당성 미검증)

사용자가 Claude Code와 함께 약식으로 진행했다. 모든 결론은 `hypothesis` 상태다. 상세는 `research/prior_experiments/`에 있다.

| ID | 폴더 | 기간 | 유형 | 핵심 결과 (문서상) | 분할 | seed | 상태 |
|---|---|---|---|---|---|---|---|
| PRIOR-DGM | `/jhlee/DGM` | 08-19 ~ 09-01 | 생성 (8 kHz 4 s dB STFT, 6 프레임워크) | 최선 OT-CFM 200k, KAD 판정선의 1.28× | split4 (선박 분리) | 1 | hypothesis |
| PRIOR-DSA | `/jhlee/deepship_analysis` | 09-04 ~ 09-09 | 데이터 분석, 보코더 왕복 | mel+HiFi-GAN 톤 피크 일치 22.6% ≈ 우연 | 해당 없음 | - | hypothesis |
| PRIOR-SLM | `/jhlee/UATR_SLM` | 09-05, 09-08 | 인식 재현 + 누수 측정 | macro-F1 S0 97.7 / S1 65.8 / S2 50.0 | S0/S1/S2 | 3 | hypothesis (가장 탄탄함) |
| PRIOR-DSP | `/jhlee/deepship_preprocessing` | 09-08 ~ 09-09 | 전처리 파이프라인, 복원 설정 결정 | n_fft 16384 + GL로 저역 피크 일치 95% | ship_disjoint | - | hypothesis |
| PRIOR-OTCFM | `/jhlee/ot-cfm` | 09-10 ~ 09-29 | 생성 (30 s 2-stream, CFM vs DDIM) | 통과 체크포인트 없음, 30k부터 모드 축소 | ship_disjoint | 1 | hypothesis |
| PRIOR-PGMCLDM | `/jhlee/PG-MCLDM` | 09-28 ~ 09-30 | 물리 조건 latent 생성 + 증강 | 증강 +0.66%p (유의성 없음), G0 재현 미통과 | DEMONet Table 10 (선박 누수 74%) | 1 | hypothesis, 중단 |

**주의**: 분할이 폴더마다 다르므로 폴더 사이에서 수치를 비교하면 안 된다 (`research/prior_experiments/README.md` §2).

## 새 실험

(아직 없음)
