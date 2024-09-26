import cv2
import numpy as np
import os
import sqlite3
from PIL import Image


# Trợ lý ảo chuyển text sang giọng nói
# import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import speech_recognition as sr
import time
import datetime
import requests
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from youtube_search import YoutubeSearch
import webbrowser
import re

path = ChromeDriverManager().install()

def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang='vi')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def get_text():
    for i in range(3):
        text = get_voice()
        if text:
            return text.lower()
        elif i < 2:
            speak("Bot không nghe rõ, bạn có thể nói lại không ?")
    time.sleep(10)
    stop()
    return 0

def get_voice():
     r = sr.Recognizer()
     with sr.Microphone() as source:
        print("Me: ", end = '')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0

def stop():
    speak("Hẹn gặp lại bạn nhé!")

# OpenWeatherMap là một dịch vụ trực tuyến, thuộc sở hữu của OpenWeather Ltd, 
# cung cấp dữ liệu thời tiết toàn cầu thông qua API, bao gồm dữ liệu thời tiết hiện tại, 
# dự báo, dự báo và dữ liệu thời tiết lịch sử cho bất kỳ vị trí địa lý nào.
def weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ!")
    time.sleep(3)
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temp = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        sun_time  = data["sys"]
        sun_rise = datetime.datetime.fromtimestamp(sun_time["sunrise"])
        sun_set = datetime.datetime.fromtimestamp(sun_time["sunset"])
        wther = data["weather"]
        weather_des = wther[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day, month = now.month, year= now.year, hourrise = sun_rise.hour, minrise = sun_rise.minute,
                                                                           hourset = sun_set.hour, minset = sun_set.minute, 
                                                                           temp = current_temp, pressure = current_pressure, humidity = current_humidity)
        speak(content)
        time.sleep(25)
    else:
        speak("Không tìm thấy thành phố!")

def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d " % (now.day, now.month, now.year))
    else:
        speak("Bot không hiểu")

def open_website(text):
    reg_ex = re.search('mở (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain + '.com'
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đã được mở.")
        return True
    else:
        return False
def play_song():
    speak('Xin mời bạn chọn tên bài hát')
    mysong = get_text()
    while True:
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    speak("Bài hát bạn yêu cầu đã được mở.")

def help_me():
    speak("""Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    1. Mở website
    2. Hiển thị giờ hiện tại
    3. Hiển thị ngày hiện tại
    4. Hiển thị thời tiết hôm nay
    5. Mở nhạc trên youtube""")
# Trợ lý ảo chuyển text sang giọng nói


#tranning hinh anh nhan dien vs thu vien nhan dien khuon mat
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
face_cascade =cv2.CascadeClassifier('haarcascades/hearcascade_fromtalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('recoginzer/trainingdata.yml')

#get profile by id from database
def getProfile(id):
    conn = sqlite3.connect('D:\\nam 4\\demoo\\hcg_python\\data.db')
    query = "SELECT * FROM people WHERE ID="+ str(id)
    cursor = conn.execute(query)

    profile = None

    for row in cursor:
        profile = row

    conn.close()
    return profile

cap = cv2.VideoCapture(0)

fontface = cv2.FONT_HERSHEY_COMPLEX
while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces :
        cv2.rectangle(frame, (x, y), (x+ w, y+ h) , (0,255,0), 2)

        roi_gray = gray[y: y+h, x: x+w]

        id, confidence = recognizer.predict(roi_gray)

        if confidence< 40:
            profile = getProfile(id)

            if(profile != None):
                cv2.putText(frame, ""+str(profile[id]), (x+ 45, y+h+ 30), fontface, 1, (0,255,0), 2)

                # Trợ lý ảo chuyển text sang giọng nói
                if(((""+str(profile[id])) == 'manh')):
                    speak("Xác thực thành công")
                    speak("Xin chào sếp")
                    speak("Sếp cần Sen giúp gì ạ!")
                    time.sleep(2)
                    while True:
                        text = get_text()
                        if not text:
                            break
                        elif "dừng" in text or "thôi" in text:
                            stop()
                            break
                        if "thời tiết" in text:
                            weather()
                        elif "ngày" in text  or "giờ" in text:
                            get_time(text)
                        elif "mở" in text:
                            open_website(text)
                        elif "chơi nhạc" in text:
                            play_song()
                        elif "chức năng" in text:
                            help_me()
                        
                # Trợ lý ảo chuyển text sang giọng nói
                    
            else:
                cv2.putText(frame, "Unknow", (x+ 45, y+h +30), fontface, 1, (0,0,255), 2)
                speak("NGƯỜI DÙNG NÀY KHÔNG PHẢi SẾP RỒI")
                speak("TRUY CẬP TRÁI PHÉP")
                # speak("TAO BÁO ĐẠI CA ĐÂY")
    cv2.imshow('frame',frame)
    if(cv2.waitKey(1) == ord('q')):
        break;


cap.release()
cv2.destroyAllWindows()