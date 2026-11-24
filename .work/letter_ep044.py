from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-044-edisons-conquest-of-mars'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'d': [('노인:', '화성인들은 반드시 돌아옵니다'), ('소년:', '그럼 우리는 어쩌죠?')]},
        {'d': [('에디슨:', '전기 반발력 — 중력을 밀어내는 힘이야!')]},
        {'d': [('빅토리아 여왕:', '하늘의 적은 하나'), ('매킨리 대통령:', '그렇다면 손도 하나로')]},
        {'n': '만국의 조선소 — 수백 척의 꿈이 동시에 철을 입는다'},
        {'d': [('에디슨:', '공기 없는 길도 간다 — 완전 기밀복이야!')]},
        {},
    ],
    [
        {'d': [('에디슨:', '전 함대 항로 유지 — 목표는 화성')]},
        {'d': [('관측수:', '순금 소행성… 저 채굴탑은!'), ('에디슨:', '화성인의 광산이군')]},
        {'d': [('포술수:', '번개 병기가 옵니다!'), ('에디슨:', '분해 광선, 쏴라!')]},
        {'d': [('통역:', '말이 통합니다 — 이 포로가 가르쳐 줬어요'), ('화성인 포로:', '지구 놈들, 감히…')]},
        {'n': '붉은 행성 전체가 연막에 잠기고 — 하늘을 뒤덮은 화성 함대'},
        {'d': [('에디슨:', '수가 너무 많다… 전 함대, 데모스로!')]},
    ],
    [
        {'d': [('승무원:', '사람이 있어! 감옥의…'), ('아이나:', '9천 년 만의, 지구 목소리')]},
        {'d': [('아이나:', '우리 조상은 카슈미르에서 끌려왔어요 — 피라미드도 놈들의 작품이죠')]},
        {'d': [('아이나:', '맞서지 마세요 — 부술 곳은 극관의 댐'), ('에디슨:', '물길이 끊기면, 도시는…')]},
        {'n': '댐이 열리고 하늘빛 물이 계곡으로 — 아홉 천 년 제국의 마지막 밤'},
        {'d': [('에디슨:', '더는 피 안 흘린다 — 악수다'), ('화성 지도자:', '무서운 지구인들이여')]},
        {'n': '꽃비 내리는 개선 — 망원경 너머, 아직 붉게 빛나는 저 점'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep044-p{page_number}-notext.png'
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
