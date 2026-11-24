from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-060-journey-in-other-worlds'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '1894년, 재벌 애스터가 그린 서기 2000년', 'd': [('베어워든:', '극지의 얼음마저 온실이 됐지. 이제 갈 곳은 저 하늘뿐이야')]},
        {'d': [('베어워든:', '아퍼지 — 중력을 밀어내는 힘이야. 연료 따윈 필요 없어')]},
        {'d': [('코틀랜드트:', '인류 최초의 행성 여행이군'), ('에이롤트:', '아니요, 행성 밖 최초의 여행이죠')]},
        {},
        {'d': [('에이롤트:', '망원경 속에서 목성이 자라고 있어요'), ('코틀랜드트:', '산호빛 폭풍의 행성이지')]},
        {'n': '그리고 정글 하나가, 행성 전체를 덮은 채 기다리고 있었다'},
    ],
    [
        {'n': '목성 착륙 — 모든 것이 지구의 몇 곱절', 'd': [('베어워든:', '장미가 저택보다 크잖아!')]},
        {'d': [('에이롤트:', '저 친구, 인사를 하는 건가?'), ('코틀랜드트:', '초식이니 우리가 점심은 안 되겠군')]},
        {'d': [('베어워든:', '움직이지 마! 전기 그물 — 발사!')]},
        {},
        {'d': [('코틀랜드트:', '반발력 돔이 포식자를 그냥 튕겨내 버렸네'), ('베어워든:', '우리선을 간식으로 아는 모양이야, 글쎄')]},
        {'d': [('에이롤트:', '토성 고리 앞이에요. 그런데 이 상자로… 죽은 이들과 대화가 된다니요'), ('코틀랜드트:', '황당한 소리지만, 해 보고 말자고')]},
    ],
    [
        {'n': '토성의 은빛 바다 — 고리 아래의 첫 밤'},
        {'d': [('에이롤트:', '손을 잡으세요. 수정 구슬이 반응하기 시작해요')]},
        {'d': [('베어워든:', '저길 봐 — 빛이 하늘로 올라간다!')]},
        {'d': [('에이롤트:', '…꽃밭이에요. 고리를 등에 진 사람들이 웃고 있어요'), ('코틀랜드트:', '죽음이 이렇게 따뜻하다니')]},
        {},
        {'n': '여행기의 주인공들은 무사히 집으로 돌아왔다 — 그러나 그것을 쓴 애스터는, 18년 뒤 진짜 바다에서. 그리고, 대서양의 새벽빛'},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep060-p{page_number}-notext.png'
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
for output in outputs:
    print(f'{output.relative_to(root)} | {output.stat().st_size}')