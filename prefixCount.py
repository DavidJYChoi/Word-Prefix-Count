import math

from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import re
import math
import pandas as pd
import numpy as np


def featureCount():
    arrOfStopWords = []
    arrOfURLS = []
    setOfUniqueWords = set()
    listOfUniqueWords = []
    uniqueWords = []

    frequencyOfData = []
    frequencyOfCompanies = []
    frequencyOfBusiness = []
    frequencyOfAction = []
    frequencyOfMining = []
    frequencyOfScience = []


    # made list of stop words to iterate through
    stopWordsFile = open('stop_words.txt', 'r')
    for x in stopWordsFile:
        arrOfStopWords.append(x.strip())

    # made list of urls to iterate through
    textFileWithURLS = open("urls.txt", "r")
    for i in textFileWithURLS:
        arrOfURLS.append(i.strip())

    # found paragraph tags to scrape words
    for i in arrOfURLS:
        req = Request(i, headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(r)
        paragraph = soup.find_all('p')
        dictOfWordsPerURL = {}

        # regular expressions to tokenize and remove stop words
        wordsPerUrl = []
        for j in paragraph:
            pText = j.getText().lower()
            wordsInParagraph = re.sub(r'\W', ' ', pText)
            wordsInParagraph = re.findall(r'\S+', wordsInParagraph)
            for words in list(wordsInParagraph):
                for moreWords in list(arrOfStopWords):
                    if words == moreWords:
                        wordsInParagraph.remove(moreWords)
            wordsPerUrl.extend(wordsInParagraph)

            data = re.findall(r'data', pText)
            frequencyOfData.extend(data)

            companies = re.findall(r'companies', pText)
            frequencyOfCompanies.extend(companies)

            business = re.findall(r'business', pText)
            frequencyOfBusiness.extend(business)

            action = re.findall(r'action', pText)
            frequencyOfAction.extend(action)

            mining = re.findall(r'mining', pText)
            frequencyOfMining.extend(mining)

            science = re.findall(r'science', pText)
            frequencyOfMining.extend(science)

        for k in wordsPerUrl:
            if dictOfWordsPerURL.get(k):
                dictOfWordsPerURL[k] += 1
            else:
                dictOfWordsPerURL.update({k: 1})
        for key, values in dictOfWordsPerURL.items():
            uniqueWords.append(key)

        # made a list with dictionaries of unique words inside
        listOfUniqueWords.append(dictOfWordsPerURL)

    newDict = {}
    # Find Occurrence of Every word across 6 Documents
    for words in listOfUniqueWords:
        setOfUniqueWords.update(words.keys())
    for i in setOfUniqueWords:
        listOfOccurrences = []
        for j in listOfUniqueWords:
            if j.get(i):
                listOfOccurrences.append(j.get(i))
            else:
                listOfOccurrences.append(0)
        newDict[i] = listOfOccurrences

    # Find average frequency of every word across all documents

    # creation of Pandas DataTable
    df = pd.DataFrame(newDict)
    df.index = ['url1', 'url2', 'url3', 'url4', 'url5', 'url6']
    maxPerColumn = df.idxmax(axis=1)
    maxValuePerColumn = df.max(axis=1)
    sumList = df.sum(axis=1)
    # print(list(sumList))
    #print(df)

    sumOfAllWords = 0

    answerFile = open("Q1.txt", "w")
    answerFile.write(str(len(setOfUniqueWords)))
    for label, content in df.idxmax(axis=1).items():
        x = df.loc[label, content]
        # print((df.loc[label, 'sum']))
        # print(df.loc[label,content])
        sumOfAllWords += sumList[label]

        answerFile.write(" " + content + str(df[content].values) + " " + str((x / sumList[label])))

    # Q3
    newDict2 = {}
    for i in setOfUniqueWords:
        avgFrequencyAcrossDoc = []
        for j in listOfUniqueWords:
            if j.get(i) is None:
                wordsPerDoc = 0
            else:
                # wordsPerDoc = j.get(i) / sumList[listOfUniqueWords.index(j)]
                wordsPerDoc = j.get(i)
            AvgWordAcrossAllDoc = df[i].sum() / len(arrOfURLS)
            #print(AvgWordAcrossAllDoc)
            if wordsPerDoc > AvgWordAcrossAllDoc:
                avgFrequencyAcrossDoc.append(1)

            else:
                avgFrequencyAcrossDoc.append(-1)
        newDict2[i] = avgFrequencyAcrossDoc
    df2 = pd.DataFrame(newDict2)
    df2.index = ['url1', 'url2', 'url3', 'url4', 'url5', 'url6']
    print(df2)
    answerFileQ3 = open("Q3.txt", "w")
    answerFileQ3.write("data " + str((df["data"].sum() / len(arrOfURLS))) + str(list(df2["data"])) +
                       str(math.log(len(arrOfURLS) / (1 + len(frequencyOfData)))) + "\n")
    answerFileQ3.write("companies " + str((df["companies"].sum() / len(arrOfURLS))) + str(list(df2["companies"])) +
                       str(math.log(len(arrOfURLS) / (1 + len(frequencyOfCompanies)))) + "\n")
    answerFileQ3.write("business " + str((df["business"].sum() / len(arrOfURLS))) + str(list(df2["business"])) +
                       str(math.log(len(arrOfURLS) / (1 + len(frequencyOfBusiness)))) + "\n")
    answerFileQ3.write("action " + str((df["action"].sum() / len(arrOfURLS))) + str(list(df2["action"])) +
                       str(math.log(len(arrOfURLS) / (1 + len(frequencyOfAction)))) + "\n")
    answerFileQ3.write("mining " + str((df["mining"].sum() / len(arrOfURLS))) + str(list(df2["mining"])) +
                       str(math.log(len(arrOfURLS) / (1 + len(frequencyOfMining)))) + "\n")
    answerFileQ3.write("science " + str((df["science"].sum() / len(arrOfURLS))) + str(list(df2["science"])) +
                       str(math.log(len(arrOfURLS) / (1 + len(frequencyOfScience)))) + "\n")
                       
    # Sorting by Prefix
    answerFile = open("Q2.txt", "w")
    # Wri Prefix
    listWR = ['write', 'writing', 'wrote', 'writes', 'written']
    answerFile.write("[" + "'write', 'writing', 'wrote', 'writes', 'written'" + "] " + "[")
    stringWR = ""
    for i in listWR:
      if {i}.issubset(df.columns):
        stringWR = stringWR + (str(df[i].sum()) + ",")
      else:
        stringWR = stringWR + ("0" + ",")
        stringWR = stringWR[:-1]
        stringWR = stringWR + ("]" + "\n")
        answerFile.write(stringWR)

    # Ret Prefix
    listRET = ['return', 'returns', 'returned', 'returning']
    answerFile.write("[" + "'return', 'returns', 'returned', 'returning'" + "]" + "[")
    stringRET = ""
    for i in listRET:
        if {i}.issubset(df.columns):
            stringRET = stringRET + (str(df[i].sum()) + ",")
        else:
            stringRET = stringRET + ("0" + ",")
            stringRET = stringRET[:-1]
            stringRET = stringRET + ("]" + "\n")
            answerFile.write(stringRET)

    # Sci Prefix
    listSCI = ['science', 'sciences', 'scientific', 'scientist', 'scientists']
    answerFile.write("[" + "'science', 'sciences', 'scientific', 'scientist', 'scientists'" + "]" + "[")
    stringSCI = ""
    for i in listSCI:
        if {i}.issubset(df.columns):
            stringSCI = stringSCI + (str(df[i].sum()) + ",")
        else:
            stringSCI = stringSCI + ("0" + ",")
            stringSCI = stringSCI[:-1]
            stringSCI = stringSCI + ("]" + "\n")
            answerFile.write(stringSCI)

  
    # listWork = ['work', 'worker', 'working', 'worked', 'works', 'workers']
    # answerFile.write("[" + "work', 'worker', 'working', 'worked', 'works', 'workers'" + "]" + "[")
    # stringWork = ""
    # for i in listWork:
    # if {i}.issubset(df.columns):
    # stringWork = stringWork + (str(df[i].sum()) + ",")
    # else:
    # stringWork = stringWork + ("0" + ",")
    # stringWork = stringWork[:-1]
    # stringWork = stringWork + ("]" + "\n")
    # answerFile.write(stringWork)
