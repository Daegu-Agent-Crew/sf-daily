from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-034-gullivers-travels'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '폭풍에서는 살아남았다 — 그런데 왜 몸은, 새벽까지 묶여 있는 걸까'},
        {'d': [('사자:', '소인국 릴리퍼트의 칙령이오! 폐하께 복종할 것을 맹세하시오 — 그것이 대가로, 목숨이 되겠소'), ('걸리버:', '맹세하지요. 대신 아침 식사를 — 표류한 지 사흘째라, 폐하')]},
        {'d': [('시동:', '오늘의 식사, 수레 삼십 대 분이옵니다!'), ('걸리버:', '소인국의 한 끼에 수레 서른 대 — 이 나라의 환대는, 참으로 무겁군')]},
        {'d': [('걸리버:', '전쟁의 이유를 다시 한번 — 계란이라고?'), ('대신:', '큰 끝으로 깨는 것이 국시! 작은 끝을 깨는 블레푸스큐는, 야만이오')]},
        {},
        {'d': [('걸리버:', '영웅과 반역인의 사이는, 계란 껍데기 한 장 — 두 번째 항해는 이번엔, 홀로')]},
    ],
    [
        {'n': '두 번째 표류지의 아침 — 이번에는, 밀밭이 하늘을 가린다'},
        {'d': [('농부:', '(사람이구나!) 손바닥 위로 올라와 보시오 — 여보, 아이들아, 인형이 아니라 사람이요!')]},
        {'d': [('왕녀:', '앉아, 찰리! 그건 갖고 노는 게 아니야'), ('걸리버:', '거인 나라의 개 앞에서는, 사자도 쥐새끼 신세다…')]},
        {'d': [('왕:', '시계가 아니라면 그 작은 발톱은 뭐란 말이오 — 자네, 짐승의 한 종류 아니오?'), ('걸리버:', '폐하의 신하 중 가장 작은 신하옵니다 — 하지만 웃는 법은, 폐하와 같습니다')]},
        {},
        {'d': [('선원:', '선장님! 바다에 뜬 상자가, 저절로 흔들립니다 — 문이!'), ('걸리버:', '문 좀 열어 주시오 — 안에서 신사 한 명이, 지금 나올 것이오')]},
    ],
    [
        {'n': '세 번째 바다 — 해적은 배를 훔쳐 갔고, 하늘이 나를 주운 모양이다'},
        {'d': [('걸리버:', '섬이, 떠서 내려온다 — 저 밑동의 자석이, 대지를 붙잡고 있다고?')]},
        {'d': [('하인:', '(톡톡) 각하, 답변하실 시간입니다 — 손님이오'), ('천문학자:', '아, 그래… 인사. 실례지만 금성의 위성이, 지금 몇 개더라')]},
        {'d': [('시민:', '저 섬이 해를 가린 지 마흔 하루 — 밭이 다 말라 갑니다'), ('걸리버:', '세금을 물지 않으면 섬이 내려앉는다니 — 감옥이, 하늘에 떠 있는 나라')]},
        {'d': [('학자:', '오이에서 햇빛을 뽑아 내는 중이오 — 자, 이 반짝임이!'), ('걸리버:', '지붕부터 세우는 건축가와, 눈꺼풀로 글자를 읽는 시인도 다 저 아랫방이랍니다')]},
        {'n': '런던의 아침, 손바닥 위의 소인국 양 한 마리 — 그리고 창밖, 하늘의 또 다른 지도'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep034-p{page_number}-notext.png'
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
