"""R3-DS(DC 미제거 입력) vs R3-DS-DC(5 s DC 제거 입력) 잡음 제거 출력 비교, DeepShip 클래스별 1클립.
선택 규칙: 클래스마다 전체 5 s 클립에서 seed 0으로 20개 → 원본 tonal 수 중앙값 클립.
표시: 모든 패널은 클립별 DC 제거 후(분류기 입력과 같은 조건), 행마다 원본 최댓값 기준 90 dB.
"""
import os, sys, json, numpy as np, soundfile as sf, soxr, torch, torchaudio
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from scipy.signal import welch
sys.path.insert(0, "/jhlee/UWShipNoise/thesis"); from core.evaluate import tonal
fm.fontManager.addfont("/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf")
plt.rcParams["font.family"] = "NanumBarunGothic"; plt.rcParams["axes.unicode_minus"] = False
SR, N = 16000, 80000; DS = "/jhlee/UWShipNoise/data/deepship"; O = "/jhlee/UWShipNoise/denoising/FocuS-MN/outputs"
rng = np.random.default_rng(0); OUT = os.path.dirname(os.path.abspath(__file__))
import pandas as pd
sid = pd.read_csv(f"{DS}/ship_id.csv", header=None, names=["cls", "rec", "ship", "a", "b", "c", "d"]).set_index("rec").ship.to_dict()
def raw(p):
    x, sr = sf.read(p, dtype="float32", always_2d=True); x = x[:, 0]
    return soxr.resample(x, sr, SR, quality="VHQ").astype(np.float32) if sr != SR else x
dc = lambda x: (x - x.mean()).astype(np.float32)
rows = []
for cls in ["Cargo", "Passenger", "Tanker", "Tug"]:
    cands = []
    for rec in sorted(os.listdir(f"{O}/deepship_denoised_dc/{cls}")):
        for w in os.listdir(f"{O}/deepship_denoised_dc/{cls}/{rec}"):
            n = sf.info(f"{O}/deepship_denoised_dc/{cls}/{rec}/{w}").frames // N
            cands += [(cls, rec, w, k) for k in range(n)]
    pick = [cands[i] for i in rng.choice(len(cands), 20, replace=False)]
    cache = {}
    def clip(src, c):
        cls, rec, w, k = c
        key = (src, cls, rec, w)
        if key not in cache: cache[key] = raw(f"{DS}/{cls}/{rec}/{w}") if src == "raw" else sf.read(f"{O}/{src}/{cls}/{rec}/{w}", dtype="float32")[0]
        return dc(cache[key][k * N:(k + 1) * N])
    nl = [tonal.analyze(clip("raw", c))["n_lines"] for c in pick]
    c = pick[int(np.argsort(nl, kind="stable")[len(nl) // 2])]
    rows.append((c, [clip("raw", c), clip("deepship_denoised", c), clip("deepship_denoised_dc", c)]))
mel = torchaudio.transforms.MelSpectrogram(sample_rate=SR, n_fft=2048, win_length=1024, hop_length=256, n_mels=256, power=2.0)
mdb = lambda x: 10 * np.log10(mel(torch.from_numpy(x)).numpy() + 1e-12)
E = lambda x: float(np.sum(x.astype(np.float64) ** 2))
mf = torchaudio.functional.melscale_fbanks(1025, 0, 8000, 256, SR).numpy()
centers = (np.arange(1025) * SR / 2048) @ mf / np.maximum(mf.sum(0), 1e-9)
cols = ["원본 (DC 제거)", "잡음 제거 출력: DC 미제거 입력", "잡음 제거 출력: DC 제거 입력"]
fig, ax = plt.subplots(4, 4, figsize=(17, 15), gridspec_kw=dict(width_ratios=[1, 1, 1, 1.1])); st = []
for i, ((cls, rec, w, k), ys) in enumerate(rows):
    vmax = mdb(ys[0]).max()
    for j, y in enumerate(ys):
        a = ax[i, j]; a.imshow(mdb(y), origin="lower", aspect="auto", vmin=vmax - 90, vmax=vmax, cmap="magma", extent=[0, 5, 0, 256])
        tk = [100, 300, 1000, 3000, 7000]; a.set_yticks([np.argmin(np.abs(centers - t)) for t in tk]); a.set_yticklabels(["100", "300", "1k", "3k", "7k"])
        nt = tonal.analyze(y)["n_lines"]; rm = 100 * (1 - E(y) / E(ys[0]))
        a.set_title(f"{cols[j]}\ntonal {nt}" if j == 0 else f"{cols[j]}\n지운 에너지 {rm:.0f}% · tonal {nt}", fontsize=10)
        if j == 0: a.set_ylabel("주파수 (Hz, Mel)")
        if i == 3: a.set_xlabel("시간 (s)")
        st.append(dict(cls=cls, rec=rec, k=k, col=cols[j], removed=round(rm, 1), tonal=int(nt)))
    a = ax[i, 3]
    for y, c, l in zip(ys, ["k", "tab:red", "tab:green"], ["원본", "DC 미제거 입력", "DC 제거 입력"]):
        f, P = welch(y, SR, nperseg=8192); m = (f >= 10) & (f <= 7500); a.semilogx(f[m], 10 * np.log10(P[m] + 1e-20), c, lw=1, label=l)
    a.set_xlim(10, 7500); a.grid(alpha=.3); a.set_title("장기 평균 스펙트럼 (LTAS)", fontsize=10); a.set_ylabel("dB")
    if i == 0: a.legend(fontsize=9)
    if i == 3: a.set_xlabel("주파수 (Hz)")
    ax[i, 0].text(0.01, 1.22, f"DeepShip {cls}, {sid.get(rec, '?')} ({rec}, {5*k}–{5*k+5} s)", transform=ax[i, 0].transAxes, fontsize=10.5, weight="bold")
fig.suptitle("ShipsEar로 학습한 잡음 제거기를 DeepShip에 적용: DC 미제거 입력 vs DC 제거 입력\n모든 패널은 클립별 DC 제거 후 표시(분류기 입력 조건), 행마다 원본 최댓값 기준 90 dB", fontsize=13, y=0.998)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "dsdc.png"), dpi=110)
json.dump(st, open(os.path.join(OUT, "dsdc.json"), "w"), ensure_ascii=False, indent=0)
for s in st: print(s)
