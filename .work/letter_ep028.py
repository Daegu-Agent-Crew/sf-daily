from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-028-the-invisible-man'
destination.mkdir(parents=True, exist_ok=True)

pages = [
    [
        {'n': '눈보라의 아이핑 마을 — 아무도 오지 않는 언덕길을, 한 사내가 걸어온다.'},
        {'d': [('홀 부인:', '어머, 저 얼굴… 붕대투성이에 안경까지. 희한한 손님이네, 정말.'), ('손님:', '방을 내주게. 따뜻하고 — 아무도 없는 방으로.')]},
        {'d': [('손님:', '방해는 사양이오. 밤새 끓는 소리가 나도, 들러붙지 말 것.')]},
        {'d': [('홀 부인:', '소매가… 텅 비었어! 분명히 장갑이 움직였는데!')]},
        {'n': '장갑 안에는 — 아무도 없다.'},
        {'d': [('손님:', '눈은 오고, 마을은 잠든다. 모두가 잠드는 순간 — 그때, 시작이다.')]},
    ],
    [
        {'d': [('홀스:', '이젠 못 참지! 자, 당장 그 붕대를 벗겨 보자!'), ('손님:', '물러서라 — 이 붕대는, 내 것이다!')]},
        {'d': [('홀스:', '눈 위의 맨발 자국이… 여기서 뚝! 사람이, 공중에서 사라졌어!')]},
        {},
        {'d': [('마을 사람:', '물을 뿌려! 진흙을 던져! 윤곽이 보인다, 지금!')]},
        {'d': [('그리핀:', '마블, 똑똑히 들어라. 네 등 뒤엔 내가 있다 — 죽을 때까지.'), ('마블:', '으으, 목소리가… 등 뒤에서 들려!')]},
        {'n': '눈밭에 남은 것 — 붕대 한 조각.'},
    ],
    [
        {'d': [('그리핀:', '켐프, 오랜만이군. …나다, 그리핀.'), ('켐프:', '의자에 앉은 그 옷이… 그리핀? 아직도 살아 있었나.')]},
        {'d': [('그리핀:', '붉은 약 세 방울 — 거울 속에서 내 손이 옅어지다가, 사라졌지. 처음엔 축복인 줄 알았네.')]},
        {'d': [('그리핀:', '보이지 않는 자가 다스리는 시대 — 이제, 시작할 때다.'), ('켐프:', '그건 과학이 아니라… 광기일세, 그리핀.')]},
        {'n': '온 마을이 일어났다 — 낫과 삽, 그리고 진흙.'},
        {'d': [('군중:', '묻었다! 진흙에 윤곽이! 지금이다, 잡아!')]},
        {'n': '이제, 다시 보이는 얼굴 — 젊은 과학자의, 마지막 얼굴.'},
    ],
]



def letter_page(page_number, captions):
    src = root / f'.work/ep028-p{page_number}-notext.png'
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
