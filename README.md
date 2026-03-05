# Data Exploration and Analytics Toolkit

A reusable Python toolkit for **data cleaning, transformation, and exploratory data analysis (EDA)**. This project automates common preprocessing tasks and visualizations to help generate insights quickly from raw datasets.

---

## Features

- **Data Cleaning**
  - Handle missing values automatically (mean, median, or fill with "Unknown")
  - Remove duplicate rows
- **Exploratory Data Analysis**
  - Generate summary statistics
  - Visualize distributions of numerical columns
  - Plot correlation matrices to understand feature relationships
- **Utilities**
  - Save cleaned datasets for downstream analysis
- **Reusable & Modular**
  - Functions are organized in separate modules (`data_cleaning.py`, `eda.py`, `utils.py`) for easy integration into other projects

---

## Installation

1. Clone or download the repository.
2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
