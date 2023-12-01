import streamlit as st
from pymongo import MongoClient
from faker import Faker
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# MongoDB에 연결
client = MongoClient('localhost', 27017)
db = client['user_database']
collection = db['user_collection']

# Faker를 사용하여 100개의 더미 데이터 미리 저장
fake = Faker()
dummy_data = []
for _ in range(100):
    user = {
        'username': fake.user_name(),
        'phone_number': fake.phone_number(),
        'email': fake.email(),
        'timestamp': datetime.now()
    }
    dummy_data.append(user)

# MongoDB에 더미 데이터 저장
collection.insert_many(dummy_data)

# Streamlit 앱 구현
st.title("사용자 정보 업데이트")

# 사용자 입력 폼
username = st.text_input("사용자 이름을 입력하세요:")
phone_number = st.text_input("전화번호를 입력하세요:")
email = st.text_input("이메일을 입력하세요:")

# 이메일 전송 함수
def send_email(receiver_email, body):
    sender_email = "zz10888@naver.com"
    sender_password = "gunhee100^^"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "사용자 정보 업데이트"

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# MongoDB에 사용자 정보 업데이트
if st.button("정보 업데이트"):
    updated_data = {
        'username': username,
        'phone_number': phone_number,
        'email': email,
        'timestamp': datetime.now()
    }
    collection.insert_one(updated_data)

    # 이메일로 업데이트 정보 전송
    send_email(email, f"귀하의 정보가 성공적으로 업데이트되었습니다.\n\n"
                       f"사용자 이름: {username}\n"
                       f"전화번호: {phone_number}\n"
                       f"이메일: {email}")


    st.success("사용자 정보가 업데이트되었으며 이메일이 전송되었습니다!")
    
