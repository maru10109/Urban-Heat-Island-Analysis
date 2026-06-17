import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="전체 종합 분석", page_icon="📊", layout="wide")

COL_REGION = "행정구역별"
COL_URBAN  = "도시지역면적"

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(axis=1, how="all")
    df.columns = [c.strip() for c in df.columns]
    return df

def find_col(df, keyword):
    for c in df.columns:
        if keyword in c:
            return c
    return None

try:
    df = load_data("통합본.csv")
except FileNotFoundError:
    st.error("CSV 파일(통합본.csv)을 찾을 수 없습니다.")
    st.stop()

# 컬럼 매칭
c_temp  = find_col(df, "평균기온")
c_wind  = find_col(df, "풍속")
c_park  = find_col(df, "공원")
c_build = find_col(df, "건축물")

# 파생 지표
df["건물밀집도"] = df[c_build] / df[COL_URBAN] * 1_000_000
df["녹지율(%)"]  = df[c_park] * 1000 / df[COL_URBAN] * 100

st.title("📊 전체 도시 종합 분석")
st.markdown("##### 8개 도시 데이터로 열섬효과 가설을 검증합니다")
st.markdown("---")

# ── 1. 전체 데이터 테이블 ──
st.subheader("📋 도시별 핵심 지표")
show_cols = [COL_REGION, c_temp, c_wind, "건물밀집도", "녹지율(%)"]
table = df[show_cols].copy().round(2)
table = table.sort_values("건물밀집도", ascending=False).reset_index(drop=True)
st.dataframe(table, use_container_width=True)

st.markdown("---")

# ── 2. 건물밀집도 vs 평균기온 산점도 ──
st.subheader("🌡️ 건물밀집도와 평균기온의 관계")
st.caption("가설: 건물밀집도가 높을수록 기온이 높다 (열섬효과)")

fig1 = px.scatter(
    df, x="건물밀집도", y=c_temp, text=COL_REGION,
    size="녹지율(%)", color=c_temp,
    color_continuous_scale="RdYlBu_r",
    labels={"건물밀집도": "건물밀집도 (면적당 건물 수)", c_temp: "평균기온(℃)"},
)
# 추세선
coef = np.polyfit(df["건물밀집도"], df[c_temp], 1)
x_line = np.linspace(df["건물밀집도"].min(), df["건물밀집도"].max(), 100)
fig1.add_trace(go.Scatter(
    x=x_line, y=coef[0]*x_line + coef[1],
    mode="lines", name="추세선",
    line=dict(color="gray", dash="dash"),
))
fig1.update_traces(textposition="top center", selector=dict(mode="markers+text"))
fig1.update_layout(height=480)
st.plotly_chart(fig1, use_container_width=True)

corr_temp = df["건물밀집도"].corr(df[c_temp])
st.info(f"📈 건물밀집도와 평균기온의 **상관계수 = {corr_temp:.3f}** "
        f"{'(양의 상관관계: 가설 부합 가능성)' if corr_temp > 0 else '(음의 상관관계: 가설과 다름)'}")

st.markdown("---")

# ── 3. 건물밀집도 vs 풍속 ──
st.subheader("🌬️ 건물밀집도와 풍속의 관계")
st.caption("가설: 건물밀집도가 높을수록 풍속이 느리다")

fig2 = px.scatter(
    df, x="건물밀집도", y=c_wind, text=COL_REGION,
    color=c_wind, color_continuous_scale="Blues",
    labels={"건물밀집도": "건물밀집도", c_wind: "평균 풍속(m/s)"},
)
coef2 = np.polyfit(df["건물밀집도"], df[c_wind], 1)
fig2.add_trace(go.Scatter(
    x=x_line, y=coef2[0]*x_line + coef2[1],
    mode="lines", name="추세선",
    line=dict(color="gray", dash="dash"),
))
fig2.update_traces(textposition="top center", selector=dict(mode="markers+text"))
fig2.update_layout(height=480)
st.plotly_chart(fig2, use_container_width=True)

corr_wind = df["건물밀집도"].corr(df[c_wind])
st.info(f"📉 건물밀집도와 풍속의 **상관계수 = {corr_wind:.3f}** "
        f"{'(음의 상관관계: 가설 부합 가능성)' if corr_wind < 0 else '(양의 상관관계: 가설과 다름)'}")

st.markdown("---")

# ── 4. 녹지율 vs 평균기온 ──
st.subheader("🌳 녹지율과 평균기온의 관계")
st.caption("가설: 녹지율이 높을수록 기온이 낮다")

fig3 = px.scatter(
    df, x="녹지율(%)", y=c_temp, text=COL_REGION,
    color=c_temp, color_continuous_scale="RdYlGn_r",
    labels={"녹지율(%)": "녹지율(%)", c_temp: "평균기온(℃)"},
)
coef3 = np.polyfit(df["녹지율(%)"], df[c_temp], 1)
x_line3 = np.linspace(df["녹지율(%)"].min(), df["녹지율(%)"].max(), 100)
fig3.add_trace(go.Scatter(
    x=x_line3, y=coef3[0]*x_line3 + coef3[1],
    mode="lines", name="추세선",
    line=dict(color="gray", dash="dash"),
))
fig3.update_traces(textposition="top center", selector=dict(mode="markers+text"))
fig3.update_layout(height=480)
st.plotly_chart(fig3, use_container_width=True)

corr_green = df["녹지율(%)"].corr(df[c_temp])
st.info(f"🌿 녹지율과 평균기온의 **상관계수 = {corr_green:.3f}** "
        f"{'(음의 상관관계: 가설 부합 가능성)' if corr_green < 0 else '(양의 상관관계: 가설과 다름)'}")

st.markdown("---")

# ── 5. 상관계수 히트맵 ──
st.subheader("🔥 전체 변수 상관관계 히트맵")
corr_cols = [c_temp, c_wind, "건물밀집도", "녹지율(%)"]
corr_matrix = df[corr_cols].corr()

fig4 = px.imshow(
    corr_matrix, text_auto=".2f",
    color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
    aspect="auto",
)
fig4.update_layout(height=450, title="변수 간 상관계수")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── 6. 종합 결론 ──
st.subheader("📝 종합 결론")
st.success(f"""
**상관계수 요약**
- 건물밀집도 ↔ 평균기온: **{corr_temp:.3f}**
- 건물밀집도 ↔ 풍속: **{corr_wind:.3f}**
- 녹지율 ↔ 평균기온: **{corr_green:.3f}**

> 💭 **생각해볼 질문**
> - 8개 도시만으로 결론 내리기에 충분한 표본일까요?
> - 해안 도시(부산, 인천, 울산)와 내륙 도시는 다르게 봐야 하지 않을까요?
> - 위도(남쪽일수록 따뜻함) 같은 다른 변수의 영향은 없을까요?
""")
