import ast
import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Tech Job Market Insights", layout="wide")

TEAL = "#0F766E"
PURPLE = "#6D5BD0"
CSV_PATH = Path(__file__).with_name("tech_jobs_cleaned.csv")


def parse_skills(value):
    # Read quoted skills with or without commas.
    if not isinstance(value, str):
        return []

    tokens = re.findall(r"""'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*" """.strip(), value)
    skills = []

    for token in tokens:
        try:
            skill = ast.literal_eval(token).strip()
        except (ValueError, SyntaxError):
            continue

        if skill:
            skills.append(skill)

    return list(dict.fromkeys(skills))


@st.cache_data
def load_jobs(path, modified_at):
    jobs = pd.read_csv(path, dtype="string", keep_default_na=False)

    for column in ["job_title", "country", "employment_type"]:
        jobs[column] = jobs[column].str.strip()

    jobs["skills"] = jobs["required_skills"].map(parse_skills)
    return jobs


def ranking_chart(counts, label, color, axis_title):
    chart_data = counts.sort_values().rename_axis(label).reset_index(name="Postings")

    fig = px.bar(
        chart_data,
        x="Postings",
        y=label,
        orientation="h",
        text="Postings",
        color_discrete_sequence=[color],
        template="plotly_white",
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        height=max(240, 36 * len(chart_data) + 80),
        margin=dict(l=12, r=30, t=16, b=45),
        font=dict(color="#1E293B", size=13),
        bargap=0.3,
    )
    fig.update_xaxes(
        title=axis_title,
        range=[0, counts.max() * 1.2],
        tickformat="d",
        gridcolor="#E8EDF3",
    )
    fig.update_yaxes(title=None, automargin=True)
    return fig


st.title("Tech Job Market Insights")

with st.sidebar:
    st.header("Dataset")
    st.markdown(
        "Public tech job postings from DataForge. "
        "Snapshot: August 1, 2026.\n\n"
        "[View dataset on Hugging Face]"
        "(https://huggingface.co/datasets/zalizedata/tech-job-postings-salary-dataset)"
    )

if not CSV_PATH.is_file():
    st.error("Run the notebook cell that saves tech_jobs_cleaned.csv first.")
    st.stop()

jobs = load_jobs(CSV_PATH, CSV_PATH.stat().st_mtime_ns)

with st.sidebar:
    st.header("Filters")
    countries = st.multiselect(
        "Country",
        sorted(jobs.loc[jobs["country"].ne(""), "country"].unique()),
        placeholder="All countries",
    )
    employment_types = st.multiselect(
        "Employment type",
        sorted(jobs.loc[jobs["employment_type"].ne(""), "employment_type"].unique()),
        placeholder="All employment types",
    )

if countries:
    jobs = jobs.loc[jobs["country"].isin(countries)]

if employment_types:
    jobs = jobs.loc[jobs["employment_type"].isin(employment_types)]

if jobs.empty:
    st.info("No postings match these filters. Try a different selection.")
    st.stop()

title_counts = jobs.loc[jobs["job_title"].ne(""), "job_title"].value_counts()
has_skills = jobs["skills"].map(len).gt(0)

total, top_title, coverage = st.columns([1, 2, 1])
total.metric("Job postings", f"{len(jobs):,}")
top_title.metric("Most common job title", title_counts.index[0] if len(title_counts) else "—")
coverage.metric("Postings with recorded skills", f"{has_skills.mean():.0%}")

overview_tab, skills_tab, data_tab = st.tabs(
    ["Market Overview", "Skills Explorer", "Job Postings"]
)

with overview_tab:
    st.subheader("Top 10 Job Titles")
    if title_counts.empty:
        st.info("No job titles are available for these filters.")
    else:
        st.plotly_chart(ranking_chart(
            title_counts.head(10), "Job title", TEAL, "Number of postings"
        ))

with skills_tab:
    st.subheader("Top Skills by Job Title")

    if title_counts.empty:
        st.info("No job titles are available for these filters.")
    else:
        available_titles = title_counts.index.tolist()
        default_index = (
            available_titles.index("AI Engineer")
            if "AI Engineer" in available_titles else 0
        )
        selected_title = st.selectbox("Choose a job title", available_titles, index=default_index)

        role_jobs = jobs.loc[jobs["job_title"].eq(selected_title)]
        recorded_skills = role_jobs.loc[role_jobs["skills"].map(len).gt(0), "skills"]

        st.caption(
            f"{len(role_jobs):,} matching postings · "
            f"{len(recorded_skills):,} with recorded skills"
        )

        if recorded_skills.empty:
            st.info("No skills were recorded for this job title under these filters.")
        else:
            top_skills = recorded_skills.explode().value_counts().head(10)
            st.plotly_chart(ranking_chart(
                top_skills, "Skill", PURPLE, "Number of postings mentioning the skill"
            ))

with data_tab:
    st.subheader("Job Postings Preview")
    preview_columns = ["job_title", "company", "country", "employment_type"]
    preview = jobs[preview_columns].head(20)
    st.dataframe(preview, hide_index=True)
    st.caption(f"Showing {len(preview):,} of {len(jobs):,} matching postings.")
