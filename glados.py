import torch
from utils.tools import prepare_text
from scipy.io.wavfile import write
import time
from sys import modules as mod
try:
    import winsound
except ImportError:
    from subprocess import call
import requests
import datetime as dt
from random import *
import json
import random
import calendar
import webbrowser
import wikipedia

def get_time():
    timer = dt.datetime.now()
    hour = timer.strftime('%H')
    minute = timer.strftime('%M')
    second = timer.strftime('%S')

    print("Time : " + hour + ":" + minute + ":" + second)

    r = randint(1, 4)

    if r == 1:
        speak("The current time is " + hour + " " + minute + "and" + second + "seconds. ")
    elif r == 2:
        speak("Its " + hour + " " + minute + "and" + second + "seconds. ")
    elif r == 3:
        speak("its currently " + hour + " " + minute + "and" + second + "seconds. ")
    elif r == 4:
        speak("The time is " + hour + " " + minute + "and" + second + "seconds. ")

def get_date():
    now = dt.datetime.now()
    my_date = dt.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day
    yearNum = now.year
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th','14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

    text = 'Today is ' + weekday + ', ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + " " + str(yearNum)

    r = randint(1, 4)

    if r == 1:
        text = text + " "
    elif r == 2:
        text = text + "\nEnjoy the days you have left !  "
    elif r == 3:
        text = text + "\nCarpe Diem...Or as I prefer saying, Memento Mori, remember that you WILL die."
    elif r == 4:
        text = text + "\nOr did you want me to start counting from the human extinction? "

    print(text)
    speak(text)

def get_webpage(input_str):

    text = ""

    if "google" in input_str:
        page = 'https://www.google.ca'
    elif "netflix" in input_str:
        page = 'https://www.netflix.com'
    elif "youtube" in input_str:
        page = 'https://www.youtube.com'
    elif "facebook" in input_str:
        page = 'https://www.facebook.com'
    else:
        text = "I don't know that one. Let me try."
        page = "https://www."
        page = page + input_str[5:]

    text = text + " Opening " + page[12:]

    print(text)
    speak(text)
    webbrowser.open(page)



def get_weather():

  api_key = "g90NdK9wbQkx3wswGshhedCW57AAPGW6"
  response = requests.get(
    "http://dataservice.accuweather.com/currentconditions/v1/56186",
    params={
      "apikey": api_key,
      "language": "en-us",
    }
  )

  # Check the status code of the response
  if response.status_code == 200:
    # The request was successful. Parse the response data
    data = response.json()
    # Print the temperature in Celsius
    temperature = data[0]["Temperature"]["Metric"]["Value"]
    weather_text = data[0]["WeatherText"]

  else:
    # The request was not successful. Print the error message
    print(f"Error getting weather data: {response.text}")

  text = "It is %s °C outside." % temperature
  text += " " + weather_text + "."
  print(text)
  speak(text)

def process_input(input_str):

  input_str = input_str.lower()
  hellos = ["hello", "hi", "hola", "good morning", "good evening", "good night"]

  if input_str[0:3] == "say":
    speak(input_str[3:])
    print(input_str[3:])

  elif "date" in input_str or "day" in input_str:
    get_date()

  elif "time" in input_str:
    get_time()

  elif bool([ele for ele in hellos if(ele in input_str)]):
    greet()

  elif "joke" in input_str:
    joke()

  elif "weather" in input_str:
    get_weather()

  elif input_str[0:4] == "open":
      get_webpage(input_str)

  elif "wikipedia" in input_str:
      print("Checking the wikipedia ")
      speak("Checking the wikipedia ")
      input_str = input_str.replace("wikipedia", "")
      result = wikipedia.summary(input_str, sentences=2)
      text = "According to wikipedia : " + result
      print(text)
      speak(text)

  else:
    text = "I'm sorry, I can't do that. I am just a virtual assistant."
    print(text)
    speak(text)

def greet():
    global greeting_index

    greeting = greetings[greeting_index]["greeting"]
    greeting_index += 1;

    # Loop the "playlist"
    if (greeting_index > len(greetings)):
        joke_index = 0
        random.shuffle(greetings)

    print(greeting)
    speak(greeting)

def joke():
    global joke_index

    joke = jokes[joke_index]["body"]
    joke_index += 1;

    # Loop the "playlist"
    if (joke_index > len(jokes)):
        joke_index = 0
        random.shuffle(jokes)

    print(joke)
    speak(joke)


def speak(text):

    # Tokenize, clean and phonemize input text
    x = prepare_text(text).to('cpu')

    with torch.no_grad():

        # Generate generic TTS-output
        old_time = time.time()
        tts_output = glados.generate_jit(x)
        # print("Forward Tacotron took " + str((time.time() - old_time) * 1000) + "ms")

        # Use HiFiGAN as vocoder to make output sound like GLaDOS
        old_time = time.time()
        mel = tts_output['mel_post'].to(device)
        audio = vocoder(mel)
        # print("HiFiGAN took " + str((time.time() - old_time) * 1000) + "ms")

        # Normalize audio to fit in wav-file
        audio = audio.squeeze()
        audio = audio * 32768.0
        audio = audio.cpu().numpy().astype('int16')
        output_file = ('output.wav')

        # Write audio file to disk
        # 22,05 kHz sample rate
        write(output_file, 22050, audio)

        # Play audio file
        if 'winsound' in mod:
            winsound.PlaySound(output_file, winsound.SND_FILENAME)
        else:
            call(["aplay", "./output.wav"])



print("Initializing....")
print(r"   _____ _           _  ____   _____")
print(r"  / ____| |         | |/ __ \ / ____|")
print(r" | |  __| | __ _  __| | |  | | (___")
print(r" | | |_ | |/ _` |/ _` | |  | |\___ \ ")
print(r" | |__| | | (_| | (_| | |__| |____) |")
print(r"  \\____|_|\__,_|\__,_|\____/|_____/")

# Select the device
if torch.is_vulkan_available():
    device = 'vulkan'
if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

# Load models
glados = torch.jit.load('models/glados.pt')
vocoder = torch.jit.load('models/vocoder-gpu.pt', map_location=device)

# Prepare models in RAM
for i in range(4):
    init = glados.generate_jit(prepare_text(str(i)))
    init_mel = init['mel_post'].to(device)
    init_vo = vocoder(init_mel)

# Load skills

# Greetings
file = open("greetings.json")
greetings = json.load(file)
random.shuffle(greetings)
greeting_index = 0;

# Jokes
file = open("jokes.json")
jokes = json.load(file)
random.shuffle(jokes)
joke_index = 0;

greet()

while True:
    text = input(">> ")
    process_input(text)