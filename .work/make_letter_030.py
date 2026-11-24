from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
src = (root / '.work/letter_ep029.py').read_text(encoding='utf-8')

pages_new = '''
pages = [
    [
        {'n': '난파 여드레째 밤 — 나를 건져 준 배는, 짐승 냄새가 났다'},
        {'d': [('몽고메리:', '천천히 마시게. …그리고 갑판 위에선, 눈을 너무 크게 뜨지 말게.'), ('프렌딕:', '저 선원들 얼굴이… 왜 다들 저런 모양이지?')]},
        {'d': [('선장:', '여기까지야! 조각배로 저 섬에나 내려가시지!'), ('프렌딕:', '섬이라뇨? 여긴 사람이 살 수 없는 곳이잖소!')]},
        {'d': [('몽고메리:', '밀링, 짐을 챙겨라. …저 사람을, 잘 부탁한다.')]},
        {'d': [('모로 박사:', '머무는 건 허하네. 단 한 가지 — 내 울타리 안에는 들어오지 말게.'), ('프렌딕(독백):', '저 눈은 동정이 아니야. 계산이다.')]},
        {'n': '첫날 밤, 창밖 숲 — 반짝이는 눈동자들, 줄지어'},
    ],
    [
        {'d': [('짐승인간들:', '네 발로 기지 말 것… 살점을 먹지 말 것… 우리는 법이다…')]},
        {'d': [('원숭이인간:', '다리가 둘뿐인 걸 보아, 걸을 줄 아는 짐승이 또 왔구나!'), ('프렌딕:', '짐승이라니… 당신들야말로 대체, 뭐지?')]},
        {},
        {'d': [('프렌딕:', '퓨마의 울음소리… 밤마다 저 문 너머에서. 대체 무엇을 만들고 있는 거야?')]},
        {'d': [('프렌딕:', '밀링의 손목에 손가락이 다섯, 꼬매진 자국 — 짐승을 사람으로 만들고 있어')]},
        {'d': [('모로 박사:', '비명에 신경 쓰지 말게. 고통은 내 연구의, 가장 값싼 재료일 뿐.')]},
    ],
    [
        {'n': '그날 밤 — 고통의 집 문이 부서지고, 퓨마가 어둠으로 달아났다'},
        {'d': [('짐승인간:', '법을 어긴 자는… 법 밖으로 나갈 뿐.'), ('프렌딕:', '모로 박사가 죽었어. 이 섬에 이제 법을 지킬 사람은, 아무도 없다.')]},
        {'d': [('프렌딕:', '창을 내려! 네 발로 기지 마! …대답이 없구나, 이미 늦었나.')]},
        {'n': '홀로 저으면 바다 — 등 뒤로 섬은 조용히 타고 있었다'},
        {'d': [('프렌딕:', '런던의 이 얼굴들… 모자 아래로, 아직도 섬이 보여.')]},
        {'n': '촛불 하나, 별이 가득한 창 — 나는 오늘도, 사람이 무섭다'},
    ],
]
'''

ast.parse(pages_new)

start = src.index('pages = [')
end = src.index('\n]\n', start) + len('\n]\n')
out = src[:start] + pages_new + '\n\n' + src[end:]
old_dir = 'episodes/sf-daily-029-the-lost-world'
new_dir = 'episodes/sf-daily-030-the-island-of-doctor-moreau'
assert old_dir in out
out = out.replace(old_dir, new_dir)
out = out.replace('.work/ep029-p', '.work/ep030-p')
assert 'ep029' not in out
ast.parse(out)
(root / '.work/letter_ep030.py').write_text(out, encoding='utf-8')
print('written', len(out), 'chars; pages literal AST OK; full script AST OK')
