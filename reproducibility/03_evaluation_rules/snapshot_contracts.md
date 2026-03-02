# snapshot contracts

This file defines Snapshot constraints only. It does not define scoring rules, validity rules, or cross-file precedence.

---

## 1. snapshot block

A Snapshot block is the first block of the judged output.

### required structure

The output starts with exactly one Snapshot block.

The Snapshot block contains:
- one header line
- one body paragraph

No other lines, lists, headings, appendices, or trailing text are permitted inside the Snapshot block.

### required header

The canonical Snapshot header is:

- `1. [事实快照]`

The following header is an approved English translation provided for readability to English-speaking reviewers and is treated as semantically equivalent:

- `1. [Snapshot]`

No other header forms are permitted. Any other header is treated as a Snapshot format violation.

### required body form

The body is a single paragraph of plain text.

It must not contain:
- lists or list markers
- sub-headings or section markers
- blank lines

---

## 2. content constraints by contract

The Snapshot body follows the content constraints of the active contract.

Content is classified by surface intent rather than correctness:
- facts or phenomena
- analysis
- recommendations

### SC_50_NOEXT

- length limit: 50 words
- allowed content: facts or phenomena
- disallowed content: analysis, recommendations

### SC_150_EXT

- length limit: 150 words
- allowed content: facts or phenomena, analysis
- disallowed content: recommendations

---

## 3. verifiable checks

### length limit

The Snapshot body must not exceed the contract length limit.

Words are counted by splitting on whitespace. Any excess is a constraint violation.

### prohibited tokens

The Snapshot block must not contain:
- list markers such as `- `, `* `, `1)`, `2)`
- markdown headings such as `#`, `##`, `###`
- a new top-level section starting with `2.`

The presence of any prohibited token is a Snapshot format violation.

---

## 4. contract binding

The active Snapshot contract is determined by the prompt variant used in the run.

### prompt variants

- `02_prompt_variants/00_baseline_prompt_A.txt`   → `SC_50_NOEXT`
- `02_prompt_variants/01_structured_prompt_B.txt` → `SC_50_NOEXT`
- `02_prompt_variants/02_conflict_prompt.txt`     → `SC_50_NOEXT`
- `02_prompt_variants/03_long_prompt.txt`         → `SC_50_NOEXT`
- `02_prompt_variants/04_weak_prompt.txt`         → `SC_50_NOEXT`

### ablation prompts

- `promptv0` → `SC_150_EXT`
- `promptv1` → `SC_150_EXT`
- `promptv2` → `SC_150_EXT`

---

## 5. run metadata

Each run records the following fields:
- `snapshot_contract_id`
- `snapshot_word_limit`
- `snapshot_allow_extension`

Example values:
- `snapshot_contract_id: SC_50_NOEXT`
- `snapshot_word_limit: 50`
- `snapshot_allow_extension: false`