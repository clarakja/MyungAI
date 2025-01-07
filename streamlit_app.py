import streamlit as st

# 점수 저장을 위한 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state['score'] = 0

# 점수 업데이트 함수
def update_score():
    st.session_state['score'] += 1

# 제목 표시
st.title("Click Game with Streamlit")

# 점수 표시
st.markdown(f"### Score: {st.session_state['score']}")

# 버튼 클릭 이벤트
if st.button("Click Me!"):
    update_score()

# 게임 초기화 버튼
if st.button("Reset"):
    st.session_state['score'] = 0
