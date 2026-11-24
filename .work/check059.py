from PIL import Image, ImageChops

for n in (1, 2, 3):
    a = Image.open(f'.work/ep059-p{n}-notext.png').convert('RGB')
    b = Image.open(f'episodes/sf-daily-059-professor-dowells-head/page-{n:02d}.png').convert('RGB')
    diff = ImageChops.difference(a, b)
    bbox = diff.getbbox()
    hist = diff.convert('L').histogram()
    changed = sum(hist[32:])
    print(n, 'bbox=', bbox, 'changed_px=', changed)
    assert bbox is not None and changed > 20000, f'page {n}: overlay missing?'
print('OVERLAY OK')
