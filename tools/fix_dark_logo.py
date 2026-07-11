# -*- coding: utf-8 -*-
"""다크 로고 재생성 v2:
1) 엄격한 BFS로 순수 배경(주황/흰색)만 남색 변환 — 아트 내부 보존
2) 남색 경계에서 제한적 팽창으로 테두리 잔여물(흰↔주황 혼합 픽셀)만 정리"""
from PIL import Image
from collections import deque
from pathlib import Path
import shutil

SRC_DIR = Path(r"C:/Users/BRAIN/Downloads/너구리굴-앱인토스-에셋")
OUT = Path(__file__).resolve().parent.parent / "toss-assets"
NAVY = (23, 26, 31)

src = Image.open(SRC_DIR / "raccoon.png").convert("RGB")
w, h = src.size
px = src.load()
bg = px[w // 2, 20]
WHITE = (255, 255, 255)

def near(c, ref, t):
    return (c[0]-ref[0])**2 + (c[1]-ref[1])**2 + (c[2]-ref[2])**2 <= t*t

# 1단계: 엄격 BFS (순수 배경색만)
strict = lambda c: near(c, bg, 60) or near(c, WHITE, 60)
visited = bytearray(w * h)
q = deque()
for x in range(w):
    for y in (0, h - 1):
        if strict(px[x, y]) and not visited[y*w+x]:
            visited[y*w+x] = 1; q.append((x, y))
for y in range(h):
    for x in (0, w - 1):
        if strict(px[x, y]) and not visited[y*w+x]:
            visited[y*w+x] = 1; q.append((x, y))
while q:
    x, y = q.popleft()
    for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0 <= nx < w and 0 <= ny < h and not visited[ny*w+nx] and strict(px[nx, ny]):
            visited[ny*w+nx] = 1; q.append((nx, ny))

# 2단계: 남색 영역 경계에서 최대 8px 팽창 — 흰↔주황 혼합처럼 '밝고 따뜻한' 픽셀만 흡수
# (아트 외곽선은 어두워서 여기서 걸러짐 → 내부 침투 불가)
def blendish(c):
    return c[0] >= 225 and c[1] >= 95 and c[2] >= 45 and near(c, bg, 200)

frontier = deque()
for y in range(h):
    for x in range(w):
        if visited[y*w+x]:
            frontier.append((x, y, 0))
extra = 0
while frontier:
    x, y, d = frontier.popleft()
    if d >= 8:
        continue
    for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0 <= nx < w and 0 <= ny < h and not visited[ny*w+nx] and blendish(px[nx, ny]):
            visited[ny*w+nx] = 1
            extra += 1
            frontier.append((nx, ny, d + 1))

dark = src.copy()
dpx = dark.load()
cnt = 0
for y in range(h):
    for x in range(w):
        if visited[y*w+x]:
            dpx[x, y] = NAVY; cnt += 1

# 3단계: 가장자리 마감 — 아트가 닿지 않는 외곽 밴드(50px)와 코너 사각(180px)은 무조건 남색
# (원본 둥근 사각형 모서리 곡선의 어두운 경계 픽셀 제거)
for y in range(h):
    for x in range(w):
        edge_band = x < 50 or x >= w - 50 or y < 50 or y >= h - 50
        corner_sq = min(x, w - 1 - x) < 180 and min(y, h - 1 - y) < 180
        if (edge_band or corner_sq) and dpx[x, y] != NAVY:
            dpx[x, y] = NAVY

print(f"배경 {cnt}px 변환 (팽창 정리 {extra}px 포함, 전체의 {cnt*100//(w*h)}%)")
dark.resize((600, 600), Image.LANCZOS).save(OUT / "logo-dark.png")
shutil.copy(OUT / "logo-dark.png", SRC_DIR / "logo-dark.png")
print("완료")
