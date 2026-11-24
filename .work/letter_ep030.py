from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-030-the-island-of-doctor-moreau'
destination.mkdir(parents=True, exist_ok=True)



pages = [
    [
        {'n': '난파 여드레째 밤 — 나를 건져 준 배는, 짐승 냄새가 났다'},
        {'d': [('몽고메리:', '천천히 마시게. …그리고 갑판 위에선, 눈을 너무 크게 뜨지 말게.'), ('프렌딕:', '저 선원들 얼굴이… 왜 다들 저런 모양이지?')]},
        {'d': [('선장:', '여기까지야! 조각배로 저 섬에나 내려가시지!'), ('프렌딕:', '섬이라뇨? 여긴 사람이 살 수 없는 곳이잖소!')]},
        {'d': [('몽고메리:', '밀링, 짐을 챙겨라. …저 사람을, 잘 부탁한다.')]},
        {'d': [('모로 박사:', '머무는 건 허하네. 단 한 가지 — 내 울타리 안에는 들어오지 말게.'), ('프렌딕(독백):', '저 눈은 동정이 아니야. 계산이다.')]},
        {'n': '첫날 밤, 창밖 숲 — 반짝이는 눈동자들, 줄지어'},
    ],
    [
        {'d': [('짐승인간들:', '네 발로 기지 말 것… 살점을 먹지 말 것… 우리는 법이다…')]},
        {'d': [('원숭이인간:', '다리가 둘뿐인 걸 보아, 걸을 줄 아는 짐승이 또 왔구나!'), ('프렌딕:', '짐승이라니… 당신들야말로 대체, 뭐지?')]},
        {},
        {'d': [('프렌딕:', '퓨마의 울음소리… 밤마다 저 문 너머에서. 대체 무엇을 만들고 있는 거야?')]},
        {'d': [('프렌딕:', '밀링의 손목에 손가락이 다섯, 꼬매진 자국 — 짐승을 사람으로 만들고 있어')]},
        {'d': [('모로 박사:', '비명에 신경 쓰지 말게. 고통은 내 연구의, 가장 값싼 재료일 뿐.')]},
    ],
    [
        {'n': '그날 밤 — 고통의 집 문이 부서지고, 퓨마가 어둠으로 달아났다'},
        {'d': [('짐승인간:', '법을 어긴 자는… 법 밖으로 나갈 뿐.'), ('프렌딕:', '모로 박사가 죽었어. 이 섬에 이제 법을 지킬 사람은, 아무도 없다.')]},
        {'d': [('프렌딕:', '창을 내려! 네 발로 기지 마! …대답이 없구나, 이미 늦었나.')]},
        {'n': '홀로 저으면 바다 — 등 뒤로 섬은 조용히 타고 있었다'},
        {'d': [('프렌딕:', '런던의 이 얼굴들… 모자 아래로, 아직도 섬이 보여.')]},
        {'n': '촛불 하나, 별이 가득한 창 — 나는 오늘도, 사람이 무섭다'},
    ],
]







def letter_page(page_number, captions):
    src = root / f'.work/ep030-p{page_number}-notext.png'
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
