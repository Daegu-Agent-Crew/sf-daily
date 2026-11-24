from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-031-the-heads-of-cerberus'
destination.mkdir(parents=True, exist_ok=True)




pages = [
    [
        {'n': '1919년 필라델피아, 폭우 — 우리 셋은 골목 끝 잡화점으로 몸을 피했다'},
        {'d': [('주인:', '이 수정 잔에는 값을 매기지 않았소. …필요한 이에겐, 공짜.'), ('바비:', '공짜라… 뭔가 굉장히 속보이는걸요?')]},
        {'d': [('테리:', '영감, 이 회색 가루 말인가?'), ('바이올라:', '장미 향… 아니, 훨씬 오래된 냄새')]},
        {'d': [('바이올라:', '그저 향이 좋아서, 들이마셨을 뿐이에요')]},
        {},
        {'d': [('바비:', '여긴 방금 그 가리가 아닌가? 저 첨탑들은 대체…'), ('테리:', '둘 다 내 뒤로. 이 거리 전체가, 우리를 보고 있어')]},
    ],
    [
        {'n': '2118년 — 낡은 벽돌 도시 위로, 돌처럼 차가운 탑들이 자라 있었다'},
        {'d': [('바이올라:', '저 사람들 목에… 번호판이 달린 목걸이'), ('바비:', '죄수 표시가 아니야. 저들 모두가, 저걸 차고 있어')]},
        {'d': [('경비:', '목걸이 없는 자는 즉시 연행 대상이다. 따라와.'), ('바비:', '우린 이 도시 사람이 아니에요! 정말이에요!')]},
        {'d': [('테리:', '먼저 건드리는 놈이, 이 손바닥부터 본다')]},
        {'d': [('관리관:', '번호 3271, 노동 구획 배정. 항소는 없다.'), ('테리:', '…감히 내 목에 이걸 채웠겠다')]},
        {'n': '새벽 창살 너머 — 번호를 단 사람들의, 끝없는 행렬'},
    ],
    [
        {'d': [('테리:', '문을 열어라! 오늘 밤 이 도시의 목걸이는, 전부 벗겨진다')]},
        {'d': [('바이올라:', '여러분! 그 번호는, 여러분의 이름이 아니에요'), ('시민들:', '목걸이를 벗어라! 벗어라!')]},
        {'n': '수정 잔 바닥에 남은 — 마지막 한 꼬집의 가루'},
        {'d': [('바비:', '눈 감아요, 두 분. 그 폭풍의 가게로, 우리 다시')]},
        {'n': '아침의 우리 골목 — 잡화점이 있던 자리엔, 낡은 벽돌벽뿐'},
        {'n': '아직 손안에 — 별처럼 빛나는 회색 가루, 몇 알'},
    ],
]









def letter_page(page_number, captions):
    src = root / f'.work/ep031-p{page_number}-notext.png'
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
