# -*- coding: utf-8 -*-
import io, sys
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-057-she'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'scroll.png': (1024, 3088)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print(f'OK {name} | {p.stat().st_size:,} bytes | {size[0]}x{size[1]}')

readme_line = "- #057 2026-11-23: 헨리 라이더 해거드 「그녀」(She: A History of Adventure, 1887) — 이천 년을 산 불멸의 여왕 아예샤, 불의 기둥 앞에서 시들다 · 14:30 실행분 1페이지 완성 후 발행 중단, 18:30 실행분 2페이지 완성 후 발행 중단, 20:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-057" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README: appended #057")
else:
    print("README: #057 already present")

entry = "<div class=\"ep\"><div class=\"no\">#057 · 2026-11-23</div><div class=\"t\">헨리 라이더 해거드 「그녀」(She: A History of Adventure, 1887)</div><div class=\"cap\">1885년 케임브리지의 밤, 유언처럼 남겨진 깨진 항아리 조각 — 어깨에 뱀 문양 흉터를 지닌 레오와 학자 홀리, 집사 잡은 폭풍의 아프리카 동해안을 지나 늪 위에 앉은 죽은 도시 코르에 닿는다. 석관 통로 끝의 흰 빛, 이천 년을 산 여왕 아예샤 — 베일 아래의 얼굴은 죽은 연인 킬리크라테스의 환생을 알아보고, 영원을 걸고 불의 기둥을 내민다. 먼저 걸어 들어간 그녀의 몸으로 이천 년의 시간이 한꺼번에 밀려오고 — 새벽 안개 속을 걸어 나오는 두 사람, 손바닥 위의 항아리 조각 하나, 이제는 그녀의 무게</div><img loading=\"lazy\" src=\"episodes/sf-daily-057-she/scroll.png\"></div>" + NL

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-057-she" not in html:
    marker = '<div class="ep">'
    idx = html.find(marker)
    if idx == -1:
        sys.exit("index.html: marker not found")
    html = html[:idx] + entry + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html: inserted #057 at top")
else:
    print("index.html: #057 already present")
