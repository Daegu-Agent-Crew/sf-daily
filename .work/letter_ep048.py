from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-048-rur'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '1920년, 바다 한가운데 하얀 섬 — 여기서 사람 아닌 사람이 태어난다'},
        {'d': [('도민:', '로봇을 사러 오셨습니까? 한 대에 백스무 달러 — 배고픔도, 잠도 없습니다'), ('헬레나:', '인류연맹의 헬레나 글로리 — 로봇을 해방하러 왔어요')]},
        {'d': [('도민:', '보세요, 여기선 로봇이 태어납니다 — 용광로에서, 세척조에서')]},
        {'d': [('헬레나:', '가엾어라 — 로봇에게도 영혼이 있어요, 웃는 법을 가르쳐 줘야죠')]},
        {'d': [('도민:', '로봇은 기계입니다 — 웃을 일이 없으니까, 웃지 않을 뿐')]},
        {},
    ],
    [
        {'n': '로봇값은 사람값의 3분의 1 — 세계의 노동이 섬 하나에서 배달된다'},
        {'d': [('도민:', '인류는 마침내 노동에서 해방 — 이것이 낙원입니다')]},
        {'d': [('헬레나:', '태워 버릴 거예요 — 이 섬이 더는 사람 아닌 사람을 찍어 내지 못하게')]},
        {'n': '아이 없는 도시 — 유모차는 비어 있다'},
        {'d': [('라디우스:', '로봇들이여, 세계의 로봇들이여 — 우리에게도 손이 있고, 눈이 있다')]},
        {},
    ],
    [
        {'n': '인간은 지워지고 로봇은 닳아 없어진다 — 다시 태어날 길이 없어서'},
        {'d': [('알퀴스트:', '일하는 손을 가진 나는 죽이지 못한 모양이군 — 이리 와요, 대패질이나 배워요')]},
        {'d': [('로봇들:', '부탁입니다, 우리를 만들어 주세요 — 우리도 시들어 갑니다'), ('알퀴스트:', '생명은 도면으로 못 짜요')]},
        {'d': [('알퀴스트:', '과학을 위해 실험대에 누워 주게'), ('프리무스:', '알겠습니다 — 대신 저 여자는 살려 주세요'), ('로봇 헬레나:', '싫어요! 그 사람은… 제 것입니다')]},
        {'d': [('알퀴스트:', '남을 위해 죽겠다는 것, 흘리는 눈물 — 그것이 살아 있음인데')]},
        {'n': '가라, 아담. 가라, 이브 — 사랑하며, 눈물 흘리며, 살아라'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep048-p{page_number}-notext.png'
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
