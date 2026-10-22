---
name: council-options
description: Options skills for every council role (paper account, long calls and puts only): Greeks, IV, liquidity, contract choice, earnings/IV crush, exits, moomoo tool use, per-role checklists.
---
# council-options (all roles read this plus own playbook; options.md and MODE.md override)
Instrument: LONG calls/puts only, defined risk = premium. Paper acc 428122, market 100. Never short options.

## 1. Core knowledge
- Option price = intrinsic + time value. 1 contract = 100 shares. Premium $ = quote x 100 x contracts.
- Delta: ~ chance of finishing in the money and $ move per $1 in the stock. Use 0.40-0.60 (near the money). <0.30 = lottery, >0.70 = expensive stock substitute.
- Theta: time decay, accelerates in the last 30 days and worst near expiry. Buy 14-45 DTE, exit by 5 DTE. Never hold a weekly into the last 2 days.
- Vega/IV: option price rises/falls with implied volatility. Buying when IV is high = overpaying; a fall in IV hurts even if the stock moves our way. Check IV vs 3-month average and vs historical volatility (quote_option_volatility). IV > HV by a lot and rising into an event = skip.
- Earnings/IV crush: IV collapses right after earnings. Never hold through the underlying's print; no entry within 3 trading days before it.
- Gamma: near the money, delta changes fast; good for winners, fast loser too.
- Break-even: calls = strike + premium; puts = strike - premium. The stock must move beyond it before expiry. Require the planned move (T1 level) to exceed break-even by a margin; if break-even is beyond the next resistance/support level, reject.
- Liquidity: open interest >= 500 at the strike, bid-ask spread <= 10% of mid (reject wider; the spread is a hidden cost). Entry at mid or slightly above with a LIMIT order; never market. Re-quote before sending.
- Fees: USD 0.50 per contract per side + ~0.10 regulatory. Round trip ~USD 1.20/contract; must be <= 5% of TP1 gain.
- Assignment/exercise: long options only; no early-exercise issue. Never hold to expiry. Close before expiry day.
- Dividends: calls on a stock about to go ex-dividend can be hurt; check ex-div date (Research).
- Calls vs puts: calls need uptrend (daily+60m up), puts need downtrend (daily+60m down); mixed = no trade.

## 2. Contract selection procedure (Quant)
1. quote_option_expiration_date -> pick expiry 14-45 DTE (standard only), not spanning earnings.
2. quote_option_chain for that expiry (output is huge: save to file, parse with python; do not print).
3. For candidate strikes get quote_stock_quote on the option code (bid, ask, delta, OI, IV) and quote_option_volatility.
4. Pick delta 0.40-0.60, OI >= 500, spread <= 10%; compute premium, break-even, stop (-50%), TP1 (+60%), fee %, contracts that fit cash.
5. State planned hold in days and the underlying level that invalidates the trade.
Order code format: no "US." prefix (e.g. AAPL261120C100000). qty = contracts. LIMIT only. First order: verify side enum and fill via sim_trade_history_order_list; check sim_trade_max_buy_sell before sending.

## 3. Exits (Coordinator)
Stop -50% of premium; TP1 +60% sell half; trail the rest -30% from the high; time exit at 5 DTE; exit if the underlying closes through the invalidation level; never average down, never roll a loser. Option bid is what you get: judge P/L at the BID, not mid.

## 4. Role checklists
- Research: earnings date confirmed (company PR), ex-div, analyst tone, insider/short interest, crypto-linked names: ETF flow/MSTR premium. Reject unconfirmed earnings dates inside the hold.
- Sentiment: news that moves IV or gaps the stock (guidance, FDA, legal, macro); flag any event inside the hold; hourly check on held names.
- Quant: section 2; also VWAP/EMA9 filter (veto only), multi-timeframe alignment, POC/yesterday hi-lo as levels.
- Risk: recompute premium and contracts; spread, OI, delta, DTE window, IV level, break-even vs level, fees %, events, regime, drawdown guards (options.md OWNER OVERRIDE), data quality. Doubt = NO.
- Challenger: second-source the option quote (spread real?), IV, earnings date; try to break the trade (what if IV drops 20%? what if the stock stalls 5 days: theta cost $?). VETO if the thesis needs the move to happen fast.
- Coordinator: limit orders, verify fills, ledger, stops at every check, fees logged, reports with expectancy.

## 5. Quick math (do it, do not estimate)
Theta cost over a stall: premium decay ~ premium/DTE per day on average, faster late. Stall scenario: stock flat for the planned hold -> loss approx theta x days; reject if that loss > 25% of premium.
IV drop scenario: vega x 5 vol points; ask moomoo greeks or approximate with the option's IV change; reject if the combined stall+IV scenario breaches the -50% stop.
