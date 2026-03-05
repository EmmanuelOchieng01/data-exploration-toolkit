import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def summary(df):
    desc = df.describe(include='all')
    info = df.info()
    print(desc)
    return desc, info

def plot_distribution(df, col):
    plt.figure(figsize=(6,4))
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.show()

def correlation_matrix(df):
    plt.figure(figsize=(8,6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()
