from PIL import Image, ImageDraw, ImageFont
import os, sys

FONTS = "/data/data/com.termux/files/home/tmp/sf-daily/assets/fonts"
BOLD = os.path.join(FONTS, "NanumGothic-Bold.ttf")

CAPTIONS = {
  1: [
    '메트로폴리스 — 위에 사는 자들, 아래에서 사는 자들',
    '"저 아이들은… 우리 형제예요" — 처음 보는 눈빛',
    '"저 위에 사는 분들은, 우리가 여기 있다는 걸 몰라요"',
    '"10시간 — 팔을 바늘처럼 벌리고 버티는 시간"',
    '"기계가… 사람을 삼킨다!"',
    '"몰로크…!" — 도시의 아들이, 처음 아래를 본다',
  ],
  2: [
    '"바벨탑 이야기를 들려 드릴게요" — 촛불 아래의 예배',
    '"머리와 손 사이엔, 심장이 필요해요"',
    '"내 기계 인간이오 — 무엇이든 시키는 몸이지"',
    '"…그 얼굴을, 마리아로 주게"',
    '"싫어… 놔주세요!"',
    '빛이 내려오고 — 마리아의 얼굴을 가진 기계가, 눈을 뜬다',
  ],
  3: [
    '"죽음의 기계를, 부숴라!" — 낯선 빛이 도는 눈',
    '"부숴라! 부숴라!" — 함성이 천장을 때린다',
    '',
    '"아이들이 있어요 — 물이 오기 전에!"',
    '"저건… 마리아가 아니야!" — 불길 속의 은빛 골격',
    '"머리와 손을 잇는 것은 — 심장" — 저녁 종이 운다',
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
