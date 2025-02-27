# 노인들을 위한 웹 개발 - 라온하제

급속한 인구 고령화와 노인 빈곤이 심각한 사회적 문제로 대두되고 있으며, 특히 고립된 생활을 하거나 고독사에 이르는 노인 수가 크게 증가하고 있습니다. 
디지털 활용 능력이 낮은 고령층은 일자리가 있더라도 이를 찾고 구직하는 데 어려움을 겪고 있습니다.<br><br>



이러한 사회 문제를 해결하는 데 조금이나마 기여하고자, 본 팀은 ‘라온하제’라는 플랫폼을 기획했습니다.<br> 

**본 플랫폼은 서울시 노인들에게 적합한 시니어 맞춤형 일자리 및 복지시설을 추천하는 서비스 웹 애플리케이션입니다.**<br> 

사용자의 지역 정보와 요구 사항에 맞는 일자리 및 복지 시설을 추천하며, 사용자는 챗봇과의 대화를 통해 쉽게 정보를 검색할 수 있습니다.


---

### 스플래시 화면 및 로그인 화면
![image](https://github.com/user-attachments/assets/5fc059f7-d224-452e-a1c8-433bf3380d3e)

![image](https://github.com/user-attachments/assets/cb0b0a8a-75c5-45f3-a0bc-5098bd62d170)




### 메인 서비스 페이지
![image](https://github.com/user-attachments/assets/d0902aff-a560-48c1-9f86-1375ff8e6aa2)

### 노인 복지시설 정보 페이지
- 사용자가 주소와 키워드(치매, 경로당, 노인교실, 노인복지관 등)를 입력
- 사용자가 입력한 키워드와 시설 정보(combined_text) 간의 유사도를 Fuzzy Matching으로 비교
- TF-IDF를 사용해 문장을 벡터화하고, 사용자 입력 키워드와 시설 정보의 유사도를 코사인 유사도로 계산
- 유사도가 높은 상위 3개 시설을 추천
- 사용자가 시설을 선택하면 상세 정보를 표시
- Google Maps API로 지도를 활용하고 folium으로 현재위치(빨강마커)와 복지 시설 위치(파랑마커)를 표시
<br>

![image](https://github.com/user-attachments/assets/b9f81e4f-512e-4e14-a39c-e1696d32be5a)
![image](https://github.com/user-attachments/assets/dff59c39-e9ec-4fc1-9e8d-e6ed4411d889)

![image](https://github.com/user-attachments/assets/c24cfd83-e76c-45ac-ace1-4ccdf2ce5000)

<br><br>

---

### 노인 일자리 추천 챗봇
- GPT-4를 사용하여 사용자의 질문에서 "구 정보"와 "일자리 관련 키워드"만 추출
- 텍스트 기반 검색("구 정보"와 일치하는 행을 우선 필터링)
- 사용자가 입력한 문장을 SentenceTransformer을 통해 벡터화
- 사전 계산된 final_embeddings.npy(일자리 정보 벡터)와 코사인 유사도 계산 
- GPT-4를 사용하여 최종 응답 생성

<br>

![image](https://github.com/user-attachments/assets/b01de011-32e3-4441-ba54-b1462f6b72b7)

![image](https://github.com/user-attachments/assets/a78ab706-f404-46cb-a19b-5a3db5d4c9b0)



