"""
Fetch HCDE 530 Week 4 app review data from the course API, print category and
helpful vote counts, and save them to a CSV in this folder.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

BASE_URL = "https://hcde530-week4-api.onrender.com"
REVIEWS_PATH = "/reviews"
PAGE_SIZE = 100
TIMEOUT_SEC = 60

#Function to fetch all reviews from the API
def fetch_all_reviews() -> list[dict[str, object]]:
    """GET /reviews with pagination until all rows are retrieved."""
    reviews: list[dict[str, object]] = []
    offset = 0
#Loop that continues until all reviews are fetched
    while True:
        query = urlencode({"limit": PAGE_SIZE, "offset": offset})
        url = f"{BASE_URL}{REVIEWS_PATH}?{query}"
        with urlopen(url, timeout=TIMEOUT_SEC) as resp:  # noqa: S310 — fixed course URL
            payload = json.loads(resp.read().decode("utf-8"))

        if not isinstance(payload, dict) or "reviews" not in payload:
            raise ValueError("Unexpected API response: missing 'reviews'.")

        batch = payload["reviews"]
        if not isinstance(batch, list):
            raise ValueError("Unexpected API response: 'reviews' is not a list.")

        reviews.extend(batch)
        returned = int(payload.get("returned", len(batch)))
        total = int(payload.get("total", len(reviews)))

        if returned == 0 or len(reviews) >= total:
            break
        offset += returned

    return reviews


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    out_path = script_dir / "category_helpful_votes.csv"

    try:
        reviews = fetch_all_reviews()
    except HTTPError as e:
        raise SystemExit(f"HTTP error from API: {e.code} {e.reason}") from e
    except URLError as e:
        raise SystemExit(f"Could not reach API: {e.reason}") from e
    except TimeoutError as e:
        raise SystemExit("Request timed out. Try again in a moment.") from e

    fieldnames = ["category", "helpful_votes"]
    rows: list[dict[str, str]] = []

    for r in reviews:
        if not isinstance(r, dict):
            continue
        cat = r.get("category", "")
        votes = r.get("helpful_votes", "")
        rows.append(
            {
                "category": str(cat) if cat is not None else "",
                "helpful_votes": str(votes) if votes is not None else "",
            }
        )
        print(f"category: {cat!s}, helpful votes: {votes!s}")

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"Wrote {len(rows)} row(s) to: {out_path}")


if __name__ == "__main__":
    main()
