# -*- coding: utf-8 -*-
import io, sys
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-055-the-future-eve'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'scroll.png': (1024, 3088)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print(f'OK {name} | {p.stat().st_size:,} bytes | {size[0]}x{size[1]}')

readme_line = "- #055 2026-11-23: 비리에 드 리라다당 「미래의 이브」(L'Ève future, 1886) — '안드로이드'라는 단어가 태어난 소설, 에디슨이 완벽한 사랑을 설계하다 — 04:30 실행분 이미지 완성 후 발행 중단, 06:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-055" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README: appended #055")
else:
    print("README: #055 already present")

entry = "<div class=\"ep\"><div class=\"no\">#055 · 2026-11-23</div><div class=\"t\">비리에 드 리라다당 「미래의 이브」(L'Ève future, 1886)</div><div class=\"cap\">1886년 눈 내리는 멘로파크, 은둔한 에디슨의 성채에 절망한 귀족 에월드가 찾아온다 — 사랑하는 여배우 알리샤는 얼굴도 목소리도 완벽한데 속이 텅 비어 있었다. 에디슨의 대답은 간단하다, 그럼 속만 바꾸지요. 알리샤와 똑같은 몸에 가슴 속 축음기 두 대를 박은 인조인간 하달리, '이상(理想)'이라는 이름으로. 대서양의 불꽃 속으로 사라진 이상과, 멀리 런던에서 이유 모를 눈물을 흘리는 진짜 알리샤 — 나의 절반이, 바다에 남아 온 것 같아</div><img loading=\"lazy\" src=\"episodes/sf-daily-055-the-future-eve/scroll.png\"></div>" + NL

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-055-the-future-eve" not in html:
    marker = '<div class="ep">'
    idx = html.find(marker)
    if idx == -1:
        sys.exit("index.html: marker not found")
    html = html[:idx] + entry + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html: inserted #055 at top")
else:
    print("index.html: #055 already present")