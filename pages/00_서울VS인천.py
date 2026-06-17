import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울 VS 인천", page_icon="🏙️", layout="wide")

REGION_A = "서울특별시"
REGION_B = "인천광역시"

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(axis=1, how="all")
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = load_data("통합본.csv")
except FileNotFoundError:
    st.error("CSV 파일(통합본.csv)을 찾을 수 없습니다.")
    st.stop()

st.title(f"🏙️ {REGION_A} VS {REGION_B}")
st.markdown("---")

# 두 지역 데이터 추출
two = df[df["행정구역별"].isin([REGION_A, REGION_B])].copy()

st.subheader("📋 데이터")
st.dataframe(two, use_container_width=True)

# 비교할 수치형 항목 자동 추출
numeric_cols = [c for c in two.columns
                if c not in ["행정구역별", "일시"]
                and pd.api.types.is_numeric_dtype(two[c])]

st.subheader("📊 항목별 비교")
selected = st.selectbox("비교할 항목 선택", numeric_cols)

fig = go.Figure(go.Bar(
    x=two["행정구역별"],
    y=two[selected],
    marker_color=["#5bc0de", "#e88"],
    text=two[selected].round(2),
    textposition="outside",
))
fig.update_layout(
    title=f"{selected} 비교",
    yaxis_title=selected,
    height=420,
)
st.plotly_chart(fig, use_container_width=True)

# 평균기온과 다른 요소 관계
st.subheader("🌡️ 평균기온 vs 선택 요소")
temp_col = [c for c in two.columns if "평균기온" in c]
if temp_col and selected != temp_col[0]:
    st.info(
        f"💡 두 도시의 **{temp_col[0]}** 과 **{selected}** 값을 함께 살펴보고, "
        "공원면적·건축물·도시면적이 기온과 어떤 관련이 있을지 생각해보세요!"
    )
