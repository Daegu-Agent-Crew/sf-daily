# -*- coding: utf-8 -*-
import io, sys
NL = chr(10)
readme_line = "- #052 2026-11-22: 너새니얼 호손 「라파치니의 딸」(Rappaccini's Daughter, 1844) — 광신 과학자 문학의 효시, 「프랑켄슈타인」과 나란히 놓이는 초기 SF · 20:30 실행분 이미지 완성 후 발행 중단, 22:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "#052" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README: appended #052")
else:
    print("README: #052 already present")

entry = '<div class="ep"><div class="no">#052 · 2026-11-22</div><div class="t">너새니얼 호손 「라파치니의 딸」(Rappaccini\'s Daughter, 1844)</div><div class="cap">르네상스 파도바의 밀폐된 정원 — 의사 라파치니가 독초로 가꾼 진보라 관목 곁에서 꽃처럼 자란 딸 베아트리체. 그녀의 숨결에 나비가 떨어지고, 사랑에 젖은 조르바니의 손끝도 어느새 독이 된다. 은빛 해독제를 기꺼이 들이켠 아가씨의 마지막 말 — 두려운 존재가 아니라, 사랑받고 싶었을 뿐. 분수가에는 조용히, 보라 꽃잎 한 점</div><img loading="lazy" src="episodes/sf-daily-052-rappaccinis-daughter/scroll.png"></div>' + NL

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-052-rappaccinis-daughter" not in html:
    marker = '<div class="ep">'
    idx = html.find(marker)
    if idx == -1:
        sys.exit("index.html: marker not found")
    html = html[:idx] + entry + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html: inserted #052 at top")
else:
    print("index.html: #052 already present")
