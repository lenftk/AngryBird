from flask import Flask, request, jsonify, render_template
from konlpy.tag import Komoran
from sentence_transformers import SentenceTransformer, util
from cryptography.fernet import Fernet, InvalidToken
import csv
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# 메시지 복호화 함수
def decrypt_message(encrypted_message, key):
    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message
    except InvalidToken as e:
        print("에러 발생: 복호화 실패 - 잘못된 키 또는 데이터입니다.")
        return None



user_name = None

with open('user_data.csv', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        user_name = row['User Name']

komoran = Komoran()



# SentenceTransformers 모델 로드
model = SentenceTransformer("distiluse-base-multilingual-cased")

app = Flask(__name__)

# 그래프에 사용할 데이터
graph_data = {"user_input": "", "similarities": []}

# Flask 애플리케이션이 시작될 때 초기화
@app.before_first_request
def before_first_request():
    global graph_data
    # 초기 가상 데이터 설정
    graph_data = {"user_input": "virtual sentence", "similarities": [0, 0, 0, 0]}


# app.py에서 대화 내용을 받아서 처리
@app.route('/receive', methods=['POST'])
def receive():
    global graph_data

    data = request.json

    # 암호화 된 데이터 가져오기
    encrypted_data = data.get('content')

    # 랜덤 키를 파일로부터 읽어옴
    with open("encryption_key.key", "rb") as key_file:
        key = key_file.read()

    # 메시지 복호화 시도
    decrypted_message = decrypt_message(encrypted_data, key)

    if decrypted_message is not None:
        print("복호화된 메시지:", decrypted_message)
        content = decrypted_message
    else:
        print("복호화 실패. 에러가 발생했습니다.")


    # 문장과 단어와의 유사도 비교
    test_sentence = content
    test_words = ["연락처", "놀러가자", "사귈래", "사진"]

    # 문장 토큰화
    sentence_tokens = komoran.morphs(test_sentence)

    # 문장 임베딩 생성
    sentence_embedding = model.encode(test_sentence, convert_to_tensor=True)

    similarities = []
    for word in test_words:
        # 단어 임베딩 생성
        word_embedding = model.encode(word, convert_to_tensor=True)

        # 코사인 유사도 계산
        cosine_score = util.pytorch_cos_sim(sentence_embedding, word_embedding)

        # 백분율로 변환하여 출력
        similarity_percentage = (cosine_score.item() + 1) * 50  # [0, 100] 범위로 변환
        print(f"단어 '{word}'와 문장 '{test_sentence}' 간의 유사도: {similarity_percentage:.2f}%")
        similarities.append(similarity_percentage)

        if similarity_percentage >= 80:
                send_capture_request(test_sentence, user_name)

    graph_data = {"user_input": test_sentence, "similarities": similarities}
    return jsonify({'message': "received"})

def send_capture_request(captured_sentence, user_name):
    print(user_name, "아동의 대화 중에 의심되는 문장", captured_sentence, "가 나왔습니다. 어린이와 천천히 대화를 잘 해보세요")


# 그래프 데이터
@app.route('/get_graph_data', methods=['GET'])
def get_graph_data():
    global graph_data
    return jsonify(graph_data)

# HTML 페이지를 렌더링
@app.route('/', methods=['GET'])
def index():
    return render_template('graph.html', user_input=graph_data['user_input'], similarities=graph_data['similarities'])

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
