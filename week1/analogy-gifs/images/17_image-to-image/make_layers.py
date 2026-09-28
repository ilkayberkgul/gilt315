# Composite n sheets of tracing paper (35% white each, slight paper texture) over the real sketch scan.
# Each sheet also diffuses what is under it a little (small blur), as real tracing paper does.
# Usage: python3 images/17_image-to-image/make_layers.py   (run from week1/analogy-gifs)
from PIL import Image, ImageFilter, ImageChops
D = 'images/17_image-to-image'
base = Image.open(f'{D}/ingres_sketch.jpg').convert('RGB')
def sheet(size, seed):
    n = Image.effect_noise((size[0] // 4, size[1] // 4), 18 + seed).resize(size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(2))
    # map noise (centered on 128) to near-white 245..255 so each sheet is slightly uneven
    n = n.point(lambda v: max(0, min(255, 250 + (v - 128) * 10 // 64)))
    return Image.merge('RGB', (n, n, n))
img = base
for k in range(1, 6):
    img = Image.blend(img.filter(ImageFilter.GaussianBlur(3)), sheet(base.size, k), 0.35)
    if k in (1, 3, 5):
        img.save(f'{D}/sketch_layers_{k}.jpg', quality=93)
print('ok')
