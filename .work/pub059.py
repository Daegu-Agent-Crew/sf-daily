# -*- coding: utf-8 -*-
import io, sys
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-059-professor-dowells-head'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'page-03.png': (1024, 1536), 'scroll.png': (1024, 4608)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print('OK %s | %s bytes | %dx%d' % (name, format(p.stat().st_size, ','), size[0], size[1]))

readme_line = "- #059 2026-11-24: 알렉산드르 벨랴예프 「도웰 교수의 머리」(Голова профессора Доуэля, 1925) — 영양액 속에 살아 남은 머리의 고백, 소련 SF 개척자의 대표작 · 04:30 실행분 1페이지·06:30 실행분 2페이지 완성 후 발행 중단, 08:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-059" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README updated")

ep_div = '<div class="ep"><div class="no">#059 · 2026-11-24</div><div class="t">알렉산드르 벨랴예프 「도움 교수의 머리」(Голова профессора Доуэля, 1925)</div><div class="cap">1925년 여름 아침, 담쟁이 넝쿨 저택 연구소의 취직 조건은 단 하나 — 묻지 않는 것. 커튼 너머 받아쓰기 목소리의 주인은 하늘색 영양액 속에 살아 있는 도웰 교수의 머리였다. 병상의 마지막 당부를 손에 쥔 조수 케른은 논문마다 제 이름을 올리고, 옆 배양조의 늙은 개처럼 머리는 말 없이 지워져 간다. 밤마다 돔 곁에 의자를 붙이는 마리, 서랍 세 번째의 낡은 노트 — 학회 객석 위로 치켜든 진짜 저자의 증거 앞에서 훈장의 빛이 흔들리고. 다음 날 아침 유리 돔 속의 긴 잠, 정원의 빈 의자를 지나가는 바람</div><img loading="lazy" src="episodes/sf-daily-059-professor-dowells-head/scroll.png"></div>'

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-059" not in html:
    marker = '<div class="meta">삼체 연재와 별개 시스템 · 1일 12화 2시간 주기 · codex 생성 · 원작 충실 다중 페이지</div>' + NL
    idx = html.find(marker)
    assert idx >= 0, "index marker not found"
    idx += len(marker)
    html = html[:idx] + ep_div + NL + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated")
print("PUB059 DONE")
