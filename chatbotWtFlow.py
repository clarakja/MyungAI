import sqlite3
import streamlit as st

# 데이터베이스 초기화
def initialize_database():
    conn = sqlite3.connect('chatbot_scenario.db')
    cursor = conn.cursor()
    # 기존 테이블 삭제 (올바른 동작을 위하여 혹시 남아 있을 잔재를 삭제)
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

# 챗봇 실행
def chatbot():
    initialize_database()

    print("안녕하세요! 챗봇입니다. '종료'를 입력하면 대화를 종료합니다.")

    while True:
        current_intent_id = 1  # 시작 Intent

        while True:
            response, next_intents = get_response(current_intent_id)
            print(f"챗봇: {response}")

            user_input = input("사용자: ").strip()
            if user_input == "종료":
                print("챗봇: 안녕히 가세요!")
                return

            if not next_intents:  # 다음 선택지가 없으면 처음으로 돌아감
                print("챗봇: 처음으로 돌아갑니다.")
                break

            # 다음 intent로 이동
            next_intent_found = False
            for intent_id in next_intents:
                conn = sqlite3.connect('chatbot_scenario.db')
                cursor = conn.cursor()
                cursor.execute("SELECT intent FROM Intents WHERE id = ?", (intent_id,))
                intent_name = cursor.fetchone()[0]
                conn.close()

                if user_input == intent_name:
                    current_intent_id = intent_id
                    next_intent_found = True
                    break

            if not next_intent_found:
                print("챗봇: 이해하지 못했습니다. 다시 선택해주세요.")
                continue

# 실행
if __name__ == "__main__":
    chatbot()
