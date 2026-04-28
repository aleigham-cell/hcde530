# C4 — APIs and Data Acquisition

## Draft competency claim

I practiced pulling structured data from REST APIs using Python’s standard library (`urllib` for the HTTP GET, `json.loads` for the response body). For my main evidence, I used **Massive’s stock aggregates API** ([Daily market summary / grouped bars](https://massive.com/docs/rest/stocks/aggregates/daily-market-summary)) at `api.massive.com`, **not only** the instructor-hosted Week 4 demo API. That endpoint expects a **trade date** in the URL path (`/v2/aggs/grouped/locale/us/market/stocks/{date}`), supports query parameters like `**adjusted`**, and returns JSON whose `**results**` array lists one **OHLC/V bar object per ticker** that traded that day. Each bar uses short field names (`**T`** = ticker symbol, `**o**` open, `**c**` close, `**v**` volume, etc.—see Massive docs for full shape).

In `fetch_aapl_grouped.py` I assembled the request URL safely with `urllib.parse.urlencode`, passed my key as `**apiKey**`, downloaded the grouped daily payload for **2025-11-03**, **located the row for `T == "AAPL"`** inside `results`, and extracted **open, volume, and close**—then **printed those values for quick inspection** and **wrote a one-row CSV** (`aapl_open_volume_close.csv`) with columns `ticker`, `date`, `open`, `volume`, and `close` so the output stays structured and reproducible.

I keep my `**POLYGON_API_KEY` in a local `.env`** file beside the script (`load_dotenv` reads `.env` into `os.environ` without extra packages). My repo’s `**.gitignore` ignores `.env**` (but allows committing `.env.example` as a blank template), so the key is not checked into version control. I also added basic error handling for HTTP failures and timeouts so failed calls fail loudly instead of silently producing bad CSVs.

**Related work (also in this Week 4 folder / parent `week 4/`):** I wrote `fetch_reviews.py` against the **course Week 4 API** on Render, paginated `/reviews`, and exported `category` and `helpful_votes` to CSV—useful for comparing a **keyless / known** API shape to a **key-authenticated vendor API**.

Lastly, I added comments thorughout explaining what was happening as instructed.

---

## How this maps to the rubric prompts


| What counts as evidence                    | Where it shows up in my work                                                                                                      |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Python HTTP request + JSON parsing         | `fetch_aapl_grouped.py`: `urllib.request.urlopen`, `json.loads`; same pattern in `fetch_reviews.py` for the `/reviews` feed.      |
| API you identified yourself                | Massive `api.massive.com` grouped daily endpoint for OHLC/V (plus optional course `/reviews` API for contrast).                   |
| Key safety (ignore file and/or env vars)   | `.env` + `POLYGON_API_KEY`; repo root `.gitignore` lists `.env` / `.env.*` with `!.env.example`; script never prints the key.     |
| Short explanation of response + what I did | Grouped endpoint returns `**results`** list of ticker bars → I filtered to **AAPL** and persisted **open, volume, close** to CSV. |


---

## Optional one-liner (strong style)

> I called Massive’s grouped daily US stocks endpoint for a single calendar date; the JSON response includes per-ticker OHLC/V bars, so I selected **AAPL** and saved **open, volume, and close** to a CSV. My API key lives in `**.env`**, which is **gitignored**, and `fetch_aapl_grouped.py` documents the request pattern and field names I relied on.

