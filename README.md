# Data Exploration Toolkit

A reusable data analysis toolkit with an interactive web interface. Upload any CSV or Excel file and instantly clean, explore, and visualise it — no code required.

---

## What it does

**Data Quality Report** — Shows missing values, null percentages, unique value counts, and data types for every column. Highlights problem areas before you start analysis.

**Data Cleaning** — Fills missing numeric values using mean or median strategy. Removes duplicate rows. Returns a report of exactly what was changed and by how much.

**Exploratory Analysis** — Summary statistics, correlation heatmap, distribution charts with outlier detection, scatter plots, and category value breakdowns. All interactive Plotly charts.

**Export** — Download the cleaned dataset as a CSV file ready for downstream use in models, reports, or further analysis.

---

## Launch Procedure

Requirements: Python 3.8+

```bash
git clone https://github.com/EmmanuelOchieng01/data-exploration-toolkit
cd data-exploration-toolkit
pip install -r requirements.txt
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## How to use it

1. Upload a CSV or Excel file using the file uploader
2. Check the **Data Quality** tab — review missing values and column types
3. Go to **Clean Data** — choose a missing value strategy and click Clean Dataset
4. Go to **Explore** — view correlation matrix, distributions, scatter plots, and category breakdowns
5. Go to **Export** — download the cleaned file as CSV

---

## Project structure

```
├── app.py                          # Streamlit dashboard
├── requirements.txt
├── src/
│   ├── data_cleaning.py            # Missing value handling, duplicates, quality report
│   ├── eda.py                      # Plotly charts — distributions, correlation, scatter
│   └── utils.py                    # Save, export, dataset info helpers
└── notebooks/
    └── demo.ipynb                  # Jupyter notebook walkthrough
```

---

## Tech stack

**Backend** — Python, Pandas, NumPy

**Frontend** — Streamlit, Plotly

**Analysis** — Descriptive statistics, IQR outlier detection, Pearson correlation

---

## Author

**Emmanuel Ochieng**
GitHub: https://github.com/EmmanuelOchieng01

---

*For educational and portfolio purposes.*
