import sys
from vosk import Model, KaldiRecognizer
import pyaudio
import paho.mqtt.client as mqtt
import time
from pyphonetics import Metaphone
import zahlwort2num
import logging
from logging.handlers import RotatingFileHandler


handler = RotatingFileHandler(
    'speech.log',
    mode = 'a',
    maxBytes= 2000000,
    backupCount= 1,
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%d-%b-%y %H:%M:%S")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

z2n = zahlwort2num
mp = Metaphone()

distance = []

dictionary = [
    "hey",
    "computer",
    "aus",
    "licht",
    "an",
    "rolladen",
    "hoch",
    "runter",
    "stopp",
    "selbstzerstörung",
    "aktivieren",
    "shop"
]

client = mqtt.Client()

model = Model(r"vosk-model-small-de-0.15")

recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1,
                  rate=16000, input=True, frames_per_buffer=8192)
try:
    client.connect("192.168.30.9", 1883, 60)
except TimeoutError:
    logger.exception(
        "Couldn't connect to mqtt Broker! \nWith the following message:")
except Exception:
    logger.exception(
        "Couldn't connect to mqtt Broker! \nWith the following message:")

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
    logger.debug('testing phonetics of: %s', string)
    for index, word in enumerate(array):
        for phrase in dictionary:
            distance.append(mp.distance(word, phrase))
        min_dist = distance.index(min(distance))
        logger.debug('min_dist = %s', str(min_dist))
        if min(distance) < 2:
            array[index] = dictionary[min_dist]
        distance.clear()
    final_string = ' '.join(array)
    logger.debug('result: %s', final_string)
    return final_string

def check_for_known_phrases(readable_result):
    if readable_result.find("hey computer") >= 0:
        if readable_result.find("stopp") >= 0:
            sys.exit()
            logger.warning('Stopped because of User Input')
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
            try:
                client.publish("main/hm/manuel/licht/panel", "1")
            except Exception:
                logger.warning("!!! Couldn't send mqtt message !!!")
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
        logger.debug('Voice detected: %s', decoded_voice)
        print(decoded_voice)
        check_for_known_phrases(phonetic_dist(decoded_voice))
        decoded_voice = None