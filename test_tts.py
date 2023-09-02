import pyttsx3
engine = pyttsx3.init()

voices = engine.setProperty('voice', 'german')

engine.say('Hallo Welt.')

engine.runAndWait()