# Daily Routine (Melbourne AEDT, UTC+11). Weekdays ET sessions only.

US session 9:30-16:00 ET = 00:30-07:00 AEDT while US is on daylight time (until Nov 1, 2026). From Nov 2, 2026 the US session is 01:30-08:00 AEDT: shift every time below +1 hour. Check quote_trading_days / quote_market_state for holidays and early closes; skip the cycle if the market is closed.

Cycle runs Mon-Fri evenings AEDT (for the Tue-Sat morning session). Start of cycle: read charter.md, roster.md, watchlist.md, state.md, ledger.csv.

| Step | AEDT | Owner | Task | Output |
|---|---|---|---|---|
| R1 | 23:00 | Research | FULL-MARKET SCAN of all ~6,100 US stocks via moomoo quote_stock_screen funnel (recipe in council-research playbook section 2) plus watchlist; shortlist 12, full check max 6. Full background check + analyst cross-check on max 6 names. Calendar: earnings/ex-div/macro in next 5 trading days. Max 40 lines. | handoff/research_DATE.md |
| S1 | 23:15 | Sentiment | Filter Research's list: news confidence per name, drop rumours, flag HIGH impact. Max 20 lines. | handoff/sentiment_DATE.md |
| Q1 | 23:20 | Data & Quant | SPY regime; for each survivor entry trigger, stop (1.5xATR), T1 (3R), shares (min $10 risk, $200), R:R, volume condition. Max 30 lines. | handoff/quant_DATE.md |
| C1 | 23:35 | Coordinator | Lock plan: staged names with triggers. Send owner summary (<= 10 lines). Update state.md and watchlist.md. | handoff/plan_DATE.md |
| H | 01:00,02:00,03:00,04:00,05:00,06:00 | Sentiment + Coordinator | Only if a position is open or a name is staged. Sentiment: news on those names, SPY tone. Coordinator: positions, quotes vs stops/profit-lock stages, enforce stops. One line unless something changed. | state.md |
| Q2 | 06:15 | Data & Quant | Confirm breakouts/pullbacks with price near the close (volume pace vs 20d avg, close vs trigger). Max 15 lines. | handoff/quant_confirm_DATE.md |
| RC | 06:30 | Risk then Challenger | Risk YES/NO per staged name; Challenger fact-check + VETO/NO VETO. Max 12 lines each. | handoff/riskchallenger_DATE.md |
| X | 06:45 | Coordinator | Place paper orders ONLY for names with Risk YES + Challenger NO VETO + Quant confirmed + Research PASS + Sentiment not red. Verify fill, record ledger, set/track stops. | ledger.csv |
| A | 08:15 | Research | After-close news pass: earnings reactions, filings, held and staged names, tomorrow's calendar. Max 15 lines. | handoff/afterclose_DATE.md |
| E | 08:30 | Coordinator | Update ledger marks, profit-lock stages, watchlist, state.md. Schedule next cycle. Owner message <= 8 lines. | state.md |

Weekly (Saturday AEDT after cycle E): weekly review per charter (trades, win rate, average R, P/L, rule breaks, lock vs fixed-stop comparison) and graphify --update of the hub.

Owner commands (typed in chat): PAUSE, RESUME, DETAIL, STATUS, LIVE STOCK (not authorised yet).
