import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="도시 열섬효과 분석",
    page_icon="🏙️",
    layout="wide",
)

st.title("🏙️ 도시 열섬효과 분석 프로젝트")
st.markdown("---")

st.markdown("""
### 📌 프로젝트 소개
이 프로젝트는 **도시 열섬효과**를 행정구역별 데이터로 분석합니다.

도시의 **평균기온**이 다음 요소들과 어떤 관계가 있는지 살펴봅니다.
- 🌳 총 도시공원면적
- 🏢 면적별 건축물 현황
- 🌆 도시지역면적
- 🌬️ 평균 풍속

### 📂 페이지 안내
왼쪽 사이드바에서 분석할 페이지를 선택하세요.
- **서울 VS 인천**
- **세종 VS 대전**
- **대구 VS 울산**
- **광주 VS 부산**
- **전체 종합**
""")

st.markdown("---")

# 전체 데이터 미리보기
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # 완전히 비어있는 열 제거
    df = df.dropna(axis=1, how="all")
    # 열 이름 공백 정리
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = load_data("통합본.csv")
    st.subheader("📊 전체 데이터 미리보기")
    st.dataframe(df, use_container_width=True)
except FileNotFoundError:
    st.error("CSV 파일(통합본.csv)을 찾을 수 없습니다. 저장소 루트에 파일이 있는지 확인해 주세요.")
