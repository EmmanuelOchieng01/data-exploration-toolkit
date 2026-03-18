"""
Exploratory Data Analysis — summary stats, distributions, correlations.
Returns Plotly figures for embedding in Streamlit.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#C8D8E8', family='DM Mono, monospace', size=11),
    xaxis=dict(gridcolor='#141E30', color='#5A7090', linecolor='#1C2A40'),
    yaxis=dict(gridcolor='#141E30', color='#5A7090', linecolor='#1C2A40'),
)

def summary_stats(df):
    """Return summary statistics as a DataFrame."""
    return df.describe(include='all').round(4)

def plot_distribution(df, col):
    """Histogram with KDE for a numeric column."""
    fig = px.histogram(df, x=col, marginal='box',
                       color_discrete_sequence=['#C9A84C'],
                       title=f'Distribution — {col}')
    fig.update_layout(**THEME, title_font_color='#EAF0F8')
    return fig

def plot_correlation(df):
    """Correlation heatmap for numeric columns."""
    numeric = df.select_dtypes(include='number')
    if numeric.shape[1] < 2:
        return None
    corr = numeric.corr().round(2)
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale=[[0,'#E05252'],[0.5,'#141E30'],[1,'#00BFA5']],
        text=corr.values, texttemplate='%{text}',
        showscale=True,
    ))
    fig.update_layout(**THEME, title='Correlation Matrix',
                      title_font_color='#EAF0F8')
    return fig

def plot_missing(df):
    """Bar chart of missing values per column."""
    nulls = df.isna().sum()
    nulls = nulls[nulls > 0].sort_values(ascending=False)
    if nulls.empty:
        return None
    fig = px.bar(x=nulls.index, y=nulls.values,
                 labels={'x':'Column','y':'Missing Values'},
                 color_discrete_sequence=['#E05252'],
                 title='Missing Values by Column')
    fig.update_layout(**THEME, title_font_color='#EAF0F8')
    return fig

def plot_categorical(df, col, top_n=15):
    """Bar chart of value counts for a categorical column."""
    vc = df[col].value_counts().head(top_n)
    fig = px.bar(x=vc.index.astype(str), y=vc.values,
                 labels={'x': col, 'y': 'Count'},
                 color_discrete_sequence=['#00BFA5'],
                 title=f'Top {top_n} Values — {col}')
    fig.update_layout(**THEME, title_font_color='#EAF0F8')
    return fig

def plot_scatter(df, x_col, y_col, color_col=None):
    """Scatter plot between two numeric columns."""
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                     color_discrete_sequence=px.colors.qualitative.Bold,
                     title=f'{x_col} vs {y_col}')
    fig.update_layout(**THEME, title_font_color='#EAF0F8')
    return fig

def get_outliers(df, col):
    """Return outlier count using IQR method."""
    q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    iqr = q3 - q1
    mask = (df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)
    return int(mask.sum())
