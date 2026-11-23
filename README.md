# Tech Job Market Insights Dashboard

An interactive Streamlit dashboard for exploring **29,194 technology job postings**. It brings job titles, locations, employment types and skills into one place so users can see which roles appear most often and which skills employers mention for a specific role.

## What you can explore

Use the sidebar to filter by **country** and **employment type**. The dashboard updates the posting count, most common job title, and percentage of postings with recorded skills for the selected filters.

| Dashboard tab | What it shows |
| --- | --- |
| **Market Overview** | The top 10 job titles by posting count. |
| **Skills Explorer** | The top skills mentioned for a selected job title, with counts of matching postings and postings that list skills. |
| **Job Postings** | A preview of up to 20 matching records with the title, company, country, and employment type. |

## Dataset and preparation

The dashboard uses the **S subset** of the [DataForge Tech Job Postings Salary Dataset](https://data.zalize.com/datasets/tech-job-postings-salary-dataset), distributed via [Hugging Face](https://huggingface.co/datasets/zalizedata/tech-job-postings-salary-dataset). The snapshot is dated **August 1, 2026**, and the dashboard data includes postings dated from January 2020 through August 2026.

| Stage | Job postings |
| --- | ---: |
| Raw dataset | 35,417 |
| After deduplication by job ID | 31,676 |
| Final dashboard dataset | 29,194 |

The notebook loads the source Parquet file, keeps the most recently scraped record for each job ID, standardizes text and date fields, converts salary bounds to numeric values, fills selected missing categories with `Unknown`, and checks salary ranges. It then applies a character-based job title filter and exports `tech_jobs_cleaned.csv`. The exported file has 23 columns and no duplicate job IDs.

The title filter allows unaccented Latin letters, digits, spaces, and selected punctuation. Titles in other languages can pass this filter when written with those characters. The dataset reflects the postings captured in this snapshot, so counts describe the sample. Salary bounds use different currencies and pay periods and would need to be normalized before comparing compensation across postings.

### Dataset attribution and license

[`tech_jobs_cleaned.csv`](tech_jobs_cleaned.csv) is a modified subset of the DataForge dataset ([data.zalize.com](https://data.zalize.com)). The project team deduplicated, standardized, and filtered the source records, added a title-language field, and exported the result as CSV.

The DataForge curated data is shared under the [Creative Commons Attribution–NonCommercial 4.0 International license (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). Commercial use requires a separate DataForge license. Upstream license terms continue to apply to the underlying data.

## Notebook visualizations

- Top 8 skills across Data Engineer, Machine Learning Engineer, and AI Engineer roles. Each percentage uses the postings with recorded skills for that role.
- Top 10 job titles by posting count.

Both notebook charts use the cleaned data before the title filter. The dashboard reads the filtered CSV.

## Findings from the dashboard dataset

- **Senior Software Engineer** was the most frequent exact job title, with **288** postings.
- The **United States** led among recorded countries, with **12,495** postings.
- **Full-time** was the most common known employment type, with **18,632** postings.
- **8,545 postings (29.3%)** were marked as remote.
- **13,223 postings (45.3%)** had both a minimum and a maximum salary value.

## Run locally

Download or clone this repository, then run these commands from the project folder using Python 3:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) once Streamlit starts. Keep `tech_jobs_cleaned.csv` alongside `app.py`. The bundled CSV is enough to run the dashboard. Open the notebook in Google Colab to review or rerun data preparation and exploratory analysis.

## Project files

| File | Purpose |
| --- | --- |
| [Tech_Job_Market_Insights.ipynb](Tech_Job_Market_Insights.ipynb) | Data inspection, cleaning, exploratory analysis, and visualization. |
| [requirements.txt](requirements.txt) | Python dependencies for the dashboard. |
| [app.py](app.py) | Streamlit app with Pandas for data handling and Plotly for interactive charts. |
| [tech_jobs_cleaned.csv](tech_jobs_cleaned.csv) | Cleaned data used by the dashboard. |

## Team

- Afnan Alharbi
- Taif Alharbi
- Nawaf Alshaye
