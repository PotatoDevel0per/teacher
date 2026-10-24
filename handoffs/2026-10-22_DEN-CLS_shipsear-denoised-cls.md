# Handoff → DEN·CLS: ShipsEar 잡음 제거 데이터로 분류 (R3-SE)

- 작성: 2026-10-22 (Teacher). 사용자 결정: ShipsEar로 학습한 FocuS-MN(R2 통과 모델, 시도 2b)을 **ShipsEar**에 적용하고, 분류기를 원본과 같은 설정으로 학습해 정확도를 비교한다. 실행은 R2c가 끝난 뒤(GPU), 준비는 지금(CPU).
- **누출 표시(필수):** R2 모델은 ShipsEar 선박 7종류와 배경 12녹음 전체로 학습했다. 그래서 우리 Ships-disjoint test fold의 선박 소리를 이미 봤다. 결과는 "잡음 제거기에 test 선박 누출이 있는 조건"으로만 해석한다.

## DEN (지금, CPU)

1. thesis ShipsEar 로더와 같은 방식(원본 52,734 Hz → soxr VHQ 16 kHz)으로 90 녹음 전체를 불러온다. `denoise()`(시도 2b ckpt, 3 s 창 50% 겹침 overlap-add)를 **녹음 단위**로 적용한다. 출력은 길이가 같은 16 kHz float 파형이고, `outputs/shipsear_denoised/<원본 파일명>.wav`(float32)에 저장한다.
2. 확인: 녹음마다 출력 길이가 입력과 같은지, NaN이 없는지.
3. 실녹음 진단(R2b와 같은 항목, 5 s 클립 2,223개 기준): 지운 에너지 비율, tonal 수 변화(thesis `core/evaluate/tonal.py` import), LTAS 대역별 변화. 클래스별(A–E)로도 낸다.
4. 커밋하고 경로와 진단 결과를 Teacher에게 보고한다.

## CLS (DEN 완료 후 CPU 준비, R2c 종료 후 GPU)

1. `core/` 데이터셋 레지스트리에 `shipsear_den`을 추가한다. 원본 경로만 DEN 출력으로 바꾸고, 클립 정의(`shipsear_clips.csv`, 2,223 클립)와 분할(`shipsear_shipcv_fold*`)은 원본과 **같게** 쓴다. 이미 16 kHz이므로 리샘플하지 않는다(편차로 기록).
2. MEL 캐시를 만든다(E1-rep MEL과 같은 추출기).
3. 학습: E1-rep ShipsEar D안과 같다(lr 3e-5 상수, 200 epoch, 마지막 epoch 지표). MEL × fold 5 × seed 0,1,2 = **15 run**.
4. 판정(사전 등록, `exp/R3_se/summarize.py` 먼저 커밋):
   - Δ = F1(잡음 제거) − F1(원본, E1-rep ShipsEar MEL), fold별 seed 평균, paired.
   - "도움": 평균 Δ > 0 이고 4/5 fold 이상 Δ > 0
   - "해로움": 평균 Δ < 0 이고 4/5 fold 이상 Δ < 0
   - 그 외: 판단 불가
   - 보조: acc, 클래스별 F1, seed sd. ShipsEar는 seed sd가 최대 8.7 pp라 검출력이 낮다는 점을 함께 적는다.
5. 결과 표에 원본과 잡음 제거를 나란히 두고, 누출 표시를 제목에 단다.
