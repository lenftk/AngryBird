import requests

content = 'gAAAAABlXosZvk0u7If-S91zKcgkn_SBAKaFB32uPqdci3N1a3rHSdGENCQbbaKqK-2RW2qwXw8XKfAFtR8LTLZ8m-ZDf9yLoKpw8jytVJ3ki4-ox9Rz0oWLQA-VFqOGk_aH-PkPpYCY'
url = "http://localhost:5001/receive"
data = {"content": content}
requests.post(url, json=data)