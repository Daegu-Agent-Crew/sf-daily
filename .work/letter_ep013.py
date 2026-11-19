from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep013-notext.png'
dst = root / 'episodes/sf-daily-013-the-country-of-the-blind.png'
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

narration(0, '1904년, 페루 안데스의 밤 — 얼음 다리가 무너지며 등반 가이드 누녜스가 어둠 속으로 떨어졌다.')
narration(1, '깨어난 곳은, 낭떠러지로 세상에서 잘려 나간 초록 계곡이었다.')
dialogue(1, '누녜스:', '저기 마을이… 사람이 산다!')
narration(2, '마을 사람들의 눈은, 모두 감겨 있었다.')
dialogue(2, '누녜스:', '눈먼 자들의 나라에서는 외눈박이가 왕이다!')
narration(3, "그러나 그들에게 '보다'라는 말은 존재하지 않았다.")
dialogue(3, '노인:', '그 눈 혹이 병이지. 도려내면 제정신이 될 게야.')
narration(4, '그는 눈먼 처녀 메디나사로테를 사랑하게 되었다.')
dialogue(4, '누녜스:', '당신이… 제일 아름다워요.')
narration(5, '혼인 허락의 조건 — 그의 눈을 도려내는 것.')
dialogue(5, '의사:', '눈 혹을 도려내면, 그도 우리처럼 행복해질 것이오.')
narration(6, '수술 전날 밤.')
dialogue(6, '메디나사로테:', '당신이 어둠을 받아들이면, 내 손이 평생 당신의 눈이 되어 드릴게요.')
narration(7, '새벽 — 그는 눈을 지키기 위해 사랑을 두고 고개를 오르기 시작했다. 세상은, 여전히 눈부셨다.')

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)
