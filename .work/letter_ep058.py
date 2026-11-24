from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-058-robur-the-conqueror'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '1886년 4월, 필라델피아 웰던 연구소 — 이 나라 제일가는 풍선 마니아들이 모여 든 밤', 'd': [('회원:', '고프 씨의 구형이 정답이야!'), ('회원:', '아니, 시가형 장형이다!')]},
        {'d': [('로뷔르:', '풍선은 하늘의 고래일 뿐 — 미래는 기계의 것이다')]},
        {'d': [('프루던트:', '이보게! 이름을 밝혀라!'), ('로뷔르:', '로뷔르 — \'정복자\'라고 불러 주지')]},
        {'n': '그날 자정 — 잠옷 차림으로 통째로 하늘에 끌려 올라가는 회장과 비서, 그리고 하인', 'd': [('프라이콜린:', '주인님, 저는 땅에 두고 가세요!')]},
        {'n': '눈을 뜬 곳은 3천 미터 상공, 프로펠러 서른여섯 개의 비행선 알바트로스호', 'd': [('로뷔르:', '잘 잤나, 신사들 — 지구가 발밑에서 지나가고 있네')]},
        {'d': [('로뷔르:', '자, 세계 일주다. 도망은 꿈도 꾸지 말게')]},
    ],
    [
        {'n': '새벽의 파리 — 전기 가로등이 지도처럼 흐르고', 'd': [('에반스:', '프로펠러 소리뿐이야… 새 한 마리 없는 하늘')]},
        {},
        {'d': [('로뷔르:', '나는 발명가가 아니네 — 세상보다 반 걸음 앞을 걸었을 뿐')]},
        {'n': '밤마다 도끼가 밧줄을 찾았지만', 'd': [('프루던트:', '이번엔 틀림없이…!'), ('선원:', '두 분, 그 손에 든 게 뭔지')]},
        {'d': [('프라이콜린:', '다시는 게으르게 안 살겠습니다 — 제발 땅으로만 돌려주세요!')]},
        {'n': '뇌운이 배를 삼켜도', 'd': [('로뷔르:', '침착하라 — 우리는 폭풍 위를 간다')]},
    ],
    [
        {'n': '8월, 나이아가라 — 안개에 무지개가 걸리고 알바트로스는 공중에 멈춰 섰다'},
        {'d': [('에반스:', '다이너마이트를 프로펠러 축에. 이번 한 번이면 끝이야'), ('프루던트:', '자정까지 네 시간.')]},
        {'n': '자정 — 마스트가 불꽃 속에 부서지고, 세 사람은 폭포 안개 속으로'},
        {'n': '1년 뒤 — 웰던 연구소의 열기구 고 어헤드가 하늘로', 'd': [('군중:', '만세! 풍선의 승리다!')]},
        {'n': '로뷔르는 살아 있었다', 'd': [('에반스:', '저 배는…!')]},
        {'n': '두 번 다시 오지 않겠다던 작별 인사 — 구름 저편으로, 프로펠러 소리만이'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep058-p{page_number}-notext.png'
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