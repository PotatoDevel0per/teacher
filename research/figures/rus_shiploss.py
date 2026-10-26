"""R-US가 선박 소리도 지운다는 것을 보이는 그림 (UniqueShip, 누출 없는 fold1 test).
(위) 클래스별 지운 에너지와 대역별 LTAS 변화: 전체 153,595 클립 진단(DEN diag_summary.json).
(아래) fold1 test 선박 클립 2개(cargo, tug): 입력 / R-US 출력 / 지워진 성분(입력 - 출력).
선택 규칙: 클래스별 fold1 test 클립에서 seed 0으로 20개 → 입력 tonal 수 중앙값 클립. 입력은 DC 제거.
"""
import os, sys, json, numpy as np, pandas as pd, soundfile as sf, soxr, torch, torchaudio
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
sys.path.insert(0, "/jhlee/UWShipNoise/thesis"); from core.evaluate import tonal
fm.fontManager.addfont("/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf")
plt.rcParams["font.family"] = "NanumBarunGothic"; plt.rcParams["axes.unicode_minus"] = False
DEN = "/jhlee/UWShipNoise/denoising/FocuS-MN"; US = "/jhlee/UWShipNoise/data/uniqueship/5class_balanced/stage/main5_balanced/audio"
OUT = os.path.dirname(os.path.abspath(__file__)); SR = 16000; rng = np.random.default_rng(0)
dg = json.load(open(f"{DEN}/outputs/uniqueship_denoised/diag_summary.json"))
ts = pd.read_csv(f"{DEN}/exp/rus_pool_test_ship.csv")
def inp(cls, f):
    x, sr = sf.read(f"{US}/{cls}/{f}", dtype="float32", always_2d=True)
    x = soxr.resample(x[:, 0], sr, SR, quality="VHQ").astype(np.float32); return x - x.mean()
outp = lambda cls, f: sf.read(f"{DEN}/outputs/uniqueship_denoised/{cls}/{f}", dtype="float32")[0]
picks = []
for cls in ["cargo", "tug"]:
    c = ts[ts.cls == cls].iloc[rng.choice((ts.cls == cls).sum(), 20, replace=False)]
    xs = [(r.fname, r.mmsi, inp(cls, r.fname)) for r in c.itertuples()]
    n = [tonal.analyze(x)["n_lines"] for *_, x in xs]
    f, m, x = xs[int(np.argsort(n, kind="stable")[len(n) // 2])]
    picks.append((cls, f, m, x, outp(cls, f)))
mel = torchaudio.transforms.MelSpectrogram(sample_rate=SR, n_fft=2048, win_length=1024, hop_length=256, n_mels=256, power=2.0)
mdb = lambda x: 10 * np.log10(mel(torch.from_numpy(np.ascontiguousarray(x, dtype=np.float32))).numpy() + 1e-12)
mf = torchaudio.functional.melscale_fbanks(1025, 0, 8000, 256, SR).numpy()
centers = (np.arange(1025) * SR / 2048) @ mf / np.maximum(mf.sum(0), 1e-9)
fig = plt.figure(figsize=(16, 13)); gs = fig.add_gridspec(3, 3, height_ratios=[1, 1, 1], hspace=0.45, wspace=0.25)
order = ["background", "cargo", "passengership", "tanker", "tug"]; lab = {"background": "배경", "cargo": "cargo", "passengership": "passenger", "tanker": "tanker", "tug": "tug"}
a = fig.add_subplot(gs[0, 0]); v = [100 * dg["by_class"][c]["removed_frac_mean"] for c in order]
b = a.bar([lab[c] for c in order], v, color=["#888"] + ["tab:orange"] * 4)
for r, val in zip(b, v): a.text(r.get_x() + r.get_width() / 2, val + 1, f"{val:.0f}%", ha="center", fontsize=10)
a.set_ylim(0, 100); a.set_ylabel("지운 에너지 (%)"); a.set_title("클래스별 지운 에너지 (UniqueShip 전체 153,595 클립)", fontsize=11)
a = fig.add_subplot(gs[0, 1:]); bands = list(dg["by_class"]["cargo"]["ltas_delta_db"].keys())
for c, col in zip(order, ["#888", "tab:blue", "tab:green", "tab:red", "tab:purple"]):
    a.plot(bands, [dg["by_class"][c]["ltas_delta_db"][k] for k in bands], "o-", color=col, label=lab[c], lw=2 if c == "background" else 1.3)
a.axhline(0, color="k", lw=.6); a.set_ylabel("LTAS 변화 (dB)"); a.set_xlabel("대역 (Hz)"); a.grid(alpha=.3); a.legend(ncol=5, fontsize=9)
a.set_title("대역별 LTAS 변화: 선박 클래스도 배경과 거의 같은 폭(-6~-9 dB)으로 줄어든다", fontsize=11)
for i, (cls, f, m, x, y) in enumerate(picks):
    r = x - y; vmax = mdb(x).max()
    for j, (z, t) in enumerate([(x, "입력 (DC 제거)"), (y, "잡음 제거 출력"), (r, "지워진 성분 (입력 - 출력)")]):
        a = fig.add_subplot(gs[i + 1, j]); a.imshow(mdb(z), origin="lower", aspect="auto", vmin=vmax - 90, vmax=vmax, cmap="magma", extent=[0, 5, 0, 256])
        tk = [100, 300, 1000, 3000, 7000]; a.set_yticks([np.argmin(np.abs(centers - q)) for q in tk]); a.set_yticklabels(["100", "300", "1k", "3k", "7k"])
        e = 100 * np.sum(z.astype(np.float64) ** 2) / np.sum(x.astype(np.float64) ** 2); nt = tonal.analyze(z)["n_lines"]
        a.set_title(f"{t}\n에너지 {e:.0f}% · tonal {nt}", fontsize=10)
        if j == 0: a.set_ylabel(f"UniqueShip {cls} (fold1 test)\nMMSI {m}\n주파수 (Hz, Mel)", fontsize=9.5)
        if i == 1: a.set_xlabel("시간 (s)")
fig.suptitle("UniqueShip으로 학습한 잡음 제거기는 배경뿐 아니라 선박 소리도 지운다 (UniqueShip fold1, 누출 없음)", fontsize=13, y=0.995)
fig.savefig(os.path.join(OUT, "rus_shiploss.png"), dpi=110, bbox_inches="tight")
print([(p[0], p[1]) for p in picks])
