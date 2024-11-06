# 베이스 이미지로 Python 3.9 사용
FROM python:3.9 AS builder

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 앱 파일을 이미지로 복사
COPY app /app

# Streamlit 애플리케이션 실행
CMD ["streamlit", "run", "main2.py"]
