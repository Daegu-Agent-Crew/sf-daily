from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-035-somnium'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '별이 쏟아지는 섬의 밤 — 이 집 마당에 지붕이 없는 까닭은, 달'},
        {'d': [('피옥실데:', '달의 정령이여, 아이에게 저 달까지의 길을 가르쳐 주오'), ('다이몬:', '길은 하나, 그림자 — 달그림자가 땅에 닿는 동안만, 문이 열린다')]},
        {'d': [('다이몬:', '처음의 밀림이 가장 사나우니 — 살과 뼈를 단단히 묶어라'), ('두라코투스:', '제 발이… 저 어둠 속으로, 절로 걸어들어가는')]},
        {'d': [('다이몬:', '숨은 아껴라, 말도 하지 마라 — 이 다리에서 무게는, 목숨의 값'), ('두라코투스:', '심장이 등 뒤로 몰려도 — 발끝은, 앞으로')]},
        {},
        {'d': [('다이몬:', '이제부터는 걷는 것이 아니다 — 꿈의 무게로, 흘러라')]},
    ],
    [
        {'n': '레바니아의 하늘에는 바다가 떠 있다 — 그 푸른 별의 이름은, 볼바'},
        {'d': [('다이몬:', '낮에는 돌이 물러질 만큼 뜨겁고 밤에는 숨이 얼어붙는다 — 여기의 하루는, 너희의 한 달')]},
        {'d': [('두라코투스:', '이 골짜기의 풀은 벌써 늙어가는데 — 저 새싹은, 방금?'), ('다이몬:', '태어나고, 자라고, 지는 것이 여기선 하루일 — 저들은 너희의 긴 목숨을 부러워한다')]},
        {'d': [('다이몬:', '물을 보라 — 얼음과 김 사이를 오가며 하루를 견디는, 저것이 레바니아의 바다')]},
        {},
        {'n': '눈을 뜬 새벽 — 이마의 식은땀, 문틈에서 조용히 닫히는 어머니의 책장. 창밖에는, 아직도 저 달'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep035-p{page_number}-notext.png'
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