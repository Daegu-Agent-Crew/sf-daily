# -*- coding: utf-8 -*-
import io, sys
NL = chr(10)
readme_line = "- #050 2026-11-22: 쥘 베른 「혹성 여행 — 헥토르 세르바다크」(Off on a Comet, 1877) — 새해 첫날 밤 땅 통째로 혜성에 실려 태양계를 일주 · 16:30 실행분 이미지 완성 후 발행 중단, 18:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "#050" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README: appended #050")
else:
    print("README: #050 already present")

entry = '<div class="ep"><div class="no">#050 · 2026-11-22</div><div class="t">쥘 베른 「혹성 여행 — 헥토르 세르바다크」(Off on a Comet, 1877)</div><div class="cap">새해 첫날 밤 하늘이 갈라지고, 땅 덩어리 통째로 혜성 갈리아에 실렸다 — 서쪽에서 뜨는 해, 12미터를 가볍게 오르는 아침, 66도에 끓는 물. 은화 마흔 닢으로 잰 하늘의 무게, 동굴집 "니나의 벌집"의 두 겨울, 돛천 풍선 한 장으로 건너온 푸른 지구 — 밤하늘에는 아직, 은빛 꼬리</div><img loading="lazy" src="episodes/sf-daily-050-off-on-a-comet/scroll.png"></div>' + NL

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-050-off-on-a-comet" not in html:
    marker = '<div class="ep">'
    idx = html.find(marker)
    if idx == -1:
        sys.exit("index.html: marker not found")
    html = html[:idx] + entry + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html: inserted #050 at top")
else:
    print("index.html: #050 already present")