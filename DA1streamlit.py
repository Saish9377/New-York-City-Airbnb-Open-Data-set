import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Page setup
st.set_page_config(page_title="Airbnb NYC Analysis", layout="wide")
st.title("🏨 Airbnb NYC 2019 - Data Analysis Dashboard")

# Styling
sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
warnings.filterwarnings("ignore")

# File upload
uploaded_file = st.file_uploader("📁 Upload the Airbnb NYC 2019 CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"File uploaded successfully! Shape: {df.shape}")

    # Show basic info
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(5))

    st.subheader("📊 Missing Values")
    st.write(df.isnull().sum())

    # --- Analysis Sections ---
    st.subheader("📅 Reviews Per Month")
    review_counts = df['reviews_per_month'].dropna()
    fig1, ax1 = plt.subplots()
    sns.histplot(review_counts, bins=30, kde=True, ax=ax1)
    ax1.set_title("Distribution of Reviews per Month")
    st.pyplot(fig1)

    st.subheader("🏘️ Room Type Distribution")
    room_counts = df['room_type'].value_counts()
    st.bar_chart(room_counts)

    st.subheader("🏠 Room Type Breakdown")
    room_summary = df['room_type'].value_counts().reset_index()
    room_summary.columns = ['Room Type', 'Count']
    st.dataframe(room_summary)

    st.subheader("📅 Last Review Date Filter")
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    min_date = df['last_review'].min()
    max_date = df['last_review'].max()

    selected_date = st.slider("Select review date range", min_value=min_date, max_value=max_date, value=(min_date, max_date))
    filtered_df = df[(df['last_review'] >= selected_date[0]) & (df['last_review'] <= selected_date[1])]
    st.write(f"Filtered entries: {filtered_df.shape[0]}")
    st.dataframe(filtered_df[['name', 'host_name', 'last_review']].head(10))

    st.subheader("💵 Price Distribution by Neighborhood Group")
    fig2, ax2 = plt.subplots()
    sns.boxplot(x="neighbourhood_group", y="price", data=df[df['price'] < 500], ax=ax2)
    ax2.set_title("Price Distribution by Neighborhood Group (Price < $500)")
    st.pyplot(fig2)

    st.subheader("📌 Host Listings per Neighborhood Group")
    host_table = df.groupby(['host_id', 'neighbourhood_group']).size().reset_index(name='Listings')
    st.dataframe(host_table.head(10))
else:
    st.info("Please upload the Airbnb NYC CSV file to begin.")
