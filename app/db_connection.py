# import pymysql

# # MySQL connection setup
# def create_connection():
#     connection = pymysql.connect(
#         host='34.47.106.147',  # MySQL 서버 호스트
#         user='root',  # MySQL 사용자 이름
#         password='dkrlrhfo0992!',  # MySQL 비밀번호 (사용 중인 MySQL 비밀번호 입력)
#         database='mulpaas',  # 생성한 데이터베이스 이름 
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     return connection

# import pymysql

# # MySQL connection setup
# def create_connection():
#     connection = pymysql.connect(
#         host='localhost',  # MySQL 서버 호스트
#         user='root',  # MySQL 사용자 이름
#         password='894601',  # MySQL 비밀번호 (사용 중인 MySQL 비밀번호 입력)
#         database='test',  # 생성한 데이터베이스 이름 (이미지는 'test' DB를 사용 중)
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     return connection

# MySQL connection setup
import os
from dotenv import load_dotenv
import pymysql

# .env 파일의 환경 변수를 로드
load_dotenv()

# MySQL connection setup
def create_connection():
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),  # MySQL 서버 호스트
        user=os.getenv('MYSQL_USER'),  # MySQL 사용자 이름
        password=os.getenv('MYSQL_PASSWORD'),  # MySQL 비밀번호
        database=os.getenv('MYSQL_DATABASE'),  # 데이터베이스 이름
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

