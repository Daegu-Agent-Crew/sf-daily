# -*- coding: utf-8 -*-
import io
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-066-the-red-one'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'page-03.png': (1024, 1536), 'scroll.png': (1024, 4608)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print('OK %s | %s bytes | %dx%d' % (name, format(p.stat().st_size, ','), size[0], size[1]))

readme_line = "- #066 2026-11-25: 잭 런던 「붉은 것」(The Red One, 1918) — 병든 과학자 바셋이 과달카날 밀림에서 만난 '별에서 태어난 것'과 우주의 노래, 우주적 경외 SF의 선구적 걸작(1916년 호놀룰루 집필) · 06:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-066" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README updated")

ep_div = "<div class=\"ep\"><div class=\"no\">#066 · 2026-11-25</div><div class=\"t\">잭 런던 「붉은 것」(The Red One, 1918)</div><div class=\"cap\">과달카날의 밀림을 가르는 한 시간짜리 소리 — 열병에 야윈 박물학자 바셋은 들것에 실려 그 근원을 찾아가, 웅덩이에 박힌 지름 200피트의 붉은 구체를 만난다. 원주민은 '별에서 태어난 것'이라 불렀고, 손끝이 닿자 살아 움직이는 그 금속은 별들 사이를 건너온 우주의 편지였다. 죽음을 앞둔 바셋은 늙은 주술의 응른과 약속한다 — 마지막에 그 노래를 들려다오, 그러면 내 머리는 네 것이다. 빵나무 그늘의, 느긋한 연기와 붉은 노래. 잭 런던이 1916년 호놀룰루에서 쓰고 2년 뒤 출간한 우주적 경외(cosmic awe)의 고전</div><img loading=\"lazy\" src=\"episodes/sf-daily-066-the-red-one/scroll.png\"></div>"

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-066" not in html:
    marker = '<div class="meta">삼체 연재와 별개 시스템 · 1일 12화 2시간 주기 · codex 생성 · 원작 충실 다중 페이지</div>' + NL
    idx = html.find(marker)
    assert idx >= 0, "index marker not found"
    idx += len(marker)
    html = html[:idx] + ep_div + NL + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated")
print("PUB066 DONE")
