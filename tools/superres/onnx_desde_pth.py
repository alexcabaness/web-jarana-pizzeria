import zipfile, pickle, numpy as np, onnx
from onnx import helper, numpy_helper, TensorProto
P='realesr-general-x4v3.pth'
z=zipfile.ZipFile(P); names=z.namelist(); root=names[0].split('/')[0]
class Stor:
    def __init__(s,key,dtype): s.key=key; s.dtype=dtype
def rebuild(storage, offset, size, stride, *a):
    buf=np.frombuffer(z.read(f'{root}/data/{storage.key}'),dtype=storage.dtype)
    n=int(np.prod(size)) if size else 1
    arr=buf[offset:offset+ (max((s-1)*st for s,st in zip(size,stride))+1 if size else 1)]
    return np.lib.stride_tricks.as_strided(arr,shape=size,strides=[x*buf.itemsize for x in stride]).copy()
class U(pickle.Unpickler):
    def find_class(s,mod,name):
        if name=='_rebuild_tensor_v2': return rebuild
        if name=='FloatStorage': return np.float32
        if mod=='collections' and name=='OrderedDict':
            import collections; return collections.OrderedDict
        return super().find_class(mod,name)
    def persistent_load(s,pid):
        _,dt,key,loc,n=pid; return Stor(key,dt if isinstance(dt,type) else np.float32)
sd=U(z.open(f'{root}/data.pkl')).load()
if 'params' in sd: sd=sd['params']
keys=list(sd.keys()); print(len(keys), keys[:4], keys[-3:])
nodes=[];inits=[];cur='x';li=0
body=[k for k in keys]
# body.N.weight / bias for conv; body.N.weight (1-D) for PReLU
idx=sorted({int(k.split('.')[1]) for k in keys})
for i in idx:
    w=sd[f'body.{i}.weight']
    if w.ndim==4:
        b=sd[f'body.{i}.bias']; wn,bn=f'w{i}',f'b{i}'
        inits+= [numpy_helper.from_array(w.astype(np.float32),wn),numpy_helper.from_array(b.astype(np.float32),bn)]
        out=f'c{i}'; nodes.append(helper.make_node('Conv',[cur,wn,bn],[out],pads=[1,1,1,1],kernel_shape=[3,3])); cur=out
    else:
        sn=f's{i}'; inits.append(numpy_helper.from_array(w.astype(np.float32).reshape(-1,1,1),sn))
        out=f'p{i}'; nodes.append(helper.make_node('PRelu',[cur,sn],[out])); cur=out
nodes.append(helper.make_node('DepthToSpace',[cur],['ps'],blocksize=4,mode='CRD'))
nodes.append(helper.make_node('Resize',['x','','sc'],['up'],mode='nearest'))
inits.append(numpy_helper.from_array(np.array([1,1,4,4],np.float32),'sc'))
nodes.append(helper.make_node('Add',['ps','up'],['y']))
g=helper.make_graph(nodes,'sr',[helper.make_tensor_value_info('x',TensorProto.FLOAT,[1,3,None,None])],[helper.make_tensor_value_info('y',TensorProto.FLOAT,[1,3,None,None])],inits)
m=helper.make_model(g,opset_imports=[helper.make_opsetid('',13)],ir_version=8); onnx.checker.check_model(m); onnx.save(m,'sr/sr.onnx'); print('ok')
