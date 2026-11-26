import numpy as np, glob, sys
from PIL import Image
W,H=720,990
x=np.linspace(0,1,W); y=np.linspace(0,1,H)
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
mx=ss(x/0.07)*ss((1-x)/0.07); my=ss(y/0.06)*ss((1-y)/0.04)
A=(np.outer(my,mx)*255).astype(np.uint8)
files=sorted(glob.glob('raw/*.png'))
for i,f in enumerate(files):
    im=Image.open(f).convert('RGB').resize((W,H),Image.LANCZOS)
    im.putalpha(Image.fromarray(A))
    im.save('site/f/%03d.webp'%i,'WEBP',quality=60,method=5,alpha_quality=60)
print(len(files))
