# import streamlit as st
# import pymysql
# from db_connection import create_connection  # DB 연결 함수 임포트

# # 닉네임 중복 확인 함수
# def is_nickname_unique(nickname):
#     connection = create_connection()
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT COUNT(*) FROM users WHERE nickname = %s"
#             cursor.execute(sql, (nickname,))
#             result = cursor.fetchone()
#             return result['COUNT(*)'] == 0  # 닉네임이 존재하지 않으면 True 반환
#     finally:
#         connection.close()

# # 사용자가 본인 닉네임으로 로그인할 수 있도록 하는 함수
# def is_valid_user(nickname, password):
#     connection = create_connection()
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT * FROM users WHERE nickname = %s AND password = %s"
#             cursor.execute(sql, (nickname, password))
#             result = cursor.fetchone()
#             if result:
#                 return result['id']  # 유저의 ID 반환
#             return None
#     finally:
#         connection.close()

# # 새 사용자 저장 함수
# def save_new_user(nickname, password):
#     connection = create_connection()
#     try:
#         with connection.cursor() as cursor:
#             sql = "INSERT INTO users (nickname, password) VALUES (%s, %s)"
#             cursor.execute(sql, (nickname, password))
#         connection.commit()
#         # 새로 저장한 사용자의 ID 가져오기
#         return cursor.lastrowid
#     finally:
#         connection.close()

# # 로그인 함수
# def login():
#     if 'nickname' not in st.session_state:
#         st.session_state['nickname'] = None
#     if 'user_id' not in st.session_state:
#         st.session_state['user_id'] = None

#     st.write("로그인하세요. 닉네임과 비밀번호를 입력해주세요.")
    
#     nickname_input = st.text_input("닉네임 입력", key="nickname_input")
#     password_input = st.text_input("비밀번호 입력", type="password", key="password_input")
    
#     if st.button("로그인"):
#         if nickname_input and password_input:
#             # 세션에 닉네임이 있는 사용자는 동일 닉네임으로 로그인 가능
#             if st.session_state['nickname'] == nickname_input:
#                 st.success(f"환영합니다, {nickname_input}님!")
#             # 닉네임이 처음 사용된다면
#             elif is_nickname_unique(nickname_input):
#                 user_id = save_new_user(nickname_input, password_input)  # 새 사용자 저장
#                 st.session_state['nickname'] = nickname_input
#                 st.session_state['user_id'] = user_id  # 새 사용자 ID 세션에 저장
#                 st.success(f"환영합니다, {nickname_input}님! 닉네임이 등록되었습니다.")
#             # 이미 존재하는 닉네임과 비밀번호가 일치할 경우 로그인
#             else:
#                 user_id = is_valid_user(nickname_input, password_input)
#                 if user_id:
#                     st.session_state['nickname'] = nickname_input
#                     st.session_state['user_id'] = user_id  # 로그인한 사용자 ID 세션에 저장
#                     st.success(f"{nickname_input}님으로 로그인하셨습니다.")
#                 else:
#                     st.error("닉네임 또는 비밀번호가 잘못되었습니다.")

# # 북마크 저장 함수
# def save_bookmark(facility_name, facility_address, facility_type):
#     if 'user_id' not in st.session_state:
#         st.warning("로그인 후 북마크할 수 있습니다.")
#         return
    
#     user_id = st.session_state['user_id']
    
#     connection = create_connection()
#     try:
#         with connection.cursor() as cursor:
#             sql = """
#             INSERT INTO bookmarks (user_id, facility_name, facility_address, facility_type)
#             VALUES (%s, %s, %s, %s)
#             """
#             cursor.execute(sql, (user_id, facility_name, facility_address, facility_type))
#         connection.commit()
#         st.success("북마크가 저장되었습니다!")
#     finally:
#         connection.close()

# # 로그아웃 함수
# def logout():
#     if st.button("로그아웃"):
#         # 세션 초기화
#         for key in list(st.session_state.keys()):
#             del st.session_state[key]  # 세션에 있는 모든 값 삭제
        
#         # 초기 상태로 돌아가기 위해 페이지를 리로드
#         st.experimental_rerun()

# # 메인 앱 로직
# def main():
#     login()  # 로그인 로직 호출

#     # 로그인 상태에서 메인 페이지 표시
#     if 'nickname' in st.session_state and 'user_id' in st.session_state:
#         st.write(f"{st.session_state['nickname']}님, 로그인 중입니다.")
#         st.write("여기에서 서비스를 이용할 수 있습니다.")
        
#         # 예시: 시설 북마크 저장 (실제 데이터로 대체 가능)
#         if st.button("북마크 저장"):
#             save_bookmark("강동노인복지관", "서울 강동구", "요양원")
#     else:
#         st.write("로그인되지 않았습니다. 로그인 후 이용해주세요.")

# # 세션 초기화 및 로그인 처리
# if __name__ == "__main__":
#     main()





import streamlit as st
import pymysql
from db_connection import create_connection  # DB 연결 함수 임포트

# 닉네임 중복 확인 함수
def is_nickname_unique(nickname):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM users WHERE nickname = %s"
            cursor.execute(sql, (nickname,))
            result = cursor.fetchone()
            return result['COUNT(*)'] == 0  # 닉네임이 존재하지 않으면 True 반환
    finally:
        connection.close()

# 사용자가 본인 닉네임으로 로그인할 수 있도록 하는 함수
def is_valid_user(nickname, password):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE nickname = %s AND password = %s"
            cursor.execute(sql, (nickname, password))
            result = cursor.fetchone()
            if result:
                return result['id']  # 유저의 ID 반환
            return None
    finally:
        connection.close()

# 새 사용자 저장 함수
def save_new_user(nickname, password):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (nickname, password) VALUES (%s, %s)"
            cursor.execute(sql, (nickname, password))
        connection.commit()
        # 새로 저장한 사용자의 ID 가져오기
        return cursor.lastrowid
    finally:
        connection.close()

# 로그인 함수
def login():
    if 'nickname' not in st.session_state:
        st.session_state['nickname'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

    st.write("로그인하세요. 닉네임과 비밀번호를 입력해주세요.")
    
    nickname_input = st.text_input("닉네임 입력", key="nickname_input")
    password_input = st.text_input("비밀번호 입력", type="password", key="password_input")
    
    if st.button("로그인"):
        if nickname_input and password_input:
            # 세션에 닉네임이 있는 사용자는 동일 닉네임으로 로그인 가능
            if st.session_state['nickname'] == nickname_input:
                st.success(f"환영합니다, {nickname_input}님!")
            # 닉네임이 처음 사용된다면
            elif is_nickname_unique(nickname_input):
                user_id = save_new_user(nickname_input, password_input)  # 새 사용자 저장
                st.session_state['nickname'] = nickname_input
                st.session_state['user_id'] = user_id  # 새 사용자 ID 세션에 저장
                st.success(f"환영합니다, {nickname_input}님! 닉네임이 등록되었습니다.")
            # 이미 존재하는 닉네임과 비밀번호가 일치할 경우 로그인
            else:
                user_id = is_valid_user(nickname_input, password_input)
                if user_id:
                    st.session_state['nickname'] = nickname_input
                    st.session_state['user_id'] = user_id  # 로그인한 사용자 ID 세션에 저장
                    st.success(f"{nickname_input}님으로 로그인하셨습니다.")
                else:
                    st.error("닉네임 또는 비밀번호가 잘못되었습니다.")

# 북마크 저장 함수
def save_bookmark(facility_name, facility_address, facility_type):
    if 'user_id' not in st.session_state:
        st.warning("로그인 후 북마크할 수 있습니다.")
        return
    
    user_id = st.session_state['user_id']
    
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO bookmarks (user_id, facility_name, facility_address, facility_type)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, facility_name, facility_address, facility_type))
        connection.commit()
        st.success("북마크가 저장되었습니다!")
    finally:
        connection.close()

# 로그아웃 함수
def logout():
    if st.button("로그아웃"):
        # 세션 초기화
        for key in list(st.session_state.keys()):
            del st.session_state[key]  # 세션에 있는 모든 값 삭제
        
        # 초기 상태로 돌아가기 위해 페이지를 리로드
        st.experimental_rerun()

# 메인 앱 로직
def main():
    login()  # 로그인 로직 호출

    # 로그인 상태에서 메인 페이지 표시
    if 'nickname' in st.session_state and 'user_id' in st.session_state:
        st.write(f"{st.session_state['nickname']}님, 로그인 중입니다.")
        st.write("여기에서 서비스를 이용할 수 있습니다.")
        
        # 예시: 시설 북마크 저장 (실제 데이터로 대체 가능)
        if st.button("북마크 저장"):
            save_bookmark("강동노인복지관", "서울 강동구", "요양원")
    else:
        st.write("로그인되지 않았습니다. 로그인 후 이용해주세요.")

# 세션 초기화 및 로그인 처리
if __name__ == "__main__":
    main()