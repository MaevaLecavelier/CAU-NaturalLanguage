

import time

##########################################################################################
# -------------------------------- Calculate docs score ---------------------------------#

#calculate score of each file, and return the 5 best results
def getResult(query):
    result = dict()
    genres = ['Family', 'Horror', 'SciFi']
    for genre in genres:
        for fileNb in range(1,12):
            nameFile = genre+'/'+str(fileNb)+'Sorted.txt' #Family/3Sorted.txt
            tmpScore = scoreDoc(nameFile, query)
            result[nameFile] = tmpScore
            #sort by score
            #return 5 bests
    result = sorted(result.items(), reverse = True, key=lambda key:key[1])
    result = getPertinentResults(result)
    return result

#get info (word and occurences) from a line like : "256:donkey"
def decodeLine(line):
    for i in range(len(line)):
        if(line[i] == ':'):
            occurences = line[0:i]
            word = line[(i+1):len(line)-1]
    return word, occurences


#get the occurences of the different words of the query from the movie scripts
#sum the different occurences
#make a average by divide the sum by the number of words of the Query
#exemple: query = 'shrek donkey'
        # in shrek movie, shrek occurences = 168, donkey occurences = 112
        # 168 + 112 = 280
        # 280 / 2 (shrek donkey = 2 words) = 140
        # the movie shrek has a score of 140 for the query 'shrek donkey'
def scoreDoc(nameFile, query):
    score = 0
    file = open(nameFile, 'r')
    lines = file.readlines()
    for line in lines:
        word, occurences = decodeLine(line)
        if str(word) in query:
            score += int(occurences)
    score = score / len(query)
    score = round(score,2)
    file.close()
    return score

#return only the key with positive value
def getPertinentResults(dictionnary):
    finalResult = dict()
    for i in range(len(dictionnary)):
        if(float(dictionnary[i][1]) >= 1):
            finalResult[i] = dictionnary[i]
        else:
            return finalResult
    return finalResult

##########################################################################################
#----------------------------- Transform str query into list of words -------------------#


def strToArr(string):
    result = []
    currentWord = ''
    for i in range(len(string)):
        if(string[i] == ' '):
            result.append(currentWord)
            currentWord = ''
        else:
            currentWord += string[i]
    result.append(currentWord)
    return result


def deletePonctuation(string, ponctuation):
    for i in range(len(ponctuation)):
        string = string.replace(ponctuation[i], '')
    return string


def deleteStopWords(array, listStopWords):
    index = 0
    for i in range(len(array)):
        if i >= len(array) - 1:
            return array
        for j in range(len(listStopWords)):
            if array[i] == listStopWords[j]:
                array.pop(i)

    return array


def tokenize(string, listStopWords, ponctuation):
    string = deletePonctuation(string, ponctuation)
    string = string.lower()
    query = strToArr(string)
    query = deleteStopWords(query, listStopWords)
    return query


##########################################################################################
#---------------------- Pretty print for see the result ---------------------------------#

def getMovie(fileName):
    genre = ''
    movie = 0
    for i in range(len(fileName)):
        if( fileName[i] == '/'):
            movie = fileName[i+1]
            if isInt(fileName[i+2]):
                movie += fileName[i+2]
            break
        genre += fileName[i]
    return genre, movie


def isInt(n):
    try:
        float(n)
    except:
        return False
    else:
        return True


def printResult(result):
    if(len(result) == 0):
        print("No data found. Please, try another request.")
        return
    Family = {'1':'  American Pie  \t', '2':'      Bean      \t', '3':' Crazy, Stupid, Love \t', '4':'     HappyFeet     \t', '5':'   Kung Fu Panda  \t', '6':'     Shrek     \t', '7':'       Ted       \t', '8':' The Brothers Bloom \t', '9':'   The Incredibles   \t', '10':'     The Mask     \t', '11':'  The proposal   \t'}
    Horror = {'1':'     Alien III     \t', '2':'   Evil Dead   \t', '3':'     Evil Dead 2     \t', '4':' Friday the 13th \t', '5':'     Halloween    \t', '6':'     Hannibal     \t', '7':'     Insidious     \t', '8':'       It       \t', '9':'    The Grudge     \t', '10':'The Haunting of Hill House ', '11':'    The Mummy   \t'}
    SciFi = { '1':'2001 a Space Odyssey\t', '2':'      Cube      \t','3':'Eternal Sun[..]less Mind', '4':'  Ghostbuster 2  \t', '5':'Hot Tub Time Machine\t', '6':'  Jurassic Park 2 \t', '7':'  Men In Black  \t', '8':'   Prometheus  \t', '9': '   StarWars 2  \t', '10':'  The Martian  \t','11': '    Watchmen     \t'}
    print('\n')
    print('*************************************************************************')
    print('|\tRank\t|\tGenre\t|\tMovie title\t|\tScore\t|')
    print('-------------------------------------------------------------------------')
    for i in range(len(result)):
        genre, movie = getMovie(result[i][0])
        if genre == 'Family':
            print('|\t'+str(i+1)+'\t|\t'+genre+'\t|'+Family[str(movie)]+'|\t'+ str(result[i][1])+'\t|')
        elif genre == 'Horror':
            print('|\t'+str(i+1)+'\t|\t'+genre+'\t|'+Horror[str(movie)]+'|\t'+ str(result[i][1])+'\t|')
        else :
            print('|\t'+str(i+1)+'\t|\t'+genre+'\t|'+SciFi[str(movie)]+'|\t'+ str(result[i][1])+'\t|')
        print('-------------------------------------------------------------------------')
    print('\n')

##########################################################################################


def main():

    stopWords = \
        ["am","for","from", \
        "that","you","i","his","he","it","her","with", \
        "not", "him","she", "if","then", "well","up", \
        "down","yes","no","okay","out", "me","this","what",\
        "the",  "at",  "there",  "some",  "my",  "of",  "be",  "use",  "her", \
        "than",  "and",  "this",  "an",  "would",  "first",  "a",  "have",  "each", \
        "make",  "water",  "to",  "from",  "which",  "like",  "been",  "in",  "or", \
        "she",  "him",  "call",  "is",  "one",  "do",  "into",  "who",  "you",  "had", \
        "how",  "time",  "oil",  "that",  "by",  "their",  "has",  "its",  "it",  "word", \
        "if",  "look",  "now",  "he",  "but",  "will",  "two",  "find",  "was",  "not", \
        "up",  "more",  "long",  "for",  "what",  "other",  "write",  "down",  "on", \
        "all",  "about",  "go",  "day",  "are",  "were",  "out",  "see",  "did", \
        "as",  "we",  "many",  "number",  "get",  "when",  "then",  "no", \
        "come",  "his",  "your",  "them",  "way",  "made",  "they",  "can",  "these", \
        "could",  "may",  "I",  "said",  "so",  "people",  "part", "over", "im", "off",\
        "just", "dont", "know", "back", "looks", "here","through","ted","where","po"]

    ponctuation = ['.',',','(',')',':','?','!',';','\'','-','*',"--"]

    #get query
    userQuery = input('Query (at least one word): ')
    startTime = time.time()
    arrQuery = tokenize(userQuery, stopWords, ponctuation)
    result = getResult(arrQuery)
    print('\n')
    print("Time requiered for this query: ", round((time.time()-startTime)*1000), "ms")
    printResult(result)

main()
