import csv
from pathlib import Path


def is_blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / "responses.csv"
    output_path = script_dir / "responses_cleaned.csv"

    if not input_path.exists():
        raise FileNotFoundError(
            f"Could not find {input_path.name}. Put it in: {script_dir}"
        )

    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV appears to be missing a header row.")

        fieldnames = list(reader.fieldnames)
        if "name" not in fieldnames:
            raise KeyError("Expected a 'name' column in responses.csv.")
        if "role" not in fieldnames:
            raise KeyError("Expected a 'role' column in responses.csv.")

        cleaned_rows: list[dict[str, str]] = []
        removed = 0

        for row in reader:
            if is_blank(row.get("name")):
                removed += 1
                continue

            # Keep the same columns/order as the input file.
            cleaned = {k: ("" if row.get(k) is None else str(row.get(k))) for k in fieldnames}
            cleaned["role"] = cleaned["role"].upper()
            cleaned_rows.append(cleaned)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Wrote {len(cleaned_rows)} cleaned rows to {output_path.name}.")
    print(f"Removed {removed} rows where 'name' was empty.")


if __name__ == "__main__":
    main()
