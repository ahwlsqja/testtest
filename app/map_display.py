import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from streamlit_folium import st_folium
from googlemap import user_map
import googlemap  # googlemap.py에서 함수 불러옴
from db_connection import create_connection  # MySQL 연결 함수

# 페이지 이동을 처리하는 함수
def navigate_to_page(page_name):
    """ 페이지 이동을 처리하는 함수 """
    # 현재 페이지를 기록에 추가
    if 'page' in st.session_state and st.session_state.page != page_name:
        if 'page_history' not in st.session_state:
            st.session_state.page_history = []
        st.session_state.page_history.append(st.session_state.page)
    st.session_state.page = page_name

# '뒤로 가기' 기능을 처리하는 함수
def go_back():
    """ '뒤로 가기' 기능을 처리하는 함수 """
    if 'page_history' in st.session_state and st.session_state.page_history:
        st.session_state.page = st.session_state.page_history.pop()

# 북마크를 MySQL에 저장하는 함수
# 북마크 저장 기능
def save_bookmark(facility_name, facility_address, facility_type):
    # 로그인 여부 확인
    if 'nickname' not in st.session_state or not st.session_state['nickname']:
        st.warning("로그인 후 북마크할 수 있습니다.")
        return

    nickname = st.session_state['nickname']

    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            # 북마크 데이터베이스에 사용자와 시설 정보를 저장
            sql = """
            INSERT INTO bookmarks (user_id, facility_name, facility_address, facility_type)
            VALUES (
                (SELECT id FROM users WHERE nickname = %s), 
                %s, %s, %s
            )
            """
            cursor.execute(sql, (nickname, facility_name, facility_address, facility_type))
        connection.commit()
        st.success("북마크가 저장되었습니다!")
    except Exception as e:
        st.error(f"북마크 저장 중 오류 발생: {e}")
    finally:
        connection.close()


# 복지시설 상세 정보를 보여주는 함수
def display_facility_detail(facility):
    st.write("### 선택된 노인 복지시설 상세 정보")
    for column in facility.index:
        st.write(f"**{column}**: {facility[column]}")

    facility_address = facility.get('시설주소')
    facility_name = facility.get('시설명')

    if facility_address and facility_name:
        facility_lat, facility_lon = googlemap.get_lat_lon_from_address(facility_address)
        if facility_lat and facility_lon:
            current_lat, current_lon, accuracy = googlemap.get_location_from_google()
            st.write(f"현재 위치: 위도 {current_lat}, 경도 {current_lon} (정확도: {accuracy} meters)")
            map_object = user_map(
                lat=current_lat, lon=current_lon, accuracy=accuracy, 
                facility_lat=facility_lat, facility_lon=facility_lon, 
                facility_name=facility_name, facility_address=facility_address
            )
            st_folium(map_object, width=725, height=500)

    # 북마크 버튼
    if st.button("북마크"):
        save_bookmark(facility_name, facility_address, facility.get('시설종류명(시설유형)'))


    # '다른 복지시설 정보 보기' 버튼을 눌렀을 때 welfare_continue 페이지로 이동
    if st.button("다른 복지시설 정보 보기"):
        navigate_to_page('welfare_continue')

    # '뒤로 가기' 버튼 구현
    if st.button("뒤로 가기"):
        go_back()

# 시설 추천을 계속 보여주는 함수
def continue_recommendation():
    st.empty()  # 이전 화면을 지우고 새로운 화면처럼 보이게
    st.write("### 해당 지역 정보 계속 보기")
    if 'recommended_indices' not in st.session_state:
        st.session_state.recommended_indices = []

    # 필터링된 데이터프레임 사용
    filtered_df = st.session_state.filtered_df

    # TF-IDF 벡터화 수행
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(filtered_df['combined_text'])
    available_keywords = filtered_df['combined_text'].unique()
    best_match_keyword, similarity_score = process.extractOne(st.session_state.keyword, available_keywords)

    if similarity_score < 50:
        st.warning(f"입력하신 키워드 '{st.session_state.keyword}'에 해당하는 시설을 찾을 수 없습니다.")
    else:
        user_tfidf_vector = tfidf.transform([best_match_keyword])
        cosine_similarities = cosine_similarity(user_tfidf_vector, tfidf_matrix)

        sorted_indices = cosine_similarities[0].argsort()[::-1]
        most_similar_idx = None

        for idx in sorted_indices:
            if idx not in st.session_state.recommended_indices:
                most_similar_idx = idx
                st.session_state.recommended_indices.append(idx)
                break

        if most_similar_idx is not None:
            recommended_facility = filtered_df.iloc[most_similar_idx]

            facility_name = recommended_facility['시설명']
            facility_address = recommended_facility['시설주소'] if '시설주소' in filtered_df.columns else '주소 정보 없음'
            st.write(f"추천된 노인 복지시설: **{facility_name}**")
            st.write(f"시설 주소: **{facility_address}**")

            if st.button(f"{facility_name} - {facility_address}"):
                st.session_state.selected_facility = recommended_facility
                navigate_to_page('facility_detail')  # 상세 페이지로 이동

    if st.button("해당 지역 정보 계속 보기"):
        navigate_to_page('welfare_continue')

    if st.button("다시 입력하기"):
        st.session_state.page = 'welfare_facility'
        st.session_state.location = None
        st.session_state.keyword = None
        st.session_state.selected_facility = None
        st.session_state.recommended_indices = []
        st.session_state.invalid_keyword = False
        st.experimental_rerun()