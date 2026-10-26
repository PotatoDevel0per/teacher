"""S17 그림: R-US vs ShipsEar 모델(시도 2b)을 UniqueShip/DeepShip/ShipsEar 클립에 적용.

클립 선택 규칙(미리 고정): 데이터셋별 후보 풀에서 seed 0으로 5 s 클립 20개를 뽑고,
원본 tonal 수가 중앙값인 클립을 고른다(동률이면 앞의 것). 모든 입력은 16 kHz soxr VHQ + 클립별 DC 제거.
"""
import json, os, sys
import numpy as np, pandas as pd, soundfile as sf, soxr, torch, torchaudio
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from scipy.signal import welch

DEN = "/jhlee/UWShipNoise/denoising/FocuS-MN"
sys.path.insert(0, os.path.join(DEN, "src")); sys.path.insert(0, "/jhlee/UWShipNoise/thesis")
from focusmn.infer import load_model, denoise_with, DEFAULT_CFG
from core.evaluate import tonal

fm.fontManager.addfont("/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf")
plt.rcParams["font.family"] = "NanumBarunGothic"; plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.dirname(os.path.abspath(__file__))
SR, N = 16000, 80000
rng = np.random.default_rng(0)

def load16(path, start_s=None):
    x, sr = sf.read(path, dtype="float32", always_2d=True); x = x[:, 0]
    if sr != SR: x = soxr.resample(x, sr, SR, quality="VHQ").astype(np.float32)
    if start_s is not None: x = x[int(start_s * SR): int(start_s * SR) + N]
    return x

def dc(x): return (x - x.mean()).astype(np.float32)

def pick(cands):
    """cands: list of (label, loader). 20개 뽑아 tonal 수 중앙값 클립."""
    idx = rng.choice(len(cands), size=min(20, len(cands)), replace=False)
    xs = [(cands[i][0], dc(cands[i][1]())) for i in idx]
    xs = [(l, x) for l, x in xs if len(x) == N]
    n = [tonal.analyze(x)["n_lines"] for _, x in xs]
    order = np.argsort(n, kind="stable"); m = order[len(order) // 2]
    return xs[m][0], xs[m][1], n[m]

# UniqueShip fold1 test (cargo 선박, background)
US = "/jhlee/UWShipNoise/data/uniqueship/5class_balanced/stage/main5_balanced/audio"
ts = pd.read_csv(f"{DEN}/exp/rus_pool_test_ship.csv"); tb = pd.read_csv(f"{DEN}/exp/rus_pool_test_bg.csv")
us_ship = [(f"UniqueShip cargo, MMSI {r.mmsi}", (lambda p=f"{US}/cargo/{r.fname}": load16(p))) for r in ts[ts.cls == "cargo"].itertuples()]
us_bg = [(f"UniqueShip background", (lambda p=f"{US}/background/{r.fname}": load16(p))) for r in tb.itertuples()]
# DeepShip Cargo: R-US 학습 선박과 겹치지 않는 녹음만
DS = "/jhlee/UWShipNoise/data/deepship"
sid = pd.read_csv(f"{DS}/ship_id.csv", header=None, names=["cls", "rec", "ship", "a", "b", "c", "d"])
ov = set(pd.read_csv(f"{DEN}/runs/rus_ds_overlap/ship_matches.csv").ds_rec)
ds = []
for r in sid[(sid.cls == "Cargo") & (~sid.rec.isin(ov))].itertuples():
    d = f"{DS}/Cargo/{r.rec}"
    if not os.path.isdir(d): continue
    for w in os.listdir(d):
        p = f"{d}/{w}"; dur = sf.info(p).duration
        for s in range(0, int(dur) - 5, 5):
            ds.append((f"DeepShip Cargo, {r.ship} ({r.rec}, {s}–{s+5} s)", (lambda p=p, s=s: load16(p, s))))
# ShipsEar tugboat(두 모델 모두 학습에 없음: R2 test 선종)
SE = "/jhlee/UWShipNoise/legacy/Underwater_Acoustic/LIG_Diffusion/Datasets/ShipSEAR/AUDIOS"
se = []
for f in os.listdir(SE):
    if f.startswith(("15__", "31__")):
        dur = sf.info(f"{SE}/{f}").duration
        for s in range(0, int(dur) - 5, 5):
            se.append((f"ShipsEar tugboat ({f.split('__')[1][:-4]}, {s}–{s+5} s)", (lambda p=f"{SE}/{f}", s=s: load16(p, s))))

rows = [pick(us_ship), pick(ds), pick(se), pick(us_bg)]
m_se = load_model(os.path.join(DEN, "runs/r2_res_joint/ckpt/stage2_best.pt"), DEFAULT_CFG)
m_us = load_model(os.path.join(DEN, "runs/rus/ckpt/stage2_best.pt"), DEFAULT_CFG)
mel = torchaudio.transforms.MelSpectrogram(sample_rate=SR, n_fft=2048, win_length=1024, hop_length=256, n_mels=256, power=2.0)

def mdb(x): return 10 * np.log10(mel(torch.from_numpy(x)).numpy() + 1e-12)
E = lambda x: float(np.sum(x.astype(np.float64) ** 2))
cols = ["원본 (DC 제거)", "ShipsEar 모델 (시도 2b)", "UniqueShip 모델 (R-US)"]
fig, ax = plt.subplots(4, 4, figsize=(17, 15), gridspec_kw=dict(width_ratios=[1, 1, 1, 1.1]))
stats = []
for i, (lab, x, nl) in enumerate(rows):
    ys = [x, denoise_with(m_se, x), denoise_with(m_us, x)]
    S0 = mdb(x); vmax = S0.max(); vmin = vmax - 90
    mf = torchaudio.functional.melscale_fbanks(1025, 0, 8000, 256, SR).numpy()
    centers = (np.arange(1025) * SR / 2048) @ mf / np.maximum(mf.sum(0), 1e-9)
    for j, y in enumerate(ys):
        S = mdb(y)
        a = ax[i, j]; a.imshow(S, origin="lower", aspect="auto", vmin=vmin, vmax=vmax, cmap="magma",
                               extent=[0, 5, 0, 256])
        tk = [100, 300, 1000, 3000, 7000]
        a.set_yticks([np.argmin(np.abs(centers - t)) for t in tk]); a.set_yticklabels(["100", "300", "1k", "3k", "7k"])
        nt = tonal.analyze(y)["n_lines"]
        rm = 100 * (1 - E(y) / E(x))
        t = cols[j] if j == 0 else f"{cols[j]}\n지운 에너지 {rm:.0f}% · tonal {nt}"
        if j == 0: t = f"{cols[0]}\ntonal {nt}"
        a.set_title(t, fontsize=10)
        if j == 0: a.set_ylabel("주파수 (Hz, Mel)", fontsize=10)
        if i == 3: a.set_xlabel("시간 (s)")
        stats.append(dict(row=lab, col=cols[j], removed_pct=round(rm, 1), n_tonal=int(nt)))
    a = ax[i, 3]
    for y, c, l in zip(ys, ["k", "tab:blue", "tab:orange"], ["원본", "ShipsEar 모델", "R-US"]):
        f, P = welch(y, SR, nperseg=8192); k = (f >= 10) & (f <= 7500); a.semilogx(f[k], 10 * np.log10(P[k] + 1e-20), c, lw=1, label=l)
    a.set_xlim(10, 7500); a.grid(alpha=.3); a.set_title("장기 평균 스펙트럼 (LTAS)", fontsize=10); a.set_ylabel("dB")
    if i == 0: a.legend(fontsize=9)
    if i == 3: a.set_xlabel("주파수 (Hz)")
    ax[i, 0].text(0.01, 1.22, lab, transform=ax[i, 0].transAxes, fontsize=10.5, weight="bold")
fig.suptitle("같은 클립에 두 잡음 제거기를 적용 (행마다 원본 최댓값 기준 90 dB 색 범위 공유)", fontsize=13, y=0.995)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "rus3.png"), dpi=110)
json.dump(dict(rows=[r[0] for r in rows], stats=stats), open(os.path.join(OUT, "rus3.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(stats, ensure_ascii=False, indent=0))
