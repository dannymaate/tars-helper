import speech_recognition as sr
import pyttsx3
import datetime
import random
import re
import webbrowser
from weather import *


def onStart(name):
    print('starting...')


def onWord(name, location, length):
    print('word', location, length)


def onEnd(name, completed):
    print('finishing?', completed)


def setupVoice():
    engine = pyttsx3.init(driverName='nsss')
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')

    # set speech properties
    newVoiceRate = 250
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
    engine.setProperty('rate', newVoiceRate)
    engine.setProperty('volume', volume+0.5)

    return engine


def speak(engine, speech):
    # listen to events
    # engine.connect('started-utterance', onStart)
    # engine.connect('started-word', onWord)
    # engine.connect('finished-utterance', onEnd)

    engine.say(speech)
    print(speech)
    engine.runAndWait()


def listen():
    # obtain audio from microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source)
    speechInput = ""

    try:
        speechInput = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + "'" + speechInput + "'")
    except sr.UnknownValueError:
        print("Google Speech could not recognise audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition Service; {0}".format(e))
        return "None"
    return speechInput


def greet(engine):
    hour = datetime.datetime.now().hour
    print(hour)
    twelveHour = hour % 12
    if (hour >= 5) and (hour < 12):
        speak(engine, "Good morning sir")
    elif (hour >= 12) and (hour < 18):
        speak(engine, "Good afternoon sir")
    else:
        speak(
            engine, f"Good evening sir. It is {twelveHour}'o clock at night.")


def whoAmI(engine):
    speak(engine, "Hello sir, I am TARS! I am a program, a helper if you like, developed by Mr D Morgan. My job is to support Mr Morgan in his day to day activities.")


def google(engine, request):
    searchQuery = re.search('google (.*)', request)
    url = 'https://www.google.com/'
    if (searchQuery):
        subQuery = searchQuery.group(1)
        url = url + '/search?q={0}'.format(subQuery)
    webbrowser.open(url)
    print("Done!")

def get_weather_city(engine, request):
    detectedCity = ''
    nonCityWords = ['hey', 'jarvis', 'tars', 'what', 'is', 'the', 'weather', 'in', 'today', 'how', 'tell', 'me', 'forecast', 'for', 'like', 'explain'] # words that aren't likely to be a city
    requestWords = request.split()
    isCityFound = False
    if (len(request.split()) > 1):
        for word in requestWords:
            if word not in nonCityWords:
                detectedCity += ' ' + word
                isCityFound = True
        detectedCity = detectedCity.strip(' ')
    if not isCityFound:
        detectedCity = 'Brisbane'

    print('Detected city for weather... {0}'.format(detectedCity))
    speak(engine, Weather().fetch_weather(detectedCity))


if __name__ == "__main__":
    engine = setupVoice()
    greet(engine)

    errors = [
        "I'm sorry, what do you mean?",
        "Can you repeat that?",
        "I don't understand."
    ]
    commands = [
        "what can you do?",
        "commands",
        "ideas"
    ]
    exit = [
        "goodbye",
        "shutdown",
        "exit"
    ]
    while True:
        request = listen()
        if (request in commands):
            print(
                "Launching websites...\n" +
                " 'google'\n" +
                " 'spotify'\n" +
                " 'youtube'\n" +
                " 'wikipedia'\n\n" +
                "Exiting TARS...\n" +
                " 'goodbye'"
            )
            speak(engine, "I've listed out some useful voice commands")
        if (request in exit):
            speak(engine, "Goodbye sir")
            break
        if ("time" in request):
            speak(engine, "Current time is " +
                  datetime.datetime.now().strftime("%I:%M"))
        if ("google" in request):
            google(engine, request)
        if ("who" in request):
            whoAmI(engine)
        if ("weather" in request):
            get_weather_city(engine, request)
        else:
            speak(engine, random.choice(errors))

    # speak(engine, "Hello sir, I am TARS!")
    # speak(engine, "What would you like to do today?")


# good voice names
# Alex
# milena
# samantha
# tessa
# 150
