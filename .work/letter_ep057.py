from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-057-she'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'d': [('홀리:', '네 아버지가 남긴 마지막 상자다 — 깨진 항아리 조각과, 이천 년을 묵은 맹세'), ('레오:', '이 뱀 문양… 어릴 적부터 제 어깨에 새겨진 흉터와 같아요')]},
        {'d': [('잡:', '폭풍입니다! 돛대가— 돛대가 부러집니다!'), ('홀리:', '붙들어라! 저 암초만 넘으면 살 수 있다')]},
        {'d': [('빌랄리:', '어깨에 뱀을 지닌 분이 오실 때가 되었다고, 촌장들이 일러 두었소'), ('레오:', '우리를 기다렸다고요? 처음 온 땅인데')]},
        {},
        {'d': [('잡:', '무덤마다 등불을 밝혀 두다니… 죽은 도시가 산 도시보다 밝습니다'), ('홀리:', '말 소리를 죽여라 — 저 통로 끝에서 흰 빛이 새어 나온다')]},
        {'d': [('베일 속 목소리:', '가까이 오라, 아이여 — 나는 이 문이 닫힌 뒤로도, 오래 기다렸다')]},
    ],
    [
        {'d': [('아예샤:', '보아라 — 이 베일 아래, 이천 년을 견디고도 시들지 않은 얼굴을'), ('홀리:', '눈이 부시다… 이건 사람의 얼굴이 아니다')]},
        {'d': [('아예샤:', '그 문양을 기억한다 — 나의 킬리크라테스, 그대는 무덤에서도 나에게 돌아왔구나'), ('레오:', '꿈에서 계속 당신을 보았어요, 처음부터')]},
        {'d': [('아예샤:', '저 불의 기둥을 지나면 나이도 죽음도 없다 — 영원한 젊음으로, 나와 함께')]},
        {'d': [('레오:', '못 들어가겠어요… 저 불이 사람을 살려 준다는 보장이 어디 있죠'), ('홀리:', '레오, 정신을 차려라 — 그녀의 그림자가, 벌써 저렇게 커졌다')]},
        {'d': [('아예샤:', '내가 먼저 들어가 본다 — 자, 이렇게… 아니, 왜 몸이… 이천 년이, 한꺼번에')]},
        {'n': '새벽 안개 속을 걸어 나오는 두 사람 — 손바닥 위의 항아리 조각 하나, 이제는 그녀의 무게'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep057-p{page_number}-notext.png'
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
