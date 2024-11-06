# import streamlit as st
# import pymysql
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from fuzzywuzzy import process
# import re  # 정규식을 사용하기 위해 추가
# # from db_connection import create_connection  # 데이터베이스 연결 모듈 가져오기

# # # MySQL에서 데이터 로드
# # def load_data_from_db():
# #     connection = create_connection()  # 모듈화된 데이터베이스 연결 사용
# #     try:
# #         with connection.cursor() as cursor:
# #             sql = "SELECT * FROM 여가시설"  # 테이블 이름을 지정하세요
# #             cursor.execute(sql)
# #             result = cursor.fetchall()  # 결과를 가져옴
# #             df = pd.DataFrame(result)  # Pandas DataFrame으로 변환
# #     finally:
# #         connection.close()
# #     return df

# # # 데이터베이스에서 데이터를 가져오기
# # df = load_data_from_db()
# # df

# # MySQL 데이터베이스 연결 설정
# def get_db_connection():
#     try:
#         connection = pymysql.connect(
#             host='34.47.106.147', 
#             user='root',  # MySQL 사용자 이름
#             password='dkrlrhfo0992!',  # MySQL 비밀번호
#             db='mulpaas',  # 공백 포함된 데이터베이스 이름
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         print("Connection successful!")
#         return connection
#     except pymysql.err.OperationalError as e:
#         print(f"Error connecting to the database: {e}")
#         raise

# # MySQL에서 데이터 로드
# def load_data_from_db():
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT * FROM 여가시설"  # 테이블 이름을 지정하세요
#             cursor.execute(sql)
#             result = cursor.fetchall()  # 결과를 가져옴
#             df = pd.DataFrame(result)  # Pandas DataFrame으로 변환
#     finally:
#         connection.close()
#     return df

# # 데이터베이스에서 데이터를 가져오기
# df = load_data_from_db()
# df

# # 세션 초기화
# if 'location' not in st.session_state:
#     st.session_state.location = None
# if 'keyword' not in st.session_state:
#     st.session_state.keyword = None
# if 'invalid_keyword' not in st.session_state:
#     st.session_state.invalid_keyword = False
# if 'selected_facility' not in st.session_state:
#     st.session_state.selected_facility = None
# if 'page' not in st.session_state:
#     st.session_state.page = 'home'

# def recommend_facilities():
#     # 위치 정보 입력
#     st.write("위치 정보를 입력해주세요.")
    
#     # 이미 입력된 위치 정보가 있다면 기본값으로 제공
#     location_input = st.text_input("주소를 입력하세요(ex. 종로구)", value=st.session_state.location if st.session_state.location else "")

#     # 위치 정보가 바뀔 때마다 업데이트
#     if st.button("위치 확인"):
#         # 시군구명 또는 시설주소에서 정확한 지역명만 필터링
#         valid_location_pattern = r'[가-힣]+(구)?'  # "종로", "종로구", "강남구" 등을 필터링
#         match = re.match(valid_location_pattern, location_input)

#         if match:
#             # "종로"처럼 "구"가 없는 경우 자동으로 "구"를 붙여서 처리
#             if not location_input.endswith("구"):
#                 location_input += "구"

#             # 필터링 수행
#             filtered_df = df[df['시군구명'].str.contains(location_input) | df['시설주소'].str.contains(location_input)]

#             if filtered_df.empty:
#                 st.warning(f"입력하신 위치 '{location_input}'에 해당하는 시설을 찾을 수 없습니다.")
#                 st.session_state.invalid_keyword = True  # 잘못된 위치 정보로 플래그 설정
#                 st.session_state.location = None  # 이전 잘못된 입력을 초기화
#                 st.session_state.filtered_df = None
#             else:
#                 # combined_text 생성
#                 if all(col in filtered_df.columns for col in ['시설명', '시설종류명(시설유형)', '시설종류상세명(시설종류)']):
#                     filtered_df['combined_text'] = (
#                         filtered_df['시설명'] + " " +
#                         filtered_df['시설종류명(시설유형)'] + " " +
#                         filtered_df['시설종류상세명(시설종류)']
#                     )
#                     st.session_state.location = location_input
#                     st.session_state.filtered_df = filtered_df
#                     st.session_state.invalid_keyword = False  # 올바른 위치 정보로 플래그 초기화
#                     st.write(f"**{location_input}**에 있는 노인 복지시설에 대한 정보를 알려드리겠습니다.")
#                 else:
#                     st.warning("데이터에 필요한 컬럼들이 없습니다. ('시설명', '시설종류명(시설유형)', '시설종류상세명(시설종류)')")
#         else:
#             st.warning(f"입력하신 위치 '{location_input}'는 올바른 형식이 아닙니다. '구' 단위의 정확한 지역명을 입력해주세요.")
#             st.session_state.invalid_keyword = True

#     # 키워드 입력
#     if st.session_state.location and not st.session_state.invalid_keyword:
#         st.write("원하는 사회복지시설 서비스 키워드를 입력하세요 (예: 치매)")
#         keyword_input = st.text_input("키워드 입력", value=st.session_state.keyword if st.session_state.keyword else "")

#         if st.button("키워드 확인"):
#             # 사용자 입력 키워드에 대한 처리
#             filtered_df = st.session_state.filtered_df
#             if not filtered_df.empty:
#                 available_keywords = filtered_df['combined_text'].unique()
#                 best_match_keyword, similarity_score = process.extractOne(keyword_input, available_keywords)

#                 if similarity_score < 50:
#                     st.warning(f"입력하신 키워드 '{keyword_input}'에 해당하는 시설을 찾을 수 없습니다.")
#                     st.session_state.invalid_keyword = True  # 잘못된 키워드 플래그 설정
#                     st.session_state.keyword = None  # 잘못된 키워드를 초기화
#                 else:
#                     st.session_state.keyword = keyword_input
#                     st.session_state.invalid_keyword = False  # 올바른 키워드로 플래그 초기화
#                     st.write(f"'{keyword_input}'와 관련된 시설 정보를 알려드리겠습니다.")
#                     # 화면 자동 리렌더링에 맡김

#     # 시설 추천 로직
#     if st.session_state.location and st.session_state.keyword:
#         filtered_df = st.session_state.filtered_df
#         if all(col in filtered_df.columns for col in ['시설명', '시설종류명(시설유형)', '시설종류상세명(시설종류)']):
#             tfidf = TfidfVectorizer(stop_words='english')
#             tfidf_matrix = tfidf.fit_transform(filtered_df['combined_text'])
#             available_keywords = filtered_df['combined_text'].unique()
#             best_match_keyword, similarity_score = process.extractOne(st.session_state.keyword, available_keywords)

#             if similarity_score < 50:
#                 st.warning(f"입력하신 키워드 '{st.session_state.keyword}'에 해당하는 시설을 찾을 수 없습니다.")
#                 st.session_state.invalid_keyword = True
#             else:
#                 user_tfidf_vector = tfidf.transform([best_match_keyword])
#                 cosine_similarities = cosine_similarity(user_tfidf_vector, tfidf_matrix)
#                 most_similar_indices = cosine_similarities[0].argsort()[::-1]
#                 unique_facilities = []

#                 for idx in most_similar_indices:
#                     facility_name = filtered_df.iloc[idx]['시설명']
#                     if facility_name not in unique_facilities:
#                         unique_facilities.append(facility_name)
#                     if len(unique_facilities) >= 3:
#                         break

#                 if len(unique_facilities) > 0:
#                     for idx, facility_name in enumerate(unique_facilities):
#                         recommended_facility = filtered_df[filtered_df['시설명'] == facility_name].iloc[0]
#                         facility_address = recommended_facility['시설주소'] if '시설주소' in filtered_df.columns else '주소 정보 없음'
#                         st.write(f"추천된 노인 복지시설: **{facility_name}**")
#                         st.write(f"시설 주소: **{facility_address}**")

#                         facility_key = f"{facility_name}_{facility_address}_{idx}"
#                         if st.button(f"시설명: {facility_name} - 주소: {facility_address}", key=facility_key):
#                             st.session_state.selected_facility = recommended_facility
#                             st.session_state.page = 'facility_detail'
#                             # 화면 자동 리렌더링에 맡김
#                 else:
#                     st.write("해당 키워드에 맞는 시설을 찾을 수 없습니다.")
#         else:
#             st.warning("데이터에 필요한 컬럼들이 없습니다. ('시설명', '시설종류명(시설유형)', '시설종류상세명(시설종류)')")




# 기존 코드 내 로컬db . csv
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
import pandas as pd
import re  # 정규식을 사용하기 위해 추가

# CSV 파일 로드
df = pd.read_csv("서울시 사회복지시설 병합.csv", encoding='utf-8')

# 세션 초기화
if 'location' not in st.session_state:
    st.session_state.location = None
if 'keyword' not in st.session_state:
    st.session_state.keyword = None
if 'invalid_keyword' not in st.session_state:
    st.session_state.invalid_keyword = False
if 'selected_facility' not in st.session_state:
    st.session_state.selected_facility = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def recommend_facilities():
    # 위치 정보 입력
    st.write("위치 정보를 입력해주세요.")
    
    # 이미 입력된 위치 정보가 있다면 기본값으로 제공
    location_input = st.text_input("주소를 입력하세요(ex. 종로구)", value=st.session_state.location if st.session_state.location else "")

    # 위치 정보가 바뀔 때마다 업데이트
    if st.button("위치 확인"):
        # 시군구명 또는 시설주소에서 정확한 지역명만 필터링
        valid_location_pattern = r'[가-힣]+(구)?'  # "종로", "종로구", "강남구" 등을 필터링
        match = re.match(valid_location_pattern, location_input)

        if match:
            # "종로"처럼 "구"가 없는 경우 자동으로 "구"를 붙여서 처리
            if not location_input.endswith("구"):
                location_input += "구"

            # 필터링 수행
            filtered_df = df[df['시군구명'].str.contains(location_input) | df['시설주소'].str.contains(location_input)]

            if filtered_df.empty:
                st.warning(f"입력하신 위치 '{location_input}'에 해당하는 시설을 찾을 수 없습니다.")
                st.session_state.invalid_keyword = True  # 잘못된 위치 정보로 플래그 설정
                st.session_state.location = None  # 이전 잘못된 입력을 초기화
                st.session_state.filtered_df = None
            else:
                # combined_text 생성
                if all(col in filtered_df.columns for col in ['시설명', '시설종류명(시설유형)', '시설종류상세명(시설종류)']):
                    filtered_df['combined_text'] = (
                        filtered_df['시설명'] + " " +
                        filtered_df['시설종류명(시설유형)'] + " " +
                        filtered_df['시설종류상세명(시설종류)']
                    )
                    st.session_state.location = location_input
                    st.session_state.filtered_df = filtered_df
                    st.session_state.invalid_keyword = False  # 올바른 위치 정보로 플래그 초기화
                    st.write(f"**{location_input}**에 있는 노인 복지시설에 대한 정보를 알려드리겠습니다.")
                else:
                    st.warning("데이터에 필요한 컬럼들이 없습니다. ('시설명', '시설종류명(시설유형)', '시설종류상세명(시설종류)')")
        else:
            st.warning(f"입력하신 위치 '{location_input}'는 올바른 형식이 아닙니다. '구' 단위의 정확한 지역명을 입력해주세요.")
            st.session_state.invalid_keyword = True

    # 키워드 입력
    if st.session_state.location and not st.session_state.invalid_keyword:
        st.write("원하는 사회복지시설 서비스 키워드를 입력하세요 (예: 치매)")
        keyword_input = st.text_input("키워드 입력", value=st.session_state.keyword if st.session_state.keyword else "")

        if st.button("키워드 확인"):
            # 사용자 입력 키워드에 대한 처리
            filtered_df = st.session_state.filtered_df
            if not filtered_df.empty:
                available_keywords = filtered_df['combined_text'].unique()
                best_match_keyword, similarity_score = process.extractOne(keyword_input, available_keywords)

                if similarity_score < 50:
                    st.warning(f"입력하신 키워드 '{keyword_input}'에 해당하는 시설을 찾을 수 없습니다.")
                    st.session_state.invalid_keyword = True  # 잘못된 키워드 플래그 설정
                    st.session_state.keyword = None  # 잘못된 키워드를 초기화
                else:
                    st.session_state.keyword = keyword_input
                    st.session_state.invalid_keyword = False  # 올바른 키워드로 플래그 초기화
                    st.write(f"'{keyword_input}'와 관련된 시설 정보를 알려드리겠습니다.")
                    # 화면 자동 리렌더링에 맡김

    # 시설 추천 로직
    if st.session_state.location and st.session_state.keyword:
        filtered_df = st.session_state.filtered_df
        if all(col in filtered_df.columns for col in ['시설명', '시설종류명(시설유형)', '시설종류상세명(시설종류)']):
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(filtered_df['combined_text'])
            available_keywords = filtered_df['combined_text'].unique()
            best_match_keyword, similarity_score = process.extractOne(st.session_state.keyword, available_keywords)

            if similarity_score < 50:
                st.warning(f"입력하신 키워드 '{st.session_state.keyword}'에 해당하는 시설을 찾을 수 없습니다.")
                st.session_state.invalid_keyword = True
            else:
                user_tfidf_vector = tfidf.transform([best_match_keyword])
                cosine_similarities = cosine_similarity(user_tfidf_vector, tfidf_matrix)
                most_similar_indices = cosine_similarities[0].argsort()[::-1]
                unique_facilities = []

                for idx in most_similar_indices:
                    facility_name = filtered_df.iloc[idx]['시설명']
                    if facility_name not in unique_facilities:
                        unique_facilities.append(facility_name)
                    if len(unique_facilities) >= 3:
                        break

                if len(unique_facilities) > 0:
                    for idx, facility_name in enumerate(unique_facilities):
                        recommended_facility = filtered_df[filtered_df['시설명'] == facility_name].iloc[0]
                        facility_address = recommended_facility['시설주소'] if '시설주소' in filtered_df.columns else '주소 정보 없음'
                        st.write(f"추천된 노인 복지시설: **{facility_name}**")
                        st.write(f"시설 주소: **{facility_address}**")

                        facility_key = f"{facility_name}_{facility_address}_{idx}"
                        if st.button(f"시설명: {facility_name} - 주소: {facility_address}", key=facility_key):
                            st.session_state.selected_facility = recommended_facility
                            st.session_state.page = 'facility_detail'
                            # 화면 자동 리렌더링에 맡김
                else:
                    st.write("해당 키워드에 맞는 시설을 찾을 수 없습니다.")
        else:
            st.warning("데이터에 필요한 컬럼들이 없습니다. ('시설명', '시설종류명(시설유형)', '시설종류상세명(시설종류)')")

