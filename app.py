import streamlit as st
from api import get_data
import pandas as pd
import folium
from streamlit_folium import st_folium

st.write("# 무더위쉼터 정보")

st.write("---")
st.write("## 검색하기")

# 검색어 입력
search_query = st.text_input("검색어를 입력하세요", "익산시 금마면")

# 검색 버튼
if "search_button" not in st.session_state:
    st.session_state.search_button = False


def search():
    st.session_state.search_button = True


st.button("검색", on_click=search)

# 데이터 가져오기
data = get_data()

# 데이터를 데이터프레임으로 변환
df = pd.DataFrame(data["HeatWaveShelter"][1]["row"])

# 불필요한 열 제거 및 열 이름 변경
df = df[["restname", "restaddr", "fclty_ty_nm", "la", "lo"]].rename(
    columns={
        "restname": "이름",
        "restaddr": "주소",
        "fclty_ty_nm": "시설 종류",
        "la": "위도",
        "lo": "경도",
    }
)

# 검색 버튼이 눌렸을 때만 지도와 데이터프레임 출력
if st.session_state.search_button:
    st.write("---")
    st.write("## 지도 보기")

    # 지도 추가를 위한 위도와 경도를 분리
    map_df = df[["이름", "위도", "경도"]]

    # 위도와 경도를 제거한 데이터프레임 출력
    display_df = df.drop(columns=["위도", "경도"])

    # 지도 중심 설정
    center = [36.01457166, 127.0347845]
    map = folium.Map(location=center, zoom_start=13)

    # 마커 추가
    for i in range(len(map_df)):
        popup_info = f"""
        <div style="font-size: 16px;">
            <b>이름:</b> {map_df["이름"][i]}<br>
            <b>주소:</b> {df["주소"][i]}<br>
            <b>시설 종류:</b> {df["시설 종류"][i]}<br>
        </div>
        """
        folium.Marker(
            location=[map_df["위도"][i], map_df["경도"][i]],
            popup=folium.Popup(popup_info, max_width=300),
            tooltip=map_df["이름"][i],
        ).add_to(map)

    st_folium(map, width=700, height=500)
    st.write(display_df)
