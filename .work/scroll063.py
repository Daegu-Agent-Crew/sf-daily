from PIL import Image
import sys

srcs = sys.argv[1:-1]
dst = sys.argv[-1]
ims = [Image.open(s).convert("RGB") for s in srcs]
w = min(im.width for im in ims)
ims = [im.resize((w, int(im.height * w / im.width))) for im in ims]
H = sum(im.height for im in ims)
out = Image.new("RGB", (w, H), "white")
y = 0
for im in ims:
    out.paste(im, (0, y)); y += im.height
out.save(dst, optimize=True)
print(dst, out.size)
