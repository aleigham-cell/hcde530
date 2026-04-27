"""
Fetch HCDE 530 Week 4 app review data from the course API, total reviews by
rating (1–5), and save the results to a CSV in this folder.
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


def fetch_all_reviews() -> list[dict[str, object]]:
    """GET /reviews with pagination until all rows are retrieved."""
    reviews: list[dict[str, object]] = []
    offset = 0

    while True:
        query = urlencode({"limit": PAGE_SIZE, "offset": offset})
        url = f"{BASE_URL}{REVIEWS_PATH}?{query}"
        with urlopen(url, timeout=TIMEOUT_SEC) as resp:  # noqa: S310 — fixed course URL
            payload = json.loads(resp.read().decode("utf-8"))
#Checking if the API response is valid
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

#setting up the script's main entry point and deciding where to save the output
def main() -> None:
    script_dir = Path(__file__).resolve().parent
    out_path = script_dir / "review_counts_by_rating.csv"

    try:
        reviews = fetch_all_reviews()
    except HTTPError as e:
        raise SystemExit(f"HTTP error from API: {e.code} {e.reason}") from e
    except URLError as e:
        raise SystemExit(f"Could not reach API: {e.reason}") from e
    except TimeoutError as e:
        raise SystemExit("Request timed out. Try again in a moment.") from e

    counts: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for r in reviews:
        if not isinstance(r, dict):
            continue
        rating = r.get("rating")
        try:
            rating_int = int(rating)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            continue
        if rating_int in counts:
            counts[rating_int] += 1

    # Print results
    for rating in range(1, 6):
        print(f"rating {rating}: {counts[rating]}")

    # Save CSV
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rating", "count"])
        writer.writeheader()
        for rating in range(1, 6):
            writer.writerow({"rating": rating, "count": counts[rating]})

    print()
    print(f"Wrote counts to: {out_path}")


if __name__ == "__main__":
    main()

