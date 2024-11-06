import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import openai
import re
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 설정에 키 사용
import openai
openai.api_key = openai_api_key

# 임베딩 로드 함수
def load_embeddings(filename):
    try:
        embeddings = np.load(filename)
        return embeddings
    except Exception as e:
        st.error(f"임베딩 로드 중 오류 발생: {e}")
        return None

def cosine_similarity(a, b):
    """코사인 유사도 계산 함수"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def extract_keywords_with_gpt(user_input):
    """GPT 모델을 사용해 '구 정보'와 '직업 관련 단어'만 추출"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.3,
        messages=[
            {"role": "system", "content": "너는 한국어 사용자의 질문에서 '구 정보'와 '직업 관련 단어'만 남기고 불필요한 단어는 모두 제거하는 AI입니다. 예를 들어, 질문에 '서초구 일자리 알려줘'라고 입력되면 '서초구 일자리'만 남기고 '알려줘' 같은 단어는 제거해야 합니다."},
            {"role": "user", "content": f"사용자의 질문: {user_input}\n\n이 질문에서 '구 정보'와 '직업 관련 단어'만 남기고 나머지 불필요한 단어를 제거해 주세요."}
        ]
    )
    keywords = response['choices'][0]['message']['content'].strip()
    return keywords

def get_jobs(query, df_jobs, embeddings, top_k=3):
    """사용자 질문에 따른 직업 검색: 지역 필터링 후 텍스트 및 유사도 검색"""

    # 상태 메시지용 임시 공간 생성
    status_message = st.empty()
    status_message.info("답변을 생성 중입니다. 잠시만 기다려주세요...")

    # 1. 키워드 추출
    keywords = extract_keywords_with_gpt(query)
    keyword_list = keywords.split()  # 키워드를 단어별로 분리
    
    # 2. 텍스트 기반 검색: address에서 키워드의 일부라도 포함된 행 필터링
    text_matches = df_jobs[df_jobs['address'].apply(lambda x: any(kw in str(x) for kw in keyword_list))]
    
    if not text_matches.empty:
        # 작업 완료 직전에 상태 메시지를 제거
        status_message.empty()
        return text_matches.head(top_k)

    # 3. 텍스트 기반 검색 결과가 없을 경우, 임베딩 유사도 검색 수행
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    query_embedding = model.encode([keywords])[0]

    # 코사인 유사도 계산
    similarities = [cosine_similarity(query_embedding, emb) for emb in embeddings]

    # 유사도 기준으로 내림차순 정렬
    df_jobs['similarity'] = similarities
    similar_jobs = df_jobs.sort_values(by='similarity', ascending=False).head(top_k)

    if similar_jobs.empty:
        # 유사한 직업이 없을 경우 경고 메시지 표시
        status_message.warning("유사한 직업을 찾을 수 없습니다.")
        return pd.DataFrame()
    
    # 작업 완료 직전에 상태 메시지를 제거
    status_message.empty()
    return similar_jobs


def classify_query(user_input):
    """GPT 모델을 사용하여 질문의 유형을 판단합니다."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.3,  # 자유도 낮추기
        messages=[
            {"role": "system", "content": "당신은 사용자의 질문이 일자리 관련 질문인지, 아니면 일반적인 대화인지 분류하는 전문가입니다."},
            {"role": "user", "content": f"사용자의 질문: {user_input}\n\n이 질문이 일자리 관련인지, 일반적인 대화인지 판단해 주세요."}
        ]
    )
    classification = response['choices'][0]['message']['content'].strip().lower()
    return "일자리" in classification

def generate_answer(context, user_input, is_job_related):
    """GPT 모델을 사용하여 답변 생성"""
    if is_job_related:
        system_content = "당신은 노인에게 일자리 정보를 친절히 알려주는 챗봇입니다."
        user_content = f"사용자의 질문: {user_input}\n\n관련 정보: {context}\n\n이 정보를 바탕으로 답변을 작성해 주세요."
    else:
        system_content = "당신은 노인과 대화를 나눌 수 있는 친근한 AI입니다. 일자리 관련 대화로 이끌어주세요."
        user_content = f"사용자의 질문: {user_input}\n\n이 질문에 대해 대화를 나눠 주세요."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.3,  # 자유도 낮추기
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    st.title("노인 일자리 추천 챗봇")

    # 초기 멘트를 대화 기록에 추가
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 저는 일자리를 추천해드리는 챗봇입니다. 저에게 일자리 관련 정보를 질문해보세요! 다음과 같이 질문할 수 있습니다. 예) 노원구 일자리 알려줘. 주방 보조원을 하고싶어."}]

    def print_history():
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def add_history(role, content):
        st.session_state["messages"].append({"role": role, "content": content})

    # 대화 내용 초기화 버튼
    if st.button("대화내용 초기화"):
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 저는 일자리를 추천해드리는 챗봇입니다. 저에게 일자리 관련 정보를 질문해보세요! 다음과 같이 질문할 수 있습니다. 예) 노원구 일자리 알려줘. 주방 보조원을 하고싶어."}]

    print_history()

    # 데이터 및 임베딩 로드
    df_jobs = pd.read_excel('final_jobs.xlsx')
    embeddings = load_embeddings("final_embeddings.npy")
    if embeddings is None:
        return  # 임베딩 로드에 실패한 경우 종료

    # 사용자 입력 처리
    if user_input := st.chat_input():
        add_history("user", user_input)
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            chat_container = st.empty()

            try:
                # GPT를 사용하여 질문의 유형을 분류
                is_job_related = classify_query(user_input)

                if is_job_related:
                    # 직업 검색 수행
                    similar_jobs = get_jobs(user_input, df_jobs, embeddings)

                    if not similar_jobs.empty:
                        # apply_number 열을 포함하여 출력
                        context = similar_jobs[['title', 'category', 'address', 'pay', 'detail', 'apply_number']].fillna("공백").to_string(index=False)

                        # GPT 답변 1개 출력
                        final_answer = generate_answer(context, user_input, is_job_related)
                        chat_container.markdown(final_answer)

                        add_history("assistant", final_answer)
                    else:
                        st.warning("관련 데이터를 찾지 못했습니다.")
                else:
                    # 일상적인 대화 처리
                    final_answer = generate_answer("", user_input, is_job_related)
                    chat_container.markdown(final_answer)
                    add_history("assistant", final_answer)

            except Exception as e:
                st.error(f"API 호출 중 오류 발생: {e}")

# Streamlit 앱 실행
if __name__ == "__main__":
    main()