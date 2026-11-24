from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-046-the-first-men-in-the-moon'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'d': [('베드포드:', '빚쟁이를 피해 숨은 시골의 옆집이, 하필 미친 천재라니'), ('케버:', '중력을 차단하는 물질을 만들었소, 베드포드 씨')]},
        {'d': [('케버:', '보시오 — 이 판은 지구가 잡아당기지 못하오'), ('베드포드:', '무게가… 사라졌어!')]},
        {'d': [('베드포드:', '광산은 망했지만 이건 대박이야 — 우주 여행, 세기의 사업!')]},
        {'d': [('케버:', '블라인드를 열면, 저절로 하늘로')]},
        {'d': [('베드포드:', '저 곡선이… 우리의 대양이군')]},
        {},
    ],
    [
        {'d': [('베드포드:', '가루 같은 눈밭이야… 저기, 하늘에 지구가 떠 있어'), ('케버:', '이 행성은 죽은 게 아니오, 해돋이를 기다리는 것뿐')]},
        {'d': [('케버:', '봐라! 싹이 눈처럼 부풀어 오르지 않나')]},
        {'d': [('베드포드:', '숲이야! 방금까지 황무지였는데 — 지금, 자라는 중이라고!')]},
        {'d': [('케버:', '달의 낮은 며칠이 아니라 몇 시간 — 이곳의 봄은 서두르오')]},
        {'d': [('베드포드:', '케버! 저건… 사람인가, 벌레인가?')]},
        {'d': [('케버:', '총 대신, 인사를')]},
    ],
    [
        {'n': '지혜가 자라는, 지하의 온실'},
        {'d': [('케버:', '저들의 머리는 하는 일에 맞춰 길러졌소 — 기계공의 머리, 수학자의 머리')]},
        {'d': [('베드포드:', '저건 뭐지… 뇌? 저 혼자가 저 도시 전부의, 왕이자 도서관?')]},
        {'d': [('베드포드:', '케버, 돌아가자! 구체는 풀숲에 그대로야'), ('케버:', '남겠소 — 물을 게 산더미처럼 남았으니')]},
        {'d': [('베드포드:', '케버! 창이다, 저들이 창을 들고 왔어 — 케버!!')]},
        {'n': '그리고, 달의 침묵'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep046-p{page_number}-notext.png'
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
