# Individual lab validation — Zachary Alvin

Completed using actual SEC EDGAR companyfacts downloads, keyless, with Zachary Alvin and the supplied contact email in the User-Agent. No FAskills installation, paid data sources, or price data.

- COST: every value matches the classroom reference after converting USD to USD millions and rounding ROE to one decimal for comparison. Fiscal-year ends run from 2022-08-28 through 2026-08-30. All three checks pass. Owner earnings and net income both finish above their first-year values.
- JPM: actual last five annual fiscal-year ends run from 2021-12-31 through 2025-12-31. Capital spending and owner earnings are `not found` throughout. Both owner-earnings checks are `not known`. The ROE-every-year check fails. Its memo explicitly says it cannot judge owner earnings.
- Memo audit: both saved memos contain only numeric literals found in their printed script outputs. Facts fingerprints match each memo's metadata.
- Hand-typed number: the actual COST memo was edited in Streamlit AppTest's in-memory text area to add `40.0%`. The app flagged and listed it. The saved submission memo was not altered.
- App: actual COST and JPM chart/table/memo renders pass with no app exceptions; source tags and filing provenance are available in the evidence expander.
- Decision: included as the final line under COST's memo and separately in decision.md.
- Validation: seven unit tests, actual-data acceptance tests, and the skill validator pass.

Files: reports/COST/{companyfacts.json,data.json,facts.md,memo.md,memo.meta.json}; equivalent JPM files; app.py; buffett-sec/SKILL.md and its bundled script; request.md; test_lab.py; test_acceptance.py; verify_cost.py; cost_expected.json.

Rerun from the course directory:

```sh
.venv/bin/python buffett_lab/verify_cost.py
.venv/bin/python buffett_lab/test_lab.py
.venv/bin/python buffett_lab/test_acceptance.py
.venv/bin/python -m streamlit run buffett_lab/app.py --server.port 8502
```

Prepared for an individual submission; nothing has been submitted externally. The memo is an AI-simulated business-quality judgment, and passing the screen does not establish moat durability or management quality.
