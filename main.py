import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="도시 열섬효과 분석",
    page_icon="🏙️",
    layout="wide",
)

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; padding: 1rem 0; }
    .sub-title { font-size: 1rem; color: #888; text-align: center; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏙️ 도시 열섬효과 분석 프로젝트</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">건물 밀집도 · 녹지율이 기온과 풍속에 미치는 영향 탐구</div>', unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
### 🎯 연구 질문
1. 도시의 **건물 밀집도**가 높을수록 **평균기온**이 높아질까? (열섬효과)
2. 건물 밀집도가 높은 도시는 **풍속**이 더 느릴까? (건물이 바람을 막음)
3. **녹지율**이 높은 도시는 기온이 더 낮을까?

### 📂 페이지 안내
왼쪽 사이드바에서 분석할 페이지를 선택하세요.
- **00 서울 VS 인천**
- **01 세종 VS 대전**
- **02 대구 VS 울산**
- **03 광주 VS 부산**
- **04 전체 종합** (8개 도시 상관관계 분석)

### 💡 핵심 개념: 밀도로 비교하기
도시마다 크기가 다르므로, 단순 개수가 아니라 **면적당 비율**로 비교합니다.
- **건물 밀집도** = 건축물 수 ÷ 도시지역면적
- **녹지율** = 도시공원면적 ÷ 도시지역면적
""")

st.markdown("---")

@st.cache_data
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
try:
    df = load_data("통합본.csv")
    st.subheader("📊 전체 데이터 미리보기")
    st.dataframe(df, use_container_width=True)
except FileNotFoundError:
    st.error("CSV 파일(통합본.csv)을 찾을 수 없습니다. 저장소 루트에 파일이 있는지 확인해 주세요.")
