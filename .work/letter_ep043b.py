from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-043-erewhon'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'d': [('해그스:', '지도의 이 백지장 — 저 너머에 뭐가 있는지, 제 눈으로 봐야겠어')]},
        {'d': [('차우복:', '저 고개는 신들의 땅이오. 발을 들이면 돌아올 수 없소')]},
        {},
        {'n': '백지였던 지도 위에 — 강 하나가, 지금 막 그려졌다'},
        {'d': [('해그스:', '환영인지 경고인지... 조각상들은 대답이 없고')]},
        {'d': [('청년:', '하늘에서 떨어진 이방인이군! 이름이 뭐요?')]},
    ],
    [
        {'d': [('노부인:', '쉿 — 이 은행의 이자는 음악이에요'), ('행인:', '그 동전으로 빵을 살 수 있나, 정말?')]},
        {'d': [('판사:', '밤마다 이웃을 괴롭힌 기침 — 죄를 인정하시오'), ('피고:', '기침이... 죄라고요?')]},
        {'d': [('간호사:', '도둑질은 병이에요. 부끄러워 말고 쉬세요'), ('환자:', '거울을 훔친 게... 아픈 거라고?')]},
        {'d': [('아로웨나:', '당신의 나라에도, 강이 있나요?'), ('해그스:', '강도, 바다도, 바다 위의 배들도')]},
        {'d': [('노현자:', '삼백 년 전, 우린 기계를 내쫓았다. 놈들은 진화해서 언젠가 주인이 될 터였으니')]},
        {'n': '웃기는 옛날이야기 — 인데, 왜 이렇게 가슴이 불편할까'},
    ],
    [
        {'d': [('해그스:', '금지된 유물관에 낡은 기구가 있어 — 나와 함께 날아줄래?'), ('아로웨나:', '들키면, 다신 못 만나는 벌이에요')]},
        {'d': [('해그스:', '삼백 년 만에 다시 숨을 쉬어라, 바람아')]},
        {'d': [('추격자:', '멈춰요! 하늘은 신들의 것!')]},
        {'d': [('아로웨나:', '무서워요...'), ('해그스:', '나도. 근데 이제 집이 둘 — 하나는 저 하늘에')]},
        {'n': '눈 덮인 산맥 너머 — 두 세계 사이의 첫 새벽'},
        {'n': '런던의 연단, 펼쳐진 지도 — 그 위에 아직, 백지인 산맥'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep043b-p{page_number}-notext.png'
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
