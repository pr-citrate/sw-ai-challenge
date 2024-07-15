import streamlit as st
from api import get_data
import pandas as pd
import folium
from streamlit_folium import st_folium


@st.cache_resource
def fetch() -> dict:
    data: dict = get_data()
    return data


def main() -> None:
    def handleButtonOnClick():
        st.session_state.search_button = True

    st.set_page_config(layout="wide")
    st.markdown(
        """
    <style>
        h1 {
            font-size: 4.5rem !important;
        }

        h2 {
            font-size: 3.5rem !important;
        }

        p {
            font-size: 2.5rem !important;
        }

        input[type="text"] {
            font-size: 1.5rem !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("바람터")
    st.subheader("주변 무더위 쉼터를 한 눈에", divider="rainbow")
    st.write("<div style='height: 2.5rem;' />", unsafe_allow_html=True)

    st.write("검색하기")

    search_query: str = st.text_input("검색어를 입력하세요", "익산시 금마면")

    if "search_button" not in st.session_state:
        st.session_state.search_button = False

    st.button("검색", on_click=handleButtonOnClick)

    data: dict = fetch()

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
        st.header("지도 보기")

        map_df: pd.DataFrame = df[["이름", "위도", "경도"]]
        display_df: pd.DataFrame = df.drop(columns=["위도", "경도"])

        center: list[float, float] = [map_df["위도"].mean(), map_df["경도"].mean()]
        map: folium.Map = folium.Map(location=center, zoom_start=13)

        for i in range(len(map_df)):
            popup_info: str = f"""
            <div style="font-size: 2.5rem;">
                <b>이름:</b> {map_df["이름"][i]}<br>
                <b>주소:</b> {df["주소"][i]}<br>
                <b>시설 종류:</b> {df["시설 종류"][i]}<br>
            </div>
            """
            folium.Marker(
                location=[map_df["위도"][i], map_df["경도"][i]],
                popup=folium.Popup(popup_info, max_width=300),
                # tooltip=map_df["이름"][i],
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(map)

        display_df.index += 1

        st_folium(map, width=700, height=500)

        st.write("## 표로 보기")
        styled_df: pd.DataFrame = display_df.style.set_table_styles(
            [{"selector": "th, td", "props": [("font-size", "1.5rem")]}]
        )
        st.write(styled_df.to_html(), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
