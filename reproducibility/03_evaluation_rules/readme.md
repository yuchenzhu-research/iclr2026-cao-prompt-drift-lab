# 03 evaluation rules

**Authority and reading order**

`eval_protocol.md` is the only normative protocol in this directory and MUST be read first.

All other files are subordinate references. They MUST NOT introduce additional rules or override the protocol.

This directory defines evaluation **contracts** only.

- It contains no experimental results.
- It has no dependency on `tools/` or `04_results/`.
- Tooling documents are archival and do not affect evaluation semantics.

---

## start here

1) `eval_protocol.md` — protocol entry point and precedence.

---

## file index

- `eval_protocol.md` — protocol entry point and precedence.
- `judge_prompt.md` — contract-instantiating prompt for producing one raw judge bundle.
- `schema/judge_bundle.schema.json` — JSON structure for raw judge bundle outputs.
- `schema/eval_record.schema.json` — JSON structure for canonical eval records used in aggregation and reporting.
- `snapshot_contracts.md` — Snapshot block contract definitions applied to evaluated outputs.
- `scoring_dimensions.md` — meanings of score fields used in each per-file score entry.
- `validity_criteria.md` — validity conditions applied to raw judge bundle outputs.
- `failure_taxonomy.md` — labels for observable contract-violation types used in analysis artifacts.
- `compute_scores.md` — documentation of an archival utility mapping behavior.
- `compute_scores.py` — archival scoring utility script.