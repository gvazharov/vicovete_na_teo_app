import pandas as pd
import streamlit as st

st.set_page_config(page_title="Вицовете на Тео", layout="wide")

st.markdown("""
<style>
/* Target Streamlit selectbox dropdown */
div[data-baseweb="select"] > div {
    cursor: pointer !important;
}

/* Dropdown options */
ul[role="listbox"] li {
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-baseweb="select"] > div:hover {
    border-color: #999;
}
</style>
""", unsafe_allow_html=True)

st.title("😂 Вицовете на Тео")


# =========================
# LOAD + CACHE
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("jokes.xlsx")

    df["виц_текст"] = (
        df["виц_текст"]
        .astype(str)
        .str.replace("_x000D_", "\n", regex=False)
        .str.replace("\r", "\n", regex=True)
        .str.replace("\n+", "\n", regex=True)
        .str.strip()
    )

    return df


df = load_data()


# =========================
# TOP CONTROL BAR
# =========================
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    search = st.text_input("🔎 Търси виц", placeholder="Напр. доктор, тъщата...")

with col2:
    categories = ["Всички"] + sorted(df["категория"].dropna().unique())
    selected_category = st.selectbox("📂 Категория", categories)

with col3:
    sort_by = st.selectbox("↕️ Сортиране по", ["гледания", "категория"])

ascending = st.toggle("⬆️ Възходящ ред", value=False)


# =========================
# FILTER PIPELINE
# =========================
filtered_df = df

if selected_category != "Всички":
    filtered_df = filtered_df.loc[
        filtered_df["категория"] == selected_category
    ]

if search:
    filtered_df = filtered_df.loc[
        filtered_df["виц_текст"].str.contains(search, case=False, na=False)
    ]

filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)


# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["📜 Вицове", "📊 Статистика"])


# =========================
# TAB 1 - JOKES
# =========================
with tab1:
    st.caption(f"Показани: {len(filtered_df)} от {len(df)} вицове")

    for row in filtered_df.itertuples(index=False):
        st.markdown("---")

        st.markdown(
            f"**📂 Категория:** {row.категория}  |  👁 Гледания: {row.гледания}"
        )

        st.markdown(
    f"""
    <div style="
        font-size:16px;
        line-height:1.6;
        white-space:pre-line;
    ">
    {row.виц_текст}
    </div>
    """,
    unsafe_allow_html=True
)

        


# =========================
# TAB 2 - STATS
# =========================
with tab2:
    st.subheader("📊 Статистика")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Общо вицове", len(df))

    with col2:
        st.metric("Показани вицове", len(filtered_df))

    st.bar_chart(df["категория"].value_counts())