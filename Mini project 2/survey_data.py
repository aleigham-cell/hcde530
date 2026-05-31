"""Load and transform SurveyMonkey coaching-class survey exports."""

from __future__ import annotations

from collections import OrderedDict
from typing import Iterable

import pandas as pd

SURVEY_PATH = "/Users/amattison/Documents/Coaching_Class_Survey/Survey.xlsx"

COURSE_COL = ("course title", "Open-Ended Response")
CLASS_DATE_COL = ("class date", "Open-Ended Response")

FIRST_CLASS = "Was this your first coaching class?"
RECOMMEND = "How likely is it that you would recommend a coaching class to a friend or coworker?"
ATTEND = "How likely is it that you would attend another coaching class?"
EXPLAIN_RECOMMEND = "Please explain why you would/would not recommend."
EXPLAIN_ATTEND = "Please explain why you would/would not attend another class."
SATISFIED = "How satisfied are you with the following?"
CHANGED = "How much would you say these areas have changed after you took a class?"
LIKE_MOST = "What did you like most about your class?"
WOULD_CHANGE = "What would you change, if anything, about your class?"
TOPICS = "What topics would you like to learn more about in future coaching classes?"
DAY_OF_WEEK = "Which day of the week are you most likely to attend a class?"
TIME_OF_DAY = "Which time of day are you most likely to attend a class?"
CLASS_TYPE = "What type of class would you be most likely to attend?"

ALL_COURSES = "__ALL__"
ALL_YEARS = "__ALL__"

SAT_LEVELS = [
    "Very Dissatisfied",
    "Dissatisfied",
    "Neither Satisfied nor Dissatisfied",
    "Satisfied",
    "Very Satisfied",
]
CHANGE_LEVELS = [
    "Greatly Declined",
    "Declined",
    "Did Not Change",
    "Improved",
    "Greatly Improved",
]

SAT_COLORS = {
    "Very Dissatisfied": "#00BF6F",
    "Dissatisfied": "#2E67B1",
    "Neither Satisfied nor Dissatisfied": "#F9BE00",
    "Satisfied": "#67B7DC",
    "Very Satisfied": "#EF8B33",
}
CHANGE_COLORS = {
    "Greatly Declined": "#00BF6F",
    "Declined": "#2E67B1",
    "Did Not Change": "#F9BE00",
    "Improved": "#67B7DC",
    "Greatly Improved": "#EF8B33",
}

DAY_COLORS = [
    "#00BF6F",
    "#2E67B1",
    "#F9BE00",
    "#67B7DC",
    "#EF8B33",
    "#8E7CC3",
    "#E5007E",
]

RECOMMEND_MAP = {" - 1": 1, " - 2": 2, " - 3": 3, " - 4": 4, " - 5": 5}
ATTEND_MAP = {
    " - Not at all likely": 1,
    " - 2": 2,
    " - 3": 3,
    " - 4": 4,
    " - Extremely likely": 5,
}


def load_survey(path: str = SURVEY_PATH) -> pd.DataFrame:
    df = pd.read_excel(path, header=[0, 1])
    df["year"] = pd.to_datetime(df[CLASS_DATE_COL], errors="coerce").dt.year
    return df


def display_course(name: str) -> str:
    return name.replace("_", " ")


def course_options(df: pd.DataFrame) -> list[dict]:
    titles = sorted(df[COURSE_COL].dropna().unique(), key=str)
    return [{"label": "All courses (aggregate)", "value": ALL_COURSES}] + [
        {"label": display_course(t), "value": t} for t in titles
    ]


def year_options(df: pd.DataFrame) -> list[dict]:
    years = sorted(int(y) for y in df["year"].dropna().unique())
    return [{"label": "All years", "value": ALL_YEARS}] + [
        {"label": str(y), "value": str(y)} for y in years
    ]


def filter_survey(
    df: pd.DataFrame, course: str, year: str | int | None
) -> pd.DataFrame:
    subset = df.copy()
    if year not in (None, ALL_YEARS, "All years"):
        subset = subset[subset["year"] == int(year)]
    if course not in (None, ALL_COURSES):
        subset = subset[subset[COURSE_COL] == course]
    return subset


def answered_skipped(mask: pd.Series) -> tuple[int, int]:
    answered = int(mask.sum())
    skipped = int((~mask).sum())
    return answered, skipped


def cols_for_question(df: pd.DataFrame, question: str) -> list[tuple]:
    return [c for c in df.columns if isinstance(c, tuple) and c[0] == question]


def one_hot_answered(df: pd.DataFrame, cols: Iterable[tuple]) -> pd.Series:
    subset = df[list(cols)]
    return subset.notna().any(axis=1)


def text_answered(df: pd.DataFrame, col: tuple) -> pd.Series:
    return df[col].notna() & df[col].astype(str).str.strip().ne("")


def derive_one_hot_score(df: pd.DataFrame, cols: list[tuple], mapping: dict) -> pd.Series:
    scores = []
    for _, row in df[cols].iterrows():
        value = None
        for col in cols:
            if pd.notna(row[col]):
                value = mapping.get(col[1], row[col])
                try:
                    value = float(value)
                except (TypeError, ValueError):
                    pass
                break
        scores.append(value)
    return pd.Series(scores, index=df.index, dtype=float)


def pct_of_total(count: int, total: int) -> float:
    return (count / total * 100) if total else 0.0


def matrix_items_and_levels(
    df: pd.DataFrame, question: str, levels: list[str]
) -> OrderedDict[str, list[tuple]]:
    cols = cols_for_question(df, question)
    items: OrderedDict[str, list[tuple]] = OrderedDict()
    for col in cols:
        if " - " not in str(col[1]):
            continue
        item, level = str(col[1]).rsplit(" - ", 1)
        if level not in levels:
            continue
        items.setdefault(item, []).append(col)
    for item in items:
        items[item] = sorted(
            items[item], key=lambda c: levels.index(str(c[1]).rsplit(" - ", 1)[1])
        )
    return items


def matrix_question_answered(
    df: pd.DataFrame, question: str, levels: list[str]
) -> pd.Series:
    cols = [
        c
        for c in cols_for_question(df, question)
        if " - " in str(c[1]) and str(c[1]).rsplit(" - ", 1)[1] in levels
    ]
    return one_hot_answered(df, cols)


def first_coaching_stats(df: pd.DataFrame) -> dict:
    total = len(df)
    yes = df[("Was this your first coaching class?", "Yes")].notna().sum()
    no = df[("Was this your first coaching class?", "No")].notna().sum()
    answered_mask = one_hot_answered(
        df, [("Was this your first coaching class?", "Yes"), ("Was this your first coaching class?", "No")]
    )
    answered, skipped = answered_skipped(answered_mask)
    return {
        "labels": ["Yes", "No"],
        "values": [yes, no],
        "percentages": [pct_of_total(yes, total), pct_of_total(no, total)],
        "colors": ["#00BF6F", "#2E67B1"],
        "answered": answered,
        "skipped": skipped,
    }


def rating_stats(df: pd.DataFrame, question: str, mapping: dict) -> dict:
    cols = cols_for_question(df, question)
    answered_mask = one_hot_answered(df, cols)
    answered, skipped = answered_skipped(answered_mask)
    scores = derive_one_hot_score(df, cols, mapping)
    avg = scores.mean(skipna=True)
    return {
        "average": avg if pd.notna(avg) else None,
        "answered": answered,
        "skipped": skipped,
    }


def text_responses(df: pd.DataFrame, col: tuple) -> dict:
    mask = text_answered(df, col)
    answered, skipped = answered_skipped(mask)
    responses = df.loc[mask, col].astype(str).tolist()
    return {"responses": responses, "answered": answered, "skipped": skipped}


def matrix_stats(
    df: pd.DataFrame, question: str, levels: list[str], colors: dict[str, str]
) -> dict:
    total = len(df)
    items = matrix_items_and_levels(df, question, levels)
    answered_mask = matrix_question_answered(df, question, levels)
    answered, skipped = answered_skipped(answered_mask)

    row_labels = []
    series = {level: [] for level in levels}
    for item, item_cols in items.items():
        row_labels.append(item)
        for level in levels:
            col = next(c for c in item_cols if str(c[1]).endswith(f" - {level}"))
            count = df[col].notna().sum()
            series[level].append(pct_of_total(count, total))

    return {
        "rows": row_labels,
        "levels": levels,
        "series": series,
        "colors": colors,
        "answered": answered,
        "skipped": skipped,
    }


def single_choice_stats(df: pd.DataFrame, question: str, colors: list[str] | None = None) -> dict:
    cols = cols_for_question(df, question)
    answered_mask = one_hot_answered(df, cols)
    answered, skipped = answered_skipped(answered_mask)
    labels = [c[1] for c in cols]
    counts = [int(df[c].notna().sum()) for c in cols]
    return {
        "labels": labels,
        "counts": counts,
        "colors": colors or DAY_COLORS[: len(labels)],
        "answered": answered,
        "skipped": skipped,
    }
