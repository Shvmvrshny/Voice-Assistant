import speech_recognition as sr
import webbrowser
import time
# from time import ctime
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
from twilio.rest import Client
import random


account = "ACXXXXXXXXXXXXXXX"
token = "XXXXXXXXXXXXXXX"
client = Client(account, token)

r = sr.Recognizer()


def speaking(audio_string):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio_string)
    engine.runAndWait()


def recording_you(a=False):
    print('listening')
    with sr.Microphone() as source:
        if(a):
            speaking(a)
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speaking("Sorry! didn't understand that")
        except sr.RequestError:
            speaking('Server down')

        print('recording ' + voice_data)
        return voice_data


text_message_body = ''
action_message = 0


def respond(voice_data):
    print('respond ' + voice_data)

    if 'open' in voice_data:
        search = recording_you('What do you want to search for?')
        url = 'https://google.com/search?q='+search
        webbrowser.get().open(url)

    elif 'location' in voice_data:
        location = recording_you('Name your place!')
        url = 'https://google.nl/maps/place/'+location+'/&amp;'
        webbrowser.get().open(url)
        exit()

    # elif 'what is your name' in voice_data:
    #     speaking('My name is Jarvis')
    #     speaking('what is your name?')

    elif 'play' in voice_data:
        song = voice_data.replace('play', '').replace('on youtube', '')
        speaking('playing ' + song)
        pywhatkit.playonyt(song)
        exit()
    elif 'who is' in voice_data:
        person = voice_data.replace('who is', '')
        speaking(f'searching {person} on wikipedia')
        try:
            info = wikipedia.summary(person)
            speaking(info)
        except:
            speaking(
                'first donate something to wikipedia cause wikipedia is not responding')
            pass

    # elif 'this is' in voice_data or 'my name is' in voice_data or 'i am' in voice_data:
    #     print('hello')
    #     name = voice_data.replace('this is', '').replace(
    #         'my name is', '').replace('i am', '')
    #     speaking(f'Hey there {name}, nice to meet you')
    #     speaking('How can i help you')

    elif 'call' in voice_data:
        if 'me' in voice_data:
            number = '+919315630755'
            call = client.calls.create(to=number,
                                       from_="18166563075", url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
            print(call.sid)
            exit()
        else:

            number = voice_data.replace('call', '')
            call = client.calls.create(
                to=number, from_="18166563075", url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
            print(call.sid)
            exit()

    elif 'message' in voice_data:
        text = voice_data.replace('message', '')
        print(text)
        speaking(text)
        speaking('if you want confirm the message then say yes confirm')
        speaking('to abort the message say abort message')
        global text_message_body
        text_message_body = text

    elif 'yes confirm' in voice_data:
        print(text_message_body)
        message = client.messages.create(to="+919315630755", from_="+18166563075",
                                         body=text_message_body)
    elif 'cancel text' in voice_data:
        speaking('Speak like a robot!')
        global action_message
        action_message = 1

    elif 'joke' in voice_data:
        joke = pyjokes.get_joke(language='en', category='all')
        speaking(joke)

    elif 'love you' in voice_data:
        speaking('I love you too!')
        speaking('but as a friend')

    elif 'bye-bye' or 'bi' or 'bi-bi' in voice_data:
        speaking('ba-bye')
        exit()

    else:
        speaking('Can you repeat that!')


time.sleep(1)

greeting_list = ['What up? My name is Jarvis from Iron man', 'Namaste, how can i help you today?', 'What do you want me to search for?',
                 'I have joke to tell', 'Do want to call somebody?', 'is this the right time to speak?']
ran = random.randint(0, len(greeting_list))
conv_starter = greeting_list[ran]
speaking(conv_starter)
count = 0
while 1:
    if action_message == 1:
        speaking('I can still send a message for you')
    voice_data = recording_you()
    print(voice_data)
    respond(voice_data)
