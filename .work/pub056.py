# -*- coding: utf-8 -*-
import io, sys
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-056-the-coming-race'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'scroll.png': (1024, 3088)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print(f'OK {name} | {p.stat().st_size:,} bytes | {size[0]}x{size[1]}')

readme_line = "- #056 2026-11-23: 에드워드 불워리턴 「다가오는 종족」(The Coming Race, 1871) — '브릴' 에너지와 지하 문명 브릴야의 시조 소설 · 08:30 실행분 이미지 완성 후 발행 중단, 10:30 실행분 2페이지 완성 후 발행 중단, 12:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-056" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README: appended #056")
else:
    print("README: #056 already present")

entry = "<div class=\"ep\"><div class=\"no\">#056 · 2026-11-23</div><div class=\"t\">에드워드 불워리턴 「다가오는 종족」(The Coming Race, 1871)</div><div class=\"cap\">1871년 황혼의 폐광 — 밑바닥에서 새어 올라오던 청록 빛에 이끌려 사다리를 내려가다, 디디개가 부러진다. 떨어진 곳은 태양 없는 궁창 아래 지하 세계 — 등에 새하얀 날개를 단 아이 타에, 은빛 지팡이 하나로 바위를 녹이고 병을 고치는 브릴의 민족. 돈도 문도 감옥도 없는 수정 마을에서 청년은 낯선 낙원을 배우고, 학자 지는 금지된 마음을 안은 채 인공 날개를 채워 그를 지상으로 올려 보낸다 — 새벽 풀밭에 홀로 남은 청년, 땅 밑 어딘가에서 아직 오지 않은 날갯소리</div><img loading=\"lazy\" src=\"episodes/sf-daily-056-the-coming-race/scroll.png\"></div>" + NL

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-056-the-coming-race" not in html:
    marker = '<div class="ep">'
    idx = html.find(marker)
    if idx == -1:
        sys.exit("index.html: marker not found")
    html = html[:idx] + entry + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html: inserted #056 at top")
else:
    print("index.html: #056 already present")