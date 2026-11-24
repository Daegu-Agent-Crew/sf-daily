# -*- coding: utf-8 -*-
import io
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-060-journey-in-other-worlds'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'page-03.png': (1024, 1536), 'scroll.png': (1024, 4608)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print('OK %s | %s bytes | %dx%d' % (name, format(p.stat().st_size, ','), size[0], size[1]))

readme_line = "- #060 2026-11-24: 존 제이컵 애스터 「다른 세계 여행」(A Journey in Other Worlds, 1894) — 타이타닉으로 사라진 재벌 작가가 1894년에 그린 서기 2000년, 목성 사파리와 토성의 강령 실험 · 10:30 실행분 생성, 12:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-060" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README updated")

ep_div = '<div class="ep"><div class="no">#060 · 2026-11-24</div><div class="t">존 제이컵 애스터 「다른 세계 여행」(A Journey in Other Worlds, 1894)</div><div class="cap">1894년 재벌 애스터가 상상한 서기 2000년 — 반발력 우주선 카리스토호는 온실 지구를 떠나 저택보다 큰 장미가 핀 목성 정글과 은빛 고리의 토성 바다를 지나, 강령 상자가 열린 밤 죽은 이들의 정원을 만난다. 주인공들은 무사히 집으로 돌아왔지만, 이 여행기를 쓴 사람은 18년 뒤 진짜 대서양에서 사라진다</div><img loading="lazy" src="episodes/sf-daily-060-journey-in-other-worlds/scroll.png"></div>'

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-060" not in html:
    marker = '<div class="meta">삼체 연재와 별개 시스템 · 1일 12화 2시간 주기 · codex 생성 · 원작 충실 다중 페이지</div>' + NL
    idx = html.find(marker)
    assert idx >= 0, "index marker not found"
    idx += len(marker)
    html = html[:idx] + ep_div + NL + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated")
print("PUB060 DONE")