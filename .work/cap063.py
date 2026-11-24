from PIL import Image, ImageDraw, ImageFont
import os, sys

FONTS = "/data/data/com.termux/files/home/tmp/sf-daily/assets/fonts"
BOLD = os.path.join(FONTS, "NanumGothic-Bold.ttf")

CAPTIONS = {
  1: [
    '"이번 혜성, 꼬리가 정오에 스친다더군" — 온 도시가 그 얘기뿐이었다',
    '"짐, 오늘 맨 아래 금고에 좀 내려가 주게" — 위험한 자리엔 제일 값싼 사람이 내려간다',
    '"쿵" — 돌문이 닫혔다',
    '',
    '"어제는, 이 문이 나를 들여보내지 않았는데" — 혼자 차린 첫 점심',
    '"사람 살려 주세요…!" — 죽은 도시에, 산 목소리가 울린다',
  ],
  2: [
    '"무슨 일이…? 밖이, 너무 조용해요" — "혜성이 스쳤고… 많은 사람이, 잠들었소"',
    '"할렘에, 들러야 할 곳이 있소" — 그가 꺼내 든 것은, 하얀 아기 천 모자 하나',
    '',
    '"세계는… 죽은 건가요" — "그래도, 우리 둘은 —"',
    '"빵—! 빵—!" "내 딸아!" — 도시의 불이, 하나둘 깨어났다',
    '"짐!" — "…여보" — 소리 없던 도시에, 다시 저녁이 온다',
  ],
}

def wrap(d, text, font, max_w):
    lines, cur = [], ''
    for ch in text:
        if d.textlength(cur + ch, font=font) > max_w and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    lines.append(cur)
    return lines

def make(src, dst, page):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    d = ImageDraw.Draw(im)
    for i, caption in enumerate(CAPTIONS[page]):
        if not caption:
            continue
        col, row = i % 2, i // 2
        x0, y0 = col * w // 2, row * h // 3
        x1 = (col + 1) * w // 2
        pad = int(w * 0.020)
        lines = wrap(d, caption, ImageFont.truetype(BOLD, 30), (x1 - x0) - 2 * pad - 8)
        size = 30
        while (len(lines) > 2 or max(d.textlength(l, font=ImageFont.truetype(BOLD, size)) for l in lines) > (x1 - x0) - 2 * pad - 8) and size > 20:
            size -= 1
            lines = wrap(d, caption, ImageFont.truetype(BOLD, size), (x1 - x0) - 2 * pad - 8)
        font = ImageFont.truetype(BOLD, size)
        lh = int(size * 1.3)
        box_h = lh * len(lines) + int(pad * 0.9)
        d.rounded_rectangle((x0 + pad // 2, y0 + pad // 2, x1 - pad // 2, y0 + pad // 2 + box_h), radius=10, fill=(255, 252, 241), outline=(56, 75, 78), width=2)
        ty = y0 + pad // 2 + (box_h - lh * len(lines)) / 2
        for ln in lines:
            tw = d.textlength(ln, font=font)
            d.text((x0 + (x1 - x0 - tw) / 2, ty), ln, font=font, fill=(35, 49, 51))
            ty += lh
    im.save(dst, optimize=True)
    print(dst, im.size)

if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2], int(sys.argv[3]))
