## Week 2 — Competency 2: Code Literacy & Documentation

### Why this matters for me (UX design)
- Basic **code literacy** helps me **talk with engineers**—I can follow enough of how things work to ask better questions and understand constraints and tradeoffs.

### What I worked on
- The competency asked me to **read a given block of code and explain what it does**.
- After clarifying what that meant, I **labeled sections of the script with comments** so the structure and purpose of each part are easier to follow.
- I also updated **`CONTEXT.md`** so folder-level docs describe the same documentation approach—not only the reflection in this file.

### What I learned about reading code (code literacy)
- Explaining a block means tracing what it does step by step (inputs, operations, outputs), not just naming the syntax.
- I had to understand the code well enough to describe it in plain language before the comments felt accurate.
- **Hardest part for me:** **reading the code** (parsing what each part was doing) before I could label or explain it confidently.
- **What helped:** **Asking questions in Cursor** (the chat panel) to get plain-language explanations of specific lines or blocks before I wrote comments.

### What I learned about documenting code / work
- Comments that **name sections** (e.g., load data, loop, summarize) help future readers—and me—navigate the file without rereading every line.
- Documentation here is partly **translation**: turning code behavior into short, human-readable labels.
- For this assignment, documentation is **consistent across files**: comments in the script, a reflection that points to those comments, and **`CONTEXT.md`** that explains how the folder fits together.

### Evidence (links, files, screenshots, outputs)

**Files:**

| File | Role |
|------|------|
| `Week 2 Project/demo_word_count.py` | Script with section-style comments in the code |
| `Week 2 Project/week2.md` | This reflection (competency claim) |
| `Week 2 Project/CONTEXT.md` | Run instructions, data description, documentation map |

**How I documented the “explain this block” work:** Written **in the code itself**—section comments live next to the behavior (not only in this markdown file).

**Section-style comments in `demo_word_count.py` (matches the file as submitted):**

| Comment in code | What that block does |
|-----------------|----------------------|
| Top line (`# a script to process and count wrods…`) | One-line description of what the script does |
| `# Load the CSV file` | Sets filename, opens file, reads rows into `responses` |
| `#function to count words in a response` | Introduces `count_words()` and its docstring |
| `# Count words in each response and print a row-by-row summary` | Table header before the main loop |
| `# loops through each csv row…` | Pulls `participant_id`, `role`, and `response` from each row |
| `#access each row and pull out the participant id, role, and response` | Same loop—names the three fields used |
| `# Call our function to count words in this response` | Runs `count_words()` and stores the result |
| `# create a short preview of the response for display` | Truncates long text to 60 characters for the table |
| `# Print summary statistics` | Totals, min, max, and average word counts |

### What I’d do differently next time
- **Explore more**—try additional experiments with the script or data (beyond the minimum) so I build intuition faster.
- **Break things on purpose** (e.g., change a filename, remove a column, tweak a line) to see what error messages mean and how the program fails—so I learn how the pieces depend on each other.

