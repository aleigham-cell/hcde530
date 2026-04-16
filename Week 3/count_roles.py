import csv
from collections import Counter
from pathlib import Path


def normalize_role(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip().upper()


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / "responses_cleaned.csv"

    if not input_path.exists():
        raise FileNotFoundError(
            f"Could not find {input_path.name}. Run clean_responses.py first (or put the file in: {script_dir})."
        )

    counts: Counter[str] = Counter()

    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV appears to be missing a header row.")
        if "role" not in reader.fieldnames:
            raise KeyError("Expected a 'role' column in responses_cleaned.csv.")

        for row in reader:
            role = normalize_role(row.get("role"))
            if role:
                counts[role] += 1

    print("Role counts (in file order):")
    print("-" * 30)
    for role, count in counts.items():
        print(f"{role:<20} {count}")


if __name__ == "__main__":
    main()
