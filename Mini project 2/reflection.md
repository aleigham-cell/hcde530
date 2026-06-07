# Mini Project 2 — Reflection

## 1. What did you build?

I built the **Coaching Class Survey Dashboard** for WebMD Health Services coaching operations. The tool reads a SurveyMonkey Excel export and turns it into filterable, class-level feedback views. SurveyMonkey’s built-in dashboard is aggregate-only; this app lets a coaching operations manager—and optionally individual coaches—see how a specific class performed in a given year: satisfaction matrices, likelihood to recommend or attend, scheduling preferences, and full open-ended comment lists, without manual spreadsheet work. Each section shows **Answered** and **Skipped** counts in the same spirit as SurveyMonkey reporting. The app runs locally as a Python Dash project (`python app.py` → [http://127.0.0.1:8050](http://127.0.0.1:8050)). Survey data stays on the user’s machine and is not committed to the repository.

## 2. What decisions did you make?

I chose **Dash, Plotly, and pandas** in Python rather than a no-code builder or Jupyter-only analysis because the SurveyMonkey export uses two-row headers and mixed question types—matrix, one-hot ratings, and open text—that needed custom parsing. I split `survey_data.py` (load, filter, aggregate) from `app.py` (layout, callbacks, charts) so I could verify counts independently of the UI. Scope included year and course filters and all major question types; public deployment and CSV upload were deferred because open-text responses may contain PHI/PII. Compared with staying in SurveyMonkey or using Lovable/Bolt, this approach gave precise control over class-level filtering. Relative to my MP2a declaration, I shifted from a shareable hosted URL to **local-only deployment** and expanded the build to include scrollable open-ended response lists, not just aggregate charts.

## 3. What would you do differently?

Two concrete changes to the tool itself. First, I would replace the hardcoded `SURVEY_PATH` with an **in-app file picker** or upload step so the dashboard works on any machine without editing code—a real barrier for a non-technical operations manager. Second, I would add clearer **active-filter context** above open-ended sections so stakeholders do not compare filtered dashboard comments to an unfiltered SurveyMonkey screen and assume data is missing. I might also add search or pagination for long comment lists once a single class is selected, since scrolling through hundreds of responses does not scale for a quick review workflow.

## 4. What does this work demonstrate?

**C1 — Vibecoding / rapid prototyping:** I used Cursor to scaffold the Dash layout quickly, then iterated through multiple passes to add filters, matrix charts, star ratings, and open-ended lists redirecting the generated code when it mishandled SurveyMonkey’s multi-row headers or lumped all logic into one file.

**C6 — Data visualization:** In `app.py`, I matched Plotly chart types to each question structure including horizontal percent bars for binary items, star ratings for recommend/attend scores, grouped matrix bars for satisfaction and change questions, and count bars for scheduling preferences. Each view answers a specific operational question rather than defaulting to a generic chart.

**C7 — Critical evaluation:** I verified open-ended counts against the Excel export and traced apparent mismatches with SurveyMonkey, I also chose not to deploy publicly for proper handling of sensitive open-text responses.

**C8 — Complete tool:** The project delivers a runnable local app with `readme.md` and `mp2.md` for the coaching operations team, documents honest scope limits (local-only, no survey data in the repo), and records real friction (port conflicts and filter confusion) rather than treating the first working version as finished.