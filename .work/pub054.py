# -*- coding: utf-8 -*-
import io, sys
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-054-the-man-in-the-moone'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'scroll.png': (1024, 3088)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print(f'OK {name} | {p.stat().st_size:,} bytes | {size[0]}x{size[1]}')

readme_line = "- #054 2026-11-23: 프랜시스 갓윈 「달의 인간」(The Man in the Moone, 1638) — 영어로 쓰인 최초의 SF 소설, 새가 멘 나무 엔진의 12일 달 항로 · 00:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-054" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README: appended #054")
else:
    print("README: #054 already present")

entry = '<div class="ep"><div class="no">#054 · 2026-11-23</div><div class="t">프랜시스 갓윈 「달의 인간」(The Man in the Moone, 1638)</div><div class="cap">결투로 고향을 등진 스페인 신사 곤살레스가 세인트헬레나 섬에서 길들인 것은 백조 같은 새 가사스 떼 — 나무 틀 엔진에 면 새들이 포화를 피해 오르더니, 12일 만에 달에 닿는다. 노래로 말하는 키 큰 루나인의 낙원, 왕이 건넨 세 개의 돌 — 몸을 깃털처럼 가볍게 하는 돌을 품고 아홉 날을 접어 중국 해안에 내린 아침. 달에서 온 세 돌과, 아직 고향으로 못 돌아간 한 사람</div><img loading="lazy" src="episodes/sf-daily-054-the-man-in-the-moone/scroll.png"></div>' + NL

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-054-the-man-in-the-moone" not in html:
    marker = '<div class="ep">'
    idx = html.find(marker)
    if idx == -1:
        sys.exit("index.html: marker not found")
    html = html[:idx] + entry + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html: inserted #054 at top")
else:
    print("index.html: #054 already present")
