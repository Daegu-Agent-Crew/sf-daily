from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
src = (root / '.work/letter_ep027.py').read_text(encoding='utf-8')

pages_new = '''pages = [
    [
        {'n': '눈보라의 아이핑 마을 — 아무도 오지 않는 언덕길을, 한 사내가 걸어온다.'},
        {'d': [('홀 부인:', '어머, 저 얼굴… 붕대투성이에 안경까지. 희한한 손님이네, 정말.'), ('손님:', '방을 내주게. 따뜻하고 — 아무도 없는 방으로.')]},
        {'d': [('손님:', '방해는 사양이오. 밤새 끓는 소리가 나도, 들러붙지 말 것.')]},
        {'d': [('홀 부인:', '소매가… 텅 비었어! 분명히 장갑이 움직였는데!')]},
        {'n': '장갑 안에는 — 아무도 없다.'},
        {'d': [('손님:', '눈은 오고, 마을은 잠든다. 모두가 잠드는 순간 — 그때, 시작이다.')]},
    ],
    [
        {'d': [('홀스:', '이젠 못 참지! 자, 당장 그 붕대를 벗겨 보자!'), ('손님:', '물러서라 — 이 붕대는, 내 것이다!')]},
        {'d': [('홀스:', '눈 위의 맨발 자국이… 여기서 뚝! 사람이, 공중에서 사라졌어!')]},
        {},
        {'d': [('마을 사람:', '물을 뿌려! 진흙을 던져! 윤곽이 보인다, 지금!')]},
        {'d': [('그리핀:', '마블, 똑똑히 들어라. 네 등 뒤엔 내가 있다 — 죽을 때까지.'), ('마블:', '으으, 목소리가… 등 뒤에서 들려!')]},
        {'n': '눈밭에 남은 것 — 붕대 한 조각.'},
    ],
    [
        {'d': [('그리핀:', '켐프, 오랜만이군. …나다, 그리핀.'), ('켐프:', '의자에 앉은 그 옷이… 그리핀? 아직도 살아 있었나.')]},
        {'d': [('그리핀:', '붉은 약 세 방울 — 거울 속에서 내 손이 옅어지다가, 사라졌지. 처음엔 축복인 줄 알았네.')]},
        {'d': [('그리핀:', '보이지 않는 자가 다스리는 시대 — 이제, 시작할 때다.'), ('켐프:', '그건 과학이 아니라… 광기일세, 그리핀.')]},
        {'n': '온 마을이 일어났다 — 낫과 삽, 그리고 진흙.'},
        {'d': [('군중:', '묻었다! 진흙에 윤곽이! 지금이다, 잡아!')]},
        {'n': '이제, 다시 보이는 얼굴 — 젊은 과학자의, 마지막 얼굴.'},
    ],
]'''

ast.parse(pages_new)

start = src.index('pages = [')
end = src.index('\n]\n', start) + len('\n]\n')
out = src[:start] + pages_new + '\n\n' + src[end:]
old_dir = 'episodes/sf-daily-027-dr-jekyll-and-mr-hyde'
new_dir = 'episodes/sf-daily-028-the-invisible-man'
assert old_dir in out
out = out.replace(old_dir, new_dir)
out = out.replace('.work/ep027-p', '.work/ep028-p')
assert 'ep027' not in out
ast.parse(out)
(root / '.work/letter_ep028.py').write_text(out, encoding='utf-8')
print('written', len(out), 'chars; pages literal AST OK; full script AST OK')
