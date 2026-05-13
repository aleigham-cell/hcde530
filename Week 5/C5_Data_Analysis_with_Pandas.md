# C5 — Data Analysis with Pandas

## Draft competency claim

Evidence for C5 lives entirely in `**app_reviews_demo_analysis.ipynb**`, working on `**app_reviews_demo.csv**` (500 rows × 10 columns). I used pandas to **load**, **inspect**, **summarize distributions**, **filter** a purposeful subset, **aggregate** across a grouping column, **count missing values**, and I wrote brief notes next to outputs so numbers are interpreted—not just printed.

Workflow in that notebook:

1. **Load:** `pd.read_csv('app_reviews_demo.csv')` into `**df**`.
2. **Structure:** `**print(df.shape)**` plus `**df.head()**` to see columns and sample rows (e.g. `app`, `category`, `rating`, `review`, `helpful_votes`, optional `device_type` / `app_version`). `**df.info()**` to confirm dtypes and `**Non-Null` counts**—this step showed `**device_type**` and `**app_version**` are incomplete before any grouping.
3. **Distribution of the main outcome:** `**rating**` treated as the key sentiment column. `**df['rating'].value_counts().sort_index()**` produced **1→29, 2→43, 3→61, 4→160, 5→207**. I noted in the notebook that **5** is most common, then **4**—i.e. the distribution is **skewed toward high stars**, so “average satisfaction” claims need that bias in mind.
4. **Filtered subset:** Boolean indexing `**df[(df['category'] == 'field research') & (df['rating'] >= 4)]**` → **58** rows. That answers a concrete question: *among field-research reviews, what do strong (4–5 star) rows look like?*
5. **Group aggregate:** `**df.groupby('app')['rating'].mean().round(2)**` — **Fieldkit 3.67**, **Lookback 3.90**, **Maze 4.00**, **Miro 4.02**, **Dovetail 4.12**. I frame that as an **ordinal star average**, useful for comparing apps in-table, not as a standalone “truth” metric.
6. **Missing data:** `**df.isna().sum()**` plus filtering to counts **> 0**: `**device_type**` **63** missing, `**app_version**` **111** missing (with inline comment restating counts).

Across those steps I use **multiple pandas operations**: `**read_csv**`, `**head**` / `**shape**`, `**info**`, `**value_counts**`, conditional row selection, `**groupby` + mean + round**, `**isna` + sum`**, and **`Series `boolean filtering** (`missing_counts[missing_counts > 0]`).

---

## How this maps to the rubric prompts


| What counts as evidence                                                                                                                                                                                 | Where it shows up (`app_reviews_demo_analysis.ipynb` only)                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Loads data and answers **specific analytical questions**                                                                                                                                                | Ratings distribution; field-research high-rating subset; mean rating **by app**; which columns lack values.                                                           |
| **At least two** pandas ops (e.g. `groupby`, `fillna`, `value_counts`, `merge`) — *you use*: `value_counts`, boolean filters, `**groupby`/`mean`**, `**isna`/`sum`** (no `**merge**` in this notebook). | Meets requirement with: `value_counts`, boolean filters, `**groupby`/`mean`**, `**isna`/`sum`** (no `**merge**` in this notebook but I followed this along in class). |
| **Written interpretation**                                                                                                                                                                              | Notebook comments (e.g. most common ratings; missing counts) + interpretation in the file                                                                             |


---

## Optional “strong-style” one-liner

> In `**app_reviews_demo_analysis.ipynb`** I loaded **500** app reviews, profiled them with `**head`/`info`*, quantified `**rating*` with `**value_counts`**, isolated 58 high-rated field research rows with boolean filters, compared apps via `**groupby('app')['rating'].mean()**`, and used `**isna().sum()**` to flag **63** and **111** gaps in `**device_type`** and `**app_version`**—with short notes on what each result means for later analysis.

---



