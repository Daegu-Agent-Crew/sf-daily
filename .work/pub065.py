# -*- coding: utf-8 -*-
import io
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-065-the-world-set-free'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'page-03.png': (1024, 1536), 'scroll.png': (1024, 4608)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print('OK %s | %s bytes | %dx%d' % (name, format(p.stat().st_size, ','), size[0], size[1]))

readme_line = "- #065 2026-11-25: H.G. 웰스 「해방된 세계」(The World Set Free, 1914) — '멎지 않는 폭발' 카롤리늄 폭탄과 국경 없는 세계 공화국, 레오 실러드가 이 소설을 읽고 핵 연쇄 반응을 떠올리다 · 04:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-065" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README updated")

ep_div = "<div class=\"ep\"><div class=\"no\">#065 · 2026-11-25</div><div class=\"t\">H.G. 웰스 「해방된 세계」(The World Set Free, 1914)</div><div class=\"cap\">1933년의 다락방에서 젊은 화학자 홀스텐이 원자 속의 불씨를 연다 — 카롤리늄, 한 번 시작되면 열이레를 타오르는 '멎지 않는 폭발'. 1956년, 폭격기 편대가 도시들 위에 그 불을 떨어뜨리고, 살아남은 세계는 브리사고 호수의 섬에 모인다. 영국 왕이 먼저 왕관을 내려놓고, 세르비아 왕의 마지막 폭탄이 회의장을 노리지만 — 국경이 사라진 세계 공화국은 이미 시작되어 있었다. 일흔다섯 평의원 카레닌이 마지막 날에 남긴 말, 앎과 힘에는 절대의 한계가 없다. 20년 뒤 레오 실러드가 이 소설을 읽고 핵 연쇄 반응을 떠올린, 예언이 실제가 된 SF</div><img loading=\"lazy\" src=\"episodes/sf-daily-065-the-world-set-free/scroll.png\"></div>"

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-065" not in html:
    marker = '<div class="meta">삼체 연재와 별개 시스템 · 1일 12화 2시간 주기 · codex 생성 · 원작 충실 다중 페이지</div>' + NL
    idx = html.find(marker)
    assert idx >= 0, "index marker not found"
    idx += len(marker)
    html = html[:idx] + ep_div + NL + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated")
print("PUB065 DONE")