import re #for Regular Expression


#open the directory with the scripts files
#call all other function for indexing the scripts
def sortFiles(genre, stopWords, ponctuation):
    tokenize(genre+"/moviesScripts.txt", genre+"/result.txt", ponctuation)
        #doesn't modify the source file and stock the tokenized text in "genre"/result.txt
        #all other functions modify the result.txt file
    deleteStopWords(genre+"/result.txt", stopWords)
    frequenceWords = countWords(genre+"/result.txt")
        #frequenceWords is a python dictionary with word (key) -> value (frequency)
    countedResult(genre+"/result.txt", frequenceWords)


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
        if x[1] >= 50:
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
    sortFiles("1",stopWords, ponctuation)
    sortFiles("2",stopWords, ponctuation)


#Horror :    2                              #Family: 1
    #The Hauting of hill house                  #American Pie
    #THE MUMMY                                  #Bean
    #Alien III                                  #The brothers bloom
    #BOOK OF THE DEAD                           # CRAZY, STUPID, LOVE
    #EVIL DEAD II                               # HAPPY FEET
    #Friday the 13th                            #THE INCREDIBLES
    #THE GRUDGE                                 #KUNG FU PANDA
    # HALLOWEEN                                 #THE MASK
    #HANNIBAL                                   #THE PROPOSAL
    #INSIDIOUS                                  # SHREK
    #IT                                         #TED


if __name__ == "__main__":
        main()
