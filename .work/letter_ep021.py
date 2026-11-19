from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
src = root / '.work/ep021-notext.png'
dst = root / 'episodes/sf-daily-021-the-crystal-egg.png'
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

narration(0, '1896년 여름, 런던 세븐 다이얼스 뒷골목 — 박물학자 겸 골동품상 케이브의 잡다한 가게 진열장에, 유난히 반짝이는 수정 알 하나가 있었다.')
dialogue(0, '케이브:', '그건... 5파운드입니다.')
narration(1, '아내가 응접실 문을 박차고 나왔다 — 케이브는 값을 계속 올리며, 필사적으로 판매를 막았다.')
dialogue(1, '케이브 부인:', '5파운드면 충분한 값이에요!')
narration(2, '8월의 어느 새벽 3시 — 셔터 틈 빛 한 줄기가 알을 때리자, 속에서 빛이 꿈틀거렸다. 어둠에 옮겨 놓아도, 알은 5분을 스스로 빛났다.')
dialogue(2, '케이브:', '이건... 광학이 아니야.')
narration(3, "낮에는 검은 벨벳을 머리에 뒤집어쓰고 카운터 아래에 숨어 보았다 — 어느 오후, 알 속에 '넓고 이상한 나라'가 스쳐 지나갔다.")
narration(4, '알 속 세계 — 문 없는 둥근 창의 궁전들, 이끼 같은 숲. 둥근 머리에 은빛 날개를 단 무리가 장엄하게 선회하고, 하늘의 달은 두 개였다.')
# P6 is intentionally silent.
narration(6, '과학자 웨이스와의 밤마다 관측 — 테라스 위 스무 개의 장대 끝에도 같은 수정 알이 빛났다. 두 결정은 서로 공명하고 있었다.')
dialogue(6, '웨이스:', '저쪽에서도, 이쪽을 보고 있어.')
narration(7, "케이브는 수정을 끌어안은 채 미소 지은 얼굴로 발견되었다. 알은 '키 크고 검은 신사'의 손에 사라졌다 — 지금도 이 반대편에서, 누군가 들여다보고 있을지 모른다.")

dst.parent.mkdir(parents=True, exist_ok=True)
Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
print(dst.stat().st_size)
