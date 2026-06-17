import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="대구 VS 울산", page_icon="🏙️", layout="wide")

# ══════════ 비교할 두 지역 ══════════
REGION_A = "대구광역시"
REGION_B = "울산광역시"
# ════════════════════════════════════

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

def rank_of(df, col, region, ascending=False):
    ranked = df.sort_values(col, ascending=ascending).reset_index(drop=True)
    pos = ranked[ranked[COL_REGION] == region].index[0] + 1
    return pos, len(df)

try:
    df = load_data("통합본.csv")
except FileNotFoundError:
    st.error("CSV 파일(통합본.csv)을 찾을 수 없습니다.")
    st.stop()

c_temp  = find_col(df, "평균기온")
c_wind  = find_col(df, "풍속")
c_dense = "건물밀집도"
c_green = "녹지율(%)"

two = df[df[COL_REGION].isin([REGION_A, REGION_B])].copy()
if len(two) < 2:
    st.warning("두 지역의 데이터를 모두 찾지 못했습니다.")
    st.stop()

a = two[two[COL_REGION] == REGION_A].iloc[0]
b = two[two[COL_REGION] == REGION_B].iloc[0]

st.title(f"🏙️ {REGION_A} VS {REGION_B}")
st.markdown("##### 건물 밀집도와 녹지율에 따른 기온·풍속 심층 비교")
st.markdown("---")

st.subheader("📌 핵심 지표 한눈에 보기")
m1, m2, m3, m4 = st.columns(4)
m1.metric(f"{REGION_A} 평균기온", f"{a[c_temp]:.1f}℃", f"{a[c_temp]-b[c_temp]:+.1f}℃ vs {REGION_B}")
m2.metric(f"{REGION_A} 풍속", f"{a[c_wind]:.1f}m/s", f"{a[c_wind]-b[c_wind]:+.1f}m/s vs {REGION_B}")
m3.metric(f"{REGION_A} 건물밀집도", f"{a[c_dense]:.0f}", f"{a[c_dense]-b[c_dense]:+.0f}")
m4.metric(f"{REGION_A} 녹지율", f"{a[c_green]:.2f}%", f"{a[c_green]-b[c_green]:+.2f}%p")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📊 항목별 비교", "🕸️ 종합 레이더", "🏆 전국 순위", "🔍 가설 검증"])

with tab1:
    st.markdown("#### 네 가지 핵심 지표 비교")
    metrics = [
        (c_temp, "평균기온(℃)", "#ff6b6b"),
        (c_wind, "평균 풍속(m/s)", "#4dabf7"),
        (c_dense, "건물밀집도", "#ffa94d"),
        (c_green, "녹지율(%)", "#51cf66"),
    ]
    fig = make_subplots(rows=2, cols=2, subplot_titles=[m[1] for m in metrics],
                        vertical_spacing=0.15, horizontal_spacing=0.12)
    positions = [(1,1),(1,2),(2,1),(2,2)]
    for (col, label, color), (r, c) in zip(metrics, positions):
        fig.add_trace(go.Bar(
            x=[REGION_A, REGION_B], y=[a[col], b[col]],
            marker=dict(color=[color, color], opacity=[1.0, 0.55]),
            text=[f"{a[col]:.2f}", f"{b[col]:.2f}"],
            textposition="outside", textfont=dict(size=14), showlegend=False,
        ), row=r, col=c)
    fig.update_layout(height=620, title_text="항목별 막대 비교", title_font_size=18, margin=dict(t=80))
    st.plotly_chart(fig, use_container_width=True)

    diff_temp = a[c_temp] - b[c_temp]
    diff_wind = a[c_wind] - b[c_wind]
    cc1, cc2 = st.columns(2)
    cc1.info(f"🌡️ 두 도시 기온 차이: **{abs(diff_temp):.1f}℃** "
             f"({REGION_A+'이 더 따뜻' if diff_temp>0 else REGION_B+'이 더 따뜻'})")
    cc2.info(f"🌬️ 두 도시 풍속 차이: **{abs(diff_wind):.1f}m/s** "
             f"({REGION_A+'이 더 빠름' if diff_wind>0 else REGION_B+'이 더 빠름'})")

with tab2:
    st.markdown("#### 종합 레이더 차트 (전국 대비 상대 위치)")
    st.caption("각 지표를 전체 8개 도시 중 0~100점으로 환산해 비교합니다.")

    def normalize(col, value):
        mn, mx = df[col].min(), df[col].max()
        return 50 if mx == mn else (value - mn) / (mx - mn) * 100

    categories = ["평균기온", "풍속", "건물밀집도", "녹지율"]
    cols = [c_temp, c_wind, c_dense, c_green]
    a_vals = [normalize(col, a[col]) for col in cols]
    b_vals = [normalize(col, b[col]) for col in cols]

    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(r=a_vals+[a_vals[0]], theta=categories+[categories[0]],
        fill="toself", name=REGION_A, line=dict(color="#ff6b6b", width=2),
        fillcolor="rgba(255,107,107,0.25)"))
    fig_r.add_trace(go.Scatterpolar(r=b_vals+[b_vals[0]], theta=categories+[categories[0]],
        fill="toself", name=REGION_B, line=dict(color="#4dabf7", width=2),
        fillcolor="rgba(77,171,247,0.25)"))
    fig_r.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])),
        height=500, title="전국 대비 상대적 위치 (0~100점)",
        legend=dict(orientation="h", yanchor="bottom", y=1.05))
    st.plotly_chart(fig_r, use_container_width=True)
    st.info("💡 레이더가 바깥쪽으로 갈수록 그 항목 값이 전국에서 높다는 뜻이에요.")

with tab3:
    st.markdown("#### 전국 8개 도시 중 순위")
    rank_data = [("🌡️ 평균기온", c_temp), ("🌬️ 풍속", c_wind),
                 ("🏢 건물밀집도", c_dense), ("🌳 녹지율", c_green)]
    colA, colB = st.columns(2)
    for region, col_box in [(REGION_A, colA), (REGION_B, colB)]:
        with col_box:
            st.markdown(f"##### 📍 {region}")
            for emoji_label, col in rank_data:
                pos, total = rank_of(df, col, region)
                val = df[df[COL_REGION]==region][col].iloc[0]
                medal = "🥇" if pos==1 else "🥈" if pos==2 else "🥉" if pos==3 else "  "
                st.markdown(f"{medal} **{emoji_label}**: {pos}위 / {total}개 도시 (`{val:.1f}`)")

    st.markdown("---")
    st.markdown("#### 🏢 전국 건물밀집도 순위 (두 도시 강조)")
    ranked = df.sort_values(c_dense, ascending=True)
    colors = ["#ff6b6b" if r==REGION_A else "#4dabf7" if r==REGION_B else "#495057"
              for r in ranked[COL_REGION]]
    fig_rank = go.Figure(go.Bar(x=ranked[c_dense], y=ranked[COL_REGION], orientation="h",
        marker_color=colors, text=ranked[c_dense].round(0), textposition="outside"))
    fig_rank.update_layout(height=400, title="건물밀집도 전국 비교", xaxis_title="건물밀집도")
    st.plotly_chart(fig_rank, use_container_width=True)

with tab4:
    st.markdown("#### 가설 검증 결과")
    denser = REGION_A if a[c_dense] > b[c_dense] else REGION_B
    denser_row = a if a[c_dense] > b[c_dense] else b
    other_row  = b if a[c_dense] > b[c_dense] else a
    other_name = REGION_B if denser == REGION_A else REGION_A

    temp_ok = denser_row[c_temp] > other_row[c_temp]
    wind_ok = denser_row[c_wind] < other_row[c_wind]
    green_ok = denser_row[c_green] < other_row[c_green]
    temp_check = "높습니다 ✅ (가설 부합)" if temp_ok else "낮습니다 ❌ (가설과 다름)"
    wind_check = "느립니다 ✅ (가설 부합)" if wind_ok else "빠릅니다 ❌ (가설과 다름)"
    green_check = "낮습니다 ✅ (가설 부합)" if green_ok else "높습니다 ❌ (가설과 다름)"

    st.info(f"""
**건물 밀집도가 더 높은 도시는 `{denser}` 입니다.**

- 🌡️ **기온**: `{denser}`의 기온이 `{other_name}`보다 **{temp_check}**
- 🌬️ **풍속**: `{denser}`의 풍속이 `{other_name}`보다 **{wind_check}**
- 🌳 **녹지율**: `{denser}`의 녹지율이 `{other_name}`보다 **{green_check}**
""")
    score = sum([temp_ok, wind_ok, green_ok])
    if score == 3:
        st.success("🎯 3개 가설 모두 부합! 열섬효과가 뚜렷합니다.")
    elif score == 2:
        st.warning("⚖️ 3개 중 2개 가설 부합. 부분적으로 관찰됩니다.")
    else:
        st.error(f"🤔 3개 중 {score}개만 부합. 다른 요인의 영향이 클 수 있어요.")
    st.markdown("> 💭 **04 전체 종합 페이지**에서 8개 도시 전체 경향을 확인해보세요!")

with st.expander("📋 원본 데이터 보기"):
    st.dataframe(two, use_container_width=True)
