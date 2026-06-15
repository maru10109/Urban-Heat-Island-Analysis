import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_loader import load_data

st.set_page_config(page_title="세종 vs 대전", page_icon="2️⃣", layout="wide")

df = load_data()
cities = ["세종특별자치시", "대전광역시"]
data = df[df["지역"].isin(cities)].set_index("지역")

COLORS = {"세종특별자치시": "#2D6A4F", "대전광역시": "#B7950B"}

st.title("2️⃣ 세종특별자치시 vs 대전광역시")
st.caption("📍 북위 약 36.3° | 위도 조건이 유사한 두 도시 비교 (2023년 기준)")
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
        s_val = data.loc["세종특별자치시", key]
        d_val = data.loc["대전광역시", key]
        delta = round(s_val - d_val, 2)
        st.metric(f"세종 {label}", f"{s_val:.2f}", delta=f"세종-대전: {delta:+.2f}")

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
                          yaxis=dict(range=[12, 16]), showlegend=False, height=380)
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
                          yaxis=dict(range=[0, 3]), showlegend=False, height=380)
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

sejong = data.loc["세종특별자치시"]
daejeon = data.loc["대전광역시"]
diff_temp = sejong["평균기온"] - daejeon["평균기온"]
diff_wind = sejong["평균풍속"] - daejeon["평균풍속"]
diff_density = sejong["건물밀집도"] - daejeon["건물밀집도"]
diff_green = sejong["녹지율"] - daejeon["녹지율"]

st.markdown(f"""
| 항목 | 세종 | 대전 | 차이 (세종 - 대전) | 가설 부합 여부 |
|------|------|------|-------------------|----------------|
| 평균기온 | {sejong['평균기온']:.1f}°C | {daejeon['평균기온']:.1f}°C | **{diff_temp:+.1f}°C** | {'✅' if diff_density > 0 and diff_temp > 0 else '❌'} 건물밀집↑ → 기온↑ |
| 평균풍속 | {sejong['평균풍속']:.1f} m/s | {daejeon['평균풍속']:.1f} m/s | **{diff_wind:+.1f} m/s** | {'✅' if diff_density > 0 and diff_wind < 0 else '❌'} 건물밀집↑ → 풍속↓ |
| 건물밀집도 | {sejong['건물밀집도']:.1f} 개/km² | {daejeon['건물밀집도']:.1f} 개/km² | **{diff_density:+.1f}** | — |
| 녹지율 | {sejong['녹지율']:.2f}% | {daejeon['녹지율']:.2f}% | **{diff_green:+.2f}%** | {'✅' if diff_green < 0 and diff_temp > 0 else '❌'} 녹지↓ → 기온↑ |
""")

st.info("""
💡 **세종 vs 대전 특이점**: 세종시는 2012년 출범한 계획도시로, 대전보다 녹지율이 현저히 높고 
건물밀집도가 낮습니다. 이 비교는 '계획도시 설계가 열섬현상을 완화하는가'라는 
추가적인 분석 가설을 탐색할 수 있는 좋은 사례입니다.
""")
