import streamlit as st
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import matplotlib.pyplot as plt

# 제목
st.title("AI 숫자 분류 체험")
st.write("이 앱은 손글씨 숫자를 인식하는 간단한 인공지능을 보여줍니다.")

# 데이터 로드
digits = load_digits()
X = digits.data
y = digits.target

# 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 사용자 입력: 숫자 선택
st.sidebar.title("테스트할 숫자 선택")
index = st.sidebar.slider("숫자 인덱스", 0, len(X_test) - 1, 0)

# 선택된 숫자 이미지 표시
image = X_test[index].reshape(8, 8)
plt.imshow(image, cmap='gray')
plt.axis('off')
st.pyplot(plt)

# AI 예측 결과
prediction = model.predict([X_test[index]])
st.write(f"AI가 예측한 숫자: **{prediction[0]}**")
st.write(f"정답: **{y_test[index]}**")

# 정확도 표시
accuracy = model.score(X_test, y_test)
st.write(f"모델 정확도: **{accuracy * 100:.2f}%**")
