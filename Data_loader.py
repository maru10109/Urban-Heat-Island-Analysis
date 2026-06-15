import pandas as pd
import streamlit as st

# ── GitHub raw CSV URL ──────────────────────────────────────────────────────
# 아래 URL을 본인의 GitHub 저장소 raw 링크로 교체하세요.
# 예시: https://raw.githubusercontent.com/<유저명>/<레포명>/main/통합본.csv
CSV_URL = "https://raw.githubusercontent.com/maru10109/Urban-Heat-Island-Analysis/main/통합본.csv"

@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    """GitHub에서 CSV를 불러와 파생 변수를 계산합니다."""
    df = pd.read_csv(CSV_URL, encoding="utf-8-sig")

    # 컬럼명 정리 (HTML 태그·공백 제거)
    df.columns = df.columns.str.replace(r"<br>", "", regex=True).str.strip()

    # 필요한 컬럼만 선택하고 이름 통일
    df = df.rename(columns={
        "행정구역별": "지역",
        "일시": "연도",
        "평균기온(°C)": "평균기온",
        "평균 풍속(m/s)": "평균풍속",
        "총도시공원면적(A) (천㎡)": "공원면적_천㎡",
        "면적별 건축물 현황(개)": "건축물수",
        "도시지역면적": "도시면적_㎡",
    })

    # 불필요한 Unnamed 컬럼 제거
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

    # 파생 변수 계산
    # 건물밀집도: 건축물 수 / 도시지역면적(㎡) × 1,000,000 → 개/km²
    df["건물밀집도"] = df["건축물수"] / df["도시면적_㎡"] * 1_000_000
    # 녹지율: 공원면적(천㎡) × 1000 / 도시지역면적(㎡) × 100 → %
    df["녹지율"] = (df["공원면적_천㎡"] * 1_000) / df["도시면적_㎡"] * 100

    return df
