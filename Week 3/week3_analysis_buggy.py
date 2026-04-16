import csv

from collections import Counter

def tally_primary_tools(rows):
    """
    Takes your list of dict rows (from csv.DictReader) and returns a Counter like:
    Counter({"FIGMA": 10, "JIRA": 6, ...})
    """
    counts = Counter()

    for row in rows:
        tool = row.get("primary_tool", "").strip()
        if not tool:
            continue

        tool = tool.title()  # or .upper() if you prefer
        counts[tool] += 1

    return counts

# Load the survey data from a CSV file
filename = "week3_survey_messy.csv"
rows = []

NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)
tool_counts = tally_primary_tools(rows)

print("\nPrimary tool counts:")
for tool, c in tool_counts.items():
    print(f"  {tool}: {c}")

# Count responses by role
# Normalize role names so "ux researcher" and "UX Researcher" are counted together
role_counts = {}

for row in rows:
    role = row["role"].strip().title()
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# Calculate the average years of experience including non-numeric values
total_experience = 0
count = 0
for row in rows:
    raw = row["experience_years"].strip().lower()

    if raw.isdigit():
        years = int(raw)
    elif raw in NUMBER_WORDS:
        years = NUMBER_WORDS[raw]
    else:
        continue

total_experience += years
count += 1
if count > 0:
    avg_experience = total_experience / count
    print(f"\nAverage years of experience: {avg_experience:.1f}")
else:
    print("\nAverage years of experience: (no valid numeric values)")

# Find the top 5 highest satisfaction scores updated to sort in descending order
scored_rows = []
for row in rows:
    if row["satisfaction_score"].strip():
        scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")
