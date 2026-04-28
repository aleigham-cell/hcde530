"""
Fetch grouped US stock bars for a single date from Massive (Polygon-compatible)
API, extract AAPL open / volume / close, print them, and save to CSV.

API key is read from .env next to this script as POLYGON_API_KEY (no third-party packages).
"""

from __future__ import annotations

import csv
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
#setting up the API call and the ticker
BASE = "https://api.massive.com"
GROUPED_PATH = "/v2/aggs/grouped/locale/us/market/stocks"
DATE = "2025-11-03"
TICKER = "AAPL"
TIMEOUT_SEC = 60

_ENV_KEY_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$")


def load_dotenv(path: Path) -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ (does not override)."""
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        m = _ENV_KEY_RE.match(line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if key and key not in os.environ:
            if (len(val) >= 2) and ((val[0] == val[-1] == '"') or (val[0] == val[-1] == "'")):
                val = val[1:-1].replace(r"\\n", "\n").replace(r"\\", "\\")
            os.environ[key] = val


def _ticker_from_bar(bar: dict[str, object]) -> str | None:
    if "T" in bar and bar["T"] is not None:
        return str(bar["T"]).upper()
    if "ticker" in bar and bar["ticker"] is not None:
        return str(bar["ticker"]).upper()
    return None


def find_bar_for_ticker(payload: object, ticker: str) -> dict[str, object] | None:
    want = ticker.upper()
    if not isinstance(payload, dict):
        return None
    results = payload.get("results")
    if not isinstance(results, list):
        return None
    for item in results:
        if not isinstance(item, dict):
            continue
        if _ticker_from_bar(item) == want:
            return item
    return None


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    load_dotenv(script_dir / ".env")

    api_key = os.environ.get("POLYGON_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Missing POLYGON_API_KEY. Set it in .env beside this script (see .env.example)."
        )

    query = urlencode({"adjusted": "true", "apiKey": api_key})
    url = f"{BASE}{GROUPED_PATH}/{DATE}?{query}"
    #Making the API call and handling the response
    req = Request(url, headers={"User-Agent": "hcde530-week4/1.0"})
    try:
        #request should return Apple's open, volume, and close for the given date
        with urlopen(req, timeout=TIMEOUT_SEC) as resp:  # noqa: S310 — built URL with env key
            payload = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        raise SystemExit(f"HTTP {e.code} {e.reason}. Body: {body[:500]}") from e
    except URLError as e:
        raise SystemExit(f"Could not reach API: {e.reason}") from e
    except TimeoutError as e:
        raise SystemExit("Request timed out. Try again in a moment.") from e
    #Finding the information for Apple's stock based on ticker
    bar = find_bar_for_ticker(payload, TICKER)
    if bar is None:
        raise SystemExit(f"No bar found for ticker {TICKER} in API response for {DATE}.")
    #Fetching the open, volume, and close price for Apple's stock to inform investment decisions or do advanced analysis
    try:
        open_ = float(bar["o"])
        volume = float(bar["v"])
        close = float(bar["c"])
    except (KeyError, TypeError, ValueError) as e:
        raise SystemExit(f"Unexpected bar fields for {TICKER}: {bar!r}") from e

    print(f"{TICKER} {DATE}")
    print(f"  open:   {open_}")
    print(f"  volume: {volume}")
    print(f"  close:  {close}")

    out_path = script_dir / "aapl_open_volume_close.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["ticker", "date", "open", "volume", "close"],
        )
        w.writeheader()
        w.writerow(
            {
                "ticker": TICKER,
                "date": DATE,
                "open": open_,
                "volume": volume,
                "close": close,
            }
        )

    print()
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
