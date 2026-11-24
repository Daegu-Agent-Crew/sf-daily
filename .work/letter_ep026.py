from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-026-flatland'
destination.mkdir(parents=True, exist_ok=True)

pages = [
    [
        {'n': '길이와 너비, 단 둘 — 이곳은 플랫랜드. 두께 제로의 나라.'},
        {'d': [('손자:', '8이 16이 되려면… 변을 위로 쌓으면 안 되나요?'), ('정사각형:', "'위'? 그건 북쪽의 붙임말 아니냐.")]},
        {'d': [('삼각형 이웃:', '안개 낀 아침이지? 오늘 내가 육각형처럼 보인다 해도, 놀라지 마시게.')]},
        {'n': '꿈속의 라인랜드 — 앞과 뒤뿐인, 한 줄의 왕국.'},
        {'d': [('정사각형:', '왕이여, 당신의 온 나라가 내 눈엔 한 줄로 보인다오!'), ('라인랜드 왕:', '한 줄 이상은 없다! 당장 사라지게!')]},
        {'n': '깨어난 밤 — 벽 안쪽에서, 낯선 원이 자라난다.'},
    ],
    [
        {'d': [('정사각형:', '원이… 점점 커진다. 여자도, 사제도 아닌 — 이건 뭐지?')]},
        {'d': [('구:', '놀라지 말게. 나는 3차원에서 왔다 — 위에서, 그리고 아래에서.')]},
        {'d': [('정사각형:', "술사의 재주로군! '위'라니, 북쪽이냐, 남쪽이냐?"), ('구:', '어느 쪽도 아닐세. 그대 세계 바깥으로 나가는 방향이지.')]},
        {},
        {'d': [('정사각형:', '보인다… 이웃의 주머니도, 아내의 속마음도, 한눈에 전부!')]},
        {'d': [('정사각형:', '저 하늘 위에 또 하늘이? 몇 겹까지 있는 거지?'), ('구:', '오늘은 여기까지 — 상상력은 한 겹씩 자라는 법이니.')]},
    ],
    [
        {'d': [('점 왕:', '아무도 없네, 아무도… 아니, 말하는 건 나뿐이군. 잘도 떠드는 나란 말이야.')]},
        {'d': [('정사각형:', '그럼 당신도 상상할 수 있겠군 — 4차원이라는 것을.'), ('구:', '4차원? 무슨 헛소린가. 3차원이 전부일세.')]},
        {'d': [('구:', '돌아가게 — 하지만 잊지 말게. 위가, 있다는 것을.')]},
        {'d': [('정사각형:', '여러분, 위가 있습니다! 여러분의 주머니도, 마음도, 전부 보이는 곳이요!')]},
        {'d': [('사제:', '하늘에서 온 목소리라… 아주 적합한 방이 있네. 돌로 지은, 조용한 방이.')]},
        {'n': '두꺼운 벽, 낮은 하늘 — 그래도 위만은, 아직 세지 않은 곳.'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep026-p{page_number}-notext.png'
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
