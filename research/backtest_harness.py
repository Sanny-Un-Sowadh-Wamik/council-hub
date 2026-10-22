import json, glob, os, math
from collections import defaultdict

TR="/root/.claude/projects/-home-claude/a3e2d022-832f-5b9d-b406-a491caa0a235/tool-results/"
FEE=0.001  # 0.1% round-trip slippage+comm on notional (stock)

# ---- load all daily kline files, dedup by code, keep longest ----
data={}
for f in glob.glob(TR+"mcp-Moomoo-quote_history_kline-*.txt"):
    try:
        d=json.load(open(f))
    except: continue
    kl=d.get("data",{}).get("kline_list")
    if not kl or len(kl)<200: continue
    # daily check: consecutive bars differ by >=1 day (date field changes)
    dates=[b["date"] for b in kl]
    if dates[1]==dates[0]: continue  # intraday
    code=kl[0].get("name") or kl[0].get("sc_name") or f
    if code not in data or len(kl)>len(data[code]):
        data[code]=kl

def series(kl,key): return [b[key] for b in kl]

def sma(x,n):
    out=[None]*len(x)
    s=0
    for i,v in enumerate(x):
        s+=v
        if i>=n: s-=x[i-n]
        if i>=n-1: out[i]=s/n
    return out

def atr(h,l,c,n=14):
    tr=[h[0]-l[0]]
    for i in range(1,len(c)):
        tr.append(max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])))
    out=[None]*len(c)
    # Wilder
    if len(c)>n:
        a=sum(tr[1:n+1])/n
        out[n]=a
        for i in range(n+1,len(c)):
            a=(a*(n-1)+tr[i])/n
            out[i]=a
    return out

def rsi(c,n=14):
    out=[None]*len(c)
    if len(c)<=n: return out
    gains=[0]; losses=[0]
    for i in range(1,len(c)):
        ch=c[i]-c[i-1]
        gains.append(max(ch,0)); losses.append(max(-ch,0))
    ag=sum(gains[1:n+1])/n; al=sum(losses[1:n+1])/n
    out[n]=100-100/(1+(ag/al if al else 999))
    for i in range(n+1,len(c)):
        ag=(ag*(n-1)+gains[i])/n; al=(al*(n-1)+losses[i])/n
        out[i]=100-100/(1+(ag/al if al else 999))
    return out

def rollmax(x,n):  # max of prior n bars EXCLUDING current
    out=[None]*len(x)
    for i in range(len(x)):
        if i>=n: out[i]=max(x[i-n:i])
    return out

# ---- backtest engine ----
# A strategy = function(bar index i, ctx) -> True to enter long at NEXT open.
# exit: stop=entry-1.5*ATR_entry; target=entry+3R; time stop TMAX days; plus optional custom exit.
def run(strat_name, entry_fn, tmax=20, custom_exit=None, rr=3.0, atr_mult=1.5):
    trades=[]  # (exit_date, R, ret_pct)
    for code,kl in data.items():
        o=series(kl,"open"); h=series(kl,"high"); l=series(kl,"low"); c=series(kl,"close")
        v=series(kl,"volume"); dt=series(kl,"date")
        ind=dict(
            sma5=sma(c,5), sma20=sma(c,20), sma50=sma(c,50), sma200=sma(c,200),
            atr=atr(h,l,c,14), rsi=rsi(c,14), vsma=sma(v,20),
            hh55=rollmax(h,55), hh20=rollmax(h,20),
        )
        i=210  # warmup
        N=len(c)
        pos=None
        while i<N-1:
            if pos is None:
                ctx=dict(i=i,o=o,h=h,l=l,c=c,v=v,**ind)
                if entry_fn(ctx):
                    entry=o[i+1]
                    a=ind["atr"][i]
                    if not a or a<=0: i+=1; continue
                    stop=entry-atr_mult*a
                    tgt=entry+rr*(entry-stop)
                    pos=dict(entry=entry,stop=stop,tgt=tgt,day=i+1,bars=0,R=entry-stop)
                    i+=1; continue
            else:
                j=i
                hi=h[j]; lo=l[j]; cl=c[j]
                ex=None; price=None
                # gap/stop first (conservative)
                if lo<=pos["stop"]:
                    price=min(o[j],pos["stop"]) if o[j]<pos["stop"] else pos["stop"]; ex="stop"
                elif hi>=pos["tgt"]:
                    price=pos["tgt"]; ex="target"
                else:
                    pos["bars"]+=1
                    if custom_exit and custom_exit(dict(i=j,o=o,h=h,l=l,c=c,**ind),pos):
                        price=c[j]; ex="signal"
                    elif pos["bars"]>=tmax:
                        price=c[j]; ex="time"
                if ex:
                    R=(price-pos["entry"])/pos["R"]
                    ret=(price/pos["entry"]-1)-FEE
                    trades.append((dt[j],R,ret))
                    pos=None
            i+=1
    return trades

def metrics(trades):
    if not trades: return None
    Rs=[t[1] for t in trades]; rets=[t[2] for t in trades]
    n=len(Rs); wins=[r for r in Rs if r>0]; losses=[r for r in Rs if r<=0]
    wr=len(wins)/n
    aw=sum(wins)/len(wins) if wins else 0
    al=sum(losses)/len(losses) if losses else 0
    exp=sum(Rs)/n
    gp=sum(r for r in rets if r>0); gl=-sum(r for r in rets if r<0)
    pf=gp/gl if gl else 999
    # equity in R, ordered by exit date
    ordered=sorted(trades,key=lambda t:t[0])
    eq=0; peak=0; mdd=0
    for _,R,_ in ordered:
        eq+=R; peak=max(peak,eq); mdd=min(mdd,eq-peak)
    totret=sum(rets)  # sum of per-trade net returns (1 unit each)
    return dict(n=n,wr=wr,aw=aw,al=al,exp=exp,pf=pf,mdd=mdd,totR=sum(Rs),totret=totret)

# ---- strategy definitions ----
def s_breakout55(x):
    i=x["i"]
    if None in (x["hh55"][i],x["vsma"][i],x["sma50"][i],x["rsi"][i]): return False
    return x["c"][i]>x["hh55"][i] and x["v"][i]>1.3*x["vsma"][i] and x["c"][i]>x["sma50"][i] and 55<=x["rsi"][i]<=75

def s_donchian20(x):
    i=x["i"]
    if x["hh20"][i] is None: return False
    return x["c"][i]>x["hh20"][i]

def s_pullback(x):
    i=x["i"]
    if None in (x["sma200"][i],x["sma50"][i],x["sma20"][i],x["rsi"][i],x["rsi"][i-1]): return False
    return (x["c"][i]>x["sma200"][i] and x["c"][i]>x["sma50"][i] and x["l"][i]<=x["sma20"][i]
            and x["rsi"][i]>x["rsi"][i-1] and x["rsi"][i]<60)

def s_macross(x):
    i=x["i"]
    if None in (x["sma5"][i],x["sma20"][i],x["sma5"][i-1],x["sma20"][i-1]): return False
    return x["sma5"][i-1]<=x["sma20"][i-1] and x["sma5"][i]>x["sma20"][i]
def x_macross(x,pos):
    i=x["i"]
    if None in (x["sma5"][i],x["sma20"][i]): return False
    return x["sma5"][i]<x["sma20"][i]

def s_rsmom(x):
    i=x["i"]
    if None in (x["sma50"][i],x["sma20"][i]): return False
    if i<95: return False
    r90=x["c"][i]/x["c"][i-90]-1
    return r90>0.05 and x["c"][i]>x["sma50"][i] and x["c"][i]>x["sma20"][i] and x["c"][i]<x["sma20"][i]*1.10
def x_rsmom(x,pos):
    i=x["i"]
    if x["sma50"][i] is None: return False
    return x["c"][i]<x["sma50"][i]

def s_rsimr(x):
    i=x["i"]
    if None in (x["sma200"][i],x["rsi"][i]): return False
    return x["c"][i]>x["sma200"][i] and x["rsi"][i]<35
def x_rsimr(x,pos):
    i=x["i"]
    return x["rsi"][i] is not None and x["rsi"][i]>55

def s_trendride(x):
    i=x["i"]
    if None in (x["sma20"][i],x["sma50"][i],x["sma200"][i],x["hh20"][i]): return False
    stack = x["sma20"][i]>x["sma50"][i]>x["sma200"][i]
    return stack and x["c"][i]>x["hh20"][i] and x["c"][i]>x["sma20"][i]
def x_trendride(x,pos):
    i=x["i"]
    if x["sma20"][i] is None: return False
    return x["c"][i]<x["sma20"][i]

def buyhold():
    trades=[]
    for code,kl in data.items():
        c=series(kl,"close"); dt=series(kl,"date")
        i0=210
        if len(c)<=i0+1: continue
        ret=c[-1]/c[i0]-1-FEE
        trades.append((dt[-1],ret/0.1,ret))  # R scaled vs ~10% move for comparability only
    return trades

strats=[
 ("Breakout55+vol", run("b55",s_breakout55)),
 ("Donchian20", run("d20",s_donchian20)),
 ("Pullback→SMA20", run("pb",s_pullback)),
 ("MA5x20 cross", run("mac",s_macross,tmax=60,custom_exit=x_macross)),
 ("RS momentum", run("rsm",s_rsmom,tmax=40,custom_exit=x_rsmom)),
 ("RSI<35 mean-rev", run("mr",s_rsimr,tmax=10,custom_exit=x_rsimr)),
 ("TrendRide(let run)", run("tr",s_trendride,tmax=120,custom_exit=x_trendride,atr_mult=2.0,rr=10.0)),
]

print(f"Basket: {len(data)} names | ~{min(len(v) for v in data.values())}-{max(len(v) for v in data.values())} daily bars (~18mo)")
print(f"{'Strategy':18} {'#tr':>4} {'win%':>5} {'avgW':>6} {'avgL':>6} {'exp(R)':>7} {'PF':>5} {'totR':>7} {'netRet':>7} {'maxDD(R)':>8}")
rows=[]
for name,tr in strats:
    m=metrics(tr)
    if not m: print(f"{name:18}  no trades"); continue
    rows.append((name,m))
    print(f"{name:18} {m['n']:>4} {m['wr']*100:>4.0f}% {m['aw']:>6.2f} {m['al']:>6.2f} {m['exp']:>7.3f} {m['pf']:>5.2f} {m['totR']:>7.1f} {m['totret']*100:>6.1f}% {m['mdd']:>8.1f}")
bh=metrics(buyhold())
print(f"{'Buy&Hold(basket)':18} {bh['n']:>4} {bh['wr']*100:>4.0f}% {'-':>6} {'-':>6} {'-':>7} {'-':>5} {'-':>7} {bh['totret']*100:>6.1f}% {'-':>8}")
print("\nRanked by expectancy (R per trade), min 20 trades:")
for name,m in sorted([r for r in rows if r[1]['n']>=20],key=lambda r:-r[1]['exp']):
    print(f"  {name:18} exp={m['exp']:+.3f}R  PF={m['pf']:.2f}  trades={m['n']}  maxDD={m['mdd']:.1f}R")
