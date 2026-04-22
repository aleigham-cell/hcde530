import csv
from pathlib import Path


def is_blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def main() -> None:
    #Set the paths for the input and output files
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / "responses.csv"
    output_path = script_dir / "responses_cleaned.csv"

    #If the file does not exist, raise an error
    if not input_path.exists():
        raise FileNotFoundError(
            f"Could not find {input_path.name}. Put it in: {script_dir}"
        )

    #Open the input file and read the data
    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        #Check for a header row
        if reader.fieldnames is None:
            raise ValueError("CSV appears to be missing a header row.")

        #Get all fieldnames and check for names/roles to be present
        fieldnames = list(reader.fieldnames)
        if "name" not in fieldnames:
            raise KeyError("Expected a 'name' column in responses.csv.")
        if "role" not in fieldnames:
            raise KeyError("Expected a 'role' column in responses.csv.")

        #Define a list to store cleaned rows
        cleaned_rows: list[dict[str, str]] = []

        #Define a variable to count the number of rows removed
        removed = 0

        #Loop through each row in the reader and check if the name is blank
        for row in reader:
            if is_blank(row.get("name")):
                removed += 1
                continue

            # Keep the same columns/order as the input file.
            cleaned = {k: ("" if row.get(k) is None else str(row.get(k))) for k in fieldnames}
            #Convert the role to uppercase
            cleaned["role"] = cleaned["role"].upper()
            cleaned_rows.append(cleaned)

    #Open the output file and write the cleaned data
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Wrote {len(cleaned_rows)} cleaned rows to {output_path.name}.")
    print(f"Removed {removed} rows where 'name' was empty.")


if __name__ == "__main__":
    main()
