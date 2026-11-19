from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep022-notext.png'
dst = root / 'episodes/sf-daily-022-from-the-earth-to-the-moon.png'
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

narration(0, "남북전쟁이 끝난 1865년, 볼티모어 '총포 클럽' — 나무 다리와 갈고리 팔이 트로피처럼 걸린 클럽에, 이제 쏠 전쟁이 없었다.")
narration(1, '10월의 어느 저녁, 임페이 바비컨 회장이 단상에 올랐다.')
dialogue(1, '바비컨:', '달로 포탄을 쏘겠다!')
narration(2, "플로리다의 모래언덕 — 천여 개의 용광로가 쇳물을 쏟아부어, 길이 274미터의 대포 '컬럼비아드'가 태어났다.")
narration(3, '프랑스인 미셸 아르당이 대서양을 건너왔다 — 세계의 신문들이 끓어올랐다.')
dialogue(3, '아르당:', '포탄 안에 사람을 태워 주시오 — 바로 나를!')
narration(4, '12월 1일 밤 10시 46분 40초 — 산을 뒤흔든 화염과 함께, 포탄은 별들 속으로 사라졌다.')
# P6 is intentionally silent.
narration(6, '창밖에서 달이 차오르고, 지구는 작은 푸른 등불로 멀어져 갔다.')
dialogue(6, '아르당:', '저 은빛 바다가 우리의 목적지오.')
narration(7, '포탄은 달에 닿지 않았다 — 달의 인력에 붙잡힌 새 위성이 되어, 세 사람과 개 다이애나를 태운 채 아직도 그 하늘을 돌고 있을지 모른다.')

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)
