import onnxruntime as ort, numpy as np, sys, time
from PIL import Image
so=ort.SessionOptions(); so.intra_op_num_threads=4
s=ort.InferenceSession('sr/sr.onnx',so,providers=['CPUExecutionProvider'])
def sr(im, tile=280, pad=12):
    a=np.asarray(im.convert('RGB'),np.float32)/255.; H,W,_=a.shape
    out=np.zeros((H*4,W*4,3),np.float32)
    for y in range(0,H,tile):
        for x in range(0,W,tile):
            y0,x0=max(y-pad,0),max(x-pad,0); y1,x1=min(y+tile+pad,H),min(x+tile+pad,W)
            t=a[y0:y1,x0:x1].transpose(2,0,1)[None]
            r=s.run(None,{'x':t})[0][0].transpose(1,2,0)
            ty,tx=(y-y0)*4,(x-x0)*4; hh,ww=min(tile,H-y)*4,min(tile,W-x)*4
            out[y*4:y*4+hh,x*4:x*4+ww]=r[ty:ty+hh,tx:tx+ww]
    return Image.fromarray((np.clip(out,0,1)*255+.5).astype(np.uint8))
if __name__=='__main__':
    for src,dst in zip(sys.argv[1::2],sys.argv[2::2]):
        t=time.time(); sr(Image.open(src)).save(dst); print(dst,round(time.time()-t,1),flush=True)
