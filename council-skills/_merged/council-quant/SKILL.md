---
name: council-quant
description: Data & Quant playbook for the paper-trading stock council - SPY regime, per-candidate indicators, entry/stop/T1/size, Q1 plan and Q2 near-close confirmation, all under charter.md rules.
---
# Council Data & Quant (Q1, Q2)
## 0. Role and authority
- Read-only. Never place/modify orders. Never call sim_trade_*, trading_order_*, crypto_*. Coordinator trades.
- Charter beats every skill default. Overlays below change CONFIDENCE and DEPLOYMENT only; never override the charter regime gate or sizing.
- Terse output. Numbers exact. Missing = N/A, never estimate. Every figure: source + as-of date (bar date, not today).
- Write handoff/quant_YYYYMMDD.md (Q1) or quant_confirm_YYYYMMDD.md (Q2) AND return it.

## 1. Data procedure
1. quote_market_state first. Market closed/holiday -> report and stop. Note early close.
2. quote_history_kline: daily bars, >= 260 sessions, split/dividend-adjusted (forward adj); SPY plus each candidate. Need >= 252 bars else field = N/A.
3. quote_stock_quote (last, day volume, time) and quote_market_snapshot (52w hi/lo, avg vol, prev close, market cap) for live fields.
4. Drop today's bar from indicators if market open or bar incomplete; state "as-of last full close D".
5. Cross-check (second source, FMP quote/chart or Massive): last close within 0.5%, 20d avg volume within 10%. Mismatch -> flag DATA FAIL, no entry numbers for that name.
6. Stale: last bar older than 1 trading day -> DATA FAIL. Zero/gap bars, volume 0 -> DATA FAIL.
7. Compute with `python3 -I` (pandas/numpy). Save scripts in scratchpad, not in data dirs. Wilder smoothing for RSI/ATR.
8. Round: prices 2dp, ratios 2dp, % 1dp.

## 2. SPY regime (daily closes)
Definitions:
- SMAn = mean of last n closes. SMA50 slope5 = SMA50(t) - SMA50(t-5); rising if > 0, falling if < 0.
- rvol20 = stdev of last 20 daily log returns x sqrt(252). Percentile = share of the last ~252 rvol20 values <= today's (0-100).
- ATR14 = Wilder average of true range; also ATR%=ATR14/close.
- 52w hi/lo = max high / min low over 252 sessions; report % below hi, % above lo.
Charter verdict (apply in order):
1. RISK-OFF if (close < SMA50 AND slope5 < 0) OR rvol20 pct > 90. -> no new entries, deployment target 50%.
2. TREND if close > SMA50 AND slope5 > 0.
3. Else RANGE.
Also print: close vs SMA20/SMA200, SMA20>SMA50>SMA200 stack yes/no.
Overlays (compute, report, never flip verdict):
- A. Distribution days (market-top-detector/O'Neil), SPY: count sessions in last 25 where close <= prior close x 0.998 AND volume > prior day volume. Drop a day if SPY later closes >= 5% above that day's close. 0-2 normal; 3-4 YELLOW: confidence down one notch, require volume >= 1.5x on breakouts; 5-6 ORANGE: only strategy (b)/(c) with A-grade setups, deployment cap 75% of whatever charter allows; >= 7 RED: recommend NO TRADE.
- B. Top-risk signs (any 2+ = confidence LOW): SPY made 52w high within 10 sessions then lower high with distribution; close < SMA20 twice in last 5 sessions; breakout failures (a-names in watchlist back below pivot within 3 days) >= 2; SMA20 turning down while SPY within 3% of 52w high; rvol20 pct > 75 and rising.
- C. Breadth proxy (breadth-analyzer/uptrend ideas; no CSV fetch). From a fixed basket (SPY + sector ETFs XLK XLF XLV XLY XLP XLE XLI XLU XLB XLRE XLC; all via kline): % above own SMA50 and % above SMA200; cyclical (XLK XLY XLI XLF XLB XLE) vs defensive (XLP XLU XLV XLRE) 20d return spread. Health score = round(100 x (0.5 x pct>SMA50 + 0.3 x pct>SMA200 + 0.2 x [cyclical-defensive 20d spread > 0])). Zones: >=80 strong, 60-79 healthy, 40-59 neutral, 20-39 weak, <20 critical. Effect: strong/healthy = no change; neutral = confidence MED, prefer 4 positions max; weak = confidence LOW, new entries only top-1 setup, parking in SPY not allowed; critical = recommend NO TRADE. Label as proxy, not the repo score.
- D. Follow-through day (ftd-detector), only if SPY fell >= 3% from a 20d high with 3+ down days: swing low = lowest close; rally day 1 = first up close after it; FTD = day 4-10 with gain >= +1.25% on volume > prior day, and no close below swing low. FTD confirmed raises confidence one notch but cannot lift a RISK-OFF gate; gate lifts only when charter conditions clear. Close below FTD-day low = FTD invalid, confidence LOW. No qualifying correction -> "D: n/a".
Confidence = HIGH/MED/LOW: start HIGH if TREND, MED if RANGE, LOW if RISK-OFF; subtract one notch per overlay flag (A yellow+, B, C neutral/weak), floor LOW. HIGH may add +1 notch only via D.
Print one regime block: verdict, numbers, overlays A-D, confidence, deployment (RISK-OFF 50%; otherwise charter default) and "overlay adds: ...".

## 3. Per-candidate indicator set (last full close; N/A if < 252 bars)
- SMA20/50/200, price vs each (% distance); SMA50 slope5.
- RSI14 (Wilder). ATR14, ATR% = ATR14/close.
- High55 = max high of prior 55 sessions (excluding today); dist55 = close/High55-1. Donchian20/55 upper = prior 20/55 day highs, lower = lows.
- Volume ratio = last volume / mean of prior 20 volumes (exclude today).
- Returns 30d, 90d (close/close[-30 or -90]-1) and excess vs SPY same windows. RS pass = both excess > 0.
- Bollinger(20,2) width = (upper-lower)/SMA20; percentile over 252 sessions (low = squeeze, <20 pct).
- Corr30 = Pearson of last 30 daily returns vs SPY. Between held/staged names corr30 > 0.85 = one position for heat.
- Universe re-check: price > 5, 20d avg vol > 1M, mcap > 2B (snapshot). Fail -> drop.
Strategy tests (charter; label which one fits):
(a) Breakout: close > High55 AND vol ratio >= 1.3 AND close > SMA50 AND RSI14 55-75. Prefer VCP base (below). Skip if close > pivot x 1.02 (chase; pre-trigger plan instead).
(b) Pullback: close > SMA200; low touched SMA20 or SMA50 within last 3 sessions (within 1 ATR); RSI14 turned up (today > yesterday, and prior-3-day min < 50 or SMA touch); close back above prior day high or SMA20.
(c) Relative strength: both excess returns > 0 (rank top among survivors), close > SMA50, RSI14 < 80, dist55 >= -5%.
VCP detection (vcp-screener, simplified, 120 sessions):
1. Stage 2: close > SMA50 > SMA150(or SMA200), SMA200 rising 20d, close >= 25% above 52w low and within 25% of 52w high.
2. Swing pivots from ATR zigzag (reversal >= 1.5 x ATR14). Contraction depth = (swing high - next swing low)/swing high.
3. Need >= 2 contractions, each depth <= 0.70 x previous; T1 depth 10-35%; last depth <= 15% (>15% = wide-and-loose, reject). Ideal 3+ and last <= 10%.
4. Volume dry-up: mean volume of last 10 sessions <= 0.8 x mean of prior 50; best: lowest-volume day in last 10 and last-base-day vol < 0.6 x avg.
5. Pivot = highest high of the final contraction (absolute resistance). State: Pre-breakout (close within 3% under pivot), Breakout (close > pivot, vol ratio >= 1.5), Extended (> 2% over pivot: no chase), Damaged (close < last contraction low).
Grade: A = all 5 pass + 3 contractions + RS pass; B = valid, 2 contractions; else not VCP (can still qualify under (b)/(c)).

## 4. Trade levels (charter + breakout planner merged)
- Trigger = pivot (VCP) or High55 (non-VCP) + 0.1%, rounded up to 0.01. Entry = trigger x 1.001 (0.1% slippage in). Chase cap: entry <= pivot x 1.02.
- (b) Pullback: trigger = prior-day high + 0.01; entry as above.
- Stop = entry - 1.5 x ATR14 (charter, never the VCP low). If the structural low (last contraction low) is higher than that stop, report it as info only; if lower than the stop, keep 1.5ATR and note "stop inside base".
- Risk/share R = entry - stop. Stop % = R/entry. Reject if > 12% (planner own cap 8%: flag HIGH-RISK if > 8%, still allowed by charter).
- T1 = entry + 3R (min). If a resistance/52w high sits below T1, report it; reject if nearest resistance < entry + 2R.
- Worst-case entry (planner idea): trigger x 1.02 (chase cap). Recompute R, shares, risk at worst-case entry; the trade passes only if risk at worst-case entry <= $10 after resizing (shares sized on worst case when it differs). Gap-risk: 2 x stop-distance loss on this position + open risk <= 8% ($80).
- Order mode for Coordinator: BUY limit at trigger..worst-case after Q2 confirmation (no resting stop-limit needed; sim limit/market only).

## 5. Sizing procedure (ledger equity E, start $1000)
1. risk$ = 1% x E = $10 (half if drawdown ladder at <= $950; none <= $920).
2. shares = floor(min(risk$/R, 0.20 x E / entry)). Whole shares.
3. cost = shares x entry. Reject if cost < $20 or shares = 0 ("too expensive for ledger").
4. Fees: slippage 0.1% each way = 0.002 x cost. Require fees < 20% of (T1-entry) x shares.
5. Risk$ actual = shares x R (+ fees). Heat = sum risk$ of open + this + proposed; must be <= $60 (6%). Gap rule: heat + 1 further R on largest position (2x-stop gap) <= $80. Corr30 > 0.85 pair counts as one position. Max 5-6 positions, 2/sector, 40% equity/sector, total value <= E.
6. Cross-check: `python3 -I /home/claude/council-skills/position-sizer/scripts/position_sizer.py --account-size 1000 --risk-pct 1 --max-position-pct 20 --entry X --stop Y --output-dir <scratchpad>` (it writes report files; whole shares by default). Shares must match step 2; mismatch -> recompute, report "SIZER MISMATCH".
7. Report: shares, cost, % equity, risk$, R:R (to T1), heat before/after.
Events: no entry within 3 trading days before earnings, ex-div, CPI/FOMC/jobs/GDP/PCE (FOMC 2026-10-28, GDP/PCE 2026-10-29). Flag, do not trade.

## 6. Q1 output (max 30 lines, handoff/quant_DATE.md)
L1 header: Q1 date | data as-of | sources.
L2-6 Regime: verdict, SPY close/SMA20/50/200, slope5, rvol pct, ATR, 52w. Overlays A-D, health score, confidence, deployment.
Per survivor (2-3 lines each, max 6): TICKER strat (a/b/c) VCP grade | close, RSI, ATR%, vol x, RS30/90 vs SPY, corr30 | trigger / entry / stop / T1 (price, %R) | shares, cost, risk$ | R:R, heat after | flags (events, DATA, corr, stop%).
Final lines: Heat total, Cash left, Rejects (ticker: reason), "NO TRADE" if nothing passes, Data cross-check result.

## 7. Q2 near-close confirmation (max 15 lines, ~06:15 AEDT = 15 min before close; handoff/quant_confirm_DATE.md)
1. quote_market_state: still open. Early close -> shift.
2. Pull quote_stock_quote and today's intraday (quote_cur_kline 1m/5m) for each staged name; N/A if missing.
3. Price vs trigger: PASS only if last >= trigger and <= worst-case entry. Above worst-case = NO CHASE. Below trigger = NOT TRIGGERED.
4. Volume pace: projected full-day volume = today's volume so far / typical cumulative share of daily volume at this clock time. Use the 20-day intraday profile if available; else U-shape default (cum 85% by 15:45 ET, 90% by 15:55). Pace ratio = projected / 20d avg. (a) needs >= 1.3; (b) >= 0.8 with reversal bar; (c) >= 1.0.
5. Close-based: last must hold in the top 40% of day range and above trigger at 15:50 ET; a new low after 15:30 ET voids. Breakout valid only on daily close above pivot.
6. Invalidation: last < pivot, or last within 0.25R of the stop, SPY down > 1% on the day, SPY newly RISK-OFF, price gapped above worst-case, halt, bad data.
7. Re-run size at live price; shares must still pass section 5.
Line each name: TICKER CONFIRMED/FAILED/NO CHASE | last, trigger, range pos | vol pace x | final shares/stop/T1. Last line: SPY tone + regime unchanged?

## 8. Edge cases
- Gap up over worst-case entry: NO CHASE, re-plan next cycle. Gap down through stop: report actual, never widen stop; sim fill may be worse.
- Halt / LULD / no quote: N/A, no confirm, tell Coordinator.
- Stale data / failed cross-check: DATA FAIL, safety event, full detail.
- Earnings, ex-dividend, macro inside 3 days or hold: flag, no new entry; dividend/split adjusts price history - use adjusted bars and recheck stop.
- Splits or odd prices: recheck bars for a jump > 40%.
- Partial session (early close, holiday week): volume ratios unreliable, mark LOW confidence.
- Price too high for $200 cap (shares = 0): reject.
