import pickle
import re
import time

GOOD_CHARS = [chr(value) for value in range(ord('a'), ord('z') + 1, 1)]
GOOD_CHARS.append('\'')

def pickler(pickleDict):
    for i in range(len(pickleDict)):
        fileName = str(i + 1) + "grams.pkl"
        fout = open(fileName,'wb')
        pickle.dump(pickleDict[i], fout)

    fout.close()


'''
This function reads a file line by line and appends each word to a list. It also
appends <s> and </s> tags to indicate the beginning and end of a line. 
fileName: the name of a file to read and tokenize. File must exist in the working directory
return: a list containing the entire tokenized works of Shakespeare. Each element in the
        list is a list of words representing a line in the play.
'''
def tokenizeText(fileName):
    inputFile = open(fileName, 'r', encoding='utf-8')
    sentences = []

    for line in inputFile:
        words = []
        if line != '\n':
            for word in line.split():
                wordToInsert = tokenizeWord(word)
                # A word will only be inserted if its tokenization is not empty
                if wordToInsert != '':
                    words.append(wordToInsert)
            
            # This will ensure that we only insert lines containing some text
            if len(words) > 0:
                words.insert(0, '<s>')
                words.append('</s>')

        sentences.append(words)

    return sentences


'''
This function takes a word as a string and transforms it into a clean token that we can count.
The word is transformed into lowercase and all punctuation is removed, except for the apostrophe
(') for contractions. The token is returned.
word: a string to be tokenized
return: a lowercase word 
'''
def tokenizeWord(word):
    # goodChars = [chr(value) for value in range(ord('a'), ord('z') + 1, 1)]
    # goodChars.append('\'')
    token = ""

    # In the play script, each line begins with the character name in all caps followed by a 
    # period (i.e. 'HAMLET.'). This will allow us to ignore this part of the line.
    if re.match(r'[A-Z]+\.', word) :
        return ''

    word = word.lower()
    for letter in word:
        if letter in GOOD_CHARS:
            token += letter

    return token


'''
the :
     cat : 1
     dog : 4
     man : 3
a : 
     rat : 3
     bat : 2
     hat : 9

'''
def makeFrequencyDict(sents, n):
    print("==============================================")
    print("Starting freqency dictionary for " + str(n) + "-grams...\n\n")
    start = time.time()

    probDict = {}
    ngramList = ngrams(sents, n)

    for i in range(len(ngramList) - n):
        if ngramList[i] in probDict:
            if ngramList[i + n] in probDict[ngramList[i]]:
                probDict[ngramList[i]][ngramList[i + n]] += 1
            else:
                probDict[ngramList[i]][ngramList[i + n]] = 1
        else:
            probDict[ngramList[i]] = {ngramList[i + n] : 1}

    howLong = (time.time()- start)
    print("frequency dict finished in " + str(howLong) + "s")
    
    return probDict


'''
This fuction creates a data structure to store the probability of the
next ngram given an ngram. Each ngram is a key in a dictionary. The
value is a list of tuples where each tuple is a potential ngram to
follow the key and a cumulative probaility of this ngram to follow 
the key.
freqDict: a dictionary containing ngrams as keys and a dictionary of ngrams
          as the value where the nested dictionary contains all possible ngrams
          to follow the key as keys and the frequency of appearence as values
return: a dictionary where the key is an ngram and the value is a list of 
        tuples (ngram, cumulative_probability)
'''
def makeProbabilityDict(freqDict):
    print("==============================================")
    print("Starting probability dictionary...\n\n")
    start = time.time()

    probDict = {}

    for key in freqDict.keys():
        probDict[key] = generateCumulativeList(freqDict[key])

    howLong = (time.time()- start)
    print("probability dict finished in " + str(howLong) + "s")
    print("==============================================")

    return probDict


'''
This is a helper to generate the probability list for each entry in
the frequency dictionary. For a given entry, it counts the number of 
following ngrams and generates a list of tuples described in 
makeProbabilityDict(freqDict)
ctDict: a dictionary nested in the freqDict containing all possible ngrams
        that follow a key as keys and their frequency as values
return: a list of tuples in the form (ngram, cumulative probability)
'''
def generateCumulativeList(ctDict):
    wordProbList = []
    cumProb = 0.0
    totalGrams = 0.0

    for key in ctDict.keys():
        totalGrams += ctDict[key]

    for key in ctDict.keys():
        cumProb += (ctDict[key] / totalGrams)
        wordProbList.append((key, cumProb))

    return wordProbList


'''
Returns a complete 1D list of n-grams for a 2D list of sentences
inList: a 2D list of sentences where each sentence is a list of strings
n: length of word sequences to group
'''
def ngrams(inList, n):
    output = []
    for sent in inList:
        for i in range(len(sent) - n + 1):
            output.append(' '.join(sent[i: i + n]))

    return output


def main():
    print("Begin")
    print(time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime()))
    start = time.time()

    lines = tokenizeText('shakespeare.txt')
    probDict = [makeProbabilityDict(makeFrequencyDict(lines, 1)), 
                makeProbabilityDict(makeFrequencyDict(lines, 2)),
                makeProbabilityDict(makeFrequencyDict(lines, 3)),
                makeProbabilityDict(makeFrequencyDict(lines, 4))]

    pickler(probDict)

    print(time.strftime("%a,%d %b %Y %H:%M:%S",time.localtime()))
    howLong = (time.time()- start)
    print("Finished processing in " + str(howLong) + "s")
    print("==============================================")

main()
