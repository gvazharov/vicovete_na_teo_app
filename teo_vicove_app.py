import pandas as pd
import streamlit as st

st.set_page_config(page_title="Вицовете на Тео", layout="wide")

st.title("😂 Вицовете на Тео")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("jokes.xlsx")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Филтър")

categories = sorted(df["категория"].dropna().unique())
selected_category = st.sidebar.selectbox(
    "Изберете категория",
    ["Всички"] + list(categories)
)

# Apply filter
filtered_df = df.copy()

if selected_category != "Всички":
    filtered_df = filtered_df[filtered_df["категория"] == selected_category]

# Search
search = st.text_input("Търси вицове по текст")

if search:
    filtered_df = filtered_df[
        filtered_df["виц_текст"].str.contains(search, case=False, na=False)
    ]

# Sort options
sort_by = st.selectbox("Сортиране по", ["гледания", "категория"])
ascending = st.checkbox("Възходящ ред", value=False)

filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

# Display
st.write(f"Показани са {len(filtered_df)} вицове от общо {len(df)}")

for _, row in filtered_df.iterrows():
    st.markdown("---")
    
    st.markdown(f"**📂 Категория:** {row['категория']}")
    st.markdown(f"**👁 Гледания:** {row['гледания']}")
    
    st.markdown(
        f"<div style='font-size:16px; line-height:1.6; white-space: pre-wrap;'>"
        f"{row['виц_текст']}"
        f"</div>",
        unsafe_allow_html=True
    )
