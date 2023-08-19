from pyphonetics import Metaphone
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'phon.log',
    mode = 'a',
    maxBytes= 10
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%d-%b-%y %H:%M:%S")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

mp = Metaphone()

string = "hei computor stopp"
distance = []


dictionary = [
    "hey",
    "computer",
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


def phonetic_dist(string):
    array = string.split()
    logging.debug('testing phonetics of: %s', string)
    for index, word in enumerate(array):
        for phrase in dictionary:
            distance.append(mp.distance(word, phrase))
        min_dist = distance.index(min(distance))
        logging.debug('min_dist = %s', str(min_dist))
        if min(distance) < 3:
            array[index] = dictionary[min_dist]
        distance.clear()
    final_string = ' '.join(array)
    logging.debug('result: %s', final_string)
    return final_string
        

print(phonetic_dist(string))