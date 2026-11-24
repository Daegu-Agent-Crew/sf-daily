from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
src = (root / '.work/letter_ep031.py').read_text(encoding='utf-8')

pages_new = '''
pages = [
    [
        {'n': '시리우스의 청년 미크로메가스, 나이 사백오십 — 그 별 기준으로, 아직 청년이다'},
        {'d': [('토성인:', '누구냐. 내 별을 요람 삼지 않게.'), ('미크로메가스:', '지나가는 나그네일세. 자네 별은 아담해서 좋구려')]},
        {'d': [('토성인:', '아담하다니! 수명이 만오천 년밖에 안 되어 — 짧아서 눈물이 나'), ('미크로메가스:', '나는 감각 천 개로 백만 년을 살아도, 결국 같은 걸 궁금해하지')]},
        {'d': [('미크로메가스:', '저 혜성을 타세. 우주 유람의 왕도일세'), ('토성인:', '허리야 부러지겠지만… 일단, 점프!')]},
        {},
        {'d': [('토성인:', '저건 얼음알이야. 감각 일흔둘로 장담하네 — 생명은 없어'), ('미크로메가스:', '잠깐, 내 다이아몬드를 보게 — 움직이는 점이, 아주 작은 점이 있어!')]},
    ],
    [
        {'d': [('선장:', '산이다! 산이 바다 위를 걷는다!'), ('철학자:', '아니… 저건 눈이야. 살아 있는 눈이 우리를 보고 있어')]},
        {'d': [('미크로메가스:', '이 즉석 확성 기계로 듣게 — 원자들이 과연 말을 하는가'), ('선원들:', '먹지만 말아 주시오! 우리는 생각할 줄 아는 원자들이오!')]},
        {'d': [('철학자:', '우리는 종종 전쟁을 합니다. 모자 쓴 십만 마리가 진창 몇 자를 두고 서로 죽이는…'), ('미크로메가스:', '오, 불쌍하고도 무서운 원자들…')]},
        {'d': [('신부:', '우리에겐 영혼이 있소! 그대들보다 결코 작지 않은'), ('토성인:', '들었나… 이 보송한 점들이, 영혼을 말하네')]},
        {'n': '작별 인사 대신 남긴 것 — 손톱만 한, 한 권의 책'},
        {'n': '미크로메가스가 남긴 책 — 인간의 눈에는, 새하얀 페이지뿐'},
    ],
]
'''

ast.parse(pages_new)

start = src.index('pages = [')
end = src.index('\n]\n', start) + len('\n]\n')
out = src[:start] + pages_new + '\n\n' + src[end:]
old_dir = 'episodes/sf-daily-031-the-heads-of-cerberus'
new_dir = 'episodes/sf-daily-032-micromegas'
assert old_dir in out
out = out.replace(old_dir, new_dir)
out = out.replace('.work/ep031-p', '.work/ep032-p')
assert 'ep031' not in out, 'ep031 references remain'
ast.parse(out)
(root / '.work/letter_ep032.py').write_text(out, encoding='utf-8')
print('written', len(out), 'chars; pages literal AST OK; full script AST OK')
