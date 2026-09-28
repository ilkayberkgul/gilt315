# Letterbox an image (or several side by side) onto a white 1680:750 canvas so nothing is cut.
# Usage: python3 tools_pad.py out.jpg img1 [img2 ...]   (several images are placed side by side)
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
W, H, M, G = 3360, 1500, 60, 60   # 2x the image area, margin, gap
ims = [Image.open(p).convert('RGB') for p in sys.argv[2:]]
n = len(ims); cw = (W - 2 * M - (n - 1) * G) / n; ch = H - 2 * M
out = Image.new('RGB', (W, H), 'white')
for i, im in enumerate(ims):
    s = min(cw / im.width, ch / im.height); r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = M + i * (cw + G) + (cw - r.width) / 2; y = (H - r.height) / 2
    out.paste(r, (round(x), round(y)))
out.save(sys.argv[1], quality=92); print(sys.argv[1], out.size)
