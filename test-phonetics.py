from pyphonetics import Metaphone

rs = Metaphone()

distance = []
out = []

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
    inp = ''
    inp = voice
    inp.split()
    i = 0
    while i < len(inp):
        for phrase in dictionary:
            distance.append(rs.distance(inp[i], phrase))
        min_dist = distance.index(min(distance))
        print(min_dist)
        if min(distance) < 2:
            inp[i] = dictionary[min_dist]
        i += 1
    ''.join(inp)
    return inp

print(phonetic_dist("test"))