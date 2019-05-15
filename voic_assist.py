import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
import requests
import json
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

ip_request = requests.get('https://get.geojs.io/v1/ip.json')
my_ip = ip_request.json()['ip'] 
geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
geo_request = requests.get(geo_request_url)
geo_data = geo_request.json()

api_key = "c81a44a49da3f21ace5b83650e623b2e"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
cityname=geo_data['city']
complete_url = base_url + "appid=" + api_key + "&q=" + cityname
response = requests.get(complete_url) 
x = response.json() 
y = x["main"]
current_temperature=y["temp"]-273.15
humidity=y["humidity"]
strTime = datetime.datetime.now().strftime("%H %M %S")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
speak("Hello sir I am your voice assistant ")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour<=11:
        speak("Good morning   Have a great day ahead ")
    elif hour>=12 and hour<=17:
        speak("Good afternoon")
    else:
       speak("Good evening")
    speak("The current time is "+strTime+ "IST")
    speak("Our current location is " +geo_data['city']+ "   with a latitude"+geo_data['latitude']+"and longitude of "+geo_data['longitude'])
    if( current_temperature>=35):
          speak("Today its very hot with the current temperature "+str(current_temperature)+"degree celsius and humidity of"+str(humidity)+"%")
    elif( current_temperature>=20 and current_temperature<=34):
          speak("Today the weather is moderate with the current temperature "+str(current_temperature)+"degree celsius and humidity of"+str(humidity)+"%")
    elif( current_temperature>=10 and current_temperature<=19):
          speak("Today the weather is cool with the current temperature "+str(current_temperature)+"degree celsius and humidity of"+str(humidity)+"%")
    elif(current_temperature<=9):
          speak("Today its very cold with the current temperature "+str(current_temperature)+"degree celsius and humidity of"+str(humidity)+"%")
    speak("How may I help u?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold=2
        r.energy_threshold=500
        audio=r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio,language='en-in')
        print(f"User said:\n"(query))
    except Exception as e:
        print("Say again please")
        return "None"
    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('somitsaha96@gmail.com','password')
    server.sendmail('somitsaha96@gmail.com','to','content')
    server.close()

if __name__=="__main__":
    wishMe()
    if 1:
        query = takeCommand().lower()
        if 'wikipedia' in  query:
           speak('Searching wikipedia.....')
           query = query.replace("wikipedia","")
           results = wikipedia.summary(query,sentences=2)
           speak("According to wikipedia")
           speak(results)
        elif 'open youtube' in query:
           webbrowser.open("youtube.com")
        elif 'open google' in query:
           webbrowser.open("google.com") 
        elif 'play music' in query:
           webbrowser.open("music.youtube.com")
        elif 'send email to somit' in query:
            try:
                speak("what to say?")
                content = takeCommand()
                to = "somitsaha96@gmail.com"
                sendEmail(to, content)
                speak("Email sent")
            except Exception as e:
                print (e)
                speak("Sorry not sent")
        elif 'shut down computer' in query:
            speak("Shutting down computer")
            print("Shutting down computer")
            os.system("shutdown /s /t 1")
        elif 'open calculator' in query:
            os.system('start calc.exe')
        elif 'open ms word' in query:
            os.system("start WinWord.exe")
        elif ' open notepad' in query:
            os.system("start notepad.exe")
        elif ' open computer settings ' in query:
            os.system("start ms-settings:") 
        elif ' quit' in query:
            exit()