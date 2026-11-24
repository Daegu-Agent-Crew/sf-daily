from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-027-dr-jekyll-and-mr-hyde'
destination.mkdir(parents=True, exist_ok=True)

pages = [
    [
        {'n': '런던, 정원 뒤 골목 — 이 문이, 이야기의 뒷면을 열어 준다.'},
        {'d': [('어터슨:', '잠깐 봅시다. 얼굴을 볼 수 있겠소?'), ('하이드:', '이 정도면 됐나? 무례하시군, 신사님.')]},
        {'d': [('지킬:', '유서를 남겼네 — 재산 전부를, 하이드라는 남자에게.'), ('어터슨:', '그자가 대체 누구기에?')]},
        {'d': [('지킬:', '내가 자리를 비운 동안… 그가 내 집을 지키게.')]},
        {'d': [('지킬:', '자유를 향한 약 — 이백 년의 억압에서, 단 한 모금.')]},
        {'n': '낮의 신사가 잠든 사이 — 밤의 신사, 눈을 뜬다.'},
    ],
    [
        {'d': [('행인:', '아이를 치고 그냥 가는군! 이 사람!'), ('하이드:', '비켜라. 시끄럽다.')]},
        {'d': [('지킬:', '끝났네, 하이드는 떠났어. 잘됐어, 아주 잘됐다는 걸세.')]},
        {},
        {'d': [('어터슨:', '이 지팡이는… 내가 지킬에게 준 그것인데.')]},
        {'d': [('지킬:', '그를 볼 수가 없어. 떠올리기만 해도… 이 치욕을.'), ('어터슨:', '숨기고 있는 건가, 그자를?')]},
        {'n': '봉인된 편지, 잠긴 문 — 그리고 소문만 무성한, 지킬 박사.'},
    ],
    [
        {'d': [('하이드:', '가져왔습니다, 의사님. 이 서류와… 이 약을.')]},
        {'d': [('하이드:', '보고 싶지 않으시면, 눈을 감으시오.'), ('랜년:', '미쳤군, 서두르게.')]},
        {'d': [('랜년:', '그 순간을 본 뒤로, 내 인생은 끝났네. 그 하룻밤에, 전부.')]},
        {'d': [('푸울:', '안에서 온종일 우는 소리가! 저건 우리 주인님이 아니에요!')]},
        {'n': '실험실 바닥 — 움직이지 않는 하이드, 곁엔 빈 약병 하나.'},
        {'n': '낮의 얼굴, 밤의 얼굴 — 한 약병 안의, 두 인생.'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep027-p{page_number}-notext.png'
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
