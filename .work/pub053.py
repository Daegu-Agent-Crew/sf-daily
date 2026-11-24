# -*- coding: utf-8 -*-
import io, sys
NL = chr(10)
readme_line = "- #053 2026-11-22: 표도르 도스토옙스키 「괴팍한 자의 꿈」(Dream of a Ridiculous Man, 1877) — 낙원을 잃고서야 사람을 믿게 된 어릿광두의 꿈, 환상 SF의 고전 · 22:30 실행분 이미지 완성 후 발행 중단, 11-23 00:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-053" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README: appended #053")
else:
    print("README: #053 already present")

entry = '<div class="ep"><div class="no">#053 · 2026-11-22</div><div class="t">표도르 도스토옙스키 「괴팍한 자의 꿈」(Dream of a Ridiculous Man, 1877)</div><div class="cap">죽기로 작정한 밤, 골목 소녀의 매달린 손을 뿌리친 채 잠든 어릿광두 — 꿈속 총성 너머에서 깨어난 곳은 상처 하나 없는 지구, 슬픔이 자라난 적 없는 낙원이었다. 장난처럼 가르친 거짓 한 조각이 낙원에 눈물을 심고, 사람들은 다시 별을 향해 걷는다 — 눈을 뜬 아침의 첫마디, 오늘은 태양이 뜨는 날</div><img loading="lazy" src="episodes/sf-daily-053-dream-of-a-ridiculous-man/scroll.png"></div>' + NL

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-053-dream-of-a-ridiculous-man" not in html:
    marker = '<div class="ep">'
    idx = html.find(marker)
    if idx == -1:
        sys.exit("index.html: marker not found")
    html = html[:idx] + entry + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html: inserted #053 at top")
else:
    print("index.html: #053 already present")
