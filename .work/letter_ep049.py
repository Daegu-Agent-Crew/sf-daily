from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-049-looking-backward'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '1887년의 보스턴 — 파업의 함성 속에서도, 줄리언 웨스트의 저택엔 축배가 흐른다'},
        {'d': [('에디스 바틀릿:', '5월 30일이면 새 집이 완공돼요 — 그날, 결혼식을 올려요'), ('줄리언:', '불면증만 낫는다면 말이죠')]},
        {'d': [('최면사:', '이 지하 침실은 소리도 불씨도 못 들입니다 — 편히, 깊이 잠드시길')]},
        {'d': [('하인:', '불이야! 도련님은 아직 지하에 계셔!')]},
        {'n': '밤새 타오른 불길도 눈물도 — 흙 속 침실엔 닿지 못했다'},
        {},
    ],
    [
        {'d': [('레이트 박사:', '정원 굴착 중에 방음 금고가 나왔네 — 이 젊은이는… 살아 있어!')]},
        {'d': [('줄리언:', '오늘이… 1887년 5월 31일이죠?'), ('레이트 박사:', '2000년 9월 10일일세 — 자네는 백십삼 년을 잤어')]},
        {'n': '2000년의 보스턴 — 검은 연기는 사라지고, 유리 지붕 아래 거리엔 꽃이 흐른다'},
        {'d': [('에디스:', '이 카드만 내밀면 돼요 — 배급소는 온 나라의 창고니까'), ('줄리언:', '돈이 필요 없는 거라고?')]},
        {'d': [('레이트 박사:', '노동은 하루 네 시간 — 남은 하루는 모두 자기 것이니'), ('에디스:', '저녁엔 전화로 음악을 들려드릴게요')]},
        {},
    ],
    [
        {'d': [('줄리언:', '난 증오받는 시대에서 온 유물이에요 — 이 세계에 제 자리가 없어요')]},
        {'d': [('에디스:', '따라와서 미안해요 — 그런 얼굴로 혼자 두고 올 순 없어서요')]},
        {'d': [('줄리언:', '…당신을 사랑해요'), ('에디스:', '정말 눈이 멀었네요 — 저도 그걸 보여 드리러 왔는걸요')]},
        {'d': [('레이트 부인:', '에디스는 당신의 약혼녀, 에디스 바틀릿의 증손녀예요')]},
        {'n': '십사 년을 애도한 뒤 맺은 혼인 — 그 피가 백 년을 건너 이 식탁에 앉아 있다'},
        {},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep049-p{page_number}-notext.png'
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
