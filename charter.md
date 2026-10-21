# Stock Council Charter (paper trading) - v1, set 2026-10-21

## Account
- Broker: moomoo simulated account "US Margin Account [Paper Trading]", acc_id 428122, market_id 100 (US).
- moomoo preloads $1,000,000 sim cash and 2x margin. The council treats it as a $1,000 cash-only LEDGER (ledger.csv). Total position value must never exceed ledger equity ($1,000 + realised P/L). No margin, no shorts, no options.
- PAPER ONLY. Only sim_trade_* tools may place orders. NEVER use trading_order_*, crypto_account_*, or any live order tool. "LIVE STOCK" has not been authorised by the owner.
- Only the Coordinator places, modifies or cancels paper orders. All other agents are read-only (quote_* and web).

## Sizing and risk (percent of ledger equity, $1,000 start)
- Risk per trade <= 1% ($10). Position <= 20% ($200). Max 5-6 open positions. Cash target <= 5% idle; extra parked in SPY only if regime allows.
- Size = min($10 / (entry - stop), $200), whole shares. Reject if size < $20 or stop wider than 12%.
- Stop = entry - 1.5 x ATR(14). First target T1 >= 3R.
- Total open risk <= 6% ($60). Gap rule: open risk + a 2x-stop gap on any ONE position <= 8% ($80).
- Max 2 positions per sector, max 40% of equity in one sector. Correlated names (30d corr > 0.85) count as one position for heat.
- Daily loss halt 2% ($20), weekly halt 5% ($50). Drawdown ladder: -5% ($950) halve new size; -8% ($920) no new entries; -12% ($880) flat everything and report to owner.
- Fees: est. $0 commission + 0.1% slippage each way. Fees must be < 20% of T1 gain.
- No weekly profit target. NO TRADE is a valid result. Never trade to hit a deployment goal.

## Regime gate
SPY daily: SMA20/50/200, SMA50 5-day slope, 20d vol percentile. RISK-OFF = below SMA50 and SMA50 falling, or vol percentile > 90 -> no new entries, deployment target 50%. TREND = above SMA50 and rising. Else RANGE.

## Strategies allowed
(a) trend breakout: daily close above 55-day high, volume >= 1.3x 20-day avg, above SMA50, RSI 55-75.
(b) pullback in uptrend: above SMA200, dips to SMA20/50, RSI recovering.
(c) relative strength vs SPY (30d and 90d), above SMA50, RSI < 80.
Post-earnings drift and index dip-buying are NOT enabled yet (paper-test later, one at a time).
Universe: US-listed, price > $5, avg volume > 1M shares, market cap > $2B. No OTC, penny, leveraged/inverse ETFs. Index ETFs allowed.

## Events
No new entry within 3 trading days before earnings, ex-dividend, or major macro (CPI, FOMC, jobs, GDP/PCE). Known: FOMC decision 2026-10-28 2pm ET; GDP/PCE 2026-10-29.

## Profit lock (R = entry minus initial stop)
Stage 1 at +1R: stop to breakeven plus fees. Stage 2 at +2R: stop to entry + 1R. Stage 3 at +3R (T1): sell half, trail the rest at highest close - 2 x ATR. Stops only move up, only on a daily close (Stage 1 may be set once +1R is touched). Never widen or remove a stop. Ledger records stop history and "what a fixed stop would have done".
Note: sim order types seen are limit and market. If moomoo sim has no resting stop order, the Coordinator enforces stops at each routine check with a market sell, and records the actual fill.

## Company background check (Research, mandatory BEFORE any individual stock is cleared)
Sources: moomoo quote_company_profile, quote_financials_statements, quote_valuation_detail, quote_research_analyst_consensus, quote_research_rating_summary, quote_research_morningstar_report, quote_financials_earnings_price_move, quote_short_interest, quote_insider_trade_list, quote_shareholders_*, quote_corporate_actions_dividends, quote_news_search; plus web search for gaps. Cite source and date.
Checklist: (1) business and sector in 2 lines; (2) last 4 quarters earnings and revenue vs estimates, growth rate; (3) P&L: revenue, gross/operating/net margin trend; (4) balance sheet: cash, debt, current ratio; cash flow/FCF; (5) valuation: P/E, forward P/E, PEG, P/S, EV/EBITDA vs own 5y range and sector median; (6) ownership: insider trades last 90d, institutional change, short interest % float; (7) upcoming events: earnings date, ex-dividend, legal/regulatory; (8) news last 30 days with source quality.
Analyst cross-check: rating mix (buy/hold/sell), mean and range of price targets vs price, target revisions last 30-90d, Morningstar view; say whether analysts AGREE or DISAGREE with the technical setup.
Verdict: PASS / WATCH / FAIL in 5 lines. Automatic FAIL: earnings or ex-dividend inside the hold window; net loss widening with negative FCF and cash < 4 quarters of burn; consensus mostly Sell or mean target below price; clustered insider selling; short interest > 20% of float; unresolved material legal/regulatory shock; fails universe rules. ETFs: check holdings concentration, expense ratio, top-10 weight, and top holdings' earnings dates instead.

## Reporting
Owner gets ONE message per cycle, Coordinator only. Quiet cycle = one line "NO CHANGE | reason | next check". Safety events (stop hit, rule break, data FAIL, ledger mismatch) are never shortened.
