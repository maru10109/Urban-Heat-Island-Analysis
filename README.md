# 🏙️ 도시 열섬효과 분석 프로젝트

> 건물 밀집도와 녹지율이 도시의 평균기온·풍속에 미치는 영향을 데이터로 탐구하는 프로젝트입니다.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)

---

## 📌 프로젝트 소개

도시화가 진행되면서 도심 지역의 기온이 주변보다 높아지는 **열섬효과(Urban Heat Island)** 현상이 나타납니다.
본 프로젝트는 대한민국 8개 주요 도시의 데이터를 활용하여 다음 가설들을 검증합니다.

link
평균 기온, 평균 풍속 https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36
도시 지역 면적 https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https%3A%2F%2Fkosis.kr%3A443%2FstatHtml%2FstatHtml.do%3Fconn_path%3DMT_GTITLE01%26list_id%3D107%26obj_var_id%3D%26seqNo%3D%26tblId%3DDT_1YL21291E%26vw_cd%3DMT_GTITLE01%26itm_id%3D%26language%3Dkor%26lang_mode%3Dko%26orgId%3D101%26
도시 공원 면적 https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https%3A%2F%2Fkosis.kr%3A443%2FstatHtml%2FstatHtml.do%3Fconn_path%3DMT_GTITLE01%26list_id%3D108%26obj_var_id%3D%26seqNo%3D%26tblId%3DDT_1YL21281%26vw_cd%3DMT_GTITLE01%26itm_id%3D%26language%3Dkor%26lang_mode%3Dko%26orgId%3D101%26
건축물 개수 https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https%3A%2F%2Fkosis.kr%3A443%2FstatHtml%2FstatHtml.do%3Fconn_path%3DMT_ZTITLE%26list_id%3DM1_5%26obj_var_id%3D%26seqNo%3D%26tblId%3DDT_MLTM_540%26vw_cd%3DMT_ZTITLE%26itm_id%3D%26language%3Dkor%26lang_mode%3Dko%26orgId%3D116%26


### 🎯 연구 질문 (가설)

1. **건물 밀집도가 높을수록 평균기온이 높을까?** (열섬효과)
2. **건물 밀집도가 높을수록 풍속이 느릴까?** (건물이 바람의 흐름을 막음)
3. **녹지율이 높을수록 평균기온이 낮을까?** (녹지의 냉각 효과)

---

## 📊 분석 대상 도시 (8개)

| 비교 그룹 | 도시 A | 도시 B |
|-----------|--------|--------|
| 페이지 00 | 서울특별시 | 인천광역시 |
| 페이지 01 | 세종특별자치시 | 대전광역시 |
| 페이지 02 | 대구광역시 | 울산광역시 |
| 페이지 03 | 광주광역시 | 부산광역시 |

---

## 📂 프로젝트 구조

```
urban-heat-island-analysis/
├── main.py                  # 메인 페이지 (프로젝트 소개 + 전체 데이터)
├── requirements.txt         # 필요한 라이브러리 목록
├── 통합본.csv               # 분석 데이터 (8개 도시)
├── README.md                # 프로젝트 설명 문서
└── pages/
    ├── 00_서울VS인천.py      # 서울 vs 인천 비교
    ├── 01_세종VS대전.py      # 세종 vs 대전 비교
    ├── 02_대구VS울산.py      # 대구 vs 울산 비교
    ├── 03_광주VS부산.py      # 광주 vs 부산 비교
    └── 04_전체종합.py        # 8개 도시 종합 상관관계 분석
```

---

## 🔑 핵심 개념: 왜 '밀도'로 비교할까?

도시마다 면적이 다르기 때문에 단순히 건물 **개수**나 공원 **면적**을 비교하면
"큰 도시가 무조건 건물이 많다"는 함정에 빠집니다.

그래서 **면적당 비율(밀도)** 로 환산해 공정하게 비교합니다.

| 파생 지표 | 계산식 | 의미 |
|-----------|--------|------|
| **건물밀집도** | 건축물 수 ÷ 도시지역면적 × 1,000,000 | 면적 100만㎡당 건물 수 |
| **녹지율(%)** | 도시공원면적 ÷ 도시지역면적 × 100 | 도시 면적 대비 공원 비율 |

---

## 📈 페이지별 주요 기능

### 🏠 메인 페이지 (`main.py`)
- 프로젝트 소개 및 연구 질문 안내
- 전체 8개 도시 데이터 미리보기
- 분석 도시 수, 기온/녹지율 범위 등 요약 지표

### 🆚 도시 비교 페이지 (`00`~`03`)
- **📊 항목별 비교**: 4개 지표(기온·풍속·밀집도·녹지율) 막대그래프
- **🕸️ 종합 레이더**: 전국 대비 두 도시의 상대적 위치를 방사형 차트로 표현
- **🏆 전국 순위**: 8개 도시 중 각 도시의 지표별 순위 (메달 표시)
- **🔍 가설 검증**: 두 도시 비교를 통한 가설 부합 여부 자동 판정

### 📊 전체 종합 페이지 (`04`)
- **📋 데이터 & 순위**: 전체 데이터 테이블 + 지표별 순위 막대그래프
- **🌡️ 기온 분석**: 산점도 + 추세선 + 회귀식 + 결정계수(R²)
- **🌬️ 풍속 분석**: 건물밀집도·녹지율과 풍속의 관계
- **🔥 상관관계**: 상관계수 히트맵 + 8개 도시 종합 레이더
- **📝 종합 결론**: 가설 검증 종합 점수 + 분석의 한계 논의

---

## 🛠️ 사용 기술

| 기술 | 용도 |
|------|------|
| **Python** | 데이터 처리 및 분석 |
| **Streamlit** | 웹 대시보드 제작 |
| **Pandas** | 데이터프레임 처리 |
| **Plotly** | 인터랙티브 시각화 (막대·산점도·레이더·히트맵) |
| **NumPy** | 회귀분석(추세선) 계산 |

---

## 🚀 실행 방법

### 1. 로컬에서 실행하기

```bash
# 1) 저장소 복제
git clone https://github.com/사용자명/urban-heat-island-analysis.git
cd urban-heat-island-analysis

# 2) 라이브러리 설치
pip install -r requirements.txt

# 3) 앱 실행
streamlit run main.py
```

실행 후 브라우저에서 자동으로 `http://localhost:8501` 이 열립니다.

### 2. Streamlit Cloud로 배포하기

1. 본 프로젝트를 GitHub 저장소에 업로드
2. [Streamlit Cloud](https://streamlit.io/cloud) 접속 후 로그인
3. **New app** → 저장소 선택 → Main file path를 `main.py`로 지정
4. **Deploy** 클릭

---

## 📊 데이터 정보

- **출처**: 기상청 / 통계청 / 국토교통부 (행정구역별 통계)
- **기준 연도**: 2023년
- **포함 항목**:
  - 행정구역별 / 일시(연도)
  - 평균기온(°C)
  - 평균 풍속(m/s)
  - 총 도시공원면적(천㎡)
  - 면적별 건축물 현황(개)
  - 도시지역면적

---

## 💡 분석 결과 해석 시 주의사항

> ⚠️ **상관관계 ≠ 인과관계**
> 이 분석은 변수 간 '관계'를 보여줄 뿐, '원인-결과'를 증명하지 않습니다.

- **표본 수가 적음**: 8개 도시만으로는 통계적 일반화에 한계가 있습니다.
- **해안 도시의 영향**: 부산·인천·울산은 바다의 영향으로 기온/풍속 패턴이 다를 수 있습니다.
- **숨은 변수(위도)**: 남쪽 도시일수록 기온이 높은 경향이 있어, 건물밀집도의 순수 효과와 구분이 필요합니다.

---

## 🔮 향후 개선 방향

- [ ] 더 많은 도시(시·군 단위)로 표본 확대
- [ ] 여름철(7~8월) 데이터로 열섬효과 집중 분석
- [ ] 위도·해안 여부를 통제변수로 추가한 다중회귀분석
- [ ] 연도별 시계열 데이터로 변화 추이 분석

---

- **프로젝트 주제**: 도시 열섬효과 데이터 분석

---
