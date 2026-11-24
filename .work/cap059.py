from PIL import Image, ImageDraw, ImageFont
import os, sys

FONTS = "/data/data/com.termux/files/home/tmp/sf-daily/assets/fonts"
BOLD = os.path.join(FONTS, "NanumGothic-Bold.ttf")

CAPTIONS = {
  1: [
    "\"받아쓰기 외에는 아무것도 묻지 마시오\" — 취직 첫날의 인사",
    "\"제3장, 장기 부활의 조건은…\" — 목소리는 커튼 뒤에서",
    "커튼을 걷자 — 영양액 속에, 살아 있는 머리가 있었다",
    "\"놀라지 마세요, 로랑 양 — 나는 도웰 교수요\"",
    "그날 밤부터, 돔 곁의 의자가 하나 늘었다",
    "\"케른 박사의 대발견!\" — 초상 밑의 진짜 저자는, 침묵",
  ],
  2: [
    "\"죽기 전의 마지막 부탁일세…\" — 그 조수의 이름은 케른",
    "눈을 떴을 때 세계는 — 유리 한 장이었다",
    "옆 조에는 늙은 개가 산다 — 짖지 못한 채, 오래",
    "\"말을 듣지 않으면, 영양 공급을 멈출 뿐이오\"",
    "\"교수님, 오늘은 제 이야기를 들려주세요\"",
    "\"내 원고가 있소 — 서랍 세 번째, 내 이름으로\"",
  ],
  3: [
    "서랍 세 번째의 낡은 노트 — 도표마다 도웰의 습관이 남아",
    "\"이 논문의 진짜 저자를, 여러분께 보이겠습니다\"",
    "객석이 일어서고 — 훈장의 빛이 처음으로 흔들린다",
    "\"수고했소, 마리 — 이제 나는, 좀 쉬어야겠소\"",
    "다음 날 아침 유리 돔에는 — 오래 걷고 온 사람의 잠",
    "정원의 빈 의자 — 바람이, 그의 자리를 지나간다",
  ],
}

def wrap(d, text, font, max_w):
    lines, cur = [], ""
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