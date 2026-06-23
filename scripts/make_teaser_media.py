#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
BG = (11, 18, 32)
CARD = (20, 30, 50)
CARD2 = (25, 38, 64)
TEXT = (238, 242, 248)
MUTED = (166, 178, 196)
ACCENT = (90, 170, 255)
GOOD = (90, 220, 170)
WARN = (255, 190, 90)
BAD = (255, 120, 120)

TRAJ = Path("results/plots/trajectories/MH_05_difficult_xy_trajectories.png")
ERR = Path("results/plots/errors/MH_05_difficult_error_timeline.png")
OUT_PNG = Path("media/vio_failure_teaser.png")
OUT_GIF = Path("media/vio_failure_teaser.gif")

def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

F_TITLE = font(48, True)
F_SUB = font(25, False)
F_HEAD = font(30, True)
F_BODY = font(23, False)
F_SMALL = font(18, False)
F_NUM = font(34, True)

def fit_image(path: Path, box_w: int, box_h: int) -> Image.Image:
    img = Image.open(path).convert("RGB")
    img.thumbnail((box_w, box_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (box_w, box_h), (245, 247, 250))
    x = (box_w - img.width) // 2
    y = (box_h - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas

def rounded(draw: ImageDraw.ImageDraw, xy, radius=24, fill=CARD, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def text(draw: ImageDraw.ImageDraw, xy, s: str, fnt, fill=TEXT, spacing=8):
    draw.multiline_text(xy, s, font=fnt, fill=fill, spacing=spacing)

def bullet(draw: ImageDraw.ImageDraw, x: int, y: int, s: str, fill=TEXT):
    draw.ellipse((x, y + 9, x + 8, y + 17), fill=ACCENT)
    draw.text((x + 20, y), s, font=F_BODY, fill=fill)

def base() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 8), fill=ACCENT)
    return img

def frame_dashboard() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)

    d.text((38, 24), "Reproducible VIO/SLAM Failure Atlas", font=F_HEAD, fill=TEXT)
    d.text((40, 62), "MH_05_difficult stress case • ORB-SLAM3 vs OpenVINS • fair-overlap diagnosis", font=F_SMALL, fill=MUTED)

    traj = fit_image(TRAJ, 575, 360)
    err = fit_image(ERR, 575, 360)

    rounded(d, (35, 100, 635, 490), fill=(240, 243, 248), outline=(80, 96, 120))
    img.paste(traj, (48, 115))
    d.text((52, 500), "Trajectory comparison", font=F_SMALL, fill=MUTED)

    rounded(d, (645, 100, 1245, 490), fill=(240, 243, 248), outline=(80, 96, 120))
    img.paste(err, (658, 115))
    d.text((662, 500), "Error timeline + event-count callouts", font=F_SMALL, fill=MUTED)

    rounded(d, (35, 535, 405, 690), fill=CARD2, outline=(50, 70, 105))
    d.text((60, 558), "Fair-overlap APE", font=F_BODY, fill=TEXT)
    d.text((60, 600), "ORB-SLAM3", font=F_SMALL, fill=MUTED)
    d.text((185, 592), "0.065589 m", font=F_BODY, fill=GOOD)
    d.text((60, 640), "OpenVINS", font=F_SMALL, fill=MUTED)
    d.text((185, 632), "0.242839 m", font=F_BODY, fill=BAD)

    rounded(d, (430, 535, 830, 690), fill=CARD2, outline=(50, 70, 105))
    d.text((455, 558), "Failure evidence", font=F_BODY, fill=TEXT)
    d.text((455, 600), "ORB-SLAM3: bad-IMU reset, lost frames", font=F_SMALL, fill=WARN)
    d.text((455, 635), "OpenVINS: 289 static init failures", font=F_SMALL, fill=BAD)
    d.text((455, 665), "OpenVINS: LibraryUnloadException", font=F_SMALL, fill=BAD)

    rounded(d, (855, 535, 1245, 690), fill=CARD2, outline=(50, 70, 105))
    d.text((880, 558), "Takeaway", font=F_BODY, fill=TEXT)
    d.text((880, 598), "Accuracy table + trajectory plots +", font=F_SMALL, fill=MUTED)
    d.text((880, 628), "error timelines + log evidence", font=F_SMALL, fill=MUTED)
    d.text((880, 660), "= failure diagnosis, not just metrics", font=F_SMALL, fill=ACCENT)

    return img

def frame_title() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    text(d, (70, 82), "Reproducible VIO/SLAM\nFailure Atlas", F_TITLE)
    text(d, (74, 205), "ORB-SLAM3 vs OpenVINS on EuRoC MH_05_difficult", F_SUB, MUTED)

    rounded(d, (70, 300, 1210, 610), fill=CARD2, outline=(50, 70, 105))
    bullet(d, 110, 345, "Fair-overlap metrics compare only the common timestamp interval.")
    bullet(d, 110, 400, "Error timelines show when trajectory error grows.")
    bullet(d, 110, 455, "Failure cards connect metrics to backend log evidence.")
    bullet(d, 110, 510, "CI checks tests, artifacts, PNG validity, and stale documentation.")

    d.text((74, 650), "v1.1.0 release • reproducible derived artifacts • failure-focused benchmark", font=F_SMALL, fill=MUTED)
    return img

def frame_trajectory() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    d.text((50, 30), "MH_05_difficult: trajectory comparison", font=F_HEAD, fill=TEXT)
    d.text((52, 68), "Stress sequence with bad-IMU/lost-frame evidence and OpenVINS init failures.", font=F_SMALL, fill=MUTED)

    plot = fit_image(TRAJ, 760, 500)
    rounded(d, (42, 110, 842, 650), fill=(240, 243, 248), outline=(80, 96, 120))
    img.paste(plot, (62, 130))

    rounded(d, (880, 115, 1215, 650), fill=CARD2, outline=(50, 70, 105))
    d.text((910, 150), "Fair-overlap APE", font=F_HEAD, fill=TEXT)
    d.text((910, 220), "ORB-SLAM3", font=F_BODY, fill=MUTED)
    d.text((910, 250), "0.065589 m", font=F_NUM, fill=GOOD)
    d.text((910, 330), "OpenVINS", font=F_BODY, fill=MUTED)
    d.text((910, 360), "0.242839 m", font=F_NUM, fill=BAD)
    d.text((910, 460), "Takeaway", font=F_BODY, fill=TEXT)
    text(d, (910, 495), "Lower aligned error\nfor ORB-SLAM3,\neven with clear\nfailure evidence.", F_SMALL, MUTED)
    return img

def frame_error() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)
    d.text((50, 30), "Error timeline + failure-event evidence", font=F_HEAD, fill=TEXT)
    d.text((52, 68), "The atlas connects trajectory error to backend-specific log symptoms.", font=F_SMALL, fill=MUTED)

    plot = fit_image(ERR, 800, 500)
    rounded(d, (42, 110, 882, 650), fill=(240, 243, 248), outline=(80, 96, 120))
    img.paste(plot, (62, 130))

    rounded(d, (915, 115, 1220, 650), fill=CARD2, outline=(50, 70, 105))
    d.text((945, 150), "Event evidence", font=F_HEAD, fill=TEXT)
    d.text((945, 220), "ORB-SLAM3", font=F_BODY, fill=TEXT)
    bullet(d, 945, 260, "bad-IMU reset", WARN)
    bullet(d, 945, 305, "lost-frame evidence", WARN)
    d.text((945, 380), "OpenVINS", font=F_BODY, fill=TEXT)
    bullet(d, 945, 420, "289 static init failures", BAD)
    bullet(d, 945, 465, "LibraryUnloadException", BAD)
    d.text((945, 555), "Accuracy table +\nlog evidence =\nfailure diagnosis", font=F_SMALL, fill=MUTED)
    return img

def frame_takeaway() -> Image.Image:
    img = base()
    d = ImageDraw.Draw(img)

    d.text((70, 55), "What this project demonstrates", font=F_TITLE, fill=TEXT)

    rounded(d, (70, 155, 595, 560), fill=CARD2, outline=(50, 70, 105))
    d.text((105, 195), "Robotics perception", font=F_HEAD, fill=TEXT)
    bullet(d, 110, 265, "VIO/SLAM evaluation")
    bullet(d, 110, 320, "trajectory alignment")
    bullet(d, 110, 375, "timestamp-overlap fairness")
    bullet(d, 110, 430, "failure-mode analysis")

    rounded(d, (685, 155, 1210, 560), fill=CARD2, outline=(50, 70, 105))
    d.text((720, 195), "Engineering hygiene", font=F_HEAD, fill=TEXT)
    bullet(d, 725, 265, "reproduce_results.sh")
    bullet(d, 725, 320, "CI tests + artifact checks")
    bullet(d, 725, 375, "published v1.1.0 release")
    bullet(d, 725, 430, "diagnostic README guide")

    d.text((70, 620), "Built a benchmark and failure atlas — not a new SLAM backend.", font=F_SUB, fill=ACCENT)
    return img

def main() -> int:
    missing = [str(p) for p in [TRAJ, ERR] if not p.exists()]
    if missing:
        raise SystemExit("Missing source images: " + ", ".join(missing))

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

    dashboard = frame_dashboard()
    frames = [
        dashboard,
        frame_trajectory(),
        frame_error(),
        frame_takeaway(),
    ]

    dashboard.save(OUT_PNG)

    gif_frames = [f.resize((960, 540), Image.Resampling.LANCZOS) for f in frames]
    gif_frames[0].save(
        OUT_GIF,
        save_all=True,
        append_images=gif_frames[1:],
        duration=[1200, 1800, 1800, 1600],
        loop=0,
        optimize=True,
    )

    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_GIF}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
