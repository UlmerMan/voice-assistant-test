import sys
from vosk import Model, KaldiRecognizer
import pyaudio
import paho.mqtt.client as mqtt
import time
from pyphonetics import Metaphone
import zahlwort2num
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    filename='voice.log',
    filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level='DEBUG'
)

z2n = zahlwort2num

rs = Metaphone()

distance = []

dictionary = [
    "aus",
    "licht",
    "an",
    "Rolladen",
    "hoch",
    "runter",
    "stop",
    "selbstzerstörung",
    "aktivieren"
]

client = mqtt.Client()

model = Model(r"vosk-model-small-de-0.15")

recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1,
                  rate=16000, input=True, frames_per_buffer=8192)
try:
    client.connect("192.168.30.9", 1883, 60)
except Exception as e:
    logging.exception("Couldn't connect to mqtt Broker! \nWith the following message:", exc_info=True)

stream.start_stream()


def read_voice():
    data = stream.read(4096)

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        readable_result = f"{text[14:-3]}"
        return readable_result

    else:
        return None
    
def phonetic_dist(string):
    array = string.split()
    logging.debug('testing phonetics of: "' + string + '"')
    for index, word in enumerate(array):
        for phrase in dictionary:
            distance.append(mp.distance(word, phrase))
        min_dist = distance.index(min(distance))
        logging.debug('min_dist = "' + str(min_dist) + '"')
        if min(distance) < 2:
            array[index] = dictionary[min_dist]
        distance.clear()
    final_string = ' '.join(array)
    logging.debug('result: "' + final_string + '"')
    return final_string


def check_for_known_phrases(readable_result):
    if readable_result.find("hey computer") >= 0:
        phonetic_dist(readable_result)      
        if readable_result.find("stopp") >= 0:
            sys.exit()
        elif readable_result.find("selbstzerstörung aktivieren") >= 0:
            print('Selbstzerstörung aktiviert')
            time.sleep(1)
            print('3')
            time.sleep(1)
            print('2')
            time.sleep(1)
            print('1')
            print('Booooooooommmmm!!!!')
            sys.exit()
        elif readable_result.find("licht an") >= 0:
            client.publish("main/hm/manuel/licht/panel", "1")
        elif readable_result.find("licht aus") >= 0:
            client.publish("main/hm/manuel/licht/panel", "0")
        elif readable_result.find("licht süd an") >= 0:
            client.publish("main/hm/manuel/licht/süd", "1")
        elif readable_result.find("licht süd aus") >= 0:
            client.publish("main/hm/manuel/licht/süd", "0")
        elif readable_result.find("licht nord an") >= 0:
            client.publish("main/hm/manuel/licht/nord", "1")
        elif readable_result.find("licht nord aus") >= 0:
            client.publish("main/hm/manuel/licht/nord", "0")
        elif readable_result.find("licht bett an") >= 0:
            client.publish("main/hm/manuel/licht/bett", "1")
        elif readable_result.find("licht bett aus") >= 0:
            client.publish("main/hm/manuel/licht/bett", "0")
        elif readable_result.find("rollladen hoch") >= 0:
            client.publish("main/hm/manuel/rolladen", "100")
        elif readable_result.find("rollladen runter") >= 0:
            client.publish("main/hm/manuel/rolladen", "0")
        elif readable_result.find("rollladen auf") >= 0:
            client.publish("main/hm/manuel/rolladen", "0")  

while True:
    decoded_voice = read_voice()
    if decoded_voice:
        print(decoded_voice)
        check_for_known_phrases(decoded_voice)