from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
src = (root / '.work/letter_ep030.py').read_text(encoding='utf-8')

pages_new = '''
pages = [
    [
        {'n': '1919년 필라델피아, 폭우 — 우리 셋은 골목 끝 잡화점으로 몸을 피했다'},
        {'d': [('주인:', '이 수정 잔에는 값을 매기지 않았소. …필요한 이에겐, 공짜.'), ('바비:', '공짜라… 뭔가 굉장히 속보이는걸요?')]},
        {'d': [('테리:', '영감, 이 회색 가루 말인가?'), ('바이올라:', '장미 향… 아니, 훨씬 오래된 냄새')]},
        {'d': [('바이올라:', '그저 향이 좋아서, 들이마셨을 뿐이에요')]},
        {},
        {'d': [('바비:', '여긴 방금 그 가리가 아닌가? 저 첨탑들은 대체…'), ('테리:', '둘 다 내 뒤로. 이 거리 전체가, 우리를 보고 있어')]},
    ],
    [
        {'n': '2118년 — 낡은 벽돌 도시 위로, 돌처럼 차가운 탑들이 자라 있었다'},
        {'d': [('바이올라:', '저 사람들 목에… 번호판이 달린 목걸이'), ('바비:', '죄수 표시가 아니야. 저들 모두가, 저걸 차고 있어')]},
        {'d': [('경비:', '목걸이 없는 자는 즉시 연행 대상이다. 따라와.'), ('바비:', '우린 이 도시 사람이 아니에요! 정말이에요!')]},
        {'d': [('테리:', '먼저 건드리는 놈이, 이 손바닥부터 본다')]},
        {'d': [('관리관:', '번호 3271, 노동 구획 배정. 항소는 없다.'), ('테리:', '…감히 내 목에 이걸 채웠겠다')]},
        {'n': '새벽 창살 너머 — 번호를 단 사람들의, 끝없는 행렬'},
    ],
    [
        {'d': [('테리:', '문을 열어라! 오늘 밤 이 도시의 목걸이는, 전부 벗겨진다')]},
        {'d': [('바이올라:', '여러분! 그 번호는, 여러분의 이름이 아니에요'), ('시민들:', '목걸이를 벗어라! 벗어라!')]},
        {'n': '수정 잔 바닥에 남은 — 마지막 한 꼬집의 가루'},
        {'d': [('바비:', '눈 감아요, 두 분. 그 폭풍의 가게로, 우리 다시')]},
        {'n': '아침의 우리 골목 — 잡화점이 있던 자리엔, 낡은 벽돌벽뿐'},
        {'n': '아직 손안에 — 별처럼 빛나는 회색 가루, 몇 알'},
    ],
]
'''

ast.parse(pages_new)

start = src.index('pages = [')
end = src.index('\n]\n', start) + len('\n]\n')
out = src[:start] + pages_new + '\n\n' + src[end:]
old_dir = 'episodes/sf-daily-030-the-island-of-doctor-moreau'
new_dir = 'episodes/sf-daily-031-the-heads-of-cerberus'
assert old_dir in out
out = out.replace(old_dir, new_dir)
out = out.replace('.work/ep030-p', '.work/ep031-p')
assert 'ep030' not in out, 'ep030 references remain'
ast.parse(out)
(root / '.work/letter_ep031.py').write_text(out, encoding='utf-8')
print('written', len(out), 'chars; pages literal AST OK; full script AST OK')
