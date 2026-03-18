import streamlit as st
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_cleaning import load_data, clean_missing, drop_duplicates, get_quality_report
from eda import (summary_stats, plot_distribution, plot_correlation,
                 plot_missing, plot_categorical, plot_scatter, get_outliers)
from utils import to_csv_bytes, get_dataset_info

st.set_page_config(page_title="DataIQ Toolkit", page_icon="▣", layout="wide")

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@300;400;500&family=Sora:wght@300;400;600;700&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewContainer"]>.main{background:#05080F!important;color:#C8D8E8!important;font-family:'Sora',sans-serif!important;}
#MainMenu,footer,header,[data-testid="stToolbar"]{visibility:hidden!important;display:none!important;}
.block-container{padding:0 2rem 3rem 2rem!important;max-width:1400px!important;}
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid #141E30!important;}
[data-testid="stTabs"] [data-baseweb="tab"]{background:transparent!important;color:#5A7090!important;font-family:'DM Mono',monospace!important;font-size:0.68rem!important;letter-spacing:0.12em!important;text-transform:uppercase!important;padding:0.8rem 1.6rem!important;border:none!important;border-bottom:2px solid transparent!important;}
[data-testid="stTabs"] [aria-selected="true"][data-baseweb="tab"]{color:#C9A84C!important;border-bottom:2px solid #C9A84C!important;}
[data-testid="stTabs"] [data-baseweb="tab-highlight"],[data-testid="stTabs"] [data-baseweb="tab-border"]{display:none!important;}
[data-testid="stFileUploader"]{background:#090D16!important;border:1px dashed #1C2A40!important;border-radius:10px!important;}
div[data-testid="metric-container"]{background:#090D16!important;border:1px solid #141E30!important;border-radius:10px!important;padding:1rem!important;}
div[data-testid="metric-container"] label{color:#5A7090!important;font-family:'DM Mono',monospace!important;font-size:0.6rem!important;text-transform:uppercase!important;letter-spacing:0.08em!important;}
div[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#EAF0F8!important;font-family:'Instrument Serif',serif!important;font-size:1.6rem!important;}
[data-baseweb="select"]>div{background:#090D16!important;border:1px solid #1C2A40!important;border-radius:7px!important;}
[data-baseweb="select"] span{color:#C8D8E8!important;font-family:'DM Mono',monospace!important;}
label,[data-testid="stWidgetLabel"] p{font-family:'DM Mono',monospace!important;font-size:0.65rem!important;letter-spacing:0.08em!important;text-transform:uppercase!important;color:#5A7090!important;}
.stButton>button{background:linear-gradient(135deg,#C9A84C,#E8C96A)!important;color:#05080F!important;font-family:'Sora',sans-serif!important;font-weight:700!important;border:none!important;border-radius:8px!important;}
.stDownloadButton>button{background:transparent!important;color:#C8D8E8!important;border:1px solid #1C2A40!important;border-radius:8px!important;font-family:'DM Mono',monospace!important;font-size:0.72rem!important;}
.stDownloadButton>button:hover{border-color:#C9A84C!important;color:#C9A84C!important;}
[data-testid="stDataFrame"]{border:1px solid #141E30!important;border-radius:10px!important;}
hr{border-color:#141E30!important;}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div style="padding:2rem 0 1.5rem 0;border-bottom:1px solid #141E30;margin-bottom:2rem;
            display:flex;align-items:flex-end;justify-content:space-between;">
  <div>
    <div style="font-family:'DM Mono',monospace;font-size:0.62rem;letter-spacing:0.2em;
                text-transform:uppercase;color:#C9A84C;margin-bottom:0.4rem;">
      ◈ DataIQ &nbsp;·&nbsp; Data Exploration Toolkit
    </div>
    <div style="font-family:'Instrument Serif',serif;font-size:2.2rem;font-weight:400;color:#EAF0F8;line-height:1.1;">
      Data Exploration Toolkit
    </div>
    <div style="font-family:'Sora',sans-serif;font-size:0.88rem;color:#5A7090;margin-top:0.4rem;">
      Upload any CSV or Excel file — clean, analyse, and export in seconds
    </div>
  </div>
  <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#3A4A60;text-align:right;line-height:1.8;">
    Cleaning &nbsp;·&nbsp; EDA &nbsp;·&nbsp; Visualisation<br>No code required
  </div>
</div>
""", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload CSV or Excel file", type=['csv','xlsx','xls'])

if not uploaded:
    c1, c2, c3 = st.columns(3)
    for col, title, desc in [
        (c1, "Upload Any Dataset",   "CSV or Excel files up to any size. The toolkit auto-detects column types and missing value patterns."),
        (c2, "Clean & Transform",    "Fill missing values, drop duplicates, and get a full data quality report with one click."),
        (c3, "Explore & Export",     "Distribution charts, correlation matrices, scatter plots, and category breakdowns. Download cleaned data as CSV."),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#090D16;border:1px solid #141E30;border-radius:12px;padding:1.5rem;">
                <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#C9A84C;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.8rem;">{title}</div>
                <div style="font-family:'Sora',sans-serif;font-size:0.82rem;color:#5A7090;line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)
    st.stop()

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load(file):
    return load_data(file)

df_raw = load(uploaded)
info   = get_dataset_info(df_raw)

# ── Dataset KPIs ──────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("Rows",         f"{info['rows']:,}")
k2.metric("Columns",      info['columns'])
k3.metric("Numeric",      info['numeric_cols'])
k4.metric("Text",         info['text_cols'])
k5.metric("Missing",      info['total_nulls'])
k6.metric("Duplicates",   info['duplicates'])

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────
t1, t2, t3, t4 = st.tabs(["Data Quality", "Clean Data", "Explore", "Export"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — DATA QUALITY
# ══════════════════════════════════════════════════════════════
with t1:
    st.markdown("**Quality Report**")
    qr = get_quality_report(df_raw)
    st.dataframe(pd.DataFrame(qr), use_container_width=True, hide_index=True)

    fig_missing = plot_missing(df_raw)
    if fig_missing:
        st.plotly_chart(fig_missing, use_container_width=True)
    else:
        st.success("No missing values detected in this dataset.")

    st.markdown("**Raw Data Preview**")
    st.dataframe(df_raw.head(100), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — CLEAN
# ══════════════════════════════════════════════════════════════
with t2:
    c1, c2 = st.columns(2)
    with c1:
        strategy = st.selectbox("Missing value strategy", ["mean","median"])
    with c2:
        remove_dups = st.checkbox("Remove duplicate rows", value=True)

    if st.button("Clean Dataset", type="primary"):
        df_clean, missing_report = clean_missing(df_raw.copy(), strategy)
        if remove_dups:
            df_clean, n_dups = drop_duplicates(df_clean)
        else:
            n_dups = 0

        st.session_state['df_clean'] = df_clean
        st.session_state['filename'] = uploaded.name.rsplit('.',1)[0] + '_cleaned.csv'

        st.success(f"Done — {n_dups} duplicates removed. Missing values filled using {strategy}.")

        cols_filled = {k:v for k,v in missing_report.items() if k != '_text_filled'}
        if cols_filled:
            st.markdown("**Columns filled**")
            st.dataframe(pd.DataFrame(cols_filled).T, use_container_width=True)

        st.markdown("**Cleaned Data Preview**")
        st.dataframe(df_clean.head(100), use_container_width=True, hide_index=True)
    else:
        st.info("Configure options above and click Clean Dataset.")

# ══════════════════════════════════════════════════════════════
# TAB 3 — EXPLORE
# ══════════════════════════════════════════════════════════════
with t3:
    df_work = st.session_state.get('df_clean', df_raw)
    numeric_cols  = df_work.select_dtypes(include='number').columns.tolist()
    category_cols = df_work.select_dtypes(include='object').columns.tolist()

    # Summary stats
    st.markdown("**Summary Statistics**")
    st.dataframe(summary_stats(df_work), use_container_width=True)
    st.markdown("---")

    # Correlation
    st.markdown("**Correlation Matrix**")
    fig_corr = plot_correlation(df_work)
    if fig_corr:
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns for correlation.")
    st.markdown("---")

    # Distribution
    if numeric_cols:
        st.markdown("**Distribution**")
        col_dist = st.selectbox("Select column", numeric_cols, key="dist_col")
        outliers = get_outliers(df_work, col_dist)
        st.caption(f"Outliers detected (IQR method): {outliers}")
        st.plotly_chart(plot_distribution(df_work, col_dist), use_container_width=True)
        st.markdown("---")

    # Scatter
    if len(numeric_cols) >= 2:
        st.markdown("**Scatter Plot**")
        sc1, sc2, sc3 = st.columns(3)
        with sc1: x_col = st.selectbox("X axis", numeric_cols, key="sc_x")
        with sc2: y_col = st.selectbox("Y axis", numeric_cols, index=1, key="sc_y")
        with sc3: color_col = st.selectbox("Colour by", ['None'] + category_cols, key="sc_c")
        st.plotly_chart(
            plot_scatter(df_work, x_col, y_col, None if color_col=='None' else color_col),
            use_container_width=True
        )
        st.markdown("---")

    # Categorical
    if category_cols:
        st.markdown("**Category Breakdown**")
        cat_col = st.selectbox("Select column", category_cols, key="cat_col")
        top_n   = st.slider("Top N values", 5, 30, 15)
        st.plotly_chart(plot_categorical(df_work, cat_col, top_n), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — EXPORT
# ══════════════════════════════════════════════════════════════
with t4:
    if 'df_clean' not in st.session_state:
        st.info("Clean your data in the Clean Data tab first.")
    else:
        df_clean = st.session_state['df_clean']
        fname    = st.session_state.get('filename','cleaned_data.csv')
        info2    = get_dataset_info(df_clean)

        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Rows",    f"{info2['rows']:,}")
        k2.metric("Columns", info2['columns'])
        k3.metric("Missing", info2['total_nulls'])
        k4.metric("Size",    f"{info2['memory_kb']} KB")

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.download_button(
            "Download Cleaned CSV",
            data=to_csv_bytes(df_clean),
            file_name=fname,
            mime='text/csv',
        )
        st.markdown("**Preview**")
        st.dataframe(df_clean.head(100), use_container_width=True, hide_index=True)

# Footer
st.markdown("""
<div style="margin-top:3rem;padding-top:1.5rem;border-top:1px solid #0F1923;
            display:flex;justify-content:space-between;font-family:'DM Mono',monospace;
            font-size:0.58rem;color:#1C2A40;">
  <span>DataIQ &nbsp;·&nbsp; Data Exploration Toolkit</span>
  <span>Upload · Clean · Explore · Export</span>
</div>""", unsafe_allow_html=True)
