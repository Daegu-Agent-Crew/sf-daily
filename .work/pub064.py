# -*- coding: utf-8 -*-
import io
from pathlib import Path
from PIL import Image

NL = chr(10)
root = Path('.').resolve()
dest = root / 'episodes/sf-daily-064-metropolis'
expected = {'page-01.png': (1024, 1536), 'page-02.png': (1024, 1536), 'page-03.png': (1024, 1536), 'scroll.png': (1024, 4608)}
for name, size in expected.items():
    p = dest / name
    im = Image.open(p)
    im.verify()
    im = Image.open(p)
    assert (im.format, im.size) == ('PNG', size), (name, im.format, im.size)
    assert p.stat().st_size >= 300_000, (name, p.stat().st_size)
    print('OK %s | %s bytes | %dx%d' % (name, format(p.stat().st_size, ','), size[0], size[1]))

readme_line = "- #064 2026-11-25: 테아 폰 하르보우 「메트로폴리스」(Metropolis, 1925) — 위의 탑과 아래의 기계홀, 마리아의 얼굴을 가진 기계와 물바다가 된 노동자 도시, 프리츠 랑의 영화로 이어진 기계 도시의 고전 · 00:30 실행분 이미지 완성 후 발행 중단, 02:30 실행에서 발행 완료" + NL

with io.open("README.md", "r", encoding="utf-8") as f:
    txt = f.read()
if "sf-daily-064" not in txt:
    if not txt.endswith(NL):
        txt += NL
    txt += readme_line
    with io.open("README.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("README updated")

ep_div = '<div class="ep"><div class="no">#064 · 2026-11-25</div><div class="t">테아 폰 하르보우 「메트로폴리스」(Metropolis, 1925)</div><div class="cap">위의 탑에 사는 아들 프레더는 노동자 아이들의 눈을 처음 보고 아버지의 도시 밑바닥으로 내려간다 — 팔을 바늘처럼 벌린 십 시간, 사람을 삼키는 기계 몰로크. 카타콤의 처녀 마리아는 "머리와 손 사이엔 심장이 필요하다"고 설교하고, 지배자는 발명가 로트방의 기계 인간에게 마리아의 얼굴을 씌운다. 마리아의 얼굴로 눈을 뜬 기계는 노동자들을 부추겨 심장 기계를 부수고, 노동자 도시는 물바다가 되어 아이들을 삼키려 든다. 화형의 불길 속에서 은빛 골격이 드러난 뒤, 저녁의 성당 계단에 남은 것은 — 아버지와 노동자의 손을 맞잡게 하는, 아들의 두 손. 프리츠 랑의 영화로 이어진 기계 도시의 고전</div><img loading="lazy" src="episodes/sf-daily-064-metropolis/scroll.png"></div>'

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
if "sf-daily-064" not in html:
    marker = '<div class="meta">삼체 연재와 별개 시스템 · 1일 12화 2시간 주기 · codex 생성 · 원작 충실 다중 페이지</div>' + NL
    idx = html.find(marker)
    assert idx >= 0, "index marker not found"
    idx += len(marker)
    html = html[:idx] + ep_div + NL + html[idx:]
    with io.open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated")
print("PUB064 DONE")
