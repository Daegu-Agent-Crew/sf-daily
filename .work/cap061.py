from PIL import Image, ImageDraw, ImageFont
import os, sys

FONTS = "/data/data/com.termux/files/home/tmp/sf-daily/assets/fonts"
BOLD = os.path.join(FONTS, "NanumGothic-Bold.ttf")

CAPTIONS = {
  1: [
    "\"저거 봐요! 별이… 별이 떨어져요!\"",
    "\"가장 딱딱한 강철도 통하지 않는다니 — 대학에 보내 검사하겠네\"",
    "\"돌은 사라졌는데, 밭엔 색만 남았어요 — 교수님\"",
    "\"부풀은 건 큰데… 속은 재뿌이야, 이게 도대체 뭘까?\"",
    "번개가 칠 때마다, 밭과 과수원이 저 혼자 일렁인다 — 낯선 빛깔로",
    "우물 뚜껑 틈새로 — 그 색이, 조용히 숨을 쉰다",
  ],
  2: [
    "\"소도 말도 풀을 뱉고, 우물만 바라보네\"",
    "\"머윈, 아래로 내려가 볼게요 — 지나스는 줄 놓지 마요\"",
    "\"거기 아래엔… 뭔가 있어…!\"",
    "텅 빈 부엌, 차가운 창 — 밭도 집도 재빛으로 변해 간다",
    "\"저 색이 우리를… 마셔 버린 거야…\"",
    "새벽 안개의 계곡 — 색은 마침내 별들의 하늘로 돌아간다",
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