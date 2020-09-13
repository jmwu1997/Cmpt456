import pandas as pd
import re
import matplotlib.pyplot as plt
import collections
import nltk
import math
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter
import spacy
import numpy as np
import enchant
import operator

#function used 
def remove_url_punctuation(x):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    replace_url = url_pattern.sub(r'',str(x))
    punct_pattern=re.compile(r'[^\w\s]')
    no_punct = punct_pattern.sub(r'',replace_url).lower()
    return no_punct

def split_words(x):
    split_word_list = x.split(" ")
    return split_word_list

def remove_stopwords(x):
    global stop_words
    words = []
    for word in x:
        if word not in stop_words and len(word)>2 and word != 'nan':
            words.append(word)
    return words

def detect_language(x):
    from langdetect import detect
    try:
        lang=detect(x)
        return(lang)
    except:
        return("other")


def editdistance(word1, word2):
    """functions is cited from https://stackoverflow.com/questions/2460177/edit-distance-in-python by Santosh"""
    word_len1=len(word1)+1
    word_len2=len(word2)+1

    matrix = {}
    for i in range(word_len1): matrix[i,0]=i
    for j in range(word_len2): matrix[0,j]=j

    for i in range(1, word_len1):

        for j in range(1, word_len2):
            distance = 0 if word1[i-1] == word2[j-1] else 1
            matrix[i,j] = min(matrix[i, j-1]+1, matrix[i-1, j]+1, matrix[i-1, j-1]+distance)

    return matrix[i,j]



def freqcount(word,val):
    wordcount = Counter(word)
    result = wordcount.most_common(val)                                                                                                                             
    return result

def inlineword(text,inputword):
    result =[]
    for line in text:
        if inputword in line:
            for word in line:
                result.append(word)
    return result

word_=enchant.Dict("en_US")

#Main function
columns = ['id','text']
#read text file
df = pd.read_csv('D1.csv',names = columns, sep="\t",lineterminator="\n",error_bad_lines=False)
ds = pd.read_csv('D2.csv',names = columns, sep="\t",lineterminator="\n",error_bad_lines=False)

"""remove punct and url links"""
df['tidy_tweet']=df['text'].apply(remove_url_punctuation)
ds['tidy_tweet']=ds['text'].apply(remove_url_punctuation)
# print(df['text'].head());
# print("*******")
# print(df['tidy_tweet'].head())

"""Change to english"""
df['en']=df['text'].apply(detect_language)
ds['en']=ds['text'].apply(detect_language)
# print(df['tidy_tweet'].head(10));
# print("*******")
df=df[df['en']=='en']
ds=ds[ds['en']=='en']


#print(df['tidy_tweet'].head(10));

df['word_list']=df['tidy_tweet'].apply(split_words)
ds['word_list']=ds['tidy_tweet'].apply(split_words)


# """remove stop words"""
global stop_words
#print(stopwords.words('english'))
stop_words = set (stopwords.words('english'))

df['nlp_tweet']=df['word_list'].apply(remove_stopwords)
ds['nlp_tweet']=ds['word_list'].apply(remove_stopwords)

"""data for question 1"""
nonunique1 = list(df['word_list'].explode())
nonunique2 = list(ds['word_list'].explode())
unique1 = list(df['word_list'].explode().unique())
unique2 = list(ds['word_list'].explode().unique())
data=nonunique1+nonunique1
data_unique=unique1+unique1




# """Correction for 1.1"""
print("1.1*************************")
correction = []
tempcorrection=[]
loopcount=0
for i in data_unique:
    if i!='' and word_.check(i)==True:
        for j in range(len(data)):
            if editdistance(i,data[j])<=2 and editdistance(i,data[j])!=0 and data[j]!=''and word_.check(data[j])==True:
                tempcorrection.append(data[j])
        freqcount5=freqcount(tempcorrection,5)[:5]
        if freqcount5!=[]:
            print(i,freqcount5)
            tempcorrection=[]
    loopcount+=1
    if loopcount==20:
            break

# # """new correction 1.2"""
print("1.2*************************")
newcorrection = []
newtempcorrection=[]
loopcount1=0
for i in data_unique:
    if (i!='' and word_.check(i)==False):
        for j in range(len(data)):
            if editdistance(i,data[j])<=2 and editdistance(i,data[j])!=0 and data[j]!=''and word_.check(data[j])==True:
                newtempcorrection.append(data[j])
        newfreqcount=freqcount(newtempcorrection,None)[:5]
        freqcount1=freqcount(newtempcorrection,None)[:1]
        if newfreqcount!=[]:
            newcorrection.append([i,newfreqcount])
            correction.append([i,freqcount1])
            if loopcount1<=150:
                print(i,newfreqcount)
            newtempcorrection=[]
    loopcount1+=1
    if loopcount1==500:
        break
print("1.3*************************")           
print(correction)

"""********************************************************"""
print("2*************************") 
"""data for question 2"""
datalist1 = list(df['nlp_tweet'].explode())
datalist2 = list(ds['nlp_tweet'].explode())
nonunique1_q2=[]
templist=[]
for line in df['nlp_tweet']:
        for word in line:
            if word_.check(str(word))==True and not word.isdigit():
                templist.append(word)
        if templist!=[]:
            nonunique1_q2.append(templist)
        templist=[]

nonunique2_q2=[]

templist=[]
for line in ds['nlp_tweet']:
        for word in line:
            if word_.check(str(word))==True and not word.isdigit():
                templist.append(word)
        if templist!=[]:
            nonunique2_q2.append(templist)
        templist=[]


word_list=[]
for i in freqcount(datalist1,100):
    if i[0]!='':
        if word_.check(str(i[0]))==True and not i[0].isdigit():
            word_list.append(i[0])
val = 0
kl_list = []
for word in word_list:
    lines_1 = inlineword(nonunique1_q2,word)
    lines_2 = inlineword(nonunique2_q2,word)
    for i in set(datalist1):
        lines1_counter = Counter(lines_1)
        lines2_counter = Counter(lines_2)
        lines1_length = len(lines_1)
        lines2_length = len(lines_2)
        #miu = 25
        d1cal = (lines1_counter[i]+25*Counter(datalist1)[i]/len(datalist1))/(lines1_length+25)
        d2cal = (lines2_counter[i]+25*Counter(datalist1)[i]/len(datalist1))/(lines2_length+25)
        val+= math.log2(d2cal/d1cal)*d2cal
    kl_list.append([word,val])
    val = 0
kl_list=sorted(kl_list,key=lambda x:x[1],reverse=True)
print(kl_list)
