# -*- coding: utf-8 -*-
"""앱인토스 노출 정보용 에셋 생성: 앱 로고(라이트/다크) 600x600, 썸네일 1932x828"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "toss-assets"
OUT.mkdir(exist_ok=True)

ACCENT = (255, 122, 69)
NAVY = (23, 26, 31)
WHITE = (255, 255, 255)
CREAM = (245, 193, 108)
EMBER = (224, 79, 47)

def draw_mark(d, cx, cy, R, ring_color, on_dark):
    """원형 배지 + 담배 + 연기 모티프 (기존 앱 아이콘과 동일 계열)"""
    d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=ACCENT)
    ch = R * 0.28  # 담배 두께
    y = cy + R * 0.10
    x0, x1 = cx - R * 0.62, cx + R * 0.55
    d.rounded_rectangle([x0, y-ch/2, x1, y+ch/2], radius=ch/2, fill=WHITE)
    d.rounded_rectangle([x1-R*0.22, y-ch/2, x1, y+ch/2], radius=ch/3, fill=CREAM)
    d.ellipse([x0-ch*0.1, y-ch/2, x0+ch*0.9, y+ch/2], fill=EMBER)
    for dx, dy, r in [(-0.42, -0.42, 0.085), (-0.28, -0.60, 0.105), (-0.10, -0.76, 0.125)]:
        d.ellipse([cx+R*dx-R*r, cy+R*dy-R*r, cx+R*dx+R*r, cy+R*dy+R*r], fill=WHITE)

def logo(path, bg):
    img = Image.new("RGB", (600, 600), bg)
    d = ImageDraw.Draw(img)
    draw_mark(d, 300, 310, 195, None, bg == NAVY)
    img.save(path)

logo(OUT / "logo-light.png", WHITE)   # 기본 로고 (밝은 배경)
logo(OUT / "logo-dark.png", NAVY)     # 다크모드 로고

# ── 썸네일 1932 x 828 ──
W, H = 1932, 828
img = Image.new("RGB", (W, H), (16, 20, 24))
d = ImageDraw.Draw(img)
# 배경 그라데이션 (세로)
for yy in range(H):
    t = yy / H
    d.line([(0, yy), (W, yy)], fill=(int(16+14*t), int(20+16*t), int(24+22*t)))
# 오른쪽 장식: 큰 마크 + 흐린 원
d.ellipse([W-780, -180, W+140, 740], fill=(26, 32, 39))
draw_mark(d, W-330, H//2, 250, None, True)
# 지도 핀 장식
def pin(x, y, s, color):
    d.ellipse([x-s, y-s, x+s, y+s], fill=color)
    d.polygon([(x-s*0.75, y+s*0.6), (x+s*0.75, y+s*0.6), (x, y+s*2.0)], fill=color)
    d.ellipse([x-s*0.4, y-s*0.4, x+s*0.4, y+s*0.4], fill=(16, 20, 24))
pin(W-700, 190, 34, (56, 189, 248))
pin(W-620, 620, 26, (167, 139, 250))

font_big = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 150)
font_mid = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 62)
font_small = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 40)

d.text((110, 240), "너구리굴 찾기", font=font_big, fill=WHITE)
d.text((118, 440), "눈치 보지 않고, 당당하게", font=font_mid, fill=ACCENT)
d.text((120, 545), "내 주변 흡연구역 지도 · 도보 경로 · 흡연구역 제보", font=font_small, fill=(160, 172, 184))
img.save(OUT / "thumbnail.png")

print("생성 완료:", [p.name for p in OUT.iterdir()])
