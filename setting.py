import tkinter as tk
from tkinter import ttk
import csv
import sys

def is_valid_contact(contact):
    # 보호자 연락처가 숫자로만 이루어져 있는지 확인
    return contact.isdigit()

def is_valid_name(name):
    # 이름이 글자로만 이루어져 있는지 확인
    return name.isalpha()

def save_user_info():
    user_name = user_name_entry.get()
    guardian_name = guardian_name_entry.get()
    guardian_contact = guardian_contact_entry.get()

    if not is_valid_contact(guardian_contact):
        result_label.config(text="보호자 연락처는 숫자로만 입력해야 합니다.")
    elif not is_valid_name(user_name) or not is_valid_name(guardian_name):
        result_label.config(text="이름은 글자로만 입력해야 합니다.")
    else:
        with open('user_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User Name', 'Guardian Name', 'Guardian Contact'])
            writer.writerow([user_name, guardian_name, guardian_contact])

        result_label.config(text="유저 정보가 user_data.csv 파일에 추가되었습니다.")
        root.quit()

root = tk.Tk()
root.title("유저 정보 입력")

user_name_label = ttk.Label(root, text="유저 이름:")
user_name_label.grid(row=0, column=0)
user_name_entry = ttk.Entry(root)
user_name_entry.grid(row=0, column=1)

guardian_name_label = ttk.Label(root, text="보호자 이름:")
guardian_name_label.grid(row=1, column=0)
guardian_name_entry = ttk.Entry(root)
guardian_name_entry.grid(row=1, column=1)

guardian_contact_label = ttk.Label(root, text="보호자 연락처:")
guardian_contact_label.grid(row=2, column=0)
guardian_contact_entry = ttk.Entry(root)
guardian_contact_entry.grid(row=2, column=1)

save_button = ttk.Button(root, text="정보 저장", command=save_user_info)
save_button.grid(row=3, column=0, columnspan=2)

result_label = ttk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()

sys.exit()