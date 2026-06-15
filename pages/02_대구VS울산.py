import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_loader import load_data

st.set_page_config(page_title="대구 vs 울산", page_icon="3️⃣", layout="wide")

df = load_data()
cities = ["대구광역시", "울산광역시"]
data = df[df["지역"].isin(cities)].set_index("지역")

COLORS = {"대구광역시": "#C0392B", "울산광역시": "#1A5276"}

st.title("3️⃣ 대구광역시 vs 울산광역시")
st.caption("📍 북위 약 35.5° | 위도 조건이 유사한 두 도시 비교 (2023년 기준)")
st.markdown("---")

cols = st.columns(4)
metrics = [
    ("🌡️ 평균기온(°C)", "평균기온"),
    ("💨 평균풍속(m/s)", "평균풍속"),
    ("🏙️ 건물밀집도(개/km²)", "건물밀집도"),
    ("🌿 녹지율(%)", "녹지율"),
]
for col, (label, key) in zip(cols, metrics):
    with col:
        d_val = data.loc["대구광역시", key]
        u_val = data.loc["울산광역시", key]
        delta = round(d_val - u_val, 2)
        st.metric(f"대구 {label}", f"{d_val:.2f}", delta=f"대구-울산: {delta:+.2f}")

st.markdown("---")
st.subheader("📊 세부 비교 차트")

tab1, tab2, tab3 = st.tabs(["🌡️ 온도 & 풍속", "🏙️ 건물밀집도", "🌿 녹지율"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Bar(
                name=city, x=[city], y=[data.loc[city, "평균기온"]],
                marker_color=COLORS[city],
                text=[f"{data.loc[city, '평균기온']:.1f}°C"], textposition="outside",
            ))
        fig.update_layout(title="평균기온 비교", yaxis_title="기온 (°C)",
                          yaxis=dict(range=[13, 17]), showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Bar(
                name=city, x=[city], y=[data.loc[city, "평균풍속"]],
                marker_color=COLORS[city],
                text=[f"{data.loc[city, '평균풍속']:.1f} m/s"], textposition="outside",
            ))
        fig.update_layout(title="평균풍속 비교", yaxis_title="풍속 (m/s)",
                          yaxis=dict(range=[0, 4]), showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Bar(
                name=city, x=[city], y=[data.loc[city, "건물밀집도"]],
                marker_color=COLORS[city],
                text=[f"{data.loc[city, '건물밀집도']:.1f}개/km²"], textposition="outside",
            ))
        fig.update_layout(title="건물밀집도 비교 (개/km²)", yaxis_title="건물밀집도",
                          showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Scatter(
                x=[data.loc[city, "건물밀집도"]], y=[data.loc[city, "평균기온"]],
                mode="markers+text", name=city, text=[city], textposition="top center",
                marker=dict(size=20, color=COLORS[city]),
            ))
        fig.update_layout(title="건물밀집도 vs 평균기온",
                          xaxis_title="건물밀집도 (개/km²)", yaxis_title="평균기온 (°C)", height=380)
        st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    for city in cities:
        fig.add_trace(go.Scatter(
            x=[data.loc[city, "건물밀집도"]], y=[data.loc[city, "평균풍속"]],
            mode="markers+text", name=city, text=[city], textposition="top center",
            marker=dict(size=20, color=COLORS[city]),
        ))
    fig.update_layout(title="건물밀집도 vs 평균풍속",
                      xaxis_title="건물밀집도 (개/km²)", yaxis_title="평균풍속 (m/s)", height=380)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Bar(
                name=city, x=[city], y=[data.loc[city, "녹지율"]],
                marker_color=COLORS[city],
                text=[f"{data.loc[city, '녹지율']:.2f}%"], textposition="outside",
            ))
        fig.update_layout(title="녹지율 비교 (%)", yaxis_title="녹지율 (%)",
                          showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        for city in cities:
            fig.add_trace(go.Scatter(
                x=[data.loc[city, "녹지율"]], y=[data.loc[city, "평균기온"]],
                mode="markers+text", name=city, text=[city], textposition="top center",
                marker=dict(size=20, color=COLORS[city]),
            ))
        fig.update_layout(title="녹지율 vs 평균기온",
                          xaxis_title="녹지율 (%)", yaxis_title="평균기온 (°C)", height=380)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🔍 분석 해석")

daegu = data.loc["대구광역시"]
ulsan = data.loc["울산광역시"]
diff_temp = daegu["평균기온"] - ulsan["평균기온"]
diff_wind = daegu["평균풍속"] - ulsan["평균풍속"]
diff_density = daegu["건물밀집도"] - ulsan["건물밀집도"]
diff_green = daegu["녹지율"] - ulsan["녹지율"]

st.markdown(f"""
| 항목 | 대구 | 울산 | 차이 (대구 - 울산) | 가설 부합 여부 |
|------|------|------|-------------------|----------------|
| 평균기온 | {daegu['평균기온']:.1f}°C | {ulsan['평균기온']:.1f}°C | **{diff_temp:+.1f}°C** | {'✅' if diff_density > 0 and diff_temp > 0 else '❌'} 건물밀집↑ → 기온↑ |
| 평균풍속 | {daegu['평균풍속']:.1f} m/s | {ulsan['평균풍속']:.1f} m/s | **{diff_wind:+.1f} m/s** | {'✅' if diff_density > 0 and diff_wind < 0 else '❌'} 건물밀집↑ → 풍속↓ |
| 건물밀집도 | {daegu['건물밀집도']:.1f} 개/km² | {ulsan['건물밀집도']:.1f} 개/km² | **{diff_density:+.1f}** | — |
| 녹지율 | {daegu['녹지율']:.2f}% | {ulsan['녹지율']:.2f}% | **{diff_green:+.2f}%** | {'✅' if diff_green < 0 and diff_temp > 0 else '❌'} 녹지↓ → 기온↑ |
""")

st.info("""
💡 **대구 vs 울산 특이점**: 대구는 내륙 분지 지형으로 한국에서 여름철 가장 더운 도시로 
알려져 있습니다. 울산은 해안 도시로 해양의 냉각 효과가 있어, 
지형 변인(내륙 vs 해안)도 온도 차이에 영향을 줄 수 있음을 고려해야 합니다.
""")
