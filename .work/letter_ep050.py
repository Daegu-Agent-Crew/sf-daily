from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-050-off-on-a-comet'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '188x년 새해 첫날 밤 — 별이 쏟아지는 알제리 해안, 세르바다크 대위와 뱅 주프의 모닥불'},
        {'d': [('뱅 주프:', '지진입니다, 대위님! 하늘이 저렇게 밝은데…'), ('세르바다크:', '바다가 물러간다 — 나무를 붙잡아!')]},
        {'d': [('세르바다크:', '해가 서쪽에서 떴어 — 동과 서가 바뀌었다'), ('뱅 주프:', '그럼 밤하늘의 저 파란 별은… 지구란 말입니까')]},
        {'d': [('뱅 주프:', '어머나, 열두 미터를 뛰었잖아요!'), ('세르바다크:', '물이 예순여섯 도에 끓는 것도 그 때문이야')]},
        {'n': '돌 하나가 닿자 바다가 한순간에 얼어붙는다 — 갈리아의 신비한 바다'},
        {},
    ],
    [
        {'d': [('티마셰프 백작:', '얼음 바다 너머를 봐야겠네 — 도브리나 호, 출항이다')]},
        {'d': [('로제트:', '이보게들! 나를 포르멘테라에서 데려가 주게 — 1년째 갇혀 있다네')]},
        {'d': [('로제트:', '우리가 밟는 이 땅은 내가 발견한 혜성 갈리아 — 지구를 스치며 떼어 낸 조각일세'), ('프로코프:', '그럼 우리는 지금, 우주를 항해하고 있는 겁니까')]},
        {'d': [('로제트:', '은화 마흔 닢이면 혜성의 무게를 잴 수 있네'), ('이삭:', '내 저울엔 손대지 마시오')]},
        {'n': '절벽에 지은 동굴집 니나의 벌집 — 얼음 밭의 썰매와 스케이트, 염소와 비둘기와 함께 보내는 2년'},
        {},
    ],
    [
        {'d': [('프로코프:', '갈리아의 한 조각이 떨어져 나갔습니다 — 1월 1일이 오기 전에 떠나야 합니다')]},
        {'d': [('티마셰프 백작:', '돛으로 풍선을 지어, 두 세계의 대기가 닿는 순간 건너가세'), ('니나:', '비둘기도 데려갈 거예요')]},
        {'d': [('로제트:', '가게들 — 갈리아는 내 혜성이니, 난 끝까지 남겠네')]},
        {'n': '1월 1일 — 두 하늘이 스치는 순간, 돛으로 지은 풍선이 갈리아의 밤을 떠난다'},
        {'d': [('뱅 주프:', '알제리다! 모스타가넴 언덕 위 — 무사히 돌아왔습니다!'), ('니나:', '날아라 — 우리 집이야')]},
        {},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep050-p{page_number}-notext.png'
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
