from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep020-notext.png'
dst = root / 'episodes/sf-daily-020-the-war-of-the-worlds.png'
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

narration(0, '1898년 6월 — 서리주 호셀 들판에 불꽃을 그리며 거대한 실린더가 떨어졌다.')
dialogue(0, '나레이터:', '잠들어 있는 별똥이겠지.')
narration(1, '밤이 깊자 뚜껑이 돌아가며 떨어져 나갔다 — 축축하게 빛나는 회색 촉수가, 더듬더듬 밖을 향했다.')
dialogue(1, '구경꾼:', '저것은… 살아 있다!')
narration(2, "소리도 없이 '열선'이 들판을 쓸었다 — 나는 모자를 잃은 채 도랑물에 뛰어들었다.")
narration(3, '다음 날, 세 개의 전투 기계가 강을 건너 런던을 향해 걷기 시작했다.')
narration(4, '웨이브리지 — 마침내 포탄 하나가 놈의 후드를 꿰뚫았다. 첫 거인이 무너져 내렸다.')
dialogue(4, '포병:', '쓰러뜨렸다!')
# P6 is intentionally silent.
narration(6, '나는 빈집 다락방 창가에서 마지막을 기다렸다 — 유리에 비친 다리는, 아직도 걷고 있었다.')
narration(7, '놈들을 쓰러뜨린 것은 대포가 아니었다 — 이 별의 가장 작은 것들, 세균이었다.')

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)
