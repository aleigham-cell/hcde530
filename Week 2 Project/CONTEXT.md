# Week 2 — project context

This file is for **me** and my **instructor**: a plain-language snapshot of what this folder is, how to run it, and what constraints I’m working under. I’m an HCD / **UX designer**, not a software engineer—I'm **still learning** Python and Git, so nothing here assumes advanced tooling.

## What Week 2 is for

Get more comfortable with **Python basics** and **Git/GitHub**, by working with a small script that reads a CSV and summarizes text length.

## What’s “in scope” for Week 2 (main artifacts)

- **`demo_word_count.py`** — loads a CSV, counts words per row, prints a table and summary stats.
- **`demo_responses.csv`** — the data the script reads (see below).

Optional: I also keep reflection notes in **`week2.md`** (competency / process), separate from this context.

## About the data (`demo_responses.csv`)

- The responses are **made up for class** (not real participant data).
- The prompt they answer is effectively: **the hardest part of the product process** (from the perspective of people in product roles).
- Columns:
  - `participant_id` — identifier for each row
  - `role` — role label (e.g., UX Researcher, UX Designer, Product Manager)
  - `response` — free-text answer

## How to run (Mac, Terminal)

The script opens `demo_responses.csv` using a **relative path**, so it expects the CSV to be in your **current working directory** when you run Python.

**Reliable:**

```bash
cd "/path/to/hcde530/Week 2 Project"
python3 demo_word_count.py
```

If you’re already at the repo root (`hcde530/`):

```bash
cd "Week 2 Project"
python3 demo_word_count.py
```

**Note:** Running `python3 "Week 2 Project/demo_word_count.py"` from the repo root can fail unless your shell’s working directory is also where `demo_responses.csv` lives—so **`cd` into `Week 2 Project` first**.

## Dependencies / constraints

- **Python 3**
- **Standard library only** (e.g., `csv`)—no `pip install` required for this script.
- I want code to stay **short and simple** (readable over clever).

## Git / GitHub (high level)

- Repo remote (this course project): `https://github.com/aleigham-cell/hcde530.git`
- Default branch I use: **`main`**
- Typical save-to-GitHub flow I’m practicing:

```bash
git status
git add "Week 2 Project/demo_word_count.py" "Week 2 Project/demo_responses.csv" "Week 2 Project/CONTEXT.md"
git commit -m "Describe what changed in plain language"
git push origin main
```

I’m still building fluency here—if something breaks, I’m learning from the error messages and asking questions as I go.
