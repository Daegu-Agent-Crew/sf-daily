from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep012-notext.png'
dst = root / 'episodes/sf-daily-012-twenty-thousand-leagues.png'
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

narration(0, '대서양 한복판, 항해 열째 달 — 노틸러스호가 갑자기 멈춰 섰다.')
dialogue(0, '아로낙스:', '나선이 무언가에 얽혔군!')
narration(1, '살롱 유리 너머, 거대한 눈들이 우리를 지켜보고 있었다.')
dialogue(1, '콘셜:', '문어입니다, 선생님!')
narration(2, '네모 선장이 갑판 위에 섰다.')
dialogue(2, '네모:', '껍데기 없는 놈들 — 이길 길은 도끼뿐이오.')
narration(3, '갑판 위로 촉수가 쏟아졌다. 검은 잉크가 비처럼 뿌려졌다.')
# P5 is completely silent.
narration(5, '네드의 작살이 괴물의 눈을 꿰뚫었다 — 그 순간, 두 번째 촉수가 그를 덮쳤다.')
dialogue(5, '네드:', '이 자식!')
narration(6, '네모 선장의 도끼가 괴물을 갈랐다.')
dialogue(6, '네모:', '그 사내는 프랑스인이었소… 죽는 날까지 잊지 않겠소.')
narration(7, '그날 밤 — 강철 같은 사내가 가족 초상 앞에서 소리 없이 울고 있었다.')

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)
