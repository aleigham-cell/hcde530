## Week 2 — Competency 2: Code Literacy & Documentation

### Why this matters for me (UX design)
- Basic **code literacy** helps me **talk with engineers**—I can follow enough of how things work to ask better questions and understand constraints and tradeoffs.

### What I worked on
- The competency asked me to **read a given block of code and explain what it does**.
- After clarifying what that meant, I **labeled sections of the script with comments** so the structure and purpose of each part are easier to follow.

### What I learned about reading code (code literacy)
- Explaining a block means tracing what it does step by step (inputs, operations, outputs), not just naming the syntax.
- I had to understand the code well enough to describe it in plain language before the comments felt accurate.
- **Hardest part for me:** **reading the code** (parsing what each part was doing) before I could label or explain it confidently.
- **What helped:** **Asking questions in Cursor** (the chat panel) to get plain-language explanations of specific lines or blocks before I wrote comments.

### What I learned about documenting code / work
- Comments that **name sections** (e.g., load data, loop, summarize) help future readers—and me—navigate the file without rereading every line.
- Documentation here is partly **translation**: turning code behavior into short, human-readable labels.

### Evidence (links, files, screenshots, outputs)
- **How I documented the “explain this block” work:** Written **in the code itself**—I **added lines and comments** so the explanation lives next to the behavior (not only in a separate doc).
- **File:** `Week 2 Project/demo_word_count.py`
- **Section-style comments I added (or kept) to map the script:**
  - Top: one-line description of what the script does
  - `# Load the CSV file` — sets filename, opens file, reads rows into `responses`
  - `# Count words in each response and print a row-by-row summary` — header, loop, per-row word count and preview
  - Inline note before the `for` loop — what each iteration pulls from the row (`participant_id`, `role`, `response`)
  - `# Call our function to count words in this response`
  - `# create a short preview of the response for display`
  - `# Print summary statistics` — totals, min, max, average word counts

### What I’d do differently next time
- **Explore more**—try additional experiments with the script or data (beyond the minimum) so I build intuition faster.
- **Break things on purpose** (e.g., change a filename, remove a column, tweak a line) to see what error messages mean and how the program fails—so I learn how the pieces depend on each other.

