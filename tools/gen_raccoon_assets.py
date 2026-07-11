# -*- coding: utf-8 -*-
"""사용자 생성 너구리 원화(raccoon.png)로 로고/썸네일/앱 아이콘 재제작.
외곽 흰 모서리는 크롭 대신 배경색으로 채워 풀블리드 처리(원본 손실 없음)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

SRC_DIR = Path(r"C:/Users/BRAIN/Downloads/너구리굴-앱인토스-에셋")
OUT = Path(__file__).resolve().parent.parent / "toss-assets"
ROOT = Path(__file__).resolve().parent.parent
NAVY = (23, 26, 31)

src = Image.open(SRC_DIR / "raccoon.png").convert("RGB")
w, h = src.size
bg = src.getpixel((w // 2, 20))  # 배경 주황 샘플
print("배경색 샘플:", bg)

# 1) 흰 모서리를 배경 주황으로 채움 (플러드필)
light = src.copy()
for xy in [(3, 3), (w - 4, 3), (3, h - 4), (w - 4, h - 4)]:
    ImageDraw.floodfill(light, xy, bg, thresh=90)

# 2) 다크 버전: 주황 배경만 남색으로 (외곽선 안쪽 아트는 연결이 끊겨 안전)
dark = light.copy()
seeds = [(3, 3), (w // 2, 6), (6, h // 2), (w - 6, h // 2), (w // 2, h - 6),
         (w - 4, 3), (3, h - 4), (w - 4, h - 4), (60, 60), (w - 60, 60)]
for xy in seeds:
    if abs(dark.getpixel(xy)[0] - bg[0]) < 40:  # 아직 주황이면
        ImageDraw.floodfill(dark, xy, NAVY, thresh=48)

light.resize((600, 600), Image.LANCZOS).save(OUT / "logo-light.png")
dark.resize((600, 600), Image.LANCZOS).save(OUT / "logo-dark.png")

# 3) 앱 아이콘 (사이트/홈 화면용)
for size in (512, 192, 180):
    light.resize((size, size), Image.LANCZOS).save(ROOT / f"icon-{size}.png")

# 4) 썸네일 1932x828
W, H = 1932, 828
img = Image.new("RGB", (W, H), (16, 20, 24))
d = ImageDraw.Draw(img)
for yy in range(H):
    t = yy / H
    d.line([(0, yy), (W, yy)], fill=(int(16 + 14 * t), int(20 + 16 * t), int(24 + 22 * t)))

# 오른쪽: 너구리 아트를 둥근 카드로
card = light.resize((680, 680), Image.LANCZOS)
mask = Image.new("L", (680, 680), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, 680, 680], radius=90, fill=255)
img.paste(card, (W - 680 - 90, (H - 680) // 2), mask)

font_big = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 150)
font_mid = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 62)
font_small = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 40)
d.text((110, 240), "너구리굴 찾기", font=font_big, fill=(255, 255, 255))
d.text((118, 440), "눈치 보지 않고, 당당하게", font=font_mid, fill=(255, 122, 69))
d.text((120, 545), "내 주변 흡연구역 지도 · 도보 경로 · 흡연구역 제보", font=font_small, fill=(160, 172, 184))
img.save(OUT / "thumbnail.png")

# 다운로드 폴더에도 복사
import shutil
for f in ["logo-light.png", "logo-dark.png", "thumbnail.png"]:
    shutil.copy(OUT / f, SRC_DIR / f)
print("완료: logo-light/dark(600), thumbnail(1932x828), icon-512/192/180 교체")
