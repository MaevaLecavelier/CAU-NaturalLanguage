# Maeva Lecavelier - ID: 50191580
#Project: IR evaluation

import re #for Regular Expression
import time

#open the directory with the scripts files
#call all other function for indexing the scripts
def sortFile(path, stopWords, ponctuation):
    tokenize(path+".txt", path+"Sorted.txt", ponctuation)
        #doesn't modify the source file and stock the tokenized text in "genre"/result.txt
        #all other functions modify the result.txt file
    deleteStopWords(path+"Sorted.txt", stopWords)
    frequenceWords = countWords(path+"Sorted.txt")
        #frequenceWords is a python dictionary with word (key) -> value (frequency)
    countedResult(path+"Sorted.txt", frequenceWords)


#better way to write on a file, for optimazing code
def writeFile(destFile, content):
    file = open(destFile, "w+")
    file.write(content)
    file.close()


def tokenize(sourceFile, destinationFile, ponctuation):
    #mettre les scripts tokenizés dans un autre file
    source = open(sourceFile, "r")
    result = open(destinationFile, "w+")
    lines = source.read()
    for x in lines:
        x = x.replace(' ', '\n') #replace space by new line
        x = x.replace('\t', '\n')
        for i in range(len(ponctuation)):
            x = x.replace(ponctuation[i], '') #take off the ponctuation
        result.write(x) #writes the lines in the result file
    source.close()
    result.close()


def deleteStopWords(fileToSort, listStopWords):
    file = open(fileToSort, "r")
    content = ""
    lines = file.readlines();
    for x in lines:
        if isCaps(x):
            x = ""
        x = x.lower()
        for i in range(len(listStopWords)):
            if x == listStopWords[i]: #better than "replace" in this case, because "replace" will cut the '\n' at the end of each line
                x = ''
        content += x
    file.close()
    writeFile(fileToSort, content)



def isCaps(word):
    pattern = '[A-Z][A-Z]+'
    return re.match(pattern, word)



def countWords(sortedFile):
    #créer un tableau en mode (mot, frequence)
    # et écrire ça dans un nouveau file
    # qui sera le pré-résultat
    file = open(sortedFile, "r")
    words = file.readlines()
    FreqWords = dict() #create a dictonary with Words (key) -> frequence (value)
    for x in words:
        if x not in FreqWords:
            FreqWords[x] = 1
        else:
            FreqWords[x] += 1
    FreqWords = sorted(FreqWords.items(), reverse = True, key=lambda key:key[1])
    file.close()
    return FreqWords


def countedResult(sortedFile, freqWords):
    file = open(sortedFile, "w+")
    content = ""
    for x in freqWords:
        content += str(x[1])+":"+x[0]
    file.write(content)
    file.close()


def main():
    stopWords = \
        ["am\n",'\n',"for\n","from\n", \
        "that\n","you\n","i\n","his\n","he\n","it\n","her\n","with\n", \
        "not\n", "him\n","she\n", "if\n","then\n", "well\n","up\n", \
        "down\n","yes\n","no\n","okay\n","out\n", "me\n","this\n","what\n",\
        "the\n",  "at\n",  "there\n",  "some\n",  "my\n",  "of\n",  "be\n",  "use\n",  "her\n", \
        "than\n",  "and\n",  "this\n",  "an\n",  "would\n",  "first\n",  "a\n",  "have\n",  "each\n", \
        "make\n",  "water\n",  "to\n",  "from\n",  "which\n",  "like\n",  "been\n",  "in\n",  "or\n", \
        "she\n",  "him\n",  "call\n",  "is\n",  "one\n",  "do\n",  "into\n",  "who\n",  "you\n",  "had\n", \
        "how\n",  "time\n",  "oil\n",  "that\n",  "by\n",  "their\n",  "has\n",  "its\n",  "it\n",  "word\n", \
        "if\n",  "look\n",  "now\n",  "he\n",  "but\n",  "will\n",  "two\n",  "find\n",  "was\n",  "not\n", \
        "up\n",  "more\n",  "long\n",  "for\n",  "what\n",  "other\n",  "write\n",  "down\n",  "on\n", \
        "all\n",  "about\n",  "go\n",  "day\n",  "are\n",  "were\n",  "out\n",  "see\n",  "did\n", \
        "as\n",  "we\n",  "many\n",  "number\n",  "get\n",  "with\n",  "when\n",  "then\n",  "no\n", \
        "come\n",  "his\n",  "your\n",  "them\n",  "way\n",  "made\n",  "they\n",  "can\n",  "these\n", \
        "could\n",  "may\n",  "I\n",  "said\n",  "so\n",  "people\n",  "part\n", "over\n", "im\n", "off\n",\
        "just\n", "dont\n", "know\n", "back\n", "looks\n", "here\n","through\n","ted\n","where\n","po\n"]

    ponctuation = ['.',',','(',')',':','?','!',';','\'','-','*',"--"]
    start_time = time.clock()
    for i in range(1,12): # i can take [1,2,3,4,5,6,7,8,9,10,11]
        familyMovie = "Family/"+str(i)
        horrorMovie = "Horror/"+str(i)
        scifiMovie = 'SciFi/'+str(i)
        sortFile(familyMovie, stopWords, ponctuation)
        sortFile(horrorMovie, stopWords, ponctuation)
        sortFile(scifiMovie, stopWords, ponctuation)
    print(round (time.clock() - start_time, 1), "seconds for indexing.")
if __name__ == "__main__":
        main()


#query a faire :
    # vocabulaire de la maison : door, room, floor
    # vocabulaire mignon : good, little, oh
    # plus précis : shrek, ash, bloom, brother, bob ...
    # deux mots : bloom brother, shrek donkey
    # phrase:  the movie with shrek, family with powers,

# Family
# 1 = AmericanPie
# 2 = Bean
# 3 = CrazyStupidLove
# 4 = HappyFeet
# 5 = Kungfu Panda
# 6 = Shrek
# 7 = Ted
# 8 = The Brothers bloom
# 9 = The Incredibles
# 10 = The MASK
# 11 = The Proposal


# Horror
# 1 = Alien3
# 2 = EvilDead
# 3 = EvilDead 2
# 4 = Friday the 13th
# 5 = Halloween
# 6 = Hannibal
# 7 = INSIDIOUS
# 8 = It
# 9 = The Grudge
# 10 = The haunting of hill house
# 11 = the mummy

# SciFi
# 1 = 2001_ASpaceOdyssey
# 2 = Cube
# 3 = EternalSunshineOfTheSpotlessMind
# 4 = Ghostbuster2
# 5 = HotTubTimeMachine
# 6 = JurassicPark2
# 7 = MenInBlack
# 8 = Prometheus
# 9 = StarWars2
# 10 = TheMartian
# 11 = Watchmen
