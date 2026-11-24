from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-029-the-lost-world'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '1912년, 런던의 저녁 — 학회 강당의 평화는 그날로 끝났다'},
        {'d': [('찰린저:', '남미 정글 한가운데, 공룡이 사는 고원이 있다. 내 두 눈으로 봤다!'), ('청중:', '사기꾼! 사진이나 보여주시지!')]},
        {'d': [('찰린저:', '이 스케치의 날개 폭은 백조가 아니다. 정체를 알고 싶으면 — 직접 가 보게.'), ('말론:', '저를 데려가 주십시오. 기사가 아니라 — 눈으로 보고 싶습니다.')]},
        {'d': [('록스턴 경:', '아마존이라면 내 정원이지. 총과 경험, 둘 다 가져가겠네.'), ('서머리:', '흥, 다녀와서 사과를 받아주지. 없는 고원을 찾는 놀음이지만.')]},
        {'n': '안개 저편, 분홍빛 절벽 위 — 잃어버린 세계'},
        {'d': [('찰린저:', '저 위에 있다! 보라 — 내 말이 틀렸나?')]},
    ],
    [
        {'d': [('고메즈:', '이 다리는 — 없던 걸로 하시지! 우리 형을 잡은 게 누구더라!'), ('록스턴 경:', '배신자! 도끼를 내려놔, 고메즈!')]},
        {'n': '내려갈 길은, 이제 없다 — 저 위가 우리의 전부'},
        {},
        {'d': [('말론:', '이구아노돈이다, 초식! 공룡이 아직… 살아서 숨 쉬고 있어!'), ('서머리:', '찰린저, 사과하네. 근데 — 발소리가 왜 이렇게 크지?')]},
        {'d': [('록스턴 경:', '알로사우루스! 바위 뒤로, 전원! 총은 — 아직 아니야!')]},
        {'n': '능선 위, 원숭이인간들 — 창끝보다 조용한 눈들'},
    ],
    [
        {'d': [('록스턴 경:', '동굴이다! 강가로 나가는 길 — 마지막 승부다, 젊은이들!')]},
        {'d': [('서머리:', '덮개 밖에서 숨소리가 들리는군. 대체 뭐를 데려온 거지?')]},
        {'d': [('찰린저:', '신사 여러분, 남미에서 돌아왔습니다. 증거는 — 이 상자 안에 있습니다.')]},
        {'d': [('청중:', '열어보시오! 설마 비둘기 새끼는 아니겠지?')]},
        {'d': [('서머리:', '익룡이다…! 프테라노돈! 저것 봐, 살아 있다고 — 전부!')]},
        {'n': '빈 상자 하나 — 창밖 하늘로, 아직도 열려 있는 문'},
    ],
]





def letter_page(page_number, captions):
    src = root / f'.work/ep029-p{page_number}-notext.png'
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
