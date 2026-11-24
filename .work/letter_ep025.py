from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-025-journey-to-the-center-of-the-earth'
destination.mkdir(parents=True, exist_ok=True)

pages = [
    [
        {'n': '1863년 5월의 함부르크 — 낡은 양피지 한 장이 조용한 저택을 뒤흔든다.', 'd': [('리덴브록:', '이 문양은, 암호다!')]},
        {'d': [('악셀:', '거꾸로 읽으니 보여요 — 스카르타리스 그림자가 떨어지는 굴뚝으로, 내려가라!')]},
        {'d': [('악셀:', '지구 중심은 4천 도의 불덩어리라고요!'), ('리덴브록:', '그러니 눈으로 증명하러 가는 것이다.')]},
        {'d': [('그라우벤:', '영웅의 조카는 벽난로 앞에 앉아 있지 않아요 — 부디, 다녀오세요.')]},
        {'n': '코펜하겐을 지나 바다 하나를 건너 — 6월의 아이슬란드.'},
        {'d': [('리덴브록:', '주당 3리크스달러다, 한스 — 최고의 사냥꾼이 곧 최고의 길잡이지.')]},
    ],
    [
        {'n': '6월 28일 정오 — 스카르타리스의 그림자가, 갈 길을 가리킨다.'},
        {'d': [('리덴브록:', '둘 중 어느 길이냐고? 사크누셈은 왼쪽을 택했다!')]},
        {'d': [('악셀:', '석탄층 아래 조개 화석 — 여긴 아득한 옛바다의 바닥이야.')]},
        {'d': [('악셀:', '수통이… 바닥났어요. 이대로 우린 전부 말라 비틀어질 운명인가요.')]},
        {},
        {'d': [('악셀:', '내 등불이 꺼져 간다… 이모님, 그 목소리가 혹시 환청일까.')]},
    ],
    [
        {'d': [('리덴브록:', '사크누셈이 여기까지 왔다 — 이 바위를 부숴라!')]},
        {'d': [('리덴브록:', '보라, 악셀 — 발밑에 지구의 바다가 있다!')]},
        {'d': [('악셀:', '30미터 석송 숲, 빛나는 하늘 — 하나의 실내 우수.')]},
        {'d': [('악셀:', '안개 속에 목자 같은 거인? …이 광경은, 아무에게도 말하지 않기로 하자.')]},
        {'d': [('리덴브록:', '뗏목의 이름은 레더호! 출항이다, 지구의 바다로!')]},
        {'d': [('악셀:', '바다가 갈라진다 — 어룡의 아랫니와 장경룡의 목이 얽혔다!')]},
    ],
    [
        {'d': [('악셀:', '번개 덩어리가 돛대를 타고 내려온다 — 모두, 엎드려!')]},
        {'d': [('리덴브록:', '나침반이 뒤집혀 있었군 — 폭풍이 우리를 출발점으로 되돌린 것이다.')]},
        {'d': [('리덴브록:', '사크누셈의 단검! 그도 이 통로 앞에 섰었다 — 화약을, 채워라!')]},
        {'d': [('악셀:', '바다가 구멍 속으로 쏟아져 내려간다!')]},
        {'d': [('리덴브록:', '뗏목 아래 이 바다가… 아니, 끓는 용암이다!')]},
        {'n': '스트롬볼리의 여름 하늘 — 지구를 가로지른, 세 사람.'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep025-p{page_number}-notext.png'
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
