from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-040-sultanas-dream'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '1905년 벵골의 나른한 오후 — 안락의자가 잠을 부른다'},
        {'d': [('술타나:', '창밖이… 거리가 아니라 정원이에요!'), ('사라 언니:', '어서 와요. 여긴 레이디랜드')]},
        {'d': [('술타나:', '우물도 안 보이는데, 물은 어디서?'), ('사라 언니:', '구름에서 받아요. 전기가 물을 살균하고, 오존이 병을 막죠')]},
        {},
        {'d': [('술타나:', '하늘을 달리는 차라니… 경찰은 어디 있죠?'), ('사라 언니:', '죄가 사라졌으니, 파출소도 같이 사라졌어요')]},
        {'n': '죄도 없고, 병도 없고, 전쟁도 없는 나라'},
    ],
    [
        {'d': [('여교장:', '거울로 햇살을 모으면 — 밥도 짓고, 불도 밝혀요'), ('술타나:', '햇살로 끓인 차라고요?')]},
        {'n': '그날 밤, 도시의 등불은 전부 태양의 저축'},
        {'d': [('사라 언니:', '한때 이웃 왕이 전쟁을 걸어왔었죠. 남자들은 모두 패주했어요'), ('술타나:', '그럼… 누가 나라를 지켰는데요?')]},
        {},
        {'d': [('사라 언니:', '여자들이요. 그 뒤 남자들은 안뜰로 들어가고, 우리가 세상을 굴려요'), ('술타나:', '그게 바로… 제나나의 뒤집힘!')]},
        {'n': '눈을 뜬다 — 손끝에 아직, 모아 둔 햇살의 온기'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep040-p{page_number}-notext.png'
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
