import streamlit as st
import requests

# API 엔드포인트 설정
API_URL = "http://localhost:8000/process_customer"

if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.customer_info = {
        'customer_name': None,
        'customer_age' : None,
        'customer_gender': None,
        'customer_address': None,
    }
    st.session_state.page = "INPUT FORM"

if st.button("Start"):
    st.session_state.started = True

def update_page(customer_info):
    # FastAPI 서버로 데이터 전송
    st.markdown("## 원래 정보:")
    st.json(customer_info)
    try:
        response = requests.post(API_URL, json=customer_info)
        if response.status_code == 200:
            processed_info = response.json()
            st.balloons()
            st.markdown("## 처리된 정보:")
            st.json(processed_info)
        else:
            st.error("서버 처리 중 오류가 발생했습니다.")
    except requests.exceptions.RequestException as e:
        st.error(f"서버 연결 오류: {str(e)}")

if st.session_state.started:

    if st.session_state.page == "INPUT FORM":
        st.title("INPUT FORM")
        with st.form(key="customer_info_form"):
            st.text_input("Name", key="customer_name")
            st.number_input("Age", key="customer_age", min_value=18, max_value=1000)
            st.radio("Gender", key="customer_gender", options=["Male", "Female"])
            st.selectbox("Address", key="customer_address", options=["Seoul", "Busan", "Incheon"])
            
            if st.form_submit_button("Submit"):
                # 폼 제출 시 session_state.customer_info 업데이트
                st.session_state.customer_info = {
                    'customer_name': st.session_state.customer_name,
                    'customer_age': st.session_state.customer_age,
                    'customer_gender': st.session_state.customer_gender,
                    'customer_address': st.session_state.customer_address,
                }
                st.session_state.page = "RESULT"
                # 페이지 리로드
                st.rerun()
        
            
    elif st.session_state.page == "RESULT":
        st.title("RESULT")
        update_page(st.session_state.customer_info)
        