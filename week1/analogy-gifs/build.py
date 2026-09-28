# Analogy GIF builder: 5 frames, 1.6 s each. Usage: python3 build.py spec.json
import json, sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1920, 1080
BOLD = '/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf'
REG = '/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf'
AX, AY, AW, AH = 120, 70, 1680, 750   # image area; all text sits below it, centered

def fit_cover(img, crop, w, h):
    if crop: img = img.crop(crop)
    iw, ih = img.size; s = max(w / iw, h / ih)
    img = img.resize((round(iw * s), round(ih * s)), Image.LANCZOS)
    x = (img.width - w) // 2; y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def frame(spec, f, mode):
    out = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(out)
    img = Image.open(f['image']).convert('RGB')
    out.paste(fit_cover(img, f.get('crop'), AW, AH), (AX, AY))
    d.rectangle((AX, AY, AX + AW, AY + AH), outline='black', width=3)
    if f.get('mark'):   # red circle: the human's mark, [cx, cy, r] in frame coordinates
        cx, cy, r = f['mark']; d.ellipse((cx - r, cy - r, cx + r, cy + r), outline='#E30613', width=7)
    if mode == 'no-text': return out
    cy = AY + AH + 60
    if mode == 'tr':
        fb = ImageFont.truetype(BOLD, 34); tw = d.textlength(spec['title_tr'], font=fb); gap = 16; ew = d.textlength(spec['term_en'], font=fb)
        x0 = (W - (tw + gap + ew)) / 2
        d.text((x0, cy), spec['title_tr'], font=fb, fill='black'); d.text((x0 + tw + gap, cy), spec['term_en'], font=fb, fill=(191, 191, 191))
        cy += 56
    fr = ImageFont.truetype(REG, 30); cw = d.textlength(f['caption'], font=fr)
    d.text(((W - cw) / 2, cy), f['caption'], font=fr, fill='black')
    return out

def build(spec):
    for tag in ['tr', 'tr_no-titles', 'no-text']:
        os.makedirs(f'out/{tag}', exist_ok=True); frames = []
        for i, f in enumerate(spec['frames']):
            p = f'out/{tag}/{spec["slug"]}_{i+1}.png'; frame(spec, f, tag).save(p); frames.append(p)
        lst = f'out/{tag}/{spec["slug"]}.txt'
        with open(lst, 'w') as fh:
            for p in frames: fh.write(f"file '{os.path.abspath(p)}'\nduration 1.6\n")
            fh.write(f"file '{os.path.abspath(frames[-1])}'\n")
        mp4 = f'out/{tag}/a_{spec["slug"]}_{tag}.mp4'; gif = f'out/{tag}/a_{spec["slug"]}_{tag}.gif'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-crf', '18', '-movflags', '+faststart', mp4], check=True)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=0.625,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=256[p];[b][p]paletteuse=dither=sierra2_4a', '-loop', '0', gif], check=True)
        print(mp4, gif)

if __name__ == '__main__':
    build(json.load(open(sys.argv[1])))
