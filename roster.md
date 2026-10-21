# Council Roster and Division of Labour (owner order 2026-10-21)

Principle: each agent does only its own specialty. The Coordinator (Claude main session) does NOT do the analysis. It spawns the specialist agents, locks the plan, places paper orders, and keeps ledger, stops and watchlist.

| Role | Does | Model / effort | Tools |
|---|---|---|---|
| Research | Evening screen of the universe; company background check; analyst cross-check; after-close news pass | default model | moomoo quote_* (read-only), WebSearch/WebFetch, FMP |
| Sentiment | Filters Research's list by news confidence (0-100, >= 70 actionable, rumours dropped); hourly news watch while market open on held and staged names | sonnet (cheap, hourly) | quote_news_search, quote_stock_feed, WebSearch |
| Data & Quant | SPY regime; indicators; entry, stop (1.5xATR), T1, size; confirms breakouts before the close | opus 5.5, effort medium (owner order) | quote_history_kline, quote_stock_quote, quote_market_snapshot, Python; skills: quant-analyst, pandas-pro, statistical-analysis |
| Risk | Final YES/NO on risk: sizing, heat, events, correlation, regime, data quality | default model | read-only |
| Challenger | Fact-checks with a second source; tries to break the trade; VETO / NO VETO | default model | read-only, independent data source where possible |
| Coordinator | Locks plan, owner summary, places paper orders for cleared names, ledger, stops, watchlist, memory hub | main session | sim_trade_* (paper only) |

Rules for all agents: read-only, never place orders, never call trading_order_* or crypto_account_*. Reply in caveman-voice style (terse, answer first, no filler, all numbers exact). Max lines are set per step in routine.md. If data is missing say N/A, never estimate. Write the result to handoff/<step>_<YYYYMMDD>.md AND return it as the final report.

Skills agents may use (already installed): quant-analyst, market-researcher, deep-research, statistical-analysis, pandas-pro, python-pro, validate-data, xlsx. Do not load more than needed (usage).

Spawn rules (usage control): the hourly Sentiment/stop check runs only if a position is open or a name is staged. If nothing to watch, Coordinator logs "NO CHANGE" and spawns nobody. Risk and Challenger spawn only when a name is staged to trade.

## Trading skills library (tradermonty/claude-trading-skills, MIT, cloned 2026-10-21)
Location: /home/claude/council-skills/<skill>/SKILL.md (tests removed). Agents READ the SKILL.md for method and checklists. Scripts: run only with `python3 -I`, only no-network scripts unless a data key is set; never with live-broker keys. Alpaca/portfolio-manager is NOT installed (broker execution is out of scope). FMP-key scripts cannot run (no FMP_API_KEY in this environment); use their method with moomoo quote_* and FMP MCP data instead.
- Research: us-stock-analysis (fundamentals, valuation, business quality), canslim-screener (method), earnings-calendar, earnings-trade-analyzer, pead-screener (paper-test later), institutional-flow-tracker (method)
- Sentiment: market-news-analyst
- Data & Quant: technical-analyst, vcp-screener, breakout-trade-planner, position-sizer (local script, verified: no network), market-breadth-analyzer, uptrend-analyzer, ftd-detector, market-top-detector
- Risk: drawdown-circuit-breaker, pre-trade-discipline-gate, exposure-coach, position-sizer
- Challenger: data-quality-checker, signal-postmortem
- Coordinator: trader-memory-core (thesis lifecycle), trade-performance-coach
Rule: the council charter overrides any skill default (risk 1%, position <= 20%, stop 1.5xATR, T1 >= 3R, whole shares).

## Merged role playbooks (charter + repo skills), built 2026-10-21 - READ THESE FIRST
Each agent reads ONLY its own playbook at the start of its step (instead of loading the individual repo skills; saves usage). Charter.md still overrides everything.
- Research: /home/claude/council-skills/_merged/council-research/SKILL.md
- Sentiment: /home/claude/council-skills/_merged/council-sentiment/SKILL.md
- Data & Quant: /home/claude/council-skills/_merged/council-quant/SKILL.md
- Risk: /home/claude/council-skills/_merged/council-risk/SKILL.md
- Challenger: /home/claude/council-skills/_merged/council-challenger/SKILL.md
- Coordinator: /home/claude/council-skills/_merged/council-coordinator/SKILL.md
Playbook additions NOT in the owner's original orders (owner may veto): Risk: 70% advisory exposure ceiling in RANGE, 24h cooldown after 2 consecutive losing closes, 5-trading-day block on re-entry after a stop-out, default 10-trading-day hold when not stated, chase test (price <= trigger + 0.5 ATR). Research: 0-2 scorecard with PASS >= 70%, FAIL < 50%, extra FAIL triggers labelled "added". Sentiment: SPY tone amber below -1%, red below -2%. Coordinator: markdown thesis notes in /home/claude/council-hub/theses/ instead of trader-memory-core script; half size after 2 losses.
