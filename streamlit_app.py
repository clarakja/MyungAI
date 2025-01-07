
#이전 수업 시간에 만들었던 이미지 분류 pkl 파일을 바탕으로 한 이미지 분류 모델을 Streamlit에 올리는 예제 코드
#파일 이름 streamlit_app.py

import streamlit as st
from fastai.vision.all import *
from PIL import Image
import gdown

# Google Drive 파일 ID
file_id = '1NKIhMhUeRC0vPptHwT4it-LMYhamVDyi'

# Google Drive에서 파일 다운로드 함수
@st.cache(allow_output_mutation=True)
def load_model_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    gdown.download(url, output, quiet=False)

    # Fastai 모델 로드
    learner = load_learner(output)
    return learner

# 모델 로드
st.write("모델을 로드 중입니다. 잠시만 기다려주세요...")
learner = load_model_from_drive(file_id)
st.success("모델이 성공적으로 로드되었습니다!")

# 모델의 분류 라벨 출력
labels = learner.dls.vocab
#st.write(labels)
st.title(f"이미지 분류기 (Fastai) - 분류 라벨: {', '.join(labels)}")

# 파일 업로드 컴포넌트 (jpg, png, jpeg, webp, tiff 지원)
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg", "webp", "tiff"])

if uploaded_file is not None:
    # 업로드된 이미지 보여주기
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_column_width=True)

    # Fastai에서 예측을 위해 이미지를 처리
    img = PILImage.create(uploaded_file)

    # 예측 수행
    prediction, _, probs = learner.predict(img)

    # 결과 출력
    st.write(f"예측된 클래스: {prediction}")


    # 클래스별 확률을 HTML과 CSS로 시각화
    st.markdown("클래스별 확률:", unsafe_allow_html=True)

    # if prediction == labels[0]:
    #     st.write("중냉 꿋굿")
    # elif prediction == labels[1]:
    #     st.write("짜장면은 굿")
    # elif prediction == labels[2]:
    #     st.write("짬뽕은 맵지만 맛있어!!")

    for label, prob in zip(labels, probs):
        # HTML 및 CSS로 확률을 시각화
        st.markdown(f"""
            
                {label}:
                
                    
                        {prob:.4f}
                    
                
            
        """, unsafe_allow_html=True)



     
나의 pkl 파일 주소 설정해서 나만의 모델이 인터넷에 올라가고 작동하는지 확인하기!

#나의 Pkl파일을 올려서 나만의 모델 확인하기
#파일 이름 streamlit_app.py

import streamlit as st
from fastai.vision.all import *
from PIL import Image
import gdown

# Google Drive 파일 ID (여기에 나의 pkl 파일의 id 집어넣어야 동작함!!!!!!!!!!!!!)
file_id = ''

# Google Drive에서 파일 다운로드 함수
@st.cache(allow_output_mutation=True)
def load_model_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    gdown.download(url, output, quiet=False)

    # Fastai 모델 로드
    learner = load_learner(output)
    return learner

# 모델 로드
st.write("모델을 로드 중입니다. 잠시만 기다려주세요...")
learner = load_model_from_drive(file_id)
st.success("모델이 성공적으로 로드되었습니다!")

# 모델의 분류 라벨 출력
labels = learner.dls.vocab
st.write(labels)
st.title(f"이미지 분류기 (Fastai) - 분류 라벨: {', '.join(labels)}")

# 파일 업로드 컴포넌트 (jpg, png, jpeg, webp, tiff 지원)
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg", "webp", "tiff"])

if uploaded_file is not None:
    # 업로드된 이미지 보여주기
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_column_width=True)

    # Fastai에서 예측을 위해 이미지를 처리
    img = PILImage.create(uploaded_file)

    # 예측 수행
    prediction, _, probs = learner.predict(img)

    # 결과 출력
    st.write(f"예측된 클래스: {prediction}")


    # 클래스별 확률을 HTML과 CSS로 시각화
    st.markdown("클래스별 확률:", unsafe_allow_html=True)

    # if prediction == labels[0]:
    #     st.write("중냉 꿋굿")
    # elif prediction == labels[1]:
    #     st.write("짜장면은 굿")
    # elif prediction == labels[2]:
    #     st.write("짬뽕은 맵지만 맛있어!!")

    for label, prob in zip(labels, probs):
        # HTML 및 CSS로 확률을 시각화
        st.markdown(f"""
            
                {label}:
                
                    
                        {prob:.4f}
                    
                
            
        """, unsafe_allow_html=True)



     
분류 결과와 이미지 영상 텍스트 보여주기!

#분류 결과 + 이미지 + 영상 + 텍스트 보여주기
#파일 이름 streamlit_app.py

import streamlit as st
from fastai.vision.all import *
from PIL import Image
import gdown

# Google Drive 파일 ID
file_id = '1NKIhMhUeRC0vPptHwT4it-LMYhamVDyi'

# Google Drive에서 파일 다운로드 함수
@st.cache(allow_output_mutation=True)
def load_model_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    gdown.download(url, output, quiet=False)

    # Fastai 모델 로드
    learner = load_learner(output)
    return learner

def display_left_content(image, prediction, probs, labels):
    st.write("### 왼쪽: 기존 출력 결과")
    if image is not None:
        st.image(image, caption="업로드된 이미지", use_column_width=True)
    st.write(f"예측된 클래스: {prediction}")
    st.markdown("클래스별 확률:", unsafe_allow_html=True)
    for label, prob in zip(labels, probs):
        st.markdown(f"""
            
                {label}:
                
                    
                        {prob:.4f}
                    
                
        """, unsafe_allow_html=True)

def display_right_content(labels):
    st.write("### 오른쪽: 동적 분류 결과")
    cols = st.columns(3)

    # 1st Row - Images based on labels
    for i, label in enumerate(labels[:3]):
        with cols[i]:
            st.image(f"https://via.placeholder.com/150?text={label}", caption=f"이미지: {label}", use_column_width=True)

    # 2nd Row - YouTube Videos based on labels
    for i, label in enumerate(labels[:3]):
        with cols[i]:
            st.video("https://www.youtube.com/watch?v=3JZ_D3ELwOQ", start_time=0)
            st.caption(f"유튜브: {label}")

    # 3rd Row - Text based on labels
    for i, label in enumerate(labels[:3]):
        with cols[i]:
            st.write(f"{label} 관련 텍스트 내용입니다.")

# 모델 로드
st.write("모델을 로드 중입니다. 잠시만 기다려주세요...")
learner = load_model_from_drive(file_id)
st.success("모델이 성공적으로 로드되었습니다!")

labels = learner.dls.vocab

# 레이아웃 설정
left_column, right_column = st.columns(2)

# 파일 업로드 컴포넌트 (jpg, png, jpeg, webp, tiff 지원)
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg", "webp", "tiff"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = PILImage.create(uploaded_file)
    prediction, _, probs = learner.predict(img)

    with left_column:
        display_left_content(image, prediction, probs, labels)

    with right_column:
        display_right_content(labels)

     
분류 결과 + 이미지 + 텍스트와 함께 분류 결과에 따라 다른 출력 보여주기!!!

#분류 결과 + 이미지 + 텍스트와 함께 분류 결과에 따라 다른 출력 보여주기
#파일 이름 streamlit_app.py
import streamlit as st
from fastai.vision.all import *
from PIL import Image
import gdown

# Google Drive 파일 ID
file_id = '1NKIhMhUeRC0vPptHwT4it-LMYhamVDyi'

# Google Drive에서 파일 다운로드 함수
@st.cache(allow_output_mutation=True)
def load_model_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    gdown.download(url, output, quiet=False)

    # Fastai 모델 로드
    learner = load_learner(output)
    return learner

def display_left_content(image, prediction, probs, labels):
    st.write("### 왼쪽: 기존 출력 결과")
    if image is not None:
        st.image(image, caption="업로드된 이미지", use_column_width=True)
    st.write(f"예측된 클래스: {prediction}")
    st.markdown("클래스별 확률:", unsafe_allow_html=True)
    for label, prob in zip(labels, probs):
        st.markdown(f"""
            
                {label}:
                
                    
                        {prob:.4f}
                    
                
        """, unsafe_allow_html=True)

def display_right_content(prediction, data):
    st.write("### 오른쪽: 동적 분류 결과")
    cols = st.columns(3)

    # 1st Row - Images
    for i in range(3):
        with cols[i]:
            st.image(data['images'][i], caption=f"이미지: {prediction}", use_column_width=True)
    # 2nd Row - YouTube Videos
    for i in range(3):
        with cols[i]:
            st.video(data['videos'][i])
            st.caption(f"유튜브: {prediction}")
    # 3rd Row - Text
    for i in range(3):
        with cols[i]:
            st.write(data['texts'][i])

# 모델 로드
st.write("모델을 로드 중입니다. 잠시만 기다려주세요...")
learner = load_model_from_drive(file_id)
st.success("모델이 성공적으로 로드되었습니다!")

labels = learner.dls.vocab

# 스타일링을 통해 페이지 마진 줄이기
st.markdown("""
    
    """, unsafe_allow_html=True)

# 분류에 따라 다른 콘텐츠 관리
content_data = {
    labels[0]: {
        'images': [
            "https://via.placeholder.com/300?text=Label1_Image1",
            "https://via.placeholder.com/300?text=Label1_Image2",
            "https://via.placeholder.com/300?text=Label1_Image3"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
            "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
            "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"
        ],
        'texts': [
            "Label 1 관련 첫 번째 텍스트 내용입니다.",
            "Label 1 관련 두 번째 텍스트 내용입니다.",
            "Label 1 관련 세 번째 텍스트 내용입니다."
        ]
    },
    labels[1]: {
        'images': [
            "https://via.placeholder.com/300?text=Label2_Image1",
            "https://via.placeholder.com/300?text=Label2_Image2",
            "https://via.placeholder.com/300?text=Label2_Image3"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
            "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
            "https://www.youtube.com/watch?v=2Vv-BfVoq4g"
        ],
        'texts': [
            "Label 2 관련 첫 번째 텍스트 내용입니다.",
            "Label 2 관련 두 번째 텍스트 내용입니다.",
            "Label 2 관련 세 번째 텍스트 내용입니다."
        ]
    },
    labels[2]: {
        'images': [
            "https://via.placeholder.com/300?text=Label3_Image1",
            "https://via.placeholder.com/300?text=Label3_Image2",
            "https://via.placeholder.com/300?text=Label3_Image3"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
            "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
            "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"
        ],
        'texts': [
            "Label 3 관련 첫 번째 텍스트 내용입니다.",
            "Label 3 관련 두 번째 텍스트 내용입니다.",
            "Label 3 관련 세 번째 텍스트 내용입니다."
        ]
    }
}

# 레이아웃 설정
left_column, right_column = st.columns([1, 2])  # 왼쪽과 오른쪽의 비율 조정

# 파일 업로드 컴포넌트 (jpg, png, jpeg, webp, tiff 지원)
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg", "webp", "tiff"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = PILImage.create(uploaded_file)
    prediction, _, probs = learner.predict(img)

    with left_column:
        display_left_content(image, prediction, probs, labels)

    with right_column:
        # 분류 결과에 따른 콘텐츠 선택
        data = content_data.get(prediction, {
            'images': ["https://via.placeholder.com/300"] * 3,
            'videos': ["https://www.youtube.com/watch?v=3JZ_D3ELwOQ"] * 3,
            'texts': ["기본 텍스트"] * 3
        })
        display_right_content(prediction, data)

