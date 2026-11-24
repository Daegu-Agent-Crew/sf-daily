from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent.parent
destination = root / 'episodes/sf-daily-059-professor-dowells-head'
destination.mkdir(parents=True, exist_ok=True)


pages = [
    [
        {'n': '1925년 여름 아침 — 담쟁이 저택 연구소의 채용 조건은 단 하나', 'd': [('케른:', '묻지 마시오, 로랑 의사. 그게 유일한 규칙이오')]},
        {'d': [('커튼 너머:', '…비트 넷에 혈청 세 방울… 서두르게…'), ('마리:', '저 목소리… 커튼 뒤에 누가 있죠?')]},
        {'n': '커튼이 걷히고 — 하늘빛 액체 속에서 마주 보던 것은', 'd': [('도웰:', '놀라지 말게, 의사 양반. 난 도웰이라 하네')]},
        {'d': [('마리:', '머리만… 이렇게 혼자 사 년을요?'), ('도웰:', '죽음이 나를 잊고 간 모양일세')]},
        {},
        {'n': '다음 날 아침', 'd': [('케른:', '학보 1면이야! 이 논문이 세계를 바꾸겠군!')]},
    ],
    [
        {'n': '돌아가기 직전, 노교수가 내민 손', 'd': [('도웰:', '케른… 내 연구를, 부탁하네…')]},
        {'d': [('케른:', '잘 돌아오셨군, 교수님. 당신은 이제 죽지 않소')]},
        {'n': '옆 배양조의 늙은 개도 온순한 눈으로 — 실험은 시작에 불과했고'},
        {'d': [('케른:', '논문은 내 이름으로 나가겠소. 문제 있소?')]},
        {'d': [('마리:', '오늘 밤엔 바람이 좋네요, 교수님'), ('도웰:', '그래… 그런 이야기가 듣고 싶었네')]},
        {'d': [('도웰(속삭임):', '…서랍 세 번째 칸에, 내 진짜 기록이 있네')]},
    ],
    [
        {'n': '낡은 장정 속 도표와 도면 — 진짜 저자의 손때가 남아', 'd': [('마리:', '전부… 교수님의 손글씨예요')]},
        {'d': [('케른:', '여러분! 이 발견이 인류를—'), ('마리:', '이 논문의 주인이 따로 있습니다!')]},
        {'n': '손에서 손으로 전해지는 노트, 새하얘지는 단상', 'd': [('객석:', '사기다! 서명을 확인해라!')]},
        {'d': [('마리:', '다 끝났어요, 교수님'), ('도웰:', '고맙네… 참, 나른하군…')]},
        {'n': '다음 날 아침 — 햇살 속의 긴 잠'},
        {},
    ],
]


def letter_page(page_number, captions):
    src = root / f'.work/ep059-p{page_number}-notext.png'
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
