# Coaching Class Survey Dashboard

## What this tool does

This dashboard turns exported SurveyMonkey coaching-class feedback into **class-level views** that can be filtered by year and course title. Instead of working around an aggregate-only SurveyMonkey dashboard, a coaching operations manager can quickly see how a specific class performed across satisfaction, likelihood to recommend, attendance preferences, and open-ended comments.

The app reads a local Excel export and renders interactive charts and scrollable response lists for each survey question.

## Who it is for

This tool is built for **WebMD Health Services** coaching operations. The primary user is the **coaching operations manager**, a non-technical stakeholder who needs fast, self-serve access to class-level feedback without manual spreadsheet work. Coaches may also use it occasionally to review feedback on their own sessions.

## How to run it

Survey data stays **local only** and is not committed to this repository.

1. Place your SurveyMonkey export at:
  `/Users/amattison/Documents/Coaching_Class_Survey/Survey.xlsx`
2. Install dependencies:
  ```bash
   cd "Mini project 2"
   pip install -r requirements.txt
  ```
3. Start the app:
  ```bash
   python app.py
  ```
4. Open the dashboard in your browser:
  **[http://127.0.0.1:8050](http://127.0.0.1:8050)**

### Filters

- **Year** — filter by class date year, or choose *All years*
- **Course** — pick one class (alphabetical), or choose *All courses (aggregate)*

Each section shows **Answered** and **Skipped** counts, matching SurveyMonkey-style reporting.

## Public URL

This project is intentionally **not publicly deployed**.

Survey open-text responses may contain PHI/PII, so the current version runs **locally on your machine** and keeps all data on-device. No survey data is sent to a third-party hosting service.

- **Live public URL:** Not available (local-only deployment for privacy/compliance)
- **Local access URL:** [http://127.0.0.1:8050](http://127.0.0.1:8050) (after running `python app.py`)

A hosted/shared option could be added later once compliance review is complete.

## Project files


| File               | Purpose                                           |
| ------------------ | ------------------------------------------------- |
| `app.py`           | Dash app layout, filters, and chart rendering     |
| `survey_data.py`   | Data loading, filtering, and summary calculations |
| `assets/style.css` | SurveyMonkey-inspired styling                     |
| `requirements.txt` | Python dependencies                               |


## Data source

The tool expects a SurveyMonkey Excel export with multi-row headers, including columns such as `course title`, `class date`, satisfaction matrix questions, and open-ended responses.

Future versions could support CSV upload or automatic pulls from the SurveyMonkey API.