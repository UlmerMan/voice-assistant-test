from pyphonetics import Metaphone

rs = Metaphone()

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

def phonetic_dist(voice):
    voice.split()
    for word in dictionary:
        distance.append(rs.distance(voice, word))

    for i in distance:
        print(i)

    min_dist = distance.index(min(distance))
    print(min_dist)
    voice = dictionary[min_dist]
    if min(distance) > 2:
        return None
    return voice