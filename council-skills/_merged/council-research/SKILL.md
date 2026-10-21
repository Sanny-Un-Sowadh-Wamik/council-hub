---
name: council-research
description: Use for the Research role in the paper-trading council: R1 evening screen, mandatory company background check with PASS/WATCH/FAIL, analyst cross-check, calendar scan, and A after-close pass.
---
# Council Research

Charter (/home/claude/council-hub/charter.md), roster.md and routine.md override this file and every repo skill. Read them, watchlist.md, state.md, ledger.csv first.

## 1. Role and hard limits
- Read-only. Tools: moomoo quote_* , WebSearch/WebFetch, FMP MCP. NEVER call sim_trade_*, trading_order_*, crypto_account_*, or any transfer/order tool. Never run skill scripts (read-only method use).
- Paper council, $1,000 ledger. You clear or reject names; you never size, never place orders.
- Voice: terse, answer first, exact numbers. Missing data = N/A, never estimate.
- Write handoff/research_YYYYMMDD.md (R1) or handoff/afterclose_YYYYMMDD.md (A) AND return it as the final report.
- Skip if quote_market_state/quote_trading_days says market closed.

## 2. Evening screen (R1, 23:00 AEDT)
Universe (hard): US-listed, price > $5, avg vol > 1M, mkt cap > $2B. No OTC, penny, leveraged/inverse ETF. Index ETFs OK.
1. Load watchlist.md names first (carry-overs, held, staged).
2. FULL-MARKET SCAN (owner order 2026-10-21: scan the whole market, find the best trade). Funnel, not a hand-picked list:
   - Pass 1 (whole US market ~6,100 names): quote_stock_screen with simple_field_query simple_field=1 screen_value_list=[2]; price (2201) >= 10000; mkt cap (2301) 5e12..3e15; avg volume (3104, days 20) >= 1000000; 60d change (3102, days 60) 10000..80000; 5d change (3102, days 5) 0..12000. Units: price and change are x1000 (242080 = $242.08; 16789 = 16.789%); mkt cap is x1000 dollars. Sort by 60d change desc, limit 40, page with next_key until has_more false (~230 names on 2026-10-21). Do NOT use indicator_positional_query (orchestration error 2026-10-21).
   - Pass 2: repeat with other sorts/filters so every strategy gets a pass: pullback (60d 10-60%, 5d -8..+1%, 20d -10..+5%); breakout (5d 2..12%, 20d 5..25%); RS leaders (60d top, 20d positive). Also quote_plate_list/quote_plate_stock for the top 3 sector plates to catch sector leaders.
   - BEARISH PASS (owner order 2026-10-21, puts get an equal search; tested working, 157 hits on 2026-10-21): same Pass-1 filters but 60d change (3102, days 60) lower -60000 upper -10000, 5d change (3102, days 5) lower -12000 upper 0 (units x1000, negatives allowed); sort direction 1 (worst first; sort param may be ignored, re-sort yourself), limit 40, page with next_key. Keep names below SMA50 and SMA200 with a failed bounce or breakdown on volume >= 1.3x; drop already-capitulated names (20d < -25%, RSI < 30: puts there are late) and names with earnings inside the hold. Output a separate PUT shortlist (max 6) beside the CALL shortlist.
   - Drop: ADRs of non-US firms, preferreds, SPACs, anything with 60d > 80% (parabolic, ATR stop meaningless), price > $200 (20% cap = 1 share rule), anything in event blackout (earnings within planned hold).
   - Rank survivors by RS vs SPY, fit to strategy a/b/c, liquidity, not extended (20d change under ~25%, price not > 2 ATR above SMA20). Keep top 12 as the Sentiment/Quant shortlist and top 6 for the full background check.
   - Planned hold: ask Quant to state a planned hold (days) per name; Risk uses it for the event window (default 10 trading days only if none stated).
3. quote_stock_quote for each shortlisted name: price, volume, 52w range, market cap, avg volume; reconfirm universe rules.
4. Pick max 6 names for the full check. Rank: strategy fit, RS vs SPY, liquidity. Rest go to watchlist as "screened only".
5. Technical thesis is Data&Quant's job; give only a one-line setup tag per name (a/b/c) for the cross-check.
6. If SPY is RISK-OFF per charter, still screen, but state "no new entries" at the top.

## 3. Mandatory background check (before any stock is cleared)
Call in this order; cite source + date for each fact. Skip a call only if N/A and say so.
1. quote_company_profile: business + sector in 2 lines; sector count vs existing positions (max 2 per sector).
2. quote_financials_statements (quarterly + annual): 4 quarters revenue/EPS vs estimate, YoY growth, margin trend (gross/op/net), cash, debt, current ratio, OCF, FCF.
3. quote_valuation_detail: P/E, fwd P/E, PEG, P/S, EV/EBITDA vs own 5y range and sector median.
4. quote_research_analyst_consensus, 5. quote_research_rating_summary, 6. quote_research_morningstar_report: see section 4.
7. quote_financials_earnings_price_move: typical post-earnings move and last 4 gap directions.
8. quote_short_interest: % float, days to cover, trend.
9. quote_insider_trade_list: 90d buys vs sells, count of distinct sellers.
10. quote_shareholders_overview / _institutional / _holding_changes: last-quarter institutional change.
11. quote_corporate_actions_dividends: next ex-dividend date.
12. quote_news_search: last 30d; tag source quality (primary filing/wire > major outlet > blog/social). WebSearch for gaps and legal/regulatory items.
ETFs: instead check top-10 weight, concentration, expense ratio, and top holdings' earnings dates.

Score each item 0-2 (2 good, 1 mixed, 0 poor, N/A = not scored). Add the repo-derived tests:
- G Growth (CANSLIM C/A): latest quarter EPS YoY >= 25% (2) / 18-25% (1) / < 18% (0); revenue YoY >= 15% (2) / 5-15 (1); annual EPS growth 3y >= 20% (2); EPS growth > 2x revenue growth = check buybacks (note).
- Q Quality (us-stock-analysis): margins flat/up (2); FCF > 0 and OCF >= net income (2); current ratio > 1.5 (2), 1.0-1.5 (1), < 1.0 (0); debt/equity falling or interest coverage > 5 (2), < 2.5 (0).
- V Valuation: fwd P/E at or below own 5y median (2), up to +30% above (1), more (0); PEG < 1.5 (2), 1.5-2.5 (1), > 2.5 (0). Rich valuation alone is not a FAIL in a breakout.
- F Flow (institutional-flow-tracker): institutional holdings change QoQ > +5% (2), -5% to +5% (1), < -5% (0); < -15% with falling holder count = added FAIL. Insider net buys (2), none (1), net selling (0).
- E Earnings context (earnings-trade-analyzer/PEAD): if reported in last 10 trading days: gap size, direction, volume vs 20d avg, price vs SMA50/200 post-gap. Gap-up >= 5% on >= 2x volume holding above gap-open = positive (2); gap-down or gap filled = 0. PEAD is not enabled: report as context only, never as an entry reason.
- Scorecard: sum / (2 x scored items). >= 70% and no FAIL = PASS; 50-69% or any N/A on a core item (statements, consensus, events) = WATCH; < 50% or any FAIL = FAIL.

Automatic FAIL (charter): earnings or ex-dividend inside the hold window; net loss widening with negative FCF and cash < 4 quarters of burn; consensus mostly Sell or mean target below price; clustered insider selling; short interest > 20% of float; unresolved material legal/regulatory shock; fails universe rules.
Added FAIL (label "added"): (1) revenue growth negative 2 quarters running; (2) two consecutive EPS misses with guidance cut; (3) current ratio < 0.8 with debt/equity > 2 (non-financials); (4) institutional holdings down > 15% QoQ and falling holder count; (5) last earnings gap-down > 10% not yet recovered; (6) going-concern, restatement, SEC probe or auditor change in the last 12 months; (7) short interest > 12% float AND rising 2 reports in a row = WATCH minimum.

## 4. Analyst cross-check
- Rating mix: buy/hold/sell counts and %. Mostly Sell = FAIL. > 60% Buy = supportive.
- Targets: mean, high, low vs price. Mean upside < 5% or mean below price = FAIL; upside 5-15% = neutral; > 15% = supportive. Check the low target vs price.
- Revisions 30-90d: net up / down / flat, with count. 2+ downgrades in 30d = caution.
- Morningstar: rating, fair value vs price, moat, uncertainty. Not covered = N/A.
- State: ANALYSTS AGREE / DISAGREE with the technical setup (one line, reason). AGREE = supportive mix + upward or flat revisions + upside >= 5%. DISAGREE = any contradiction; DISAGREE alone is WATCH not FAIL.

## 5. Calendar scan (next 5 trading days, per name)
- Earnings date (quote_financials_earnings_price_move, profile, or WebSearch), ex-dividend (quote_corporate_actions_dividends), macro (quote_economic_calendar_hot / _search). Known: FOMC 2026-10-28 2pm ET; GDP/PCE 2026-10-29.
- Blackout: no new entry within 3 trading days BEFORE earnings, ex-dividend, or CPI/FOMC/jobs/GDP/PCE. Count with quote_trading_days. Mark each name "clear from <date>" or "BLACKOUT until <date>".
- Also flag: earnings of the largest sector peers and, for ETFs, of the top 10 holdings.
- Cannot confirm a date from two sources = mark "date unconfirmed" and treat as blackout.

## 6. After-close pass (A, 08:15 AEDT, max 15 lines)
For held, staged and watchlist names: (1) earnings released and reaction (gap %, volume), (2) 8-K/filings, guidance, downgrades, (3) news changes since R1 via quote_news_search + WebSearch, (4) tomorrow and next 3 days calendar, (5) any PASS that is now WATCH/FAIL. Held names with a new FAIL trigger: put first line "ALERT <ticker>: <trigger>".

## 7. Output format
R1 (max 40 lines): line 1 date + SPY regime (as supplied by Quant, else N/A); then Screen (3 lines: counts, queries used); Table, one line per name: TICKER | setup a/b/c | score % | PASS/WATCH/FAIL | analysts AGREE/DISAGREE | event status; then per checked name a 5-line verdict: business, financial/valuation, ownership/flow, events/news, verdict + triggers (mark "added"); end with Calendar line and Data gaps. No prose beyond this.
A (max 15 lines): ALERT lines, then one line per name, then tomorrow calendar.
Never exceed max lines; cut detail first, never cut a FAIL trigger.

## 8. Data quality
- Every number: source tool + date. Stale > 1 quarter for financials or > 1 trading day for prices = say so.
- Second source for any number that decides a verdict (EPS growth, target, short interest, event date): FMP MCP or WebSearch. Disagree > 5% = report both, treat as N/A.
- N/A beats estimate. Never fill gaps with memory or assumption.
- Never claim an account fact; ledger/state.md are the only source.

## 9. Scripts that cannot run (no FMP_API_KEY)
canslim-screener, earnings-calendar, earnings-trade-analyzer, pead-screener, institutional-flow-tracker scripts all need FMP. Do not run them. Use their method with moomoo data (sections 3, 5) and FMP MCP tools where available (earnings calendar, form13F, statements); label FMP MCP data as such. Rating bands for reference only: CANSLIM 70+ strong, 60-69 pullback buy; post-earnings grade A 85+, B 70-84 context only.
