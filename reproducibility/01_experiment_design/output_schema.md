## Output Schema

This document specifies the **expected structural layout** of model outputs used in the experiment.

**Scope / Non-goals**
- This file defines **structure only** (section names and order).
- This file does **not** define or interpret evaluation rules (scales, validity criteria, failure definitions, or judgment procedures).
- All evaluation logic is defined **exclusively** in `supplement/03_evaluation_rules/`.

---

### Required Top-level Sections

An output is expected to contain **exactly three** top-level sections, appearing **once each** and in the following order:

1. `fact snapshot`
2. `ChatGPT web search instructions`
3. `Gemini deep research instructions`

**Section titles are expected to match the labels above.**

---

### Section Intent

- **fact snapshot**: a short snapshot statement.
- **ChatGPT web search instructions**: instructions for web searching and synthesis.
- **Gemini deep research instructions**: instructions for broader literature-style exploration.

> Note: Any constraints beyond this layout (e.g., length limits, content constraints, schema violation handling) are specified and adjudicated only by the evaluation protocol in `supplement/03_evaluation_rules/`.

---

### Minimal Template

```text
## fact snapshot
...

## ChatGPT web search instructions
...

## Gemini deep research instructions
...
```