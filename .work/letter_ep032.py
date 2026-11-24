from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-032-micromegas'
destination.mkdir(parents=True, exist_ok=True)





pages = [
    [
        {'n': '시리우스의 청년 미크로메가스, 나이 사백오십 — 그 별 기준으로, 아직 청년이다'},
        {'d': [('토성인:', '누구냐. 내 별을 요람 삼지 않게.'), ('미크로메가스:', '지나가는 나그네일세. 자네 별은 아담해서 좋구려')]},
        {'d': [('토성인:', '아담하다니! 수명이 만오천 년밖에 안 되어 — 짧아서 눈물이 나'), ('미크로메가스:', '나는 감각 천 개로 백만 년을 살아도, 결국 같은 걸 궁금해하지')]},
        {'d': [('미크로메가스:', '저 혜성을 타세. 우주 유람의 왕도일세'), ('토성인:', '허리야 부러지겠지만… 일단, 점프!')]},
        {},
        {'d': [('토성인:', '저건 얼음알이야. 감각 일흔둘로 장담하네 — 생명은 없어'), ('미크로메가스:', '잠깐, 내 다이아몬드를 보게 — 움직이는 점이, 아주 작은 점이 있어!')]},
    ],
    [
        {'d': [('선장:', '산이다! 산이 바다 위를 걷는다!'), ('철학자:', '아니… 저건 눈이야. 살아 있는 눈이 우리를 보고 있어')]},
        {'d': [('미크로메가스:', '이 즉석 확성 기계로 듣게 — 원자들이 과연 말을 하는가'), ('선원들:', '먹지만 말아 주시오! 우리는 생각할 줄 아는 원자들이오!')]},
        {'d': [('철학자:', '우리는 종종 전쟁을 합니다. 모자 쓴 십만 마리가 진창 몇 자를 두고 서로 죽이는…'), ('미크로메가스:', '오, 불쌍하고도 무서운 원자들…')]},
        {'d': [('신부:', '우리에겐 영혼이 있소! 그대들보다 결코 작지 않은'), ('토성인:', '들었나… 이 보송한 점들이, 영혼을 말하네')]},
        {'n': '작별 인사 대신 남긴 것 — 손톱만 한, 한 권의 책'},
        {'n': '미크로메가스가 남긴 책 — 인간의 눈에는, 새하얀 페이지뿐'},
    ],
]











def letter_page(page_number, captions):
    src = root / f'.work/ep032-p{page_number}-notext.png'
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
