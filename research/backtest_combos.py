import itertools
src=open("/tmp/claude-0/-home-claude/a3e2d022-832f-5b9d-b406-a491caa0a235/scratchpad/bt.py").read()
src=src.split("strats=[")[0]
exec(src)

# SPY series by date for regime + relative strength
spy_name=[k for k in data if "S&P 500" in k][0]
skl=data[spy_name]
spy_c={b["date"]:b["close"] for b in skl}
spy_dates=[b["date"] for b in skl]
spy_sma50=dict(zip(spy_dates, sma([b["close"] for b in skl],50)))
spy_idx={d:i for i,d in enumerate(spy_dates)}

def make(regime=False, vol=False, rs=False, notext=False):
    # entry fn needs date -> pass via closure over current kl
    def builder(kl):
        dts=[b["date"] for b in kl]
        def f(x):
            i=x["i"]
            if None in (x["sma20"][i],x["sma50"][i],x["sma200"][i],x["hh20"][i]): return False
            if not (x["sma20"][i]>x["sma50"][i]>x["sma200"][i]): return False
            if not (x["c"][i]>x["hh20"][i] and x["c"][i]>x["sma20"][i]): return False
            d=dts[i]
            if regime:
                s=spy_sma50.get(d)
                if s is None or spy_c[d]<=s: return False
            if vol:
                if x["vsma"][i] is None or x["v"][i]<1.2*x["vsma"][i]: return False
            if rs:
                j=spy_idx.get(d)
                if j is None or j<90 or i<90: return False
                r=x["c"][i]/x["c"][i-90]-1; rspy=spy_c[d]/spy_c[spy_dates[j-90]]-1
                if r<=rspy: return False
            if notext:
                if x["c"][i]>x["sma20"][i]*1.08: return False
            return True
        return f
    return builder

# run variant: need per-name entry fn, so wrap run()
def run_var(builder):
    trades=[]
    global data
    full=data
    for code,kl in full.items():
        data={code:kl}
        trades+=run("v",builder(kl),tmax=120,custom_exit=x_trendride,atr_mult=2.0,rr=10.0)
    data=full
    return trades

flags=["regime","vol","rs","notext"]
print(f"{'Combo':32} {'#tr':>4} {'win%':>5} {'exp(R)':>7} {'PF':>5} {'totR':>6} {'maxDD':>6}")
res=[]
for k in range(0,5):
    for combo in itertools.combinations(flags,k):
        kw={f:(f in combo) for f in flags}
        m=metrics(run_var(make(**kw)))
        name="base" if not combo else "+".join(combo)
        if not m: print(f"{name:32} no trades"); continue
        res.append((name,m))
        print(f"{name:32} {m['n']:>4} {m['wr']*100:>4.0f}% {m['exp']:>7.3f} {m['pf']:>5.2f} {m['totR']:>6.1f} {m['mdd']:>6.1f}")
