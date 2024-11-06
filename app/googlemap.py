import streamlit as st
import folium
# from streamlit_folium import st_folium
import requests
import os
from dotenv import load_dotenv
load_dotenv()
# 환경 변수에서 Google API 키 가져오기
google_api_key = os.getenv("GOOGLE_API_KEY")

# Google API 설정에 키 사용 (예시)
# 예를 들어, Google Maps API를 사용할 경우
import googlemaps

gmaps = googlemaps.Client(key=google_api_key)
# Google Maps Geolocation API를 사용하여 현재 위치 가져오기
def get_location_from_google():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={google_api_key}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'location' in data:
            lat = data['location']['lat']
            lon = data['location']['lng']
            accuracy = data.get('accuracy', 'Unknown accuracy')
            return lat, lon, accuracy
        else:
            st.error("API 응답에 위치 정보가 없습니다.")
            return None, None, "위치 정보 없음"
    else:
        st.error(f"API 요청 실패: {response.status_code} - {response.text}")
        return None, None, "API 요청 실패"

# Google Geocoding API를 사용하여 주소를 위도 및 경도로 변환하는 함수
def get_lat_lon_from_address(address):
    google_api_key = "AIzaSyCTFRyZGxrZNq5f5baPE6cxMPG6cj5dJaA"  # 여기에 실제 Google API 키를 넣으세요
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# # 현재 위치 가져오기
# lat, lon, accuracy = get_location_from_google()

# # Folium 지도 생성 및 위치 정보가 없을 때 처리
# if lat is not None and lon is not None:
#     st.write(f"현재 위치: 위도 {lat}, 경도 {lon} (정확도: {accuracy} meters)")
#     m = folium.Map(location=[lat, lon], zoom_start=12)
#     folium.Marker(location=[lat, lon], popup=f"Accuracy: {accuracy} meters", tooltip="현재 위치").add_to(m)
# else:
#     st.write("현재 위치 정보를 가져오지 못했습니다. API 호출에 문제가 있습니다.")
#     m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 기본 위치로 서울 설정

# # Folium 지도를 Streamlit에 표시
# st_folium(m, width=725, height=500)
# Folium 지도 생성 함수 정의

# 현재 위치와 추천된 시설 정보를 지도에 나타내는 함수
def user_map(lat, lon, accuracy, facility_lat=None, facility_lon=None, facility_name=None, facility_address=None):
    if lat is not None and lon is not None:
        # 현재 위치를 중심으로 지도 생성
        m = folium.Map(location=[lat, lon], zoom_start=16)

        # 빨간색 아이콘을 사용하여 현재 위치 마커 생성
        folium.Marker(
            location=[lat, lon],
            popup=f"Accuracy: {accuracy} meters",
            tooltip="현재 위치",
            icon=folium.Icon(color='red')  # 마커 아이콘을 빨간색으로 설정
        ).add_to(m)

        # 추천된 시설이 있는 경우 파란색 마커 추가
        if facility_lat is not None and facility_lon is not None:
            # 파란색 마커로 시설 위치 표시
            folium.Marker(
                location=[facility_lat, facility_lon],
                popup=f"시설명: {facility_name}\n주소: {facility_address}",
                tooltip=f"{facility_name} - {facility_address}",
                icon=folium.Icon(color='blue')  # 마커 아이콘을 파란색으로 설정
            ).add_to(m)
    
    else:
        # 기본 위치로 서울 설정
        m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
    
    return m

#현재위치
# def user_map(lat, lon, accuracy):
#     if lat is not None and lon is not None:
#         m = folium.Map(location=[lat, lon], zoom_start=16)

#         # 빨간색 아이콘을 사용하여 마커 생성
#         folium.Marker(
#             location=[lat, lon],
#             popup=f"Accuracy: {accuracy} meters",
#             tooltip="현재 위치",
#             icon=folium.Icon(color='red')  # 마커 아이콘을 빨간색으로 설정
#         ).add_to(m)
    
#     else:
#         m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 기본 위치로 서울 설정
#     return m

#실패
# # 지도 생성 함수 (시설 목록을 받아 마커 추가)
# def create_map(facilities, keyword_input=None):
#     if facilities is not None:
#         # 초기 지도를 첫 번째 시설의 위치로 생성 (없을 시 서울로 기본 설정)
#         first_lat, first_lon = facilities.iloc[0]['위도'], facilities.iloc[0]['경도']
#         m = folium.Map(location=[first_lat, first_lon], zoom_start=12)

#         # 각 시설에 대한 마커 추가
#         for idx, row in facilities.iterrows():
#             facility_name = row["시설명"]
#             facility_type = row["시설종류명(시설유형)"]
#             latitude = row["위도"]
#             longitude = row["경도"]

#             # 툴팁에 시설명과 시설종류명 표시
#             tooltip_text = f"{facility_name} ({facility_type})"
#             folium.Marker(location=[latitude, longitude],
#                           popup=tooltip_text,
#                           tooltip=tooltip_text,
#                           icon=folium.Icon(color='red')  # 빨간색 마커
#                          ).add_to(m)
#     else:
#         # 시설이 없을 경우 기본 서울 위치 표시
#         m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
    
#     return m