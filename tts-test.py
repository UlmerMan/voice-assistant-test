from gtts import gTTS
import playsound

def speak(text):
    tts = gTTS(text=text, lang='de')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)



speak('Hallo Welt')