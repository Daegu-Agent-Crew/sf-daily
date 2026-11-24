from PIL import Image, ImageDraw, ImageFont
import os, sys

FONTS = "/data/data/com.termux/files/home/tmp/sf-daily/assets/fonts"
BOLD = os.path.join(FONTS, "NanumGothic-Bold.ttf")

CAPTIONS = {
  1: [
    '인류의 역사는, 힘을 얻어 온 역사 — 불에서, 증기에서, 전기까지',
    '"왜 안 되지… 방사성은, 이끌어 낼 수 있을 텐데"',
    '"터뜨린다… 원자의 불씨를, 이 손으로"',
    '"석탄 시대는 끝났습니다 — 이제 엔진은 원자의 빛으로 돌아갑니다"',
    '"힘은 손에 넣었는데 말일세 — 우리는 아직, 동굴을 나온 지 얼마 안 된 원시인이야"',
    '그리고 그 힘은 — 진열장 벨벳 위에 놓인다. 반감기, 열이레',
  ],
  2: [
    '"1956년, 새벽 — 오늘의 목표는, 도시 하나입니다"',
    '"봉인은 이빨이다 — 깨무는 순간, 시작된다"',
    '지금까지의 폭발은 찰나였다 — 이 불은, 남아서 계속 탄다',
    '"물을 부어도 흙을 덮어도 꺼지지 않아요 — 땅에 박히면, 열이레를 타는 거예요"',
    '"짐은 이 왕관을 — 세계 앞에, 내려놓노라"',
    '마지막 폭탄 하나가 — 회의의 하늘에',
  ],
  3: [
    '그 마지막 폭탄이 남긴 것 — 국경의, 완전한 소멸',
    '"이제 지구는 한 문제입니다 — 조각조각 나눠 다룰 수, 없으니"',
    '"우리 세대는 문을 열었을 뿐 — 그 안을 걷는 건, 자네들이야"',
    '"인간의 소명은 사랑만이 아니다 — 앎과 힘, 그리고 앎에도 힘에도 절대의 한계는 없다"',
    '아침빛이 열린 창으로 스며들고 — 노현자는 마지막 모험으로, 조용히 문을 넘는다',
    '그리고 세계는 — 자유로워졌다',
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