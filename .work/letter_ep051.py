from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-051-we'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '머나먼 미래, 유리로 지어진 완전한 나라 온세계주 — 여기서 이름은 번호, D-503'},
        {'d': [('D-503:', '만인이 한 몸이 되어 시간표대로 산다 — 노동도, 식사도, 입맞춤의 시간도 정확히')]},
        {'d': [('D-503:', '우주선 인테그랄이 완성된다 — 수학의 완전함을, 별들에게로 실어 나르겠지')]},
        {'d': [('D-503:', '입맞춤에도 분홍 이용표가 필요해 — 오늘의 내 표는…')]},
        {'d': [('I-330:', '수학자 D-503 — 무한수를 겁내나요? 나를 따라오세요')]},
        {},
    ],
    [
        {'d': [('I-330:', '여기는 유리 이전의 옛것들 — 벽돌, 피아노, 아직 야생인 음악')]},
        {'d': [('D-503:', '금지된 담배와 증류주… 손이 떨린다, 이건 병인가'), ('I-330:', '당신 안에 영혼이 자라고 있어요')]},
        {'n': '녹색 장벽 너머 — 풀과 이슬, 곱슬털의 사람들. 그리고 다시는 돌아올 수 없는 초록'},
        {'d': [('D-503:', '맨발로 풀을 밟아 본 적이… 없다, 없었다는 걸 이제야'), ('I-330:', '당신은 이제 번호가 아니에요')]},
        {'n': '하늘에 구름 한 조각 — 형체도 이치도 없는 것은, 이 나라에서 병이다'},
        {},
    ],
    [
        {'d': [('온세계주 방송:', '전 번호에게 고한다 — 상상력은 병이다. 위대한 수술이 그 병을 떼어 낸다. 행복은 의무')]},
        {'d': [('D-503:', '수술대는 따뜻했다… 이제는, 아무도 그립지 않다')]},
        {'d': [('I-330:', '수술한 자의 눈을 들여다봐도 — 나는 아무 말도 하지 않겠어요')]},
        {'n': '가스 큐브 아래서도 끝내 침묵 — 그 뒤로 인테그랄은 여전히 별을 향해 서 있다'},
        {'d': [('D-503:', '논리는 이겼다 — 내일의 나는, 다시 완전하다')]},
        {'n': '그리고 유리 도시의 밤하늘에는 — 구름, 한 점'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep051-p{page_number}-notext.png'
    dst = destination / f'page-{page_number:02d}.png'
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
    panel_h = (H - 2 * margin_y - 2 * gutter_y) / 3

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

    def dialogue(i, entries):
        x0, _, x1, y1 = panel(i)
        left, right = x0 + px(12), x1 - px(12)
        inset = px(12)
        available = right - left - 2 * inset
        laid_out = []
        for name, speech in entries:
            name_width = d.textlength(name, font=speaker_font) + px(8)
            lines = wrap_chars(speech, regular, available, available - name_width)
            laid_out.append((name, name_width, lines))
        leading = px(29)
        line_count = sum(len(lines) for _, _, lines in laid_out)
        height = px(20) + leading * line_count
        bottom = y1 - px(10)
        top = bottom - height
        d.rounded_rectangle((left, top, right, bottom), radius=px(10), fill=(255, 255, 255, 238), outline=(31, 41, 55, 255), width=px(2))
        text_y = top + px(8)
        row = 0
        for name, name_width, lines in laid_out:
            d.text((left + inset, text_y + row * leading), name, font=speaker_font, fill=(245, 158, 11, 255))
            for n, line in enumerate(lines):
                line_x = left + inset + (name_width if n == 0 else 0)
                d.text((line_x, text_y + (row + n) * leading), line, font=regular, fill=(31, 41, 55, 255))
            row += len(lines)

    for i, caption in enumerate(captions):
        if 'n' in caption:
            narration(i, caption['n'])
        if 'd' in caption:
            dialogue(i, caption['d'])

    Image.alpha_composite(im, overlay).convert('RGB').save(dst, format='PNG')
    return dst


outputs = [letter_page(n, captions) for n, captions in enumerate(pages, 1)]
page_images = [Image.open(p).convert('RGB') for p in outputs]
width, height = page_images[0].size
scroll = Image.new('RGB', (width, height * len(page_images) + 16 * (len(page_images) - 1)), '#FFFFFF')
for i, page in enumerate(page_images):
    y = i * (height + 16)
    scroll.paste(page, (0, y))
    if i < len(page_images) - 1:
        ImageDraw.Draw(scroll).rectangle((0, y + height, width - 1, y + height + 15), fill='#FFF8E7')
scroll.save(destination / 'scroll.png', format='PNG')

for output in [*outputs, destination / 'scroll.png']:
    print(f'{output.relative_to(root)} | {output.stat().st_size}')