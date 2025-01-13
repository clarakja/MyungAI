import sqlite3
import streamlit as st

# 데이터베이스 초기화 함수
def initialize_database():
    conn = sqlite3.connect('chatbot_scenario.db')
    cursor = conn.cursor()

    # 기존 테이블 삭제
    cursor.execute("DROP TABLE IF EXISTS intents")
    cursor.execute("DROP TABLE IF EXISTS flows")

    # Intent 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Intents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent TEXT NOT NULL,
        response TEXT NOT NULL
    )
    ''')

    # Flows 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Flows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        current_intent INTEGER NOT NULL,
        next_intent INTEGER NOT NULL,
        FOREIGN KEY (current_intent) REFERENCES Intents(id),
        FOREIGN KEY (next_intent) REFERENCES Intents(id)
    )
    ''')

    # 초기 데이터 삽입
    cursor.executemany('''
    INSERT INTO Intents (intent, response)
    VALUES (?, ?)
    ''', [
        ('교과목', '교과목 중 하나를 선택하세요.'),
        ('공통', '국어, 영어, 수학 중 하나를 선택하세요.'),
        ('국어', '국어 교과목에 대한 상세 설명입니다.'),
        ('영어', '영어 교과목에 대한 상세 설명입니다.'),
        ('수학', '수학 교과목에 대한 상세 설명입니다.')
    ])

    cursor.executemany('''
    INSERT INTO Flows (current_intent, next_intent)
    VALUES (?, ?)
    ''', [
        (1, 2),  # 교과목 -> 공통
        (2, 3),  # 공통 -> 국어
        (2, 4),  # 공통 -> 영어
        (2, 5)   # 공통 -> 수학
    ])

    conn.commit()
    conn.close()

# 현재 intent에 따른 응답과 다음 선택지
def get_response(current_intent_id):
    conn = sqlite3.connect('chatbot_scenario.db')
    cursor = conn.cursor()

    # 현재 intent의 응답 가져오기
    cursor.execute("SELECT response FROM Intents WHERE id = ?", (current_intent_id,))
    response = cursor.fetchone()

    # 다음 intent 선택지 가져오기
    cursor.execute("SELECT next_intent FROM Flows WHERE current_intent = ?", (current_intent_id,))
    next_intents = cursor.fetchall()

    conn.close()

    if response:
        return response[0], [intent[0] for intent in next_intents]
    else:
        return "죄송합니다, 이해하지 못했습니다.", []

# Streamlit 챗봇 실행 함수
def chatbot_app():
    st.title("Streamlit 챗봇")

    if 'current_intent_id' not in st.session_state:
        st.session_state['current_intent_id'] = 1  # 초기 Intent ID

    response, next_intents = get_response(st.session_state['current_intent_id'])

    st.write(f"챗봇: {response}")

    if not next_intents:
        st.write("챗봇: 대화가 종료되었습니다. 새로 시작하려면 페이지를 새로고침하세요.")
        return

    user_input = st.text_input("사용자 입력:", "")
    if st.button("전송"):
        for intent_id in next_intents:
            conn = sqlite3.connect('chatbot_scenario.db')
            cursor = conn.cursor()
            cursor.execute("SELECT intent FROM Intents WHERE id = ?", (intent_id,))
            intent_name = cursor.fetchone()[0]
            conn.close()

            if user_input == intent_name:
                st.session_state['current_intent_id'] = intent_id
                st.set_query_params(current_intent_id=intent_id)
                st.experimental_rerun()
                break
        else:
            st.write("챗봇: 이해하지 못했습니다. 다시 시도해주세요.")

# 실행
if __name__ == "__main__":
    initialize_database()  # 데이터베이스 초기화
    chatbot_app()  # Streamlit 앱 실행
