import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="전체 종합 분석", page_icon="📊", layout="wide")

COL_REGION = "행정구역별"

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    for enc in ["utf-8", "cp949", "euc-kr", "utf-8-sig"]:
        try:
            df = pd.read_csv(path, encoding=enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("CSV 파일의 인코딩을 읽을 수 없습니다.")

    df = df.dropna(axis=1, how="all")
    df.columns = [c.strip() for c in df.columns]

    col_build = next((c for c in df.columns if "건축물" in c), None)
    col_park  = next((c for c in df.columns if "공원" in c), None)
    col_urban = next((c for c in df.columns if "도시지역면적" in c), None)

    df["건물밀집도"] = df[col_build] / df[col_urban] * 1_000_000
    df["녹지율(%)"]  = df[col_park] * 1000 / df[col_urban] * 100
    return df

def find_col(df, keyword):
    for c in df.columns:
        if keyword in c:
            return c
    return None

def scatter_with_trend(df, x, y, color_scale, x_label, y_label, size_col=None):
    """추세선 + 회귀식 + R²가 포함된 산점도 생성"""
    fig = px.scatter(df, x=x, y=y, text=COL_REGION,
                     size=size_col, color=y,
                     color_continuous_scale=color_scale,
                     labels={x: x_label, y: y_label})
    coef = np.polyfit(df[x], df[y], 1)
    x_line = np.linspace(df[x].min(), df[x].max(), 100)
    y_line = coef[0]*x_line + coef[1]
    fig.add_trace(go.Scatter(x=x_line, y=y_line, mode="lines",
                  name="추세선", line=dict(color="gray", dash="dash", width=2)))
    corr = df[x].corr(df[y])
    r2 = corr ** 2
    fig.update_traces(textposition="top center",
                      marker=dict(line=dict(width=1, color="white")),
                      selector=dict(mode="markers+text"))
    fig.update_layout(height=500, margin=dict(t=40))
    return fig, coef, corr, r2

try:
    df = load_data("통합본.csv")
except FileNotFoundError:
    st.error("CSV 파일(통합본.csv)을 찾을 수 없습니다.")
    st.stop()

c_temp = find_col(df, "평균기온")
c_wind = find_col(df, "풍속")

st.title("📊 전체 도시 종합 분석")
st.markdown("##### 8개 도시 데이터로 열섬효과 가설을 종합 검증합니다")
st.markdown("---")

# ── 상단 요약 지표 ──
corr_temp = df["건물밀집도"].corr(df[c_temp])
corr_wind = df["건물밀집도"].corr(df[c_wind])
corr_green = df["녹지율(%)"].corr(df[c_temp])
s1, s2, s3, s4 = st.columns(4)
s1.metric("분석 도시 수", f"{len(df)}개")
s2.metric("밀집도↔기온 상관", f"{corr_temp:+.2f}")
s3.metric("밀집도↔풍속 상관", f"{corr_wind:+.2f}")
s4.metric("녹지율↔기온 상관", f"{corr_green:+.2f}")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📋 데이터 & 순위", "🌡️ 기온 분석", "🌬️ 풍속 분석", "🔥 상관관계", "📝 종합 결론"]
)

# ── TAB 1: 데이터 & 순위 ──
with tab1:
    st.markdown("#### 도시별 핵심 지표 (건물밀집도 순)")
    show_cols = [COL_REGION, c_temp, c_wind, "건물밀집도", "녹지율(%)"]
    table = df[show_cols].copy().round(2)
    table = table.sort_values("건물밀집도", ascending=False).reset_index(drop=True)
    table.index = table.index + 1
    st.dataframe(table, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 지표별 도시 순위 막대그래프")
    metric_choice = st.selectbox("순위를 볼 지표 선택",
                                 [c_temp, c_wind, "건물밀집도", "녹지율(%)"])
    ranked = df.sort_values(metric_choice, ascending=True)
    fig_bar = go.Figure(go.Bar(
        x=ranked[metric_choice], y=ranked[COL_REGION], orientation="h",
        marker=dict(color=ranked[metric_choice], colorscale="Viridis"),
        text=ranked[metric_choice].round(1), textposition="outside",
    ))
    fig_bar.update_layout(height=420, title=f"{metric_choice} 도시별 순위",
                          xaxis_title=metric_choice)
    st.plotly_chart(fig_bar, use_container_width=True)

# ── TAB 2: 기온 분석 ──
with tab2:
    st.markdown("#### 🌡️ 건물밀집도와 평균기온")
    st.caption("가설: 건물밀집도가 높을수록 기온이 높다 (열섬효과)")
    fig1, coef1, corr1, r2_1 = scatter_with_trend(
        df, "건물밀집도", c_temp, "RdYlBu_r",
        "건물밀집도 (면적당 건물 수)", "평균기온(℃)", size_col="녹지율(%)")
    st.plotly_chart(fig1, use_container_width=True)
    cA, cB, cC = st.columns(3)
    cA.metric("상관계수", f"{corr1:+.3f}")
    cB.metric("결정계수 R²", f"{r2_1:.3f}")
    cC.metric("회귀 기울기", f"{coef1[0]:+.4f}")
    st.info(f"📐 회귀식: **기온 = {coef1[0]:.4f} × 밀집도 + {coef1[1]:.2f}**  \n"
            f"건물밀집도가 기온 변화의 약 **{r2_1*100:.1f}%**를 설명합니다. "
            f"{'(양의 관계: 가설 부합 가능성)' if corr1>0 else '(음의 관계: 가설과 다름)'}")

    st.markdown("---")
    st.markdown("#### 🌳 녹지율과 평균기온")
    st.caption("가설: 녹지율이 높을수록 기온이 낮다")
    fig2, coef2, corr2, r2_2 = scatter_with_trend(
        df, "녹지율(%)", c_temp, "RdYlGn_r", "녹지율(%)", "평균기온(℃)")
    st.plotly_chart(fig2, use_container_width=True)
    cD, cE, cF = st.columns(3)
    cD.metric("상관계수", f"{corr2:+.3f}")
    cE.metric("결정계수 R²", f"{r2_2:.3f}")
    cF.metric("회귀 기울기", f"{coef2[0]:+.4f}")
    st.info(f"📐 회귀식: **기온 = {coef2[0]:.4f} × 녹지율 + {coef2[1]:.2f}**  \n"
            f"{'(음의 관계: 가설 부합 가능성)' if corr2<0 else '(양의 관계: 가설과 다름)'}")

# ── TAB 3: 풍속 분석 ──
with tab3:
    st.markdown("#### 🌬️ 건물밀집도와 풍속")
    st.caption("가설: 건물밀집도가 높을수록 풍속이 느리다 (건물이 바람을 막음)")
    fig3, coef3, corr3, r2_3 = scatter_with_trend(
        df, "건물밀집도", c_wind, "Blues", "건물밀집도", "평균 풍속(m/s)")
    st.plotly_chart(fig3, use_container_width=True)
    cG, cH, cI = st.columns(3)
    cG.metric("상관계수", f"{corr3:+.3f}")
    cH.metric("결정계수 R²", f"{r2_3:.3f}")
    cI.metric("회귀 기울기", f"{coef3[0]:+.6f}")
    st.info(f"📐 회귀식: **풍속 = {coef3[0]:.6f} × 밀집도 + {coef3[1]:.2f}**  \n"
            f"{'(음의 관계: 가설 부합 가능성)' if corr3<0 else '(양의 관계: 가설과 다름)'}")

    st.markdown("---")
    st.markdown("#### 🌳 녹지율과 풍속")
    fig4, coef4, corr4, r2_4 = scatter_with_trend(
        df, "녹지율(%)", c_wind, "GnBu", "녹지율(%)", "평균 풍속(m/s)")
    st.plotly_chart(fig4, use_container_width=True)
    st.info(f"녹지율과 풍속의 상관계수: **{corr4:+.3f}** (R²={r2_4:.3f})")

# ── TAB 4: 상관관계 히트맵 + 레이더 ──
with tab4:
    st.markdown("#### 🔥 전체 변수 상관관계 히트맵")
    st.caption("값이 +1에 가까우면 강한 양의 관계, -1에 가까우면 강한 음의 관계입니다.")
    corr_cols = [c_temp, c_wind, "건물밀집도", "녹지율(%)"]
    corr_matrix = df[corr_cols].corr()
    fig_heat = px.imshow(corr_matrix, text_auto=".2f",
                         color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto")
    fig_heat.update_layout(height=500, title="변수 간 상관계수 행렬")
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🕸️ 전체 도시 종합 레이더")
    st.caption("모든 도시의 4개 지표를 0~100으로 정규화해 겹쳐 그렸습니다.")
    def normalize_col(col):
        mn, mx = df[col].min(), df[col].max()
        return (df[col]-mn)/(mx-mn)*100 if mx != mn else df[col]*0+50
    norm_df = pd.DataFrame({
        "평균기온": normalize_col(c_temp),
        "풍속": normalize_col(c_wind),
        "건물밀집도": normalize_col("건물밀집도"),
        "녹지율": normalize_col("녹지율(%)"),
    })
    cats = ["평균기온", "풍속", "건물밀집도", "녹지율"]
    fig_radar = go.Figure()
    for i, region in enumerate(df[COL_REGION]):
        vals = norm_df.iloc[i].tolist()
        fig_radar.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=cats+[cats[0]], fill="toself", name=region))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])),
                            height=550, title="8개 도시 종합 레이더 (0~100)")
    st.plotly_chart(fig_radar, use_container_width=True)

# ── TAB 5: 종합 결론 ──
with tab5:
    st.markdown("#### 📝 종합 결론")
    st.success(f"""
**상관계수 요약 (8개 도시 기준)**

| 관계 | 상관계수 | 가설 부합 여부 |
|------|---------|--------------|
| 건물밀집도 ↔ 평균기온 | **{corr_temp:+.3f}** | {'✅ 부합' if corr_temp>0 else '❌ 불일치'} |
| 건물밀집도 ↔ 풍속 | **{corr_wind:+.3f}** | {'✅ 부합' if corr_wind<0 else '❌ 불일치'} |
| 녹지율 ↔ 평균기온 | **{corr_green:+.3f}** | {'✅ 부합' if corr_green<0 else '❌ 불일치'} |
""")

    # 종합 점수 계산
    hits = sum([corr_temp > 0, corr_wind < 0, corr_green < 0])
    st.markdown("#### 🎯 가설 검증 종합 점수")
    st.progress(hits / 3)
    if hits == 3:
        st.success(f"**3 / 3 가설 부합** — 8개 도시 데이터에서 열섬효과 경향이 종합적으로 관찰됩니다!")
    elif hits == 2:
        st.warning(f"**2 / 3 가설 부합** — 부분적으로 열섬효과가 관찰됩니다.")
    else:
        st.error(f"**{hits} / 3 가설 부합** — 다른 요인(해안·위도 등)의 영향이 더 클 수 있습니다.")

    st.markdown("""
---
> 💭 **프로젝트를 더 깊게 만드는 질문**
> - 8개 도시는 표본이 적어요. 상관계수가 우연일 가능성은 없을까요?
> - **해안 도시**(부산·인천·울산)는 바다의 영향으로 기온이 완만하고 풍속이 빠를 수 있어요. 내륙 도시와 나눠서 보면 어떨까요?
> - **위도**(남쪽일수록 따뜻함)라는 숨은 변수가 기온에 영향을 줄 수 있어요. 이를 통제하지 않으면 건물밀집도의 효과가 과장/축소될 수 있어요.
> - 연 평균이 아니라 **여름철(7~8월) 데이터**로 보면 열섬효과가 더 뚜렷하게 나타날 가능성이 있어요.

> ⚠️ **분석의 한계**: 이 분석은 '상관관계'를 보여줄 뿐, '인과관계'를 증명하지는 않습니다.
> "건물이 많아서 더운 것"인지, "원래 더운 곳에 사람이 많이 살아서 건물이 많은 것"인지는 추가 연구가 필요해요.
""")
