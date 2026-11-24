from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-043-the-machine-stops'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '인류는 지하 벌집의 육각 방에서 — 기계가 주는 모든 것을 받으며, 각자 따로'},
        {'d': [('키노:', '어머니, 전 나갔어요. 기계의 허락 없이, 제 발로'), ('바쉬티:', '그건 무가옥이에요. 방 밖엔 아무것도 없는데')]},
        {'d': [('키노:', '표면에 있었어요! 이끼와 바람, 그리고 밤하늘 가득 별'), ('바쉬티:', '그런 말은... 기계 앞에서는 못 해요')]},
        {},
        {'d': [('키노:', '우리는 원래 하늘 아래에서 걸었어요. 지금도 할 수 있어요')]},
        {'n': '붙잡혀 돌아온 방 — 홀로 다리를 뻗고, 걷는 연습'},
    ],
    [
        {'n': '그 뒤로 오래지 않아 — 기계의 작은 실수들이 하나둘'},
        {'d': [('여인:', '목욕물 소리가 어제와 달라요... 확실히'), ('바쉬티:', '기계는 완벽해요. 우린 그렇게 배웠죠')]},
        {'d': [('위원회:', '수리 위원회가 움직입니다. 침착하십시오'), ('사람들:', '음악이... 아직도 멎지 않고 있어')]},
        {},
        {'d': [('키노:', '어머니, 손! 기계는 멈췄지만 우린 숨 쉬어요 — 위로, 벽 너머로')]},
        {'n': '무너진 벌집 너머, 별빛 아래 처음 선 인류 — 맨발의 온기'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep043-p{page_number}-notext.png'
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