# EXP-002 실험 지시서: UniqueShip 선박 분리 조건에서 범용 증강의 효과

- 작성: 2026-10-10 (teacher 세션)
- 실행 대상: `UATR_SLM_REPLAY` 세션 (EXP-001과 같은 파이프라인)
- 상위 결정: D-2026-10-06-02 (1순위: 물리 기반 증강으로 UATR 일반화)
- 검증할 가설: **H-AUG-1** — 누출 없는 분할에서 범용 증강의 효과는 작다
- 상태: **사용자 승인 (2026-10-10)**. A1–A4 전부 실행한다.

---

## 1. 목적

물리 기반 증강(EXP-003)이 넘어야 할 **범용 증강 기준선**을 만든다. 질문은 하나다.

> 선박(MMSI) 단위로 분리된 UniqueShip에서, 범용 증강 각각은 증강 없는 baseline 대비 macro-F1을 얼마나 바꾸는가?

문헌 근거 (`research/literature/uatr_augmentation_survey.md`):
- 기존 연구 중 선박 단위 분할에서 증강을 ablation한 연구는 0편이다.
- 녹음 단위 분할에서 CutMix 계열(LMR)은 DeepShip Mel 입력에서 +0.53 pp였다(Xu J. 2023, 단일 실행).
- 지도 학습에서는 음성용 증강도 +4.7–9.1 pp를 냈다(Hummel 2025, 날짜 분할, 단일 실행).
- 즉 기대 효과의 크기 자체가 불확실하다. 그래서 이 실험의 결과는 어느 방향이든 기여가 된다.

## 2. 고정 조건 (EXP-001 baseline과 동일, 바꾸지 않는다)

| 항목 | 값 |
|---|---|
| 데이터 | `/jhlee/data/uniqueship/5class_balanced/stage/main5_balanced/`, 공식 `fold_1..5` CSV |
| 분할 | 공식 MMSI 5-fold. train/val/test 그대로 사용 |
| 분류기 | SwinV2-Tiny (ImageNet 사전학습) + 2층 헤드 |
| 입력 | 16 kHz, 5 s, Mel (1024 window, 100% zero-pad, 75% overlap), 90 dB 동적범위(클립별 최댓값 기준), 256×256×3 |
| 학습 | AdamW, lr 1e-6, wd 0.01, CE, val loss 정체 시 lr ×1/5, 최대 30 epoch, batch 64 |
| 체크포인트 | best-val-macro-F1 (EXP-001과 동일) |
| seed | fold당 1개, EXP-001과 같은 seed |

- **증강 외에는 아무것도 바꾸지 않는다.** epoch 상한, 조기 종료 규칙, batch도 그대로 둔다.
- 증강 때문에 학습이 덜 됐는지는 best epoch를 기록해서 사후에 본다(조건을 바꾸지 않는다).

## 3. 실험 arm (각 arm은 baseline 대비 한 가지만 바꾼다)

모든 증강은 **train 배치에만, on-the-fly로** 적용한다. val과 test에는 적용하지 않는다. 혼합형 증강(A1, A2)의 짝은 **같은 train 배치 안에서만** 고른다.

| arm | 증강 | 적용 위치 | 설정 (사전 고정) | 근거 |
|---|---|---|---|---|
| A0 | 없음 (baseline) | — | EXP-001 결과를 재사용한다. §5 sanity check를 통과해야 한다 | — |
| A1 | **CutMix (LMR 근사)** | Mel 스펙트로그램 (정규화 후, 256×256) | p = 0.5. λ ~ Beta(1, 1). 직사각형 1개, 위치 균등 무작위. 라벨 혼합 λ = 1 − 면적비. 짝은 클래스와 무관하게 배치 내 무작위 | Xu J. 2023 §2.4. 원문에 빠진 패치 분포는 CutMix 표준값으로 채운다 → 기록에는 **"LMR을 CutMix 표준 구현으로 근사"**라고 쓴다 |
| A2 | **mixup** | Mel 스펙트로그램 (정규화 후) | p = 0.5. λ ~ Beta(0.4, 0.4). 라벨도 λ로 혼합 | Xu J. 2023 비교군, Mahmud 2025 |
| A3 | **SpecAugment (마스킹만)** | Mel 스펙트로그램 (정규화 후) | p = 0.5. 주파수 마스크 2개(각 폭 0–25 bin, 약 10%), 시간 마스크 2개(각 폭 0–25 프레임). 마스크 값 = 해당 스펙트로그램 평균. time warp 없음 | Park 2019. UATR 문헌에서 가장 흔하지만 ablation이 없다(Li J. 2022, Mohammadi 2025) |
| A4 | **일반 오디오 증강 묶음** | 파형 (16 kHz, 정규화 전) | p = 0.5로 다음 중 하나를 무작위 선택: pitch shift ±2 semitone, time stretch 0.9–1.1. ~~polarity 반전~~은 no-op이라 실행 전에 제외(2026-10-10, 편차 기록 참조) | Hummel 2025 Table 4(지도 학습에서 이득). tonal 절대 주파수를 바꾸는 "비물리" 증강의 대표. reverb는 수중 반향 모델이 아니므로 제외 |

### 하지 않는 것과 그 이유

- **gain(레벨) 증강은 이 파이프라인에서 하지 않는다.** UniqueShip 분류기는 클립별 최댓값 기준 90 dB 정규화를 하므로 gain을 바꿔도 입력이 거의 같다(사실상 no-op). 레벨 지름길 가설(H-AUG-3)은 절대 레벨을 보존하는 UATR-SLM에서 따로 검증한다.
- **증강 조합은 하지 않는다.** 이 실험은 개별 효과만 본다(`CLAUDE.md` §6).
- **하이퍼파라미터를 test로 고르지 않는다.** 위 설정은 사전 고정이다. 조정이 꼭 필요하면 val로만 하고, 조정 내역을 모두 기록한다.
- Gao 2026 SDA는 이번 실험에서 제외한다. 이득이 잡음 주입 조건에서만 확인됐기 때문이다. A1–A3 결과를 본 뒤 검토한다.

## 4. 실행 순서

1. **Sanity check (§5)**: 증강 hook을 넣은 코드로 증강 없이 fold 1을 다시 돌린다.
2. **A1 → A2 → A3 → A4** 순서로 각각 5 fold를 돌린다. arm 하나가 끝날 때마다 중간 보고한다.
3. **seed 확장 조건**: 어떤 arm이든 평균 paired Δ macro-F1의 절댓값이 1 pp를 넘으면, 그 arm과 A0을 seed 2개씩 더 돌린다(fold당 seed 3개).

run당 소요 시간을 첫 run에서 측정해 보고한다. 전체 일정이 GPU 2대 기준 3일을 넘을 것 같으면 실행 전에 알린다.

## 5. Sanity check와 중단 조건

- 증강 hook을 넣은 코드로 증강 없이 fold 1을 돌렸을 때 결과가 EXP-001 fold 1(acc 67.25)과 ±0.5 pp 안이어야 한다.
  - 같은 seed라면 비트 단위로 같은 것이 이상적이다. 다르면 원인(cudnn 비결정성 등)을 보고한다.
- 다음 경우에는 **중단하고 보고**한다.
  - sanity check 실패
  - 어떤 arm에서 train loss가 발산하거나 val F1이 baseline보다 10 pp 이상 낮음(구현 오류 의심)
  - 증강이 val이나 test에 적용된 흔적 발견

## 6. 기록할 것 (run마다)

- `args.json`: 증강 이름, 모든 파라미터, seed, 코드 커밋 해시 또는 파일 해시
- best epoch, 실행 epoch 수, 소요 시간
- test 지표: accuracy, macro-F1, 클래스별 F1, confusion matrix
- **test 클립별 예측 파일** (클립 경로, MMSI, 정답, 예측, softmax). 나중에 선박 단위 bootstrap과 MMSI 기준 NMI 분석에 쓴다.
- 증강 적용 확인용 샘플: arm마다 증강 전후 스펙트로그램 4장(그림 파일)

## 7. 분석과 판정 (사전 등록)

### 주 지표
fold별 **paired 차이** Δ_k = F1(arm, fold k) − F1(A0, fold k), k = 1..5

### 보고 형식
| arm | fold 1–5 Δ | 평균 Δ | Δ의 sd | 양수 fold 수 | 95% CI (t, df=4) |
|---|---|---|---|---|---|

- 클래스별 Δ도 함께 보고한다. tanker(51.1)와 passengership(51.7)을 따로 표시한다. passengership은 fold당 test 선박이 약 10척이라 해석에 주의한다.
- 보조: test 선박을 단위로 한 bootstrap CI(1000회, fold별로 선박을 재표집)

### 판정 규칙 (결과를 보기 전에 고정)
| 판정 | 조건 |
|---|---|
| **개선** | 평균 Δ > 0, 5개 fold 중 4개 이상 양수, t 95% CI가 0을 포함하지 않음 |
| **악화** | 평균 Δ < 0, 4개 이상 음수, CI가 0을 포함하지 않음 |
| **효과 불명** | 나머지 전부 |

- fold 5(EXP-001에서 63.56으로 혼자 낮았음)를 빼고 판정이 바뀌는지도 보고한다(민감도 분석). 판정 자체는 5 fold 기준이다.
- H-AUG-1 판정:
  - 모든 arm이 "효과 불명"이거나 평균 Δ가 1 pp 미만이면 → H-AUG-1 **지지**
  - 어떤 arm이든 "개선"이고 평균 Δ ≥ 1 pp이면 → H-AUG-1 **약화**. 그 arm이 EXP-003의 비교 기준이 된다.

## 8. 결과물

- `/jhlee/UATR_SLM/uniqueship_clf/runs/uniqueship_aug_<arm>_fold<k>/`
- 비교표 `/jhlee/UATR_SLM/uniqueship_clf/EXP002_COMPARE.md`: §7 표, 클래스별 Δ, best epoch, 소요 시간
- teacher 세션에 보고: §7 표, 판정, 편차 기록(지시서와 다르게 한 모든 것)

## 9. 이 실험이 답하지 않는 것

- 물리 기반 증강의 효과 (EXP-003)
- 다른 분류기(UATR-SLM, ResNet-18)에서의 일반성 (최종 확인 단계)
- 증강 조합의 효과
- DeepShip, ShipsEar에서의 효과

---

## 실행 중 발견·편차 기록

- 2026-10-10 (UATR_SLM_REPLAY 보고):
  - **A4 polarity 반전은 이 파이프라인에서 완전한 no-op이다.** Mel은 |STFT|에서 나오므로 |FFT(−x)| = |FFT(x)|이고, Mel max|Δ| = 0이다. 지시서 설계 오류다(Teacher 책임). 이대로면 A4의 실효 증강 확률은 0.5 × 2/3 ≈ 0.33이다.
  - **결정 (2026-10-10, 사용자)**: 옵션 ② — polarity를 빼고 pitch shift와 time stretch 2종만 쓴다. A4의 실효 증강 확률은 0.5다. A4를 실행하기 전에 지시서 버그를 고친 것이므로 사후 튜닝이 아니다. 보고서에는 "magnitude 스펙트로그램 입력에서는 polarity가 효과가 없어 제외했다"고 쓴다. 다른 대안: ① 3종 유지(실효 0.33), ③ p=0.75로 보정. 둘 다 기각했다. `UATR_SLM_REPLAY`에 전달했다.
  - GPU/CPU Mel 경로 일치: max|Δ| 2.44e-04로 fp16 양자화 한계보다 작다 → A4용 별도 대조군은 불필요하다.
  - pitch shift: `torchaudio.transforms.PitchShift`(resample + phase vocoder). n_steps는 {±0.5, ±1, ±1.5, ±2} 8개 이산값 중 균등 추출 → "±2 semitone"의 이산 근사. 합성 순음 기준 오차 ≤ 0.1%
  - time stretch: STFT(1024/256) → phase vocoder → ISTFT. 피치를 보존하고 5 s로 crop/pad. rate ~ U(0.9, 1.1). **배치당 값 1개**(샘플별이 아님)
- 2026-10-10 (UATR_SLM_REPLAY 보고, 결정 반영 후):
  - A4 반영 완료: `augment.py` WaveAug OPS = ("pitch", "stretch"), p = 0.5. args.json에 `removed: ["polarity"]`, 제외 이유, `stretch_scope: "batch"`(phase_vocoder가 rate를 스칼라로만 받음), `pitch_grid` 8개 이산값을 기록한다.
  - 준비 완료:
    - 파형 캐시: 153,595 클립, 24.6 GB
    - `uniqueship_clf/exp002/train.py`: A0은 EXP-001과 같은 코드 경로(hard label + CE)를 탄다
    - 산출물: args.json(코드 SHA-256), result.json, predictions.csv(MMSI, softmax 포함)
    - 실행 큐: `run_all.sh`
  - **블로커**: 14:30 KST부터 CUDA 초기화 실패.
    - cuInit → CUDA_ERROR_NOT_INITIALIZED. NVML/nvidia-smi는 정상이다(A5000 2장, 점유 0).
    - 11:02까지는 정상이었다.
    - 컨테이너 안에서는 복구할 수 없다. 호스트에서 드라이버를 재초기화하거나 컨테이너를 재시작해야 한다.
    - 복구를 감지하면 sanity check(A0 fold 1)를 자동으로 시작하는 감시 스크립트가 돌고 있다(30 s 주기, 24 h).
    - 일정 추정 28–47 h에 복구 지연 시간이 그대로 더해진다.
- 2026-10-12: 호스트 재부팅 후 GPU 복구 (cuInit 0, torch.cuda 장치 2개 연산 정상). 감시 스크립트가 만료돼서 sanity check를 수동으로 시작하도록 `UATR_SLM_REPLAY`에 요청했다. 서버 GPU 0, 1은 이 컨테이너에 마운트되어 있지 않다(/dev/nvidia2, 3만 있음). 따라서 장애가 그 GPU에 영향을 주지 않았다.
- 2026-10-12 (UATR_SLM_REPLAY 보고, sanity check 중):
  - 정규화 위치 차이(GPU fp32 나눗셈, 1 ULP)를 발견했고 수정했다. CPU 워커로 되돌린 뒤 입력이 EXP-001과 비트 일치한다. A4만 GPU Mel 경로에서 정규화한다.
  - **분류 헤드 초기화가 시드를 받지 않는다**: EXP-001과 EXP-002 모두 build_model() 뒤에 재시드한다. 그래서 Linear(768,512)-GELU-Linear(512,5) 헤드는 프로세스마다 다르게 초기화된다. ep00 val acc는 EXP-001 59.30, 1차 59.49, 2차 56.61이었다.
    - 따라서 §5의 "같은 seed면 비트 단위 동일"은 애초에 성립할 수 없었다(Teacher 지시서 가정 오류).
    - EXP-001의 fold 간 sd 2.45 pp에는 초기화 변동이 섞여 있다.
  - 진행 중: 현행 코드로 A0 fold 1을 계속 돌린다. EXP-001 fold 1과의 차이를 run 잡음의 1표본 추정치로 쓴다.
  - → **사용자 결정 대기**: 헤드 초기화를 시드로 고정할지, A0를 5 fold 모두 다시 돌릴지
- 2026-10-12 sanity check 결과 (A0 fold 1, 현행 코드, 헤드 비시드):
  - 지표 비교 (EXP-001 → EXP-002 A0)
    - acc: 67.25 → 68.37 (**+1.12 pp**, ±0.5 기준 미통과). `UATR_SLM_REPLAY`는 §5에 따라 중단했다.
    - macro-F1: 64.59 → 65.85
    - best epoch: 6 = 6
  - 구현 오류가 아니라는 근거: 증강 경로 미호출 확인, eval에 증강 없음, predictions 재계산 일치, MMSI 기준 ship-disjoint 재확인(MMSI 0 = background 자리표시자 제외 시 겹침 0), 입력 비트 일치
  - 해석 (inferred): 차이는 주로 헤드 초기화 차이에서 온다. 1표본이라 cudnn 비결정성과 분리할 수는 없다. 같은 설정을 두 번 돌릴 때 생기는 run 잡음이 약 1 pp 규모로 추정된다.
  - ±0.5 pp 기준은 "비트 단위 재현"이라는 틀린 전제에서 나온 값이었다(Teacher 오류). §7 판정 규칙(증강 효과 판정)과는 별개다.
- **결정 (2026-10-12, 사용자)**: ② 채택.
  - 시드를 build_model() **앞**으로 옮겨, 같은 fold 안의 A0–A4가 같은 헤드 초기화와 같은 데이터 순서를 쓰게 한다.
  - 증강 RNG는 학습 RNG와 분리한다.
  - A0는 EXP-001을 재사용하지 않는다. 새 코드로 **5 fold 모두 다시 돌린다**(추가 5 run).
  - §5 sanity check: 구현 정확성은 보고된 근거(증강 경로 미호출, eval 무증강, predictions 재계산, ship-disjoint, 입력 비트 일치)로 확인된 것으로 본다. 새 A0와 EXP-001의 차이는 보고만 한다.
  - ±0.5 pp 기준은 틀린 전제였으므로 폐기한다. 결과를 본 뒤 바꾼 기준이라는 사실을 보고서에 적는다. §7 판정 규칙은 바꾸지 않는다.
  - 표현: "fold 안에서 초기화와 데이터 순서를 맞춘 대응 비교"(학습 경로가 완전히 같은 것은 아니다)
- **결정 (2026-10-12, 사용자)**: EXP-002를 재개하기 전에 양성 대조군 EXP-002-PC(a)를 먼저 실행한다. 지시서: `research/experiments/EXP-002-PC_lmr_positive_control.md`
  - 같은 이유로 A1을 "CutMix(Beta(1,1)) 근사"에서 **원문 기술 그대로의 LMR**(a~U, b~U 독립, 1 패치, batch당 50%)로 바꾼다. 대조군이 검증한 모듈과 같은 모듈을 쓰기 위해서다. A1 실행 전 변경이다.
