import html, re, sys
sys.path.insert(0, '/tmp/claude-0/-home-user/5e0ea1de-e0a0-5471-8f95-a49be0421e2f/scratchpad/build')
from data import *
W='/tmp/claude-0/-home-user/5e0ea1de-e0a0-5471-8f95-a49be0421e2f/scratchpad/'
e=html.escape
def parse(s):
    out=[]
    for l in s.strip().split('\n'):
        n,p,i,a=l.split('|'); out.append((n,p,i,a))
    return out
def cap(s): return s[:1].upper()+s[1:]
MASCOT=open(W+'build/mascot_inner.svg').read()
def mascot(cls, label=None):
    a = f'role="img" aria-label="{e(label)}"' if label else 'aria-hidden="true"'
    return f'<svg class="flame {cls}" viewBox="0 0 220 250" {a}>{MASCOT}</svg>'

def items(rows, cols='two', tags={}):
    li=[]
    for n,p,i,a in rows:
        t = f'<span class="tag">{e(tags[n])}</span>' if n in tags else ''
        ing = f'<p class="ing">{e(cap(i))}.</p>' if i else ''
        al = f'<p class="al">{e(a)}</p>' if a else ''
        li.append(f'<li class="it"><div class="row"><h4>{e(n)}{t}</h4><span class="ld" aria-hidden="true"></span><span class="pr">{p} €</span></div>{ing}{al}</li>')
    return f'<ul class="list {cols}">'+''.join(li)+'</ul>'

CATS=[('pizzas','Pizzas','Masa fina, borde dorado y queso gratinado.',items(parse(PIZZAS),tags={'Barbacoa':'La del vídeo','Al gusto':'Tú mandas'})),
('porciones','Porciones','Pizza al corte para picar. Pídelas sueltas o haz tu mezcla.',items(parse(PORCIONES),'three')),
('entrantes','Entrantes','Para compartir, o no.',items(parse(ENTRANTES))),
('salsas','Salsas','Para acompañar. Todas a 1,30 €.',items(parse(SALSAS),'chips')),
('bebidas','Bebidas','Refrescos y bebidas frías.',items(parse(BEBIDAS),'three')),
('postres','Postres','Para cerrar con algo dulce.',items(parse(POSTRES)))]

tabs=''.join(f'<a href="#{k}" data-k="{k}">{t}</a>' for k,t,_,_ in CATS)+'<a href="#club" data-k="club" class="club-tab">Club Jarana</a>'
cats=''.join(f'''<section class="cat" id="{k}" aria-labelledby="h-{k}">
<header class="cat-h reveal"><span class="num">{i+1:02d}</span><h3 id="h-{k}">{t}</h3><p>{e(s)}</p></header>
<div class="reveal">{body}</div></section>''' for i,(k,t,s,body) in enumerate(CATS))

feat=[('barbacoa','Barbacoa','9,95','Tomate, mozzarella, carne picada, bacon, salsa BBQ y orégano.','La del vídeo'),
('quesos','Especial Quesos','9,95','Tomate, mozzarella, cheddar, parmesano, roquefort, emmental y orégano.','Para los de queso'),
('york','York','8,50','Tomate, mozzarella, jamón york y orégano.','La de siempre')]
cards=''.join(f'''<article class="card reveal" style="--d:{i*90}ms">
<div class="ph"><img src="assets/{img}.webp" alt="Pizza {e(n)}" loading="lazy" decoding="async"><span class="n">{i+1:02d}</span></div>
<div class="cb"><span class="kick">{e(k)}</span><div class="row"><h4>{e(n)}</h4><span class="pr">{p} €</span></div><p>{e(d)}</p></div></article>''' for i,(img,n,p,d,k) in enumerate(feat))

club=''.join(f'''<div class="rg reveal" style="--d:{i*80}ms"><h4>{e(g)}</h4><ul>'''+''.join(f'<li><span>{e(a)}</span><b>{b}</b></li>' for a,b in rows)+'</ul></div>' for i,(g,rows) in enumerate(CLUB))

words=['Pizzas','Porciones','Entrantes','Postres','Barbacoa','Club Jarana']
marq=''.join(f'<span>{w}</span><i aria-hidden="true">✺</i>' for w in words)

CARTA=f'''
<section class="intro" id="carta" aria-labelledby="h-intro">
  <div class="wrap intro-in">
    <div class="intro-t reveal">
      <span class="lbl">// La carta</span>
      <h2 id="h-intro">Si te llama,<br>contesta.</h2>
      <p class="lead">Pizzas de masa fina, porciones para picar, entrantes para compartir y algo dulce para el final. Todo lo que hay, con precio y alérgenos.</p>
      <a class="btn" href="#pizzas">Ver la carta <span aria-hidden="true">↓</span></a>
    </div>
    <div class="intro-m reveal" style="--d:120ms">
      <div class="bubble">¿Hoy toca<br>barbacoa?</div>
      {mascot('m-intro','Monigote de La Jarana: una llama blanca con cara de pillo')}
    </div>
  </div>
  <div class="marq" aria-hidden="true"><div class="mq">{marq}{marq}</div></div>
</section>

<section class="feat" aria-labelledby="h-feat">
  <div class="wrap">
    <div class="sec-h reveal"><span class="lbl">// Tres para empezar</span><h2 id="h-feat">Las que más<br>llaman.</h2></div>
    <div class="cards">{cards}</div>
  </div>
</section>

<section class="menu" aria-label="Carta completa">
  <nav class="tabs" aria-label="Secciones de la carta"><div class="tabs-in">{tabs}</div></nav>
  <div class="wrap">{cats}
  <p class="note reveal">Precios en euros. Si tienes alguna alergia, dínoslo al pedir y te contamos qué lleva cada cosa.</p>
  </div>
</section>

<section class="club" id="club" aria-labelledby="h-club">
  <div class="wrap club-in">
    <div class="club-t reveal">
      <span class="lbl dark">// Club Jarana</span>
      <h2 id="h-club">Juntos hacemos jarana.</h2>
      <p>Acumula <b>jaranitos</b> con tus pedidos y cámbialos por tus productos favoritos. Cuantos más acumules, más cosas te llevas.</p>
      <div class="rate"><span>1 €</span><em>=</em><span>1 jaranito</span></div>
    </div>
    <div class="club-m reveal" style="--d:120ms">{mascot('m-club')}</div>
  </div>
  <div class="wrap"><div class="rewards">{club}</div><p class="club-f reveal">Jaranitos necesarios para cada recompensa.</p></div>
</section>

<section class="order" id="pedir" aria-labelledby="h-order">
  <div class="wrap order-in reveal">
    {mascot('m-order')}
    <h2 id="h-order">¿Te llama?</h2>
    <p>Haz tu pedido en un par de toques.</p>
    <a class="btn big" href="#pedir">Pedir ahora</a>
  </div>
</section>

</main>
<footer class="foot" id="contacto">
  <div class="wrap foot-in">
    <img src="assets/logo.png" alt="La Jarana" width="1000" height="155" class="foot-logo" loading="lazy">
    <p>Te llama. <a href="https://www.instagram.com/la_jarana_te_llama/">@la_jarana_te_llama</a></p>
    <small>Prototipo de la nueva web · contenido de prueba</small>
  </div>
</footer>
'''
t=open(W+'build/template.html').read().replace('/*CARTA_CSS*/',open(W+'build/carta.css').read())
open(W+'work/site/index.html','w').write(t.replace('<!--CARTA-->',CARTA))
print('ok', len(t)+len(CARTA))
