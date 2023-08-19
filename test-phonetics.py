from pyphonetics import Metaphone
import logging


logging.basicConfig(
    filename='voice.log',
    filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level='DEBUG'
)

mp = Metaphone()

string = "hey computor"
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
        

print(phonetic_dist(string))