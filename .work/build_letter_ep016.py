from pathlib import Path

work = Path(__file__).resolve().parent
source = (work / 'letter_ep015.py').read_text()
source = source.replace('ep015-notext.png', 'ep016-notext.png')
source = source.replace('sf-daily-015-the-poison-belt.png', 'sf-daily-016-the-wreck-of-the-titan.png')
start = source.index("narration(0, ")
end = source.index("dst.parent.mkdir", start)
captions = '''narration(0, "1898년, 소설이 그린 4월의 대서양 — '침몰 불가능'이라 불린 세계 최대 여객선 타이탄호.")
dialogue(0, '일등석 신사:', '저 배가 가라앉다니요, 웃기지 마시오.')
narration(1, '갑판원 존 롤랜드 — 술로 몰락한 전직 해군 장교.')
dialogue(1, '롤랜드:', '빙산 지대입니다! 속도를 줄여야 합니다!')
narration(3, '한밤, 빙산이 우현을 찢었다.')
dialogue(3, '부관:', '구명보트는 24척… 사람은 3000명입니다.')
narration(4, '롤랜드는 옛 사랑의 딸, 아홉 살 미라를 안고 얼음으로 뛰었다.')
dialogue(4, '롤랜드:', '눈 감아! 꼭 잡아!')
narration(5, '얼음 섬에서 사흘째 — 그는 곰보다 먼저 움직였다.')
dialogue(5, '롤랜드:', '미라, 내 뒤로.')
narration(6, '새벽 지평선에 연기 한 줄.')
dialogue(6, '미라:', '배요, 아저씨! 배!')
narration(7, "재기한 롤랜드는 미라의 어머니와 가정을 이뤘다 — 그리고 14년 뒤, '타이타닉'이 소설과 같은 밤을 지나갔다.")

'''
(work / 'letter_ep016.py').write_text(source[:start] + captions + source[end:])
