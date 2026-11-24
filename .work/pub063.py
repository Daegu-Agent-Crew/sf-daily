# -*- coding: utf-8 -*-
import io
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-063-the-comet'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'scroll.png': (1024, 3072)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print('OK %s | %s bytes | %dx%d' % (name, format(p.stat().st_size, ','), size[0], size[1]))

readme_line = "- #063 2026-11-24: W.E.B. 듀보이스 「혜성」(The Comet, 1920) — 최초의 흑인 SF 작가가 남긴 종말 단편, 혜성 꼬리가 지나간 정오의 뉴욕에서 지하 금고와 암실에 남은 두 사람 · 22:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-063" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README updated")

ep_div = '<div class="ep"><div class="no">#063 · 2026-11-24</div><div class="t">W.E.B. 듀보이스 「혜성」(The Comet, 1920)</div><div class="cap">새 혜성의 꼬리가 정오에 스친다는 날, 흑인 은행 심부름꾼 짐은 제일 밑바닥 금고로 내려가라는 지시를 받는다 — 위험한 자리엔 제일 값싼 사람이 내려간다. 돌문이 닫히고, 지상의 세계는 조용해진다. 잠들어 버린 뉴욕을 홀로 걷던 짐은 암실에서 사진을 현상하던 줄리아를 만나고, 두 사람은 텅 빈 도시를 함께 헤맨다. 밤의 타워 옥상, 창백한 불꽃 장막 아래에서 "세계는 죽었다"고 속삭이던 두 사람 앞으로 — 클랙슨 소리와 함께 도시의 불이 하나둘 깨어난다. 최초의 아프리카계 미국 SF로 꼽히는 단편</div><img loading="lazy" src="episodes/sf-daily-063-the-comet/scroll.png"></div>'

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-063" not in html:
    marker = '<div class="meta">삼체 연재와 별개 시스템 · 1일 12화 2시간 주기 · codex 생성 · 원작 충실 다중 페이지</div>' + NL
    idx = html.find(marker)
    assert idx >= 0, "index marker not found"
    idx += len(marker)
    html = html[:idx] + ep_div + NL + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated")
print("PUB063 DONE")
