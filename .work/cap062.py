from PIL import Image, ImageDraw, ImageFont
import os, sys

FONTS = "/data/data/com.termux/files/home/tmp/sf-daily/assets/fonts"
BOLD = os.path.join(FONTS, "NanumGothic-Bold.ttf")

CAPTIONS = {
  1: [
    '"믿을 만한 별이 하나만 더 있으면, 바다에서 길 잃는 배가 없을 텐데"',
    '"그럼 우리가 달을 하나 만들자" — "…벽돌로?"',
    '20년 뒤, 메인의 겨울 골짜기 — 벽돌 달이 산 위에 우뚝 선다',
    '"이 안이 제일 따뜻하네요" — 가족들의 작은 세상',
    '철 테 두른 물레바퀴가 돈다 — 저 바퀴가 달을, 하늘로 튕긴다',
    '"멈추지 마십시오 — 댐 아래가 막히고 있습니다"',
  ],
  2: [
    '숨소리 하나 없는 마을 — 달이 있던 자리엔, 텅 빈 틀만',
    '"바퀴가 풀렸다!" — 눈보라를 갈라, 벽돌 달이 하늘로',
    '"그 안에… 서른일곱 명이?"',
    '가장자리에 사람들이 줄을 서! 긴 뜀, 짧은 뜀 — 모스 부호야!',
    '눈밭에 하얀 천을 펼치자, 달이 답을 뛰기 시작했다',
    '그 작은 별 안에는 — 지금도, 하나의 세상',
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
