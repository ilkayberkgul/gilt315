# Contact sheet of the 5 'tr' frames of one analogy. Usage: python3 contact_sheet.py NN_slug
import sys, os
from PIL import Image
slug = sys.argv[1]; tw, th, pad = 640, 360, 12
sheet = Image.new('RGB', (3 * tw + 4 * pad, 2 * th + 3 * pad), (40, 40, 40))
for i in range(5):
    im = Image.open(f'out/tr/{slug}_{i+1}.png').resize((tw, th), Image.LANCZOS)
    sheet.paste(im, (pad + (i % 3) * (tw + pad), pad + (i // 3) * (th + pad)))
os.makedirs('out/contact_sheets', exist_ok=True)
sheet.save(f'out/contact_sheets/{slug}.jpg', quality=88); print(f'out/contact_sheets/{slug}.jpg')
