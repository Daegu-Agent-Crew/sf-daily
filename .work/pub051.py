# -*- coding: utf-8 -*-
import io, sys
NL = chr(10)
readme_line = "- #051 2026-11-22: 예브게니 자먀찐 「우리들」(Мы / We, 1924) — 20세기 디스토피아 SF의 시조, 「1984」·「멋진 신세계」가 잇달아 물려받은 원형 · 18:30 실행분 이미지 완성 후 발행 중단, 20:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "#051" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README: appended #051")
else:
    print("README: #051 already present")

entry = '<div class="ep"><div class="no">#051 · 2026-11-22</div><div class="t">예브게니 자먀찐 「우리들」(Мы / We, 1924)</div><div class="cap">머나먼 미래의 유리 도시 온세계주 — 이름 대신 번호, 시간표대로 사는 완전한 나라. 수학자 D-503은 우주선 인테그랄로 수학의 완전함을 별들에게 전하려 하지만, I-330이 이끄는 옛집과 장벽 밖의 풀에서 영혼이라는 병을 얻는다. 상상력은 병이라 선언되고 위대한 수술이 그 병을 잘라 낸다 — 가스 큐브 아래 끝내 침묵한 I-330, 그리고 유리 도시의 밤하늘에는 여전히, 구름 한 점</div><img loading="lazy" src="episodes/sf-daily-051-we/scroll.png"></div>' + NL

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-051-we" not in html:
    marker = '<div class="ep">'
    idx = html.find(marker)
    if idx == -1:
        sys.exit("index.html: marker not found")
    html = html[:idx] + entry + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html: inserted #051 at top")
else:
    print("index.html: #051 already present")
