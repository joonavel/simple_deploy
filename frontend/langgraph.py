import streamlit as st
import requests


# API 엔드포인트 설정
API_URL = "http://localhost:8000/llm_workflow"

if "started" not in st.session_state:
    st.session_state.started = True
    st.session_state.thread_id = "1"
    st.session_state.initial_question = 1
    st.session_state.snapshot_values = None
    st.session_state.conversation_history = []

# Streamlit UI
st.title("GPT로 SQL 쿼리 생성기")
user_input = st.text_input("데이터에 대해 질문하세요:")


if st.button("Enter"):
    try:
        response = requests.post(API_URL, json={"user_question": int(user_input),
                                                "initial_question": st.session_state.initial_question,
                                                "thread_id": st.session_state.thread_id,
                                                "last_snapshot_values": st.session_state.snapshot_values})
        if response.status_code == 200:
            processed_info = response.json()
            st.session_state.snapshot_values = processed_info
            ask_user = processed_info["ask_user"]
            st.session_state.initial_question = 0
            if ask_user == 0:
                st.session_state.initial_question = 1
                processed_info["leading_question"] = "정답입니다!"
        else:
            st.error("서버 처리 중 오류가 발생했습니다.")
    except requests.exceptions.RequestException as e:
        st.error(f"서버 연결 오류: {str(e)}")
        
    # response의 전체 내용 확인 (디버깅 목적)
    st.write("Response 전체 내용:")
    st.write(processed_info["leading_question"])

    # 대화 기록에 추가
    st.session_state.conversation_history.append(
        {"question": user_input, "response": processed_info["leading_question"]}
    )

# 대화 기록 표시
st.subheader("대화 기록")
for entry in st.session_state.conversation_history:
    st.write(f"질문: {entry['question']}")
    st.write(f"Response 전체 내용: {entry['response']}")
    