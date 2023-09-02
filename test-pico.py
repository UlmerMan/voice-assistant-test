import pvporcupine
import pvcheetah
from pvrecorder import PvRecorder
from picovoice import Picovoice

porcupine = pvporcupine.create(
  access_key='UHqNPD8rCVOJsH8MYks3vchv5xqoWWiE7j7cSPgyJDjrIkTP5mq1uw==',
  keyword_paths=['Hey-Computer_de_linux_v2_2_0.ppn'],
  model_path='porcupine_params_de.pv'
)

cheetah = pvcheetah.create(access_key='UHqNPD8rCVOJsH8MYks3vchv5xqoWWiE7j7cSPgyJDjrIkTP5mq1uw==')

recorder = PvRecorder(
        frame_length=porcupine.frame_length)
recorder.start()

def wake_word_callback():
    # wake word detected
    pass


while True:
    pcm = recorder.read()
    result = porcupine.process(pcm)
