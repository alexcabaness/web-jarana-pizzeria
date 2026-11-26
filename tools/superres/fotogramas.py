import sys, glob, os, numpy as np
sys.path.insert(0,'sr'); from run import sr
from PIL import Image, ImageFilter
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
def alpha(W,H):
    x=np.linspace(0,1,W); y=np.linspace(0,1,H)
    mx=ss(x/0.07)*ss((1-x)/0.07); my=ss(y/0.06)*ss((1-y)/0.04)
    return Image.fromarray((np.outer(my,mx)*255).astype(np.uint8))
SETS=[('x',1218,1674,84),('h',812,1116,88),('f',720,990,66)]
AL={k:alpha(w,h) for k,w,h,q in SETS}
files=sorted(glob.glob('raw/*.png'))
for i,f in enumerate(files):
    if os.path.exists('../f/%03d.webp'%i): continue
    big=sr(Image.open(f))
    for k,w,h,q in SETS:
        im=big.resize((w,h),Image.LANCZOS)
        im.putalpha(AL[k]); im.save(f'../{k}/%03d.webp'%i,'WEBP',quality=q,method=5,alpha_quality=60)
    print(i,flush=True)
print('DONE')
