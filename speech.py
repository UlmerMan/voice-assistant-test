import sys
from vosk import Model, KaldiRecognizer
import pyaudio
import paho.mqtt.client as mqtt
import time
from pyphonetics import Metaphone
import zahlwort2num

z2n = zahlwort2num

rs = Metaphone()

distance = []
out = []

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

RESPEAKER_WIDTH = 2
mic = pyaudio.PyAudio()
stream = mic.open(format=mic.get_format_from_width(RESPEAKER_WIDTH), channels=1,
                  rate=16000, input=True, frames_per_buffer=8192)

#client.connect("192.168.30.9", 1883, 60)

stream.start_stream()


def read_voice():
    data = stream.read(4096)

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        readable_result = f"{text[14:-3]}"
        return readable_result

    else:
        return None
    
def phonetic_dist(voice):
    voice.split()
    for word in voice:
        for phrase in dictionary:
            distance.append(rs.distance(word, phrase))
        min_dist = distance.index(min(distance))
        print(min_dist)
        if min(distance) > 2:
            break
        out.append(dictionary[min_dist])
    out.join()
    return out


def check_for_known_phrases(readable_result):
    if readable_result.find("hey computer") >= 0:
        phonetic_dist(readable_result)        

while True:
    decoded_voice = read_voice()
    if decoded_voice:
        print(decoded_voice)
        check_for_known_phrases(decoded_voice)