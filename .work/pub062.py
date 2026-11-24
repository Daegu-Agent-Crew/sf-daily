# -*- coding: utf-8 -*-
import io
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-062-the-brick-moon'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'scroll.png': (1024, 3072)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print('OK %s | %s bytes | %dx%d' % (name, format(p.stat().st_size, ','), size[0], size[1]))

readme_line = "- #062 2026-11-24: 에드워드 에버렛 헤일 「벽돌 달」(The Brick Moon, 1869) — 인공위성·우주 정거장을 스푸트니크보다 한 세기 앞서 그린 소설, 벽돌 달이 모스 부호로 지구에 첫 답장을 보내다 · 18:30 실행분 1·2페이지 생성 후 발행 중단, 20:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-062" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README updated")

ep_div = '<div class="ep"><div class="no">#062 · 2026-11-24</div><div class="t">에드워드 에버렛 헤일 「벽돌 달」(The Brick Moon, 1869)</div><div class="cap">1869년 기숙학교 자습실, 소년들은 항해사를 위한 새 길잡이 별을 벽돌로 만들자 꿈꾼다. 20년 뒤 메인의 겨울 골짜기 — 거대한 물레바퀴가 돌고, 200피트 테라코타 벽돌 구체가 하늘로 튕겨 오른다. 궤도에 오른 달 안에는 우연히 남아 있던 서른일곱 명의 가족들. 지구와 달 사이 어떤 신호도 없던 어느 겨울, 눈밭에 하얀 천을 펼치자 달의 가장자리에 사람들이 줄을 서 — 긴 뜀, 짧은 뜀, 모스 부호의 첫 답장. 인공위성·우주 정거장·위성 통신을 스푸트니크보다 한 세기 앞서 그린 최초의 SF</div><img loading="lazy" src="episodes/sf-daily-062-the-brick-moon/scroll.png"></div>'

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-062" not in html:
    marker = '<div class="meta">삼체 연재와 별개 시스템 · 1일 12화 2시간 주기 · codex 생성 · 원작 충실 다중 페이지</div>' + NL
    idx = html.find(marker)
    assert idx >= 0, "index marker not found"
    idx += len(marker)
    html = html[:idx] + ep_div + NL + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated")
print("PUB062 DONE")