from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-047-herland'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'d': [('터리:', '여자만 산다는 나라라니, 웃기지 마'), ('반:', '가이드가 남긴 지도가 이 협곡에서 끝나')]},
        {'d': [('제프:', '이 고원 너머엔, 아무도 돌아온 적이 없어')]},
        {'d': [('터리:', '그러니까 가야지 — 우리가 처음 밟는, 신대륙')]},
        {'d': [('반:', '숲이 아니네… 정원이야. 가지런히 심은 과일나무들')]},
        {'d': [('제프:', '저 샌들… 아이 것이라고. 이 정원에, 아이들이 살아')]},
        {},
    ],
    [
        {'d': [('터리:', '이봐, 우리는 신사라고! 신—사!'), ('소멜:', '그러니까 다친 새처럼, 조심스럽게 모시는 중이에요')]},
        {'d': [('반:', '감옥이네… 아니, 투숙객이잖아. 과일이 산더미야')]},
        {'d': [('소멜:', '2천 년 전, 이곳에도 남자들이 살았어요 — 큰 폭풍이 그들을 데려갔죠')]},
        {'n': '마지막에 남은 것은, 어머니들이었다'},
        {'d': [('제프:', '저들에겐 모든 아이가, 모두의 아이야')]},
        {'d': [('엘라도:', '당신들의 세계는요 — 아이들이, 행복한가요?')]},
    ],
    [
        {'n': '꽃가루 아래, 세 쌍의 약속'},
        {'d': [('알리마:', '남편이 되기 전에, 친구부터'), ('터리:', '내 아내라고 했잖아!')]},
        {'d': [('모아딘:', '터리 씨는 돌아가 주셔야 해요 — 문은 언제나 열려 있고요')]},
        {'d': [('제프:', '난 셀리스와 여기 남을래'), ('엘라도:', '나는 당신들의 세계가 보고 싶어요')]},
        {'d': [('반:', '우리 세계가, 저들을 실망시키지 않기를')]},
        {'n': '두 세계를 잇는, 새벽의 날개'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep047-p{page_number}-notext.png'
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
