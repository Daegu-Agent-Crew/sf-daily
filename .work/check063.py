from PIL import Image
import os, sys

for p in [".work/ep063-p1-notext.png", ".work/ep063-p2-notext.png"]:
    im = Image.open(p)
    fmt, size, n = im.format, im.size, os.path.getsize(p)
    assert fmt == "PNG", (p, fmt)
    assert size == (1024, 1536), (p, size)
    assert n >= 300000, (p, n)
    print("OK", p, fmt, size, n)
print("CHECK063 PASS")
