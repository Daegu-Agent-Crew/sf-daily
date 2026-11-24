from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-052-rappaccinis-daughter'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '르네상스 시절 파도바 — 조르바니의 창 아래로, 의사 라파치니의 밀폐된 정원이 열린다'},
        {'d': [('라파치니:', '내 맨손이 닿으면 시드는 것들 — 오늘도 안색이 좋구나, 우리의 보배')]},
        {'d': [('베아트리체:', '어서 내게로 와 — 너에게 필요한 건, 내 숨결이니까')]},
        {'n': '진보라 꽃에 얼굴을 묻는 처녀 — 코랄빛 드레스가 저녁 햇에 젖어 든다'},
        {},
        {'d': [('조르바니:', '나비가… 떨어졌다. 저 향기에, 저 입김에?')]},
    ],
    [
        {'d': [('바글리오니:', '라파치니는 과학을 위해 사랑도 희생시키는 사람일세 — 그 정원에서 눈을 떼게')]},
        {'n': '낮의 정원을 두 사람이 나란히 걷는다 — 꽃빛은 더 짙어지고, 검은 실루엣은 더 가까이'},
        {'d': [('조르바니:', '아침에 산 꽃다발이 벌써…'), ('베아트리체:', '…그 이유를 나는 알아요, 유감스럽게도')]},
        {'d': [('조르바니:', '내 숨결에 거미가 스러졌다 — 이 손이, 이 입이 벌써 독이라고?')]},
        {'d': [('바글리오니:', '은병 하나면 충분하네 — 라파치니의 독을 이기는 해독제')]},
        {},
    ],
    [
        {'d': [('조르바니:', '당신 아버지가 나를 독으로 만든 건가, 아니면 당신이!')]},
        {'d': [('베아트리체:', '당신과 나는 같은 정원의 꽃이에요 — 미워하지 마세요')]},
        {'d': [('조르바니:', '그럼 이걸 마셔요 — 우리 둘 다, 사람으로 돌아가게'), ('베아트리체:', '기꺼이 마실게요, 물처럼')]},
        {'n': '약이 목을 지나자 꽃잎처럼 흩어진다 — 그녀의 무릎이, 꺾인다'},
        {'d': [('베아트리체:', '나는 사랑받고 싶었어요 — 두려운 존재가 아니라')]},
        {'n': '그리고 정원에는, 아직도 진보라 꽃이 핀다'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep052-p{page_number}-notext.png'
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
