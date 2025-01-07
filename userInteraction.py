import streamlit as st
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import cv2
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# 제목
st.title("AI 숫자 분류 체험")
st.write("직접 숫자를 그려보세요, AI가 어떤 숫자인지 예측합니다!")

# 데이터 로드 및 모델 학습
digits = load_digits()
X = digits.data
y = digits.target

# 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 그림 캔버스 생성
st.markdown("### 캔버스에 숫자를 그려보세요!")
canvas_result = st_canvas(
    fill_color="rgb(255, 255, 255)",  # 캔버스 배경색
    stroke_width=10,  # 선 두께
    stroke_color="rgb(0, 0, 0)",  # 선 색
    background_color="rgb(255, 255, 255)",  # 배경색
    width=200,
    height=200,
    drawing_mode="freedraw",
    key="canvas",
)

# 예측 실행
if canvas_result.image_data is not None:
    # 캔버스 이미지 데이터를 8x8 크기로 변환
    img = canvas_result.image_data[:, :, 0]  # Grayscale로 변환
    img_resized = cv2.resize(img, (8, 8), interpolation=cv2.INTER_AREA)
    img_resized = 255 - img_resized  # 색 반전 (검정=0, 흰색=255)
    img_rescaled = img_resized / 16.0  # 값 스케일링 (0~16 범위)

    # 이미지 출력
    st.markdown("### 입력된 숫자:")
    st.image(img_resized, width=100)

    # AI 예측
    prediction = model.predict([img_rescaled.flatten()])
    st.markdown(f"### AI가 예측한 숫자: **{prediction[0]}**")

# 학습된 모델 정확도 표시
accuracy = model.score(X_test, y_test)
