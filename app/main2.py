# import streamlit as st
# from recommendation import recommend_facilities
# from map_display import display_facility_detail, continue_recommendation
# from session_manager import initialize_session
# # from db_connection import yunjin_connection  # MySQL 연결 함수
# from db_connection import create_connection 
# from login_system import login
# import time
# import final4  # final4.py 모듈 가져오기
# from login_system import logout

# # 스플래시 화면 설정 - 첫 실행시에만 스플래시 화면을 보여줌
# if 'splash_shown' not in st.session_state:
#     splash = st.empty()
#     image_path = r'라온하제 스플래시 이미지 샘플.jpg'
#     splash.image(image_path,use_column_width=True)
#     splash.markdown("""
#         <div style="display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center;">
#             <h1 style="font-size: 3em; color: #4CAF50;">라온하제: 서울시 노인 복지 서비스 플랫폼</h1>
#         </div>
#     """, unsafe_allow_html=True)
#     time.sleep(3)
#     splash.empty()
#     st.session_state.splash_shown = True

# # 세션 초기화
# initialize_session()

# if 'page' not in st.session_state:
#     st.session_state.page = 'home'

# # 로그인 체크
# if 'nickname' not in st.session_state or st.session_state['nickname'] is None:
#     login()
# else:
#     if st.session_state.page == 'home':
#         st.title(f'라온하제: {st.session_state["nickname"]}님, 오늘보다 즐거운 내일')
#         st.write("아래에서 원하는 서비스를 선택하세요:")

#         st.markdown("""
#             <style>
#             .btn-container {
#                 display: flex;
#                 justify-content: space-around;
#                 margin-top: 30px;
#             }
#             .btn {
#                 padding: 20px;
#                 font-size: 1.5em;
#                 font-weight: bold;
#                 color: white;
#                 background-color: #4CAF50;
#                 border: none;
#                 border-radius: 10px;
#                 cursor: pointer;
#                 width: 40%;
#                 text-align: center;
#                 text-decoration: none;
#                 transition: background-color 0.3s ease;
#             }
#             .btn:hover {
#                 background-color: #45a049;
#             }
#             </style>
#             <div class="btn-container">
#                 <a href="#" onclick="document.getElementById('welfare_btn').click();" class="btn">노인 복지시설 정보</a>
#                 <a href="#" onclick="document.getElementById('jobs_btn').click();" class="btn">노인 일자리 정보</a>
#             </div>
#         """, unsafe_allow_html=True)

#         col1, col2 = st.columns(2)

#         with col1:
#             if st.button("노인 복지시설 정보", key="welfare_btn"):
#                 st.session_state.page = 'welfare_facility'

#         with col2:
#             if st.button("노인 일자리 정보", key="jobs_btn"):
#                 st.session_state.page = 'senior_jobs'

#     # 노인 복지시설 정보 화면
#     if st.session_state.page == 'welfare_facility':
#         recommend_facilities()

    # # 일자리 추천 페이지
    # if st.session_state.page == 'senior_jobs':
    #     final4.main()  # final4.py 모듈의 main() 함수 호출

    # #로그아웃
    # logout()





##원래 내 코드
# import streamlit as st
# from recommendation import recommend_facilities
# from map_display import display_facility_detail, continue_recommendation
# from session_manager import initialize_session
# from db_connection import create_connection
# from login_system import login, logout
# import time

# # 스플래시 화면 설정 - 첫 실행시에만 스플래시 화면을 보여줌
# if 'splash_shown' not in st.session_state:
#     splash = st.empty()
    
#     # 로컬 이미지 경로
#     # image_path = r"라온하제 스플래시 이미지 샘플.jpg"
#     image_path = r"라온하제 스플래시 이미지 샘플.jpg"
#     splash.image(image_path, use_column_width=True)  # 이미지 표시
#     splash.markdown(
#         """
#         <div style="display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center;">
#             <h1 style="font-size: 3em; color: #4CAF50;">라온하제: 서울시 노인 복지 서비스 플랫폼</h1>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
#     time.sleep(3)
#     splash.empty()
#     st.session_state.splash_shown = True

# # 세션 초기화
# initialize_session()  # 여기에 초기화 함수 추가

# # 세션 상태 초기화
# if 'page' not in st.session_state:
#     st.session_state.page = 'home'

# # 로그인 체크
# if 'nickname' not in st.session_state or st.session_state['nickname'] is None:
#     login()  # 닉네임을 입력받는 로그인 함수 호출
# else:
#     # 로그인 후에만 위치정보 및 키워드 입력 기능 제공
#     if st.session_state.page == 'home':
#         st.title(f'라온하제: {st.session_state["nickname"]}님, 오늘보다 즐거운 내일')
#         st.write("아래에서 원하는 서비스를 선택하세요:")

#         st.markdown("""
#             <style>
#             .btn-container {
#                 display: flex;
#                 justify-content: space-around;
#                 margin-top: 30px;
#             }
#             .btn {
#                 padding: 20px;
#                 font-size: 1.5em;
#                 font-weight: bold;
#                 color: white;
#                 background-color: #4CAF50;
#                 border: none;
#                 border-radius: 10px;
#                 cursor: pointer;
#                 width: 40%;
#                 text-align: center;
#                 text-decoration: none;
#                 transition: background-color 0.3s ease;
#             }
#             .btn:hover {
#                 background-color: #45a049;
#             }
#             </style>
#             <div class="btn-container">
#                 <a href="#" onclick="document.getElementById('welfare_btn').click();" class="btn">노인 복지시설 정보</a>
#                 <a href="#" onclick="document.getElementById('jobs_btn').click();" class="btn">노인 일자리 정보</a>
#             </div>
#         """, unsafe_allow_html=True)

#         col1, col2 = st.columns(2)

#         with col1:
#             if st.button("노인 복지시설 정보", key="welfare_btn"):
#                 st.session_state.page = 'welfare_facility'

#         with col2:
#             if st.button("노인 일자리 정보", key="jobs_btn"):
#                 st.session_state.page = 'senior_jobs'

#     # 노인 복지시설 정보 화면
#     if st.session_state.page == 'welfare_facility':
#         recommend_facilities()

#     # 시설 상세 정보 화면 및 북마크 버튼 추가
#     if st.session_state.page == 'facility_detail' and not st.session_state.selected_facility.empty:
#     # facility detail 화면 처리

#         display_facility_detail(st.session_state.selected_facility)

#     # 해당 지역 정보 계속 보기 화면
#     if st.session_state.page == 'welfare_continue':
#         continue_recommendation()

#     # 로그아웃
#     logout()





















# 된 코드 내 로컬 DB랑 csv로 한 코드




import streamlit as st
from recommendation import recommend_facilities
from map_display import display_facility_detail, continue_recommendation
from session_manager import initialize_session
from db_connection import create_connection
from login_system import login, logout
import time
import final_job_main

# 스플래시 화면 설정 - 첫 실행시에만 스플래시 화면을 보여줌
if 'splash_shown' not in st.session_state:
    splash = st.empty()
    
    # 로컬 이미지 경로
    image_path = r"라온하제 스플래시 이미지 샘플.jpg"
    splash.image(image_path, use_column_width=True)  # 이미지 표시
    splash.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center;">
            <h1 style="font-size: 3em; color: #4CAF50;">라온하제: 서울시 노인 복지 서비스 플랫폼</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(3)
    splash.empty()
    st.session_state.splash_shown = True

# 세션 초기화
initialize_session()  # 여기에 초기화 함수 추가

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# 로그인 체크
if 'nickname' not in st.session_state or st.session_state['nickname'] is None:
    login()  # 닉네임을 입력받는 로그인 함수 호출
else:
    # 로그인 후에만 위치정보 및 키워드 입력 기능 제공
    if st.session_state.page == 'home':
        st.title(f'라온하제: {st.session_state["nickname"]}님, 오늘보다 즐거운 내일')
        st.write("아래에서 원하는 서비스를 선택하세요:")

        st.markdown("""
            <style>
            .btn-container {
                display: flex;
                justify-content: space-around;
                margin-top: 30px;
            }
            .btn {
                padding: 20px;
                font-size: 1.5em;
                font-weight: bold;
                color: white;
                background-color: #4CAF50;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                width: 40%;
                text-align: center;
                text-decoration: none;
                transition: background-color 0.3s ease;
            }
            .btn:hover {
                background-color: #45a049;
            }
            </style>
            <div class="btn-container">
                <a href="#" onclick="document.getElementById('welfare_btn').click();" class="btn">노인 복지시설 정보</a>
                <a href="#" onclick="document.getElementById('jobs_btn').click();" class="btn">노인 일자리 정보</a>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("노인 복지시설 정보", key="welfare_btn"):
                st.session_state.page = 'welfare_facility'

        with col2:
            if st.button("노인 일자리 정보", key="jobs_btn"):
                st.session_state.page = 'senior_jobs'

    # 노인 복지시설 정보 화면
    if st.session_state.page == 'welfare_facility':
        recommend_facilities()

    # 시설 상세 정보 화면 및 북마크 버튼 추가
    if st.session_state.page == 'facility_detail' and not st.session_state.selected_facility.empty:
    # facility detail 화면 처리

        display_facility_detail(st.session_state.selected_facility)

    # 해당 지역 정보 계속 보기 화면
    if st.session_state.page == 'welfare_continue':
        continue_recommendation()
        
        # 일자리 추천 페이지
    if st.session_state.page == 'senior_jobs':
        final_job_main.main()  # final4.py 모듈의 main() 함수 호출

    # 로그아웃
    logout()





# main(2) 코드
# import streamlit as st
# from recommendation import recommend_facilities
# from map_display import display_facility_detail, continue_recommendation
# from session_manager import initialize_session
# from db_connection import create_connection  # MySQL 연결 함수
# from login_system import login
# import time
# import final_job_main # final_job_main 모듈 가져오기

# # 스플래시 화면 설정 - 첫 실행시에만 스플래시 화면을 보여줌
# if 'splash_shown' not in st.session_state:
#     splash = st.empty()
#     image_path = r"라온하제 스플래시 이미지 샘플.jpg"
#     splash.image(image_path, use_column_width=True)
#     splash.markdown("""
#         <div style="display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center;">
#             <h1 style="font-size: 3em; color: #4CAF50;">라온하제: 서울시 노인 복지 서비스 플랫폼</h1>
#         </div>
#     """, unsafe_allow_html=True)
#     time.sleep(3)
#     splash.empty()
#     st.session_state.splash_shown = True

# # 세션 초기화
# initialize_session()

# if 'page' not in st.session_state:
#     st.session_state.page = 'home'

# # 로그인 체크
# if 'nickname' not in st.session_state or st.session_state['nickname'] is None:
#     login()
# else:
#     if st.session_state.page == 'home':
#         st.title(f'라온하제: {st.session_state["nickname"]}님, 오늘보다 즐거운 내일')
#         st.write("아래에서 원하는 서비스를 선택하세요:")

#         st.markdown("""
#             <style>
#             .btn-container {
#                 display: flex;
#                 justify-content: space-around;
#                 margin-top: 30px;
#             }
#             .btn {
#                 padding: 20px;
#                 font-size: 1.5em;
#                 font-weight: bold;
#                 color: white;
#                 background-color: #4CAF50;
#                 border: none;
#                 border-radius: 10px;
#                 cursor: pointer;
#                 width: 40%;
#                 text-align: center;
#                 text-decoration: none;
#                 transition: background-color 0.3s ease;
#             }
#             .btn:hover {
#                 background-color: #45a049;
#             }
#             </style>
#             <div class="btn-container">
#                 <a href="#" onclick="document.getElementById('welfare_btn').click();" class="btn">노인 복지시설 정보</a>
#                 <a href="#" onclick="document.getElementById('jobs_btn').click();" class="btn">노인 일자리 정보</a>
#             </div>
#         """, unsafe_allow_html=True)

#         col1, col2 = st.columns(2)

#         with col1:
#             if st.button("노인 복지시설 정보", key="welfare_btn"):
#                 st.session_state.page = 'welfare_facility'

#         with col2:
#             if st.button("노인 일자리 정보", key="jobs_btn"):
#                 st.session_state.page = 'senior_jobs'

#     # 노인 복지시설 정보 화면
#     if st.session_state.page == 'welfare_facility':
#         recommend_facilities()

#     # 일자리 추천 페이지
#     if st.session_state.page == 'senior_jobs':
#         final4.main()  # final4.py 모듈의 main() 함수 호출

#     # 로그아웃
#     #logout()
