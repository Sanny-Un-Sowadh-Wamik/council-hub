# Council Hub (memory for the stock council)

Read order at the start of every cycle: README -> state.md -> charter.md -> roster.md -> routine.md -> watchlist.md -> ledger.csv -> latest handoff files.

- charter.md: rules, sizing, strategies, background-check checklist.
- roster.md: who does what, models, tools, spawn rules.
- routine.md: daily schedule and step outputs (AEDT).
- state.md: current status and open questions. Update every cycle.
- watchlist.md: names, blockers, triggers.
- ledger.csv: every paper trade with stop history.
- handoff/: one file per routine step per day (research_, sentiment_, quant_, plan_, riskchallenger_, afterclose_).
- graphify-out/: knowledge graph of this hub. Query with: graphify query "<question>". Rebuild weekly with /graphify /home/claude/council-hub --update (docs go through an LLM, so do not run it daily).

Owner: Melbourne. Prefers short replies, caveman-voice style in chat, usage kept low. Owner commands: PAUSE, RESUME, DETAIL, STATUS.
