from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep015-notext.png'
dst = root / 'episodes/sf-daily-015-the-poison-belt.png'
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

narration(0, '1913년 여름, 하늘이 이상한 구릿빛으로 물들기 시작했다.')
dialogue(0, '챌린저:', "지구가 에테르의 '독 벨트' 속으로 들어가고 있소.")
narration(1, '챌린저 교수의 전보 한 장 — 기자 말론은 저택으로 달려갔다.')
dialogue(1, '말론:', '온 세상이 잠든다고요, 교수님?')
narration(2, '창문을 틀어막고, 산소통을 곁에 두었다.')
dialogue(2, '챌린저:', '이 방이 지상의 마지막 의식이다.')
narration(3, '정원사는 장미 옆에서 잠들어 있었다.')
dialogue(3, '말론:', '숨은 쉬고 있어요 — 죽은 게 아니라, 잠들었을 뿐입니다.')
narration(5, '산소가 얇어지고, 네 사람은 졸음과 싸웠다.')
dialogue(5, '챌린저:', '관측 기록 — 독 벨트 통과 중. 최후의 문장이 될지도 모른다.')
narration(6, '푸른 안개가 걷히고, 첫 참새가 울었다.')
dialogue(6, '록스턴:', '살았어! 하늘이 돌아왔네!')
narration(7, '세상은 하품하며 깨어났다 — 아무도 기억하지 못한 채, 지구는 아직도 자기 길을 걷고 있다.')

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)
