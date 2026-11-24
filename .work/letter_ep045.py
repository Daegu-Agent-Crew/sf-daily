from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-045-the-xipehuzi'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'d': [('학자:', '해독됐네… 점토판 다섯 장이, 5천 년 만에 말을 건다')]},
        {'d': [('페후:', '저건… 신성한 나무인가, 아니면 — 살아 있는 건가?')]},
        {'n': '닿기 직전, 보이지 않는 일격'},
        {'d': [('바쿤:', '나무도 짐승도 아니야. 이름을 붙이고, 기록한다'), ('족장:', '기록이 우리를 지켜주겠나, 바쿤!')]},
        {'d': [('목동:', '양들이! 저 빛 속으로 양들이 끌려가!')]},
        {},
    ],
    [
        {'d': [('바쿤:', '보게들… 저들이 서로, 빛으로 이야기한다')]},
        {'d': [('바쿤:', '온몸이 무기인 생명이 단 한 곳만 숨기고 있어 — 밑동의, 저 별!')]},
        {'d': [('족장:', '부러진 창은 버려라, 도끼와 짧은 칼로'), ('바쿤:', '별을 향해, 단 한 번만 정확히')]},
        {'d': [('전사들:', '크시페우지여 — 오늘 밤이 저들의 마지막이다!')]},
        {'d': [('전사:', '몸이 돌았다! 별이 보인다 — 지금!')]},
        {'d': [('전사:', '하나가… 하나가 쓰러진다!')]},
    ],
    [
        {'d': [('족장:', '전열을 무너뜨려라! 평원을 되찾자!')]},
        {'n': '마지막 하나 — 별을 감춘 채, 물러서는'},
        {'d': [('바쿤:', '쉿… 다들 저 빛을 봐라. 짧게, 길게 — 저건 말이다, 마지막 인사')]},
        {'d': [('족장:', '이겼네, 바쿤! 어째서 잔을 들지 않나?'), ('바쿤:', '우리가 방금 무엇을 지웠는지… 그게 두렵네')]},
        {'n': '어쩌면 저들은 별 사이로 고향을 찾던 이주민 — 아니, 먼저 온 이웃'},
        {'n': '그리고, 하늘의 인디고'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep045-p{page_number}-notext.png'
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
