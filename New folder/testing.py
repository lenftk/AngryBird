from cryptography.fernet import Fernet

# 랜덤 키 생성
def generate_random_key():
    key = Fernet.generate_key()
    return key

# 메시지 암호화
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# 랜덤 키 생성
key = generate_random_key()

# 메시지 암호화
message = "나랑 놀러갈래?"
encrypted_message = encrypt_message(message, key)

# 암호화된 데이터를 파일로 저장
with open("encrypted_data.bin", "wb") as f:
    f.write(encrypted_message)

# 랜덤 키를 파일로 저장
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)