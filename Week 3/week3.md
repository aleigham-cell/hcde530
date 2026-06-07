C2 - Code literacy and documentation — Reading code well enough to explain what it does, change it when needed, and document it for others. Writing commit messages, docstrings, and README content that make your work legible.

1) I added comments in `clean_responses.py` for the main steps: setting paths, reading the CSV, looping through rows, and writing the cleaned file.

C3 - Data cleaning and file handling — Loading, inspecting, and cleaning messy datasets with Python. Reading error messages. Writing scripts that run repeatably on any dataset.

1) When I looked at `week3_survey_messy.csv`, the data wasn't always ready for code to use as-is. Roles were inconsistent (`ux designer` vs `UX Researcher`), R005 had a blank name, and R009 had `fifteen` written out in `experience_years` instead of the number 15.

2) For the average years of experience, the script tried to turn every value into an integer with `int()`. That worked for rows like `"3"` or `"12"`, but on R009 it hit `"fifteen"` or "5-44" and threw a `ValueError` — so that row didn't get counted and the average was off. I fixed it by adding a `NUMBER_WORDS` dictionary to convert word values before averaging.

3) For the top 5 satisfaction scores, I had sorted the list in the default ascending order and then taken the first five rows — which actually gave me the five *lowest* scores, not the highest. I added `reverse=True` to the sort so the top of the list is really the top.

4) In `clean_responses.py` (different file), `responses.csv` had two rows with empty names (P002 and P004). The script drops those and uppercases `role` so `count_roles.py` doesn't double-count the same role with different casing.
