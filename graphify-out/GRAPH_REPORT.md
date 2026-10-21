# Graph Report - council-hub  (2026-10-21)

## Corpus Check
- Corpus is ~2,125 words - fits in a single context window. You may not need a graph.

## Summary
- 69 nodes · 140 edges · 7 communities
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Risk Limits and Profit Lock
- Regime, Events and Current Verdict
- Charter and Paper Account
- Agent Roster
- Paper Only and Hub State
- Company Background Checks
- Strategies and Universe

## God Nodes (most connected - your core abstractions)
1. `Coordinator (main session)` - 12 edges
2. `Council Hub README` - 10 edges
3. `Data & Quant Agent` - 10 edges
4. `Watchlist` - 10 edges
5. `Research Agent` - 9 edges
6. `Council State` - 9 edges
7. `Oct 21 Pre-Open Run: NO TRADE` - 9 edges
8. `Event Blackout (3 trading days)` - 7 edges
9. `Council Roster and Division of Labour` - 7 edges
10. `Sentiment Agent` - 7 edges

## Surprising Connections (you probably didn't know these)
- `US Session Timing and DST Shift` --conceptually_related_to--> `Event Blackout (3 trading days)`  [INFERRED]
  routine.md → charter.md
- `CVX, V, UNH, ABBV (blocked: 1 share > $200 cap)` --references--> `Sizing Rule (1% risk, 20% position)`  [INFERRED]
  watchlist.md → charter.md
- `WMT (blocked: setup broken, earnings Nov 19)` --references--> `Stop = entry - 1.5 x ATR(14), T1 >= 3R`  [INFERRED]
  watchlist.md → charter.md
- `Risk Agent` --implements--> `Portfolio Heat, Gap, Sector and Correlation Limits`  [INFERRED]
  roster.md → charter.md
- `XLE (blocked: stale data, correlated with XOM)` --references--> `Portfolio Heat, Gap, Sector and Correlation Limits`  [INFERRED]
  watchlist.md → charter.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Agents that must all clear a name before a paper order** — roster_research, roster_sentiment, roster_data_quant, roster_risk, roster_challenger, roster_coordinator, routine_execution_gate [EXTRACTED 1.00]
- **Daily cycle step flow R1 to E** — routine_r1, routine_s1, routine_q1, routine_c1, routine_h, routine_q2, routine_rc, routine_x, routine_a, routine_e [EXTRACTED 1.00]
- **Pre-entry rule set (sizing, regime gate, event blackout, background check)** — charter_sizing_rule, charter_regime_gate, charter_event_blackout, charter_background_check, charter_portfolio_heat_limits [INFERRED 0.85]

## Communities (7 total, 0 thin omitted)

### Community 0 - "Risk Limits and Profit Lock"
Cohesion: 0.20
Nodes (8): Data & Quant Agent, Quant Skills (quant-analyst, pandas-pro, statistical-analysis), Step C1 Lock Plan, Step E End-of-Cycle Update, Step H Hourly Watch, Step Q1 Quant Plan Numbers, Step Q2 Quant Confirm, Step S1 Sentiment Filter

### Community 1 - "Regime, Events and Current Verdict"
Cohesion: 0.31
Nodes (10): Strategy C: Relative Strength vs SPY, Oct 21 Pre-Open Run: NO TRADE, SPY 769.05 vs Falling SMA50 768.29 (RANGE, borderline), Watchlist, KO (blocked: earnings Oct 27), SPY (regime gauge and parking sleeve), WMT (blocked: setup broken, earnings Nov 19), XLE (blocked: stale data, correlated with XOM) (+2 more)

### Community 2 - "Charter and Paper Account"
Cohesion: 0.22
Nodes (11): Stock Council Charter, moomoo Paper Account 428122 and $1,000 Ledger, Council Hub README, graphify-out knowledge graph, ledger.csv (paper trade ledger), Owner Commands (PAUSE, RESUME, DETAIL, STATUS, LIVE STOCK), Cycle Read Order, Daily Routine (AEDT) (+3 more)

### Community 3 - "Agent Roster"
Cohesion: 0.42
Nodes (10): Owner Reporting (one message per cycle), Council Roster and Division of Labour, Challenger Agent, Coordinator (main session), Research Agent, Risk Agent, Sentiment Agent, Step A After-Close News Pass (+2 more)

### Community 4 - "Paper Only and Hub State"
Cohesion: 0.28
Nodes (7): handoff/ step files, moomoo sim_trade_* tools (paper orders), Council State, Crypto Lane On Hold, Known Calendar (earnings, FOMC, GDP/PCE), Open Questions (sim stop order types, side enum), Re-entry Conditions

### Community 5 - "Company Background Checks"
Cohesion: 0.33
Nodes (6): Analyst Cross-Check, Company Background Check, Verdict PASS / WATCH / FAIL and Automatic FAIL Triggers, moomoo quote_* tools (read-only), WebSearch / WebFetch / FMP, Data Caveats (FMP plan limits, second-source verification)

### Community 6 - "Strategies and Universe"
Cohesion: 0.40
Nodes (5): Strategy B: Pullback in Uptrend, Allowed Strategies, Strategy A: Trend Breakout, Universe Rules, CVX, V, UNH, ABBV (blocked: 1 share > $200 cap)

## Knowledge Gaps
- **8 isolated node(s):** `Cycle Read Order`, `Owner Commands (PAUSE, RESUME, DETAIL, STATUS, LIVE STOCK)`, `Strategy B: Pullback in Uptrend`, `Universe Rules`, `Analyst Cross-Check` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 8 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Council Hub README` connect `Charter and Paper Account` to `Regime, Events and Current Verdict`, `Agent Roster`, `Paper Only and Hub State`?**
  _High betweenness centrality (0.211) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Data & Quant Agent` (e.g. with `Regime Gate (SPY RISK-OFF / TREND / RANGE)` and `Sizing Rule (1% risk, 20% position)`) actually correct?**
  _`Data & Quant Agent` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Cycle Read Order`, `Owner Commands (PAUSE, RESUME, DETAIL, STATUS, LIVE STOCK)`, `Strategy B: Pullback in Uptrend` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Why does `Watchlist` connect `Regime, Events and Current Verdict` to `Risk Limits and Profit Lock`, `Charter and Paper Account`, `Strategies and Universe`?**
  _High betweenness centrality (0.191) - this node is a cross-community bridge._
- **Why does `Council State` connect `Paper Only and Hub State` to `Risk Limits and Profit Lock`, `Regime, Events and Current Verdict`, `Charter and Paper Account`, `Company Background Checks`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._