# Handoff → CLS: E1-src-CQT — tonal 입력을 CQT로 그리면 달라지는가

- 작성: 2026-10-21 (Teacher). 받는 곳: `CLS`. 우선순위: **E1-AE보다 먼저**(사용자 결정 2026-10-21). GEN은 GPU 사용을 보류한다.
- 배경: E1-src(MEL)에서 Ships-disjoint F1은 B 53.16, O_rp 52.20, T 41.87이었다. 이것을 "클래스 정보는 broadband에 있다"(H-SC-3)로 읽었다. 그런데 MEL 이미지는 window 주엽이 ±31 Hz라 tonal 하나가 약 9칸에 번진다(GEN 사전 점검: MEL 피크 중앙값 0–1, CQT 5). 그래서 T가 MEL에서 불리했을 수 있다(사용자 지적).
- 질문: 같은 입력(O_rp, B, T)을 **CQT 이미지**로 그리면 T가 크게 좋아지는가?

## 설계 (E1-src와 한 가지만 다름: 특징 도메인 MEL → CQT)

- 입력: E1-src와 같은 파형 변환(`core/features_src.transform`, 같은 seed = 클립 idx). 특징만 E1-rep의 CQT 추출기(`Extractor("cqt")`: f_min 20 Hz, 30 bin/oct, 256 bin, hop 256)로 바꾼다.
- 캐시: `cache/deepship_src_{orp,bb,tn}_cqt256.f16` 3 × 약 4.4 GB. 만든 뒤 빈 클립·NaN을 점검한다.
- 분할: **Ships-disjoint만**(shipcv 5 fold). 이번 질문은 클래스 정보량이라 Rec-disjoint는 돌리지 않는다.
- 학습: DeepShip E1-rep v2 설정(E1-src와 같음), seed 0. 3 arm × 5 fold = **15 run**.

## 판정 (사전 등록, `exp/E1_src_cqt/summarize.py`를 먼저 커밋)

- 주 비교: ΔT = F1(T, CQT) − F1(T, MEL), fold별 짝(같은 fold, 같은 seed 0). MEL 값은 E1-src shipcv 결과를 쓴다.
  - **"MEL이 tonal 정보를 가렸다" 지지:** 평균 ΔT ≥ +2.2 pp(측정된 run 잡음 1.1 pp의 2배) 이고 5 fold 중 4개 이상에서 ΔT > 0
  - **반대:** 평균 ΔT ≤ 0 이거나 양수 fold 2개 이하 → "tonal 정보량은 표현과 거의 무관"
  - 그 사이: 보류
- 보조(판정 무관):
  - CQT 안에서의 격차 B − T, T − O_rp(MEL 안의 격차와 비교)
  - ΔB, ΔO_rp(같은 방식)
  - E1-rep CQT 원본 seed 0과 O_rp-CQT의 차이(시간 구조 기여, CQT 기준)
  - 클래스별 F1(특히 Cargo: MEL-T에서 17.7)

## 산출물

- `exp/E1_src_cqt/`: 스크립트, results, summarize.py(사전 커밋), REPORT.md
- 캐시 완성, 판정 시점에 커밋·보고(UTC). 끝나면 GEN이 E1-AE를 시작할 수 있도록 GPU가 비었다고 Teacher에게 알린다.
