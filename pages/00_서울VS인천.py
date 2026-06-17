import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="서울 VS 인천", page_icon="🏙️", layout="wide")

# ── 비교할 두 지역 ──
REGION_A = "서울특별시"
REGION_B = "인천광역시"

# ── 컬럼명 상수 (CSV 헤더와 일치) ──
COL_REGION = "행정구역별"
COL_TEMP   = "평균기온(°C)"
COL_WIND   = "평균 풍속(m/s)"
COL_PARK   = "총도시공원면적(A) (천㎡)"
COL_BUILD  = "면적별 건축물 현황(개)"
COL_URBAN  = "도시지역면적"

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    # 여러 인코딩을 순서대로 시도
    for enc in ["utf-8", "cp949", "euc-kr", "utf-8-sig"]:
        try:
            df = pd.read_csv(path, encoding=enc)
            break  # 성공하면 반복 중단
        except UnicodeDecodeError:
            continue  # 실패하면 다음 인코딩 시도
    else:
        # 모든 인코딩이 실패한 경우
        raise ValueError("CSV 파일의 인코딩을 읽을 수 없습니다.")

    df = df.dropna(axis=1, how="all")             # 완전히 빈 열 제거
    df.columns = [c.strip() for c in df.columns]  # 열 이름 공백 제거
    return df

def find_col(df, keyword):
    """헤더 이름이 살짝 달라도 키워드로 컬럼 찾기"""
    for c in df.columns:
        if keyword in c:
            return c
    return None

try:
    df = load_data("통합본.csv")
except FileNotFoundError:
    st.error("CSV 파일(통합본.csv)을 찾을 수 없습니다.")
    st.stop()

st.title(f"🏙️ {REGION_A} VS {REGION_B}")
st.markdown("##### 건물 밀집도와 녹지율에 따른 기온·풍속 비교")
st.markdown("---")

# 실제 컬럼명 매칭 (헤더 표기 차이 대비)
c_temp  = find_col(df, "평균기온")
c_wind  = find_col(df, "풍속")
c_dense = "건물밀집도"
c_green = "녹지율(%)"

two = df[df[COL_REGION].isin([REGION_A, REGION_B])].copy()
if len(two) < 2:
    st.warning("두 지역의 데이터를 모두 찾지 못했습니다. CSV의 지역명을 확인하세요.")
    st.stop()

a = two[two[COL_REGION] == REGION_A].iloc[0]
b = two[two[COL_REGION] == REGION_B].iloc[0]

# ── 핵심 지표 카드 ──
st.subheader("📌 핵심 지표 한눈에 보기")
m1, m2, m3, m4 = st.columns(4)
m1.metric(f"{REGION_A} 평균기온", f"{a[c_temp]:.1f}℃",
          f"{a[c_temp]-b[c_temp]:+.1f}℃ vs {REGION_B}")
m2.metric(f"{REGION_A} 풍속", f"{a[c_wind]:.1f}m/s",
          f"{a[c_wind]-b[c_wind]:+.1f}m/s vs {REGION_B}")
m3.metric(f"{REGION_A} 건물밀집도", f"{a[c_dense]:.0f}",
          f"{a[c_dense]-b[c_dense]:+.0f}")
m4.metric(f"{REGION_A} 녹지율", f"{a[c_green]:.2f}%",
          f"{a[c_green]-b[c_green]:+.2f}%p")

st.markdown("---")

# ── 항목별 막대 비교 ──
st.subheader("📊 항목별 비교")
metrics = [
    (c_temp, "평균기온(℃)"),
    (c_wind, "평균 풍속(m/s)"),
    (c_dense, "건물밀집도 (면적당 건물 수)"),
    (c_green, "녹지율(%)"),
]

fig = make_subplots(rows=2, cols=2, subplot_titles=[m[1] for m in metrics])
positions = [(1,1),(1,2),(2,1),(2,2)]
for (col, label), (r, c) in zip(metrics, positions):
    fig.add_trace(go.Bar(
        x=[REGION_A, REGION_B],
        y=[a[col], b[col]],
        marker_color=["#5bc0de", "#e88"],
        text=[f"{a[col]:.2f}", f"{b[col]:.2f}"],
        textposition="outside",
        showlegend=False,
    ), row=r, col=c)
fig.update_layout(height=600, title="네 가지 항목 비교")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── 가설 검증 해석 ──
st.subheader("🔍 가설 검증 해석")
denser = REGION_A if a[c_dense] > b[c_dense] else REGION_B
denser_row = a if a[c_dense] > b[c_dense] else b
other_row  = b if a[c_dense] > b[c_dense] else a
other_name = REGION_B if denser == REGION_A else REGION_A

temp_check = "높습니다 ✅ (가설 부합)" if denser_row[c_temp] > other_row[c_temp] else "낮습니다 ❌ (가설과 다름)"
wind_check = "느립니다 ✅ (가설 부합)" if denser_row[c_wind] < other_row[c_wind] else "빠릅니다 ❌ (가설과 다름)"
green_check = "낮습니다 ✅ (가설 부합)" if denser_row[c_green] < other_row[c_green] else "높습니다 ❌ (가설과 다름)"

st.info(f"""
**건물 밀집도가 더 높은 도시는 `{denser}` 입니다.**

- 🌡️ **기온**: `{denser}`의 기온이 `{other_name}`보다 **{temp_check}**
- 🌬️ **풍속**: `{denser}`의 풍속이 `{other_name}`보다 **{wind_check}**
- 🌳 **녹지율**: `{denser}`의 녹지율이 `{other_name}`보다 **{green_check}**

> 💭 위 결과가 가설과 일치하나요? 다르다면 왜 그럴지 생각해보세요.
> (예: 인천은 바다와 인접해 풍속·기온에 다른 요인이 작용할 수 있어요!)
""")

# ── 원본 데이터 ──
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(two, use_container_width=True)
