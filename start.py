from urllib.parse import quote
import urllib3
import yaml
import time
import requests
from scrapper import initialize, check

def send(message, token, chat_id):
    message_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={quote(message)}"
    requests.get(message_url)

if __name__ == '__main__':

    with open('info.yaml', 'r') as file:
        info = yaml.safe_load(file)

    send("not değişim kontrol başlatıldı", info['token'], info['chat_id'])

    driver = initialize(info['id'], info['password'], info['url'])
    prev_lessons = []

    while True:
        try:
            status, lessons, changes = check(driver, prev_lessons)
            prev_lessons = lessons

            if status:
                message = ""
                for change in changes:
                    lesson = change[0]
                    exam = change[1]
                    message += f'\nDers: {lesson}, Girilen sınav ve not: {exam} '

                send("not değişimi algılandı: " + message, info['token'], info['chat_id'])
                print("not değişimi algılandı: " + message)
            else:
                print("değişim yok")

        except Exception as exc:
            print(f'hata: {exc}')

        time.sleep(info['interval'])