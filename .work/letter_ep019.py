from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep019-notext.png'
dst = root / 'episodes/sf-daily-019-the-man-from-the-atom.png'
im = Image.open(src).convert('RGBA')
W, H = im.size
sx, sy = W / 1024, H / 1536
scale = min(sx, sy)
px = lambda n: max(1, round(n * scale))
bold = ImageFont.truetype(str(root / 'assets/fonts/NanumGothic-Bold.ttf'), px(22))
regular = ImageFont.truetype(str(root / 'assets/fonts/NanumGothic-Regular.ttf'), px(20))
speaker_font = ImageFont.truetype(str(root / 'assets/fonts/NanumGothic-Bold.ttf'), px(20))
overlay = Image.new('RGBA', im.size)
d = ImageDraw.Draw(overlay)

margin_x, margin_y = round(8 * sx), round(8 * sy)
gutter_x, gutter_y = round(8 * sx), round(8 * sy)
panel_w = (W - 2 * margin_x - gutter_x) / 2
panel_h = (H - 2 * margin_y - 3 * gutter_y) / 4

def panel(i):
    row, col = divmod(i, 2)
    x = margin_x + col * (panel_w + gutter_x)
    y = margin_y + row * (panel_h + gutter_y)
    return round(x), round(y), round(x + panel_w), round(y + panel_h)

def wrap_chars(s, font, max_width, first_width=None):
    lines, line = [], ''
    width = first_width if first_width is not None else max_width
    for ch in s:
        if d.textlength(line + ch, font=font) > width and line:
            lines.append(line.rstrip())
            line = ch.lstrip()
            width = max_width
        else:
            line += ch
    if line:
        lines.append(line.rstrip())
    return lines

def narration(i, caption):
    x0, y0, x1, _ = panel(i)
    left, right = x0 + px(12), x1 - px(12)
    inset = px(12)
    lines = wrap_chars(caption, bold, right - left - 2 * inset - px(6))
    leading = px(31)
    top = y0 + px(10)
    height = px(21) + leading * len(lines)
    d.rounded_rectangle((left, top, right, top + height), radius=px(10), fill=(13, 20, 32, 205))
    d.rounded_rectangle((left, top, left + px(6), top + height), radius=px(3), fill=(245, 158, 11, 255))
    for n, line in enumerate(lines):
        d.text((left + inset + px(6), top + px(9) + n * leading), line, font=bold, fill=(255, 255, 255, 255))

def dialogue(i, name, speech):
    x0, _, x1, y1 = panel(i)
    left, right = x0 + px(12), x1 - px(12)
    inset = px(12)
    name_width = d.textlength(name, font=speaker_font) + px(8)
    available = right - left - 2 * inset
    lines = wrap_chars(speech, regular, available, available - name_width)
    leading = px(29)
    height = px(20) + leading * len(lines)
    bottom = y1 - px(10)
    top = bottom - height
    d.rounded_rectangle((left, top, right, bottom), radius=px(10), fill=(255, 255, 255, 238), outline=(31, 41, 55, 255), width=px(2))
    text_y = top + px(8)
    d.text((left + inset, text_y), name, font=speaker_font, fill=(245, 158, 11, 255))
    for n, line in enumerate(lines):
        line_x = left + inset + (name_width if n == 0 else 0)
        d.text((line_x, text_y + n * leading), line, font=regular, fill=(31, 41, 55, 255))

narration(0, "1923년 여름 — 마틴 교수의 실험실에 '크기는 상대적'이라는 은빛 상자가 완성되었다.")
dialogue(0, '마틴 교수:', '첫 인간 피험자는 너뿐이다, 커비.')
narration(1, '교수는 잠시 뒤 되돌려 주겠다고 약속했다. 나는 상자 위에 앉아 레버를 잡았다.')
dialogue(1, '커비:', '시작합니다, 교수님!')
narration(2, '첫 순간, 나는 지붕을 뚫고 솟았다 — 세상은 시계를 멈춘 것처럼 얼어 있었다.')
dialogue(2, '커비:', '세상이… 멈춰 있다!')
narration(3, '지구는 구슬이 되어 발밑에서 멀어지고, 태양은 불씨가 되었다.')
narration(4, '별의 바다를 지나도, 이 몸은 멈추지 않았다.')
dialogue(4, '커비:', '교수님… 돌려주실 수 있죠? …교수님?')
# P6 is intentionally silent.
narration(6, '우리 우주 전체가 빛 알갱이 하나가 되어 있었다 — 그 안에 지구가, 그리고 아직 손을 내밀고 있는 교수님이.')
narration(7, '나는 오늘도 자란다 — 더 큰 세계의 눈에는, 나는 원자에서 온 남자다.')

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)
