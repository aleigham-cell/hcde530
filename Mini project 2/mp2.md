# Mini Project 2 — Competency Claims

**Project:** Coaching Class Survey Dashboard (SurveyMonkey export → class-level Dash views)  
**Evidence:** `Mini project 2/app.py`, `survey_data.py`, `assets/style.css`, `readme.md`  
**Run locally:** [http://127.0.0.1:8050](http://127.0.0.1:8050) (after `python app.py` with survey data on your machine)

---

## C1 — Vibecoding and Rapid Prototyping

I used **Cursor** (generative coding in plain language) to build a working **Dash + Plotly** dashboard from a SurveyMonkey Excel export, then iterated until it matched how coaching operations actually reviews class feedback. The first pass gave me a runnable shell with charts; I went back multiple times to add **year and course filters**, SurveyMonkey-style **Answered / Skipped** counts, **grouped matrix bars** for satisfaction and change questions, **star ratings** for recommend/attend likelihood, and scrollable **open-ended response lists**. I kept the tool’s overall layout and Plotly chart scaffolding but redirected it on data handling: SurveyMonkey’s **two-row Excel headers** became a multi-index column model in `survey_data.py`, and I split **loading/transform logic** (`survey_data.py`) from **UI/callbacks** (`app.py`) so I could verify counts without re-rendering the whole UI.

**What the tool did well:** Fast scaffolding for Dash layout, Plotly horizontal bars, and callback wiring so I could focus on the survey structure instead of boilerplate.

**What I had to correct or redirect:** Column identification for matrix questions (only columns whose names end with known level labels like  `- Satisfied`), one-hot score mapping for recommend/attend (`RECOMMEND_MAP` / `ATTEND_MAP`), and a **hardcoded local path** to `Survey.xlsx` that I would not ship to a shared host without a compliance-reviewed upload flow. I also debugged a **port 8050 already in use** error when an old Flask reloader was still running—nothing the model flagged on its own.

**Deployment note:** The app is **usable and demo-ready locally** at `http://127.0.0.1:8050`. It is **not on a public URL** because open-text survey responses may contain PHI/PII; that choice is documented in `readme.md`.

---

## C6 — Data Visualization

I generated charts in **Python with Plotly** (`plotly.graph_objects` in `app.py`) to answer specific questions about coaching-class feedback for a **non-technical operations manager**, not to decorate a spreadsheet.


| Chart                               | Data                                      | Why this type                                                                                                 |
| ----------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Horizontal **percent** bar          | First coaching class (Yes / No)           | Two categories with short labels; percentages read clearly left-to-right.                                     |
| **Star rating** + numeric average   | Recommend / attend (1–5 one-hot columns)  | Stakeholders expect NPS-style “how many stars,” not a raw distribution table.                                 |
| **Grouped horizontal** percent bars | Satisfaction and “areas changed” matrices | Many row labels (class dimensions) × five Likert levels; grouping by level keeps comparison within each item. |
| Horizontal **count** bars           | Day of week, time of day, class type      | Nominal preferences; counts are easier to scan than percentages when labels are long.                         |


Each section includes **Answered** and **Skipped** counts so the reader can judge sample size the same way they would in SurveyMonkey. The analysis lives in this **GitHub repo** as runnable Python (`app.py` / `survey_data.py`) with `readme.md` explaining what each view is for—not a Jupyter notebook, but the same intent: code, rendered charts, and written reasoning a teammate can follow.

**Finding I want a reader to take away:** When filtered to a single course and year, satisfaction and open-ended themes are **class-specific**; aggregate SurveyMonkey views hide that granularity, which is why the dashboard’s **Year** and **Course** filters are part of the argument, not just UI chrome.

---

## C7 — Critical Evaluation and Professional Judgment

I did not treat Cursor’s output or SurveyMonkey’s online totals as ground truth without checking against the **actual Excel export**.

**Example 1 — Open-ended counts “not matching” SurveyMonkey:** I noticed comment volumes could look wrong compared to SurveyMonkey’s UI. I traced the pipeline: `filter_survey()` (year/course) runs **before** `text_responses()`, and `text_answered()` only includes non-null, non-whitespace text. Against `Survey.xlsx` with **All years / All courses**, answered counts matched Excel non-null cells; mismatches were explained by **different filter scope** (e.g., SurveyMonkey class view vs dashboard still on “All courses”), not silent row dropping. I would **not** tell a client “the dashboard is wrong” without first aligning filters and confirming we’re comparing the same export file.

**Example 2 — Matrix and rating logic:** I verified that matrix charts only use columns whose suffix matches predefined levels (`SAT_LEVELS`, `CHANGE_LEVELS`) and that skipped rows for text questions use the **filtered row count** as the denominator. I would not present matrix percentages to leadership without stating which **year/course** filter is active (shown in the summary banner).

**Example 3 — Override AI structure:** When generated code lumped everything into one file or assumed simple CSV headers, I **split data logic from UI** and kept the real SurveyMonkey **multi-row header** shape. That override was necessary for correct column keys like `("What did you like most about your class?", "Open-Ended Response")`.

**Confidence I’d state to a stakeholder:** High on **code and Excel alignment** when filters match; medium on **parity with SurveyMonkey’s web UI** without documenting the same date/course scope.

---

## C8 — Building and Deploying a Complete Tool

**What I built:** A **Coaching Class Survey Dashboard** that turns a SurveyMonkey Excel export into filterable, class-level feedback: matrix satisfaction, likelihood to recommend/attend, preference bars, and full open-ended comment lists.

**Who it is for:** **WebMD Health Services** coaching operations—the **coaching operations manager** (primary) and coaches reviewing their own sessions—so they can see **per-class** performance without manual pivot tables or an aggregate-only SurveyMonkey view.

**How it is shipped:** Complete and **usable on my machine** (`python app.py` → `http://127.0.0.1:8050`). Intentionally **not** deployed to a public URL; survey text may contain PHI/PII, documented in `readme.md`. That is a deliberate product/compliance decision, not an unfinished prototype.

**What went wrong and how I handled it:**

1. **Port conflict** — A previous Dash debug process still held port 8050; I identified the PIDs with `lsof` and restarted cleanly.
2. **Scope confusion on open-ended volume** — Looked like “missing” comments until I confirmed year/course filters and Excel column keys; documented the behavior rather than changing skip logic to force a match with a mismatched SurveyMonkey screen.
3. **Local-only data path** — `SURVEY_PATH` points outside the repo so survey data is never committed; next iteration would add an approved upload or API pull after compliance review.

**Repo evidence:** `Mini project 2/` — `app.py`, `survey_data.py`, `assets/style.css`, `requirements.txt`, `readme.md`, and this `mp2.md`.