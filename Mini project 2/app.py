"""Coaching Class Survey dashboard — class-level SurveyMonkey feedback views."""

from __future__ import annotations

import dash
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go

from survey_data import (
    ALL_COURSES,
    ALL_YEARS,
    ATTEND,
    ATTEND_MAP,
    CHANGED,
    CHANGE_COLORS,
    CHANGE_LEVELS,
    CLASS_TYPE,
    DAY_OF_WEEK,
    EXPLAIN_ATTEND,
    EXPLAIN_RECOMMEND,
    FIRST_CLASS,
    LIKE_MOST,
    RECOMMEND,
    RECOMMEND_MAP,
    SATISFIED,
    SAT_COLORS,
    SAT_LEVELS,
    TIME_OF_DAY,
    TOPICS,
    WOULD_CHANGE,
    course_options,
    filter_survey,
    first_coaching_stats,
    load_survey,
    matrix_stats,
    rating_stats,
    single_choice_stats,
    text_responses,
    year_options,
)

DF = load_survey()

app = Dash(
    __name__,
    title="Coaching Class Survey Dashboard",
    assets_folder="assets",
    suppress_callback_exceptions=True,
)
server = app.server


def stats_line(answered: int, skipped: int) -> html.P:
    return html.P(
        [html.Span(f"Answered: {answered:,}"), html.Span(f"Skipped: {skipped:,}")],
        className="stats-line",
    )


def section_title(title: str, answered: int, skipped: int) -> html.Div:
    return html.Div(
        [html.H3(title, className="section-title"), stats_line(answered, skipped)],
        className="section-header",
    )


def star_rating(average: float | None) -> html.Div:
    if average is None:
        return html.Div([html.P("No responses yet.", className="empty-state")])

    full = int(average)
    partial = average - full
    stars = []
    for i in range(5):
        if i < full:
            fill = 100
        elif i == full and partial > 0:
            fill = round(partial * 100)
        else:
            fill = 0
        stars.append(
            html.Div(
                html.Span("★", className="star-icon"),
                className="star-box",
                style={"background": f"linear-gradient(90deg, #00BF6F {fill}%, #E6E6E6 {fill}%)"},
            )
        )

    return html.Div(
        [
            html.Div(
                [
                    html.Span(f"{average:.2f}", className="rating-number"),
                    html.Span("★", className="rating-star"),
                ],
                className="rating-average",
            ),
            html.P("average rating", className="rating-label"),
            html.Div(stars, className="star-row"),
        ],
        className="rating-card",
    )


def horizontal_pct_bar(
    labels: list[str],
    percentages: list[float],
    colors: list[str],
    x_max: float = 70,
) -> dcc.Graph:
    fig = go.Figure(
        go.Bar(
            y=labels[::-1],
            x=percentages[::-1],
            orientation="h",
            marker_color=colors[::-1],
            hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=20, t=10, b=10),
        height=max(180, 70 + 40 * len(labels)),
        xaxis=dict(range=[0, x_max], ticksuffix="%", dtick=10, showgrid=True, gridcolor="#EEEEEE"),
        yaxis=dict(showgrid=False),
        showlegend=False,
    )
    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def horizontal_count_bar(
    labels: list[str],
    counts: list[int],
    colors: list[str],
) -> dcc.Graph:
    fig = go.Figure(
        go.Bar(
            y=labels[::-1],
            x=counts[::-1],
            orientation="h",
            marker_color=colors[::-1],
            hovertemplate="%{y}: %{x:,} responses<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=20, t=10, b=10),
        height=max(220, 70 + 42 * len(labels)),
        xaxis=dict(showgrid=True, gridcolor="#EEEEEE"),
        yaxis=dict(showgrid=False),
        showlegend=False,
    )
    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def grouped_matrix_chart(
    rows: list[str],
    levels: list[str],
    series: dict[str, list[float]],
    colors: dict[str, str],
) -> dcc.Graph:
    fig = go.Figure()
    for level in levels:
        fig.add_trace(
            go.Bar(
                name=level,
                y=rows[::-1],
                x=series[level][::-1],
                orientation="h",
                marker_color=colors[level],
                hovertemplate="%{y}<br>" + level + ": %{x:.1f}%<extra></extra>",
            )
        )
    fig.update_layout(
        barmode="group",
        template="plotly_white",
        margin=dict(l=10, r=20, t=10, b=60),
        height=max(260, 80 + 55 * len(rows)),
        xaxis=dict(range=[0, 70], ticksuffix="%", dtick=10, showgrid=True, gridcolor="#EEEEEE"),
        yaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="top", y=-0.18, x=0),
    )
    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def response_list(responses: list[str]) -> html.Div:
    if not responses:
        return html.P("No responses yet.", className="empty-state")
    return html.Div(
        [html.Div(text, className="response-item") for text in responses],
        className="response-list",
    )


def build_dashboard(df):
    first = first_coaching_stats(df)
    recommend = rating_stats(df, RECOMMEND, RECOMMEND_MAP)
    explain_rec = text_responses(df, (EXPLAIN_RECOMMEND, "Open-Ended Response"))
    attend = rating_stats(df, ATTEND, ATTEND_MAP)
    explain_att = text_responses(df, (EXPLAIN_ATTEND, "Open-Ended Response"))
    satisfied = matrix_stats(df, SATISFIED, SAT_LEVELS, SAT_COLORS)
    changed = matrix_stats(df, CHANGED, CHANGE_LEVELS, CHANGE_COLORS)
    like_most = text_responses(df, (LIKE_MOST, "Open-Ended Response"))
    would_change = text_responses(df, (WOULD_CHANGE, "Open-Ended Response"))
    topics = text_responses(df, (TOPICS, "Open-Ended Response"))
    day = single_choice_stats(df, DAY_OF_WEEK)
    time = single_choice_stats(df, TIME_OF_DAY)
    class_type = single_choice_stats(df, CLASS_TYPE)

    return html.Div(
        [
            html.Div(
                [
                    section_title(FIRST_CLASS, first["answered"], first["skipped"]),
                    horizontal_pct_bar(first["labels"], first["percentages"], first["colors"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(RECOMMEND, recommend["answered"], recommend["skipped"]),
                    star_rating(recommend["average"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(EXPLAIN_RECOMMEND, explain_rec["answered"], explain_rec["skipped"]),
                    response_list(explain_rec["responses"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(ATTEND, attend["answered"], attend["skipped"]),
                    star_rating(attend["average"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(EXPLAIN_ATTEND, explain_att["answered"], explain_att["skipped"]),
                    response_list(explain_att["responses"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(SATISFIED, satisfied["answered"], satisfied["skipped"]),
                    grouped_matrix_chart(
                        satisfied["rows"],
                        satisfied["levels"],
                        satisfied["series"],
                        satisfied["colors"],
                    ),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(CHANGED, changed["answered"], changed["skipped"]),
                    grouped_matrix_chart(
                        changed["rows"],
                        changed["levels"],
                        changed["series"],
                        changed["colors"],
                    ),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(LIKE_MOST, like_most["answered"], like_most["skipped"]),
                    response_list(like_most["responses"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(WOULD_CHANGE, would_change["answered"], would_change["skipped"]),
                    response_list(would_change["responses"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(TOPICS, topics["answered"], topics["skipped"]),
                    response_list(topics["responses"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(DAY_OF_WEEK, day["answered"], day["skipped"]),
                    horizontal_count_bar(day["labels"], day["counts"], day["colors"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(TIME_OF_DAY, time["answered"], time["skipped"]),
                    horizontal_count_bar(time["labels"], time["counts"], time["colors"]),
                ],
                className="card",
            ),
            html.Div(
                [
                    section_title(CLASS_TYPE, class_type["answered"], class_type["skipped"]),
                    horizontal_count_bar(class_type["labels"], class_type["counts"], class_type["colors"]),
                ],
                className="card",
            ),
        ],
        className="dashboard-grid",
    )


app.layout = html.Div(
    [
        html.Header(
            [
                html.H1("Coaching Class Survey Dashboard"),
                html.P(
                    "Class-level feedback from SurveyMonkey exports for coaching operations and coaches."
                ),
            ],
            className="page-header",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Year"),
                        dcc.Dropdown(
                            id="year-filter",
                            options=year_options(DF),
                            value=ALL_YEARS,
                            clearable=False,
                        ),
                    ],
                    className="filter-item",
                ),
                html.Div(
                    [
                        html.Label("Course"),
                        dcc.Dropdown(
                            id="course-filter",
                            options=course_options(DF),
                            value=ALL_COURSES,
                            clearable=False,
                            searchable=True,
                        ),
                    ],
                    className="filter-item filter-item-wide",
                ),
            ],
            className="filters",
        ),
        html.Div(id="summary-banner", className="summary-banner"),
        html.Div(id="dashboard-content"),
    ],
    className="page",
)


@app.callback(
    Output("summary-banner", "children"),
    Output("dashboard-content", "children"),
    Input("year-filter", "value"),
    Input("course-filter", "value"),
)
def update_dashboard(year, course):
    filtered = filter_survey(DF, course, year)
    course_label = "All courses (aggregate)" if course == ALL_COURSES else course.replace("_", " ")
    year_label = "All years" if year == ALL_YEARS else str(year)
    banner = html.P(
        f"Showing {len(filtered):,} responses · {year_label} · {course_label}",
        className="summary-text",
    )
    return banner, build_dashboard(filtered)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
