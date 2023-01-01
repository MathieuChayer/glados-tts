import speech_recognition as sr
import random
import datetime
import calendar

def greeting(text):
    Greeting_Inputs = ['hi', 'hey', 'hola', 'bonjour', 'hello']
    Greeting_Response = ['hi', 'hey', 'hola', 'greetings', 'bonjour', 'hello']

    for word in text.split():
        if word.lower() in Greeting_Inputs:
            return random.choice(Greeting_Response)
    return ''

def recordAudio():
    r = sr.Recognizer()  # Creating a recognizer object

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print('Say something!')
        audio = r.listen(source)

    # Use google's speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError:  # Checking for unknown errors
        print('Google Speech Recognition could not understand the audio')
    except sr.RequestError as c:
        print('Request results from Google Speech Recognition service error')

    return data

def wakeWord(text):
    WAKE_WORD = ['hi']

    text = text.lower()

    for phrase in WAKE_WORD:
        if phrase in text:
            return True
    return False

def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']

    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th','14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

    return 'Today is ' + weekday + ', ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1]

while True:
    text = recordAudio()
    responses = ''

    if wakeWord(text.lower()) == True:
        try:
            responses = responses + greeting(text)
        except Exception as e:
            responses = responses + ''
        if 'date' in text:
            get_date = getDate()
            responses = responses + ' ' + get_date
        if responses == '':
            responses = responses + "I'm Sorry I Can't Do That Yet"

        print(responses)