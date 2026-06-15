import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_loader import load_data

st.set_page_config(page_title="서울 vs 인천", page_icon="1️⃣", layout="wide")

# ── 데이터 로드 ──────────────────────────────────────────────────────────────
df = load_data()
cities = ["서울특별시", "인천광역시"]
data = df[df["지역"].isin(cities)].set_index("지역")

COLORS = {"서울특별시": "#E63946", "인천광역시": "#457B9D"}

# ── 헤더 ────────────────────────────────────────────────────────────────────
st.title("1️⃣ 서울특별시 vs 인천광역시")
st.caption("📍 북위 약 37° | 위도 조건이 유사한 두 도시 비교 (2023년 기준)")
st.markdown("---")

# ── 핵심 지표 카드 ──────────────────────────────────────────────────────────
cols = st.columns(4)
metrics = [
    ("🌡️ 평균기온(°C)", "평균기온"),
    ("💨 평균풍속(m/s)", "평균풍속"),
    ("🏙️ 건물밀집도(개/km²)", "건물밀집도"),
    ("🌿 녹지율(%)", "녹지율"),
]
for col, (label, key) in zip(cols, metrics):
    with col:
        s_val = data.loc["서울특별시", key]
        i_val = data.loc["인천광역시", key]
        delta = round(s_val - i_val, 2)
        st.metric(f"서울 {label}", f"{s_val:.2f}", delta=f"서울-인천: {delta:+.2f}")

st.markdown("---")

# ── 그래프 섹션 ─────────────────────────────────────────────────────────────
st.subheader("📊 세부 비교 차트")

tab1, tab2, tab3 = st.tabs(["🌡️ 온도 & 풍속", "🏙️ 건물밀집도", "🌿 녹지율"])

# --- 탭1: 온도 & 풍속 ---
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Bar(
                name=city,
                x=[city],
                y=[data.loc[city, "평균기온"]],
                marker_color=COLORS[city],
                text=[f"{data.loc[city, '평균기온']:.1f}°C"],
                textposition="outside",
            ))
        fig.update_layout(
            title="평균기온 비교",
            yaxis_title="기온 (°C)",
            yaxis=dict(range=[12, 16]),
            showlegend=False,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Bar(
                name=city,
                x=[city],
                y=[data.loc[city, "평균풍속"]],
                marker_color=COLORS[city],
                text=[f"{data.loc[city, '평균풍속']:.1f} m/s"],
                textposition="outside",
            ))
        fig.update_layout(
            title="평균풍속 비교",
            yaxis_title="풍속 (m/s)",
            yaxis=dict(range=[0, 4]),
            showlegend=False,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

# --- 탭2: 건물밀집도 ---
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Bar(
                name=city,
                x=[city],
                y=[data.loc[city, "건물밀집도"]],
                marker_color=COLORS[city],
                text=[f"{data.loc[city, '건물밀집도']:.1f}개/km²"],
                textposition="outside",
            ))
        fig.update_layout(
            title="건물밀집도 비교 (개/km²)",
            yaxis_title="건물밀집도",
            showlegend=False,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # 산점도: 건물밀집도 vs 기온
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Scatter(
                x=[data.loc[city, "건물밀집도"]],
                y=[data.loc[city, "평균기온"]],
                mode="markers+text",
                name=city,
                text=[city],
                textposition="top center",
                marker=dict(size=20, color=COLORS[city]),
            ))
        fig.update_layout(
            title="건물밀집도 vs 평균기온",
            xaxis_title="건물밀집도 (개/km²)",
            yaxis_title="평균기온 (°C)",
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    # 건물밀집도 vs 풍속
    fig = go.Figure()
    for city in cities:
        fig.add_trace(go.Scatter(
            x=[data.loc[city, "건물밀집도"]],
            y=[data.loc[city, "평균풍속"]],
            mode="markers+text",
            name=city,
            text=[city],
            textposition="top center",
            marker=dict(size=20, color=COLORS[city]),
        ))
    fig.update_layout(
        title="건물밀집도 vs 평균풍속",
        xaxis_title="건물밀집도 (개/km²)",
        yaxis_title="평균풍속 (m/s)",
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 탭3: 녹지율 ---
with tab3:
    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Bar(
                name=city,
                x=[city],
                y=[data.loc[city, "녹지율"]],
                marker_color=COLORS[city],
                text=[f"{data.loc[city, '녹지율']:.2f}%"],
                textposition="outside",
            ))
        fig.update_layout(
            title="녹지율 비교 (%)",
            yaxis_title="녹지율 (%)",
            showlegend=False,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Scatter(
                x=[data.loc[city, "녹지율"]],
                y=[data.loc[city, "평균기온"]],
                mode="markers+text",
                name=city,
                text=[city],
                textposition="top center",
                marker=dict(size=20, color=COLORS[city]),
            ))
        fig.update_layout(
            title="녹지율 vs 평균기온",
            xaxis_title="녹지율 (%)",
            yaxis_title="평균기온 (°C)",
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

# ── 분석 해석 ────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🔍 분석 해석")

seoul = data.loc["서울특별시"]
incheon = data.loc["인천광역시"]

diff_temp = seoul["평균기온"] - incheon["평균기온"]
diff_wind = seoul["평균풍속"] - incheon["평균풍속"]
diff_density = seoul["건물밀집도"] - incheon["건물밀집도"]
diff_green = seoul["녹지율"] - incheon["녹지율"]

st.markdown(f"""
| 항목 | 서울 | 인천 | 차이 (서울 - 인천) | 가설 부합 여부 |
|------|------|------|-------------------|----------------|
| 평균기온 | {seoul['평균기온']:.1f}°C | {incheon['평균기온']:.1f}°C | **{diff_temp:+.1f}°C** | {'✅' if diff_density > 0 and diff_temp > 0 else '❌'} 건물밀집↑ → 기온↑ |
| 평균풍속 | {seoul['평균풍속']:.1f} m/s | {incheon['평균풍속']:.1f} m/s | **{diff_wind:+.1f} m/s** | {'✅' if diff_density > 0 and diff_wind < 0 else '❌'} 건물밀집↑ → 풍속↓ |
| 건물밀집도 | {seoul['건물밀집도']:.1f} 개/km² | {incheon['건물밀집도']:.1f} 개/km² | **{diff_density:+.1f}** | — |
| 녹지율 | {seoul['녹지율']:.2f}% | {incheon['녹지율']:.2f}% | **{diff_green:+.2f}%** | {'✅' if diff_green < 0 and diff_temp > 0 else '❌'} 녹지↓ → 기온↑ |
""")

st.info("💡 두 도시는 북위 37° 인근으로 위도 차이가 매우 작아, 관측된 온도 차이는 도시 구조적 특성(건물밀집도·녹지율)에 기인할 가능성이 높습니다.")
