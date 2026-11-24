from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
src = (root / '.work/letter_ep028.py').read_text(encoding='utf-8')

pages_new = '''
pages = [
    [
        {'n': '1912년, 런던의 저녁 — 학회 강당의 평화는 그날로 끝났다'},
        {'d': [('찰린저:', '남미 정글 한가운데, 공룡이 사는 고원이 있다. 내 두 눈으로 봤다!'), ('청중:', '사기꾼! 사진이나 보여주시지!')]},
        {'d': [('찰린저:', '이 스케치의 날개 폭은 백조가 아니다. 정체를 알고 싶으면 — 직접 가 보게.'), ('말론:', '저를 데려가 주십시오. 기사가 아니라 — 눈으로 보고 싶습니다.')]},
        {'d': [('록스턴 경:', '아마존이라면 내 정원이지. 총과 경험, 둘 다 가져가겠네.'), ('서머리:', '흥, 다녀와서 사과를 받아주지. 없는 고원을 찾는 놀음이지만.')]},
        {'n': '안개 저편, 분홍빛 절벽 위 — 잃어버린 세계'},
        {'d': [('찰린저:', '저 위에 있다! 보라 — 내 말이 틀렸나?')]},
    ],
    [
        {'d': [('고메즈:', '이 다리는 — 없던 걸로 하시지! 우리 형을 잡은 게 누구더라!'), ('록스턴 경:', '배신자! 도끼를 내려놔, 고메즈!')]},
        {'n': '내려갈 길은, 이제 없다 — 저 위가 우리의 전부'},
        {},
        {'d': [('말론:', '이구아노돈이다, 초식! 공룡이 아직… 살아서 숨 쉬고 있어!'), ('서머리:', '찰린저, 사과하네. 근데 — 발소리가 왜 이렇게 크지?')]},
        {'d': [('록스턴 경:', '알로사우루스! 바위 뒤로, 전원! 총은 — 아직 아니야!')]},
        {'n': '능선 위, 원숭이인간들 — 창끝보다 조용한 눈들'},
    ],
    [
        {'d': [('록스턴 경:', '동굴이다! 강가로 나가는 길 — 마지막 승부다, 젊은이들!')]},
        {'d': [('서머리:', '덮개 밖에서 숨소리가 들리는군. 대체 뭐를 데려온 거지?')]},
        {'d': [('찰린저:', '신사 여러분, 남미에서 돌아왔습니다. 증거는 — 이 상자 안에 있습니다.')]},
        {'d': [('청중:', '열어보시오! 설마 비둘기 새끼는 아니겠지?')]},
        {'d': [('서머리:', '익룡이다…! 프테라노돈! 저것 봐, 살아 있다고 — 전부!')]},
        {'n': '빈 상자 하나 — 창밖 하늘로, 아직도 열려 있는 문'},
    ],
]
'''

ast.parse(pages_new)

start = src.index('pages = [')
end = src.index('\n]\n', start) + len('\n]\n')
out = src[:start] + pages_new + '\n\n' + src[end:]
old_dir = 'episodes/sf-daily-028-the-invisible-man'
new_dir = 'episodes/sf-daily-029-the-lost-world'
assert old_dir in out
out = out.replace(old_dir, new_dir)
out = out.replace('.work/ep028-p', '.work/ep029-p')
assert 'ep028' not in out
ast.parse(out)
(root / '.work/letter_ep029.py').write_text(out, encoding='utf-8')
print('written', len(out), 'chars; pages literal AST OK; full script AST OK')
