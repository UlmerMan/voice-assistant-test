test = "test"

def newTest():
    global test
    test = 'passed'

def printTest():
    print(test)

newTest()
printTest()