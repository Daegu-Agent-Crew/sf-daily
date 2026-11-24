# -*- coding: utf-8 -*-
# ep066 「붉은 것」 후조판 — 대사=둥근 풍선+꼬리, 내레이션=칸 상단 테두리 부착 반투명 사각 박스
from PIL import Image, ImageDraw, ImageFont
import os, sys

FONTS = "/data/data/com.termux/files/home/tmp/sf-daily/assets/fonts"
BOLD = os.path.join(FONTS, "NanumGothic-Bold.ttf")

# (kind, text) — kind: 'n'=내레이션, 'd'=대사, ''=무음 칸
CAPS = {
  1: [
    ('n', '정오의 밀림에, 또 그 소리가 온다 — 천사의 나팔처럼'),
    ('d', '"저 소린 악마예요, 주인님! 무리로 가다간 머리를 잃어요"'),
    ('n', '그 뒤로는, 열병과 세월뿐'),
    ('d', '"별에서 태어난 것이지… 늙은이들은, 그렇게 불렀다"'),
    ('d', '"먼 나라 백인의 머리다 — 솜씨는, 형편없지만"'),
    ('', ''),
  ],
  2: [
    ('n', '웅덩이 끝에는, 완벽한 붉은 구가 있었다'),
    ('d', '"옻칠이 아니야… 이건, 살아 있는 금속이다"'),
    ('n', '별에서 태어난 것 — 원주민의 말이 과학자를, 앞서 있었다'),
    ('d', '"이 통나무가 그것을 치면, 노래가 온다"'),
    ('d', '"죽거든 내 머리는 네 것 — 그러니 그 노래를, 마지막에"'),
    ('', ''),
  ],
  3: [
    ('n', '마지막 가는 길은 들것 위 — 곁에는, 다 쓴 엽총'),
    ('d', '"지금이다 — 고개를, 숙이게"'),
    ('n', '색이 소리가 되고, 소리가 그를 감싼다'),
    ('d', '"늙은이를 속이지 않지 — 이 머리는, 네 것이다"'),
    ('', ''),
    ('n', '빵나무 그늘의, 느긋한 연기와 붉은 노래'),
  ],
}

INK = (35, 49, 51, 255)
LINE = (56, 75, 78, 255)
PAPER = (255, 252, 241, 255)
PAPER_N = (255, 252, 241, 208)

def wrap(d, text, font, max_w):
    lines, cur = [], ''
    for ch in text:
        if d.textlength(cur + ch, font=font) > max_w and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    lines.append(cur)
    return lines

def fit(d, text, max_w):
    size = 30
    while size > 20:
        font = ImageFont.truetype(BOLD, size)
        lines = wrap(d, text, font, max_w)
        if len(lines) <= 2 and max(d.textlength(l, font=font) for l in lines) <= max_w:
            return font, size, lines
        size -= 1
    font = ImageFont.truetype(BOLD, 20)
    return font, 20, wrap(d, text, font, max_w)

def make(src, dst, page):
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    d = ImageDraw.Draw(im)
    for i, (kind, caption) in enumerate(CAPS[page]):
        if not caption:
            continue
        col, row = i % 2, i // 2
        x0, y0 = col * w // 2, row * h // 3
        x1 = (col + 1) * w // 2
        pad = int(w * 0.022)
        max_w = (x1 - x0) - 2 * pad - 8
        font, size, lines = fit(d, caption, max_w)
        lh = int(size * 1.3)
        box_h = lh * len(lines) + int(size * 0.7)
        bw = x1 - x0 - 2 * pad
        if kind == 'n':
            # 내레이션: 칸 상단 테두리에 붙은 반투명 사각 박스
            bx0, by0, bx1, by1 = x0 + 5, y0 + 4, x0 + 5 + bw, y0 + 4 + box_h
            d.rectangle((bx0, by0, bx1, by1), fill=PAPER_N, outline=LINE, width=2)
        else:
            # 대사: 둥근 풍선 + 화자 방향 꼬리(아래쪽, 읽기 순서에 따라 좌/우 교차)
            bx0, by0 = x0 + pad, y0 + 16
            bx1, by1 = bx0 + bw, by0 + box_h
            d.rounded_rectangle((bx0, by0, bx1, by1), radius=16, fill=PAPER, outline=LINE, width=2)
            cx = (bx0 + bx1) // 2 + (12 if col == 0 else -12)
            d.polygon([(cx - 10, by1 - 1), (cx + 10, by1 - 1), (cx, by1 + 16)], fill=PAPER)
            d.line([(cx - 10, by1 - 1), (cx, by1 + 16)], fill=LINE, width=2)
            d.line([(cx + 10, by1 - 1), (cx, by1 + 16)], fill=LINE, width=2)
        tx = bx0 + 8
        tw_total = max(d.textlength(l, font=font) for l in lines)
        tx = bx0 + (bx1 - bx0 - tw_total) / 2
        ty = by0 + (by1 - by0 - lh * len(lines)) / 2
        for ln in lines:
            d.text((tx, ty), ln, font=font, fill=INK)
            ty += lh
    im.convert("RGB").save(dst, optimize=True)
    print(dst, im.size)

if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2], int(sys.argv[3]))
