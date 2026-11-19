from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep018-notext.png'
dst = root / 'episodes/sf-daily-018-princess-of-mars.png'
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

narration(0, '1866년 애리조나 — 아파치의 추격을 피해 숨은 동굴에서, 무언가가 그를 기다리고 있었다.')
dialogue(0, '존 카터:', '여기서 한몫 벌고 죽어주지.')
narration(1, '갑자기 몸이 굳었다. 동굴 틈새로 붉은 별 화성이 이상한 빛을 내려보냈다.')
dialogue(1, '존 카터:', '몸이… 움직이지 않아. 저 별이… 나를 부르고 있어.')
narration(2, "눈을 뜨자 붉은 사막, 산호빛 하늘 — 화성 '바르숨'. 첫 한 걸음에 아홉 미터를 뛰었다.")
dialogue(2, '존 카터:', '내 몸이… 깃털처럼 가볍다!')
narration(3, "네 개의 팔을 가진 초록 거인 '타르크'가 나를 포위했다.")
dialogue(3, '타스 타르카스:', '뼈가 약한 지구인이군. 우리 도시로 가라.')
narration(4, '그곳에서 나는 만났다 — 헬륨의 공주 데자 소리스.')
dialogue(4, '존 카터:', '이 여인은 내가 지킨다.')
# P6 is intentionally silent.
narration(6, '밤의 아레나, 흰 유인원들 앞에서 — 나는 하늘을 나는 검이 되었다.')
dialogue(6, '존 카터:', '지구에선 늙은 병사 — 여기선 하늘을 나는 검이다!')
narration(7, '눈을 떠 보니 애리조나의 동굴 — 몸은 그대로 그 자리에서, 오늘 밤도 저 붉은 별을 바라본다.')

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)
