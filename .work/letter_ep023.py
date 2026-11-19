from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep023-notext.png'
dst = root / 'episodes/sf-daily-023-the-sandman.png'
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

narration(0, "1816년 — 잠들지 못하는 아이에게 '모래 사나이'는 찾아와 눈을 가져간다고 했다.")
dialogue(0, '나타나엘:', '…눈을… 가져간대…')
narration(1, '어른이 되어도 공포는 남았다. 어느 날, 렌즈 장수 코폴라가 문 앞에 나타났다.')
dialogue(1, '코폴라:', '예쁜 눈이야 — 좋은 눈!')
narration(2, '황동 스파이글라스 너머, 발코니의 처녀 올림피아가 황금빛으로 빛났다.')
narration(3, '파티에서 그녀는 노래하고 춤추었다 — 하는 말은 언제나 단 하나뿐이었지만.')
dialogue(3, '올림피아:', '아— 아— 아—')
narration(4, '사람들의 수군거림은 들리지 않았다. 나타나엘은 청혼했다.')
dialogue(4, '나타나엘:', '당신만이 저를 이해해요.')
# P6 is intentionally silent.
narration(5, '약혼 파티 — 그림자 같은 노인이 그녀를 찢었다. 쏟아진 것은 눈물이 아니라 톱니바퀴였다.')
narration(6, '미쳐버린 그의 손에 스파이글라스가 다시 들렸다. 앞에는 약혼자 클라라.')
dialogue(6, '클라라:', '그 렌즈, 이제 그만…!')
narration(7, '올림피아가 누구의 인형이었는지는 끝내 밝혀지지 않았다.')
dialogue(7, '나타나엘:', '빙글빙글 돌아라, 나무인형들아!')

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)