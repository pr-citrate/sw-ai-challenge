import streamlit as st
from api import get_data
import pandas as pd
import folium
from streamlit_folium import st_folium


def main() -> None:
    st.write("# 무더위쉼터 정보")

    st.write("---")
    st.write("## 검색하기")

    search_query: str = st.text_input("검색어를 입력하세요", "익산시 금마면")

    if "search_button" not in st.session_state:
        st.session_state.search_button = False

    def search():
        st.session_state.search_button = True

    st.button("검색", on_click=search)

    data: dict = get_data()

    df: pd.DataFrame = pd.DataFrame(data["HeatWaveShelter"][1]["row"])

    df = df[["restname", "restaddr", "fclty_ty_nm", "la", "lo"]].rename(
        columns={
            "restname": "이름",
            "restaddr": "주소",
            "fclty_ty_nm": "시설 종류",
            "la": "위도",
            "lo": "경도",
        }
    )

    if st.session_state.search_button:
        st.write("---")
        st.write("## 지도 보기")

        map_df: pd.DataFrame = df[["이름", "위도", "경도"]]
        display_df: pd.DataFrame = df.drop(columns=["위도", "경도"])

        center: list[float, float] = [36.01457166, 127.0347845]
        map: folium.Map = folium.Map(location=center, zoom_start=13)

        for i in range(len(map_df)):
            popup_info: str = f"""
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


if __name__ == "__main__":
    main()
