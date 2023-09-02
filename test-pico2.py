from picovoice import Picovoice
from pvrecorder import PvRecorder
import json

ACCESS_KEY = 'UHqNPD8rCVOJsH8MYks3vchv5xqoWWiE7j7cSPgyJDjrIkTP5mq1uw=='
# wake word detected
def wake_word_callback():
    print('Wake on Word detcted!')

def inference_callback(inference):
   print('test')
   if inference.is_understood:
      intent = ''
      intent = inference.intent
      slots = inference.slots
      print(intent)
      print(slots)
      out = json.loads(json.dumps(slots))
      print(out['zustand'])
      # take action based on intent and slot values
   else:
      # unsupported command
      pass

picovoice = Picovoice(
     access_key=ACCESS_KEY,
     keyword_path='Hey-Computer_de_linux_v2_2_0.ppn',
     porcupine_model_path='porcupine_params_de.pv',
     wake_word_callback=wake_word_callback,
     context_path='Licht_de_linux_v2_2_0.rhn',
     rhino_model_path='rhino_params_de.pv',
     inference_callback=inference_callback)

for i, device in enumerate(PvRecorder.get_available_devices()):
            print('Device %d: %s' % (i, device))

recorder = PvRecorder(
        frame_length=picovoice.frame_length,
        device_index=1
        )
recorder.start()


while True:
   picovoice.process(recorder.read())
