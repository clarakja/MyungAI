import sqlite3
import streamlit as st

# 데이터베이스 초기화 함수
def initialize_database():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    # Intent-Response 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Intents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent TEXT UNIQUE NOT NULL,
        response TEXT NOT NULL
    )
    ''')

    # Synonyms 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Synonyms (
        synonym TEXT UNIQUE NOT NULL,
        intent TEXT NOT NULL
    )
    ''')

    # 기본 Intent 데이터 삽입
    intents = [
        ("인사", "안녕하세요! 무엇을 도와드릴까요?"),
        ("작별", "안녕히 가세요! 좋은 하루 되세요."),
        ("날씨", "날씨는 오늘 맑고 기온은 25도입니다."),
        ("도움말", "다음과 같은 질문을 할 수 있어요: 날씨, 인사, 도움말")
    ]
    for intent, response in intents:
        try:
            cursor.execute("INSERT INTO Intents (intent, response) VALUES (?, ?)", (intent, response))
        except sqlite3.IntegrityError:
            pass  # 이미 데이터가 존재하면 무시

    # 동의어 데이터 삽입
    synonyms = [
        ("안녕", "인사"), ("하이", "인사"),  ("안녕하세요", "인사"), ("잘 가", "작별"),
        ("날씨 어때", "날씨"), ("날씨 알려줘", "날씨"), ("오늘 날씨", "날씨"), ("도움", "도움말")
    ]
    for synonym, intent in synonyms:
        try:
            cursor.execute("INSERT INTO Synonyms (synonym, intent) VALUES (?, ?)", (synonym, intent))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

# Intent를 처리하고 응답을 반환하는 함수
def get_response(user_input):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    # 동의어 매핑 검색
    cursor.execute("SELECT intent FROM Synonyms WHERE synonym = ?", (user_input,))
    result = cursor.fetchone()

    # 동의어가 존재하면 intent로 변환
    if result:
        user_intent = result[0]
    else:
        user_intent = user_input  # 동의어 매핑이 없으면 원래 입력 사용

    # Intent에 해당하는 응답 검색
    cursor.execute("SELECT response FROM Intents WHERE intent = ?", (user_intent,))
    response = cursor.fetchone()
    conn.close()

    if response:
        return response[0]
    else:
        return "죄송합니다, 무슨 말씀인지 이해하지 못했어요. 도움말이 필요하면 '도움말'이라고 입력해 주세요."

# Streamlit 애플리케이션 실행
def chatbot_app():
    st.title("데이터베이스 기반 챗봇")

    st.write("안녕하세요! 데이터베이스 기반 챗봇입니다. 아래 입력창에 질문을 입력하세요.")

    # 사용자 입력 받기
    user_input = st.text_input("질문을 입력하세요", "")

    if st.button("전송"):
        if user_input.lower() == "종료":
            st.success("챗봇: 안녕히 가세요!")
        else:
            response = get_response(user_input.lower())
            st.success(f"챗봇: {response}")

# 실행
if __name__ == "__main__":
    initialize_database()  # 데이터베이스 초기화
    chatbot_app()  # Streamlit 앱 실행
