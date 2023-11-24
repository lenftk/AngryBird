from flask import Flask, render_template, request, jsonify
import openai
import requests
from cryptography.fernet import Fernet
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# 랜덤 키 생성
def generate_random_key():
    key = Fernet.generate_key()
    return key

# 메시지 암호화
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

app = Flask(__name__)

# OpenAI API 키 설정
api_key = "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"

# Flask 애플리케이션에서 openai 모듈사용
openai.api_key = api_key


conversation_history = []

# dialogue.py로 대화 내용을 보내는 함수
def send_to_dialogue(content):
    url = "http://localhost:1557/receive"
    
    # 바이트 데이터를 문자열로 변환
    content_str = content.decode('utf-8')
    
    data = {"content": content_str}
    requests.post(url, json=data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        user_input = request.form['user_input']
    except KeyError:
        return jsonify({'message': "사용자 입력이 없습니다."})
    
    if user_input == "잘 가":
        response = "챗봇: 안녕히 가세요!"
    else:
        conversation_history.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        chatbot_response = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": chatbot_response})
        
        # 대화 내용을 dialogue.py로 보냄
        # 랜덤 키 생성
        key = generate_random_key()

        # 메시지 암호화
        message = user_input
        encrypted_message = encrypt_message(message, key)

        # 랜덤 키를 파일로 저장
        with open("encryption_key.key", "wb") as key_file:
            key_file.write(key)

        send_to_dialogue(encrypted_message)
        
    return jsonify({'message': chatbot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
