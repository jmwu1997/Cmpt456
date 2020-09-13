import pandas as pd
import re
import matplotlib.pyplot as plt
import collections
import nltk
import math
from nltk.corpus import stopwords
from wordcloud import WordCloud
import spacy
import numpy as np

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

def remove_nonenglish(x):
    En_words = set(nltk.corpus.words.words())
    words=[]
    for w in x:
        if w.lower() in En_words and w.isalpha():
            words.append(w)
    return words

def powerfit(x, y, xnew):
    """line fitting on log-log scale"""
    k, m = np.polyfit(np.log(x), np.log(y), 1)
    return np.exp(m) * xnew**(k)



#Main function
columns = ['id','text']
#read text file
df = pd.read_csv('D1.txt',names = columns, sep="\t",lineterminator="\n",error_bad_lines=False)
ds = pd.read_csv('D2.txt',names = columns, sep="\t",lineterminator="\n",error_bad_lines=False)
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

"""tokenizing words in tweet"""
# df['word_list']=df['better_tweet'].apply(remove_nonenglish)
# ds['word_list']=ds['better_tweet'].apply(remove_nonenglish)


# print(df['word_list'].head(10))


"""remove stop words"""
global stop_words
#print(stopwords.words('english'))
stop_words = set (stopwords.words('english'))

df['nlp_tweet']=df['word_list'].apply(remove_stopwords)
ds['nlp_tweet']=ds['word_list'].apply(remove_stopwords)
graphlist1 = list(df['word_list'].explode())
graphlist2 = list(ds['word_list'].explode())
graphcount1=nltk.FreqDist(graphlist1)
graphcount2=nltk.FreqDist(graphlist2)
"""find freq"""
all_words_unique_list1 = (df['nlp_tweet'].explode()).unique()
all_words_unique_list2 = (ds['nlp_tweet'].explode()).unique()
print("Number of unique token in D1:",len(all_words_unique_list1))
print("Number of unique token in D2:",len(all_words_unique_list2))
word_list1 = list(df['nlp_tweet'].explode())
word_list2 = list(ds['nlp_tweet'].explode())
nltk_count1=nltk.FreqDist(word_list1)
nltk_count2=nltk.FreqDist(word_list2)
print("The top-100 most frequent token and their frequencies in D1: ",nltk_count1.most_common(100))
print("*********************************************")
print("The top-100 most frequent token and their frequencies in D2: ",nltk_count2.most_common(100))

"""compare the top 100 tokens ranked higher d2 than in d1"""
comparelist=[]
loop1=0
loop2=0
for key2, value2 in nltk_count2.most_common() :
    loop1+=1
    loop2=0
    for key1, value1 in nltk_count1.most_common() :
        loop2+=1
        if (key1==key2 and loop1 < loop2):
            comparelist.append([key2,loop1,key1,loop2])

print("*********************************************")
print("The top-100 tokens that are ranked higher in D2 than in D1: ")
for i in range(100):
    print("%s:" % (i+1),comparelist[i])


print("*********************************************")
print("Graph plot and calculation of C: ")

rank1=[]
rank1x=[]
rank1y=[]
zipf1y=[]
i=1
for key1, value1 in graphcount1.most_common() :
    rank1.append([i,key1,value1,value1/len(graphlist1),i*value1/len(graphlist1)])
    rank1x.append(i)
    rank1y.append(value1/len(graphlist1))
    if(i<100):
        zipf1y.append(i*value1/len(graphlist1))
    i+=1

rank2=[]
rank2x=[]
rank2y=[]
zipf2y=[]
j=1
for key2, value2 in graphcount2.most_common() :
    rank2.append([j,key2,value2,value2/len(graphlist2),j*value2/len(graphlist2)])
    rank2x.append(j)
    rank2y.append(value2/len(graphlist2))
    if (j <100):
        zipf2y.append(j*value2/len(graphlist2))
    j+=1

zipf1val=0
zipf2val=0

for x in range(len(zipf1y)):
    zipf1val=zipf1val+zipf1y[x]
    zipf2val=zipf2val+zipf2y[x]

zipf1val=zipf1val/len(zipf1y)
zipf2val=zipf2val/len(zipf2y)
zipf1y=[]
zipf2y=[]
for i in range(1,len(rank1x)+1):
    zipf1y.append(zipf1val/i)
for i in range(1,len(rank2x)+1):
    zipf2y.append(zipf2val/i)
rank1.pop(0)
rank2.pop(0)
print("D1 C constant = ",zipf1val)
print("D2 C constant = ",zipf2val)
# print("D1 C constant = ",zipf1val)
# print("D2 C constant = ",zipf2val)
plt.title("D1 Zipf Graph")
plt.loglog(rank1x,zipf1y,basex=10,basey=10, label='Zipfy')
plt.loglog(rank1x,rank1y,basex=10,basey=10, marker='.', linestyle=':', label='D1')
plt.legend(loc="upper right")
plt.xlabel('Rank')
plt.show()
plt.title("D2 Zipf Graph")

plt.loglog(rank2x,zipf2y,basex=10,basey=10, label='Zipfy')
plt.loglog(rank2x,rank2y,basex=10,basey=10, marker='.', linestyle=':', label='D2')
plt.legend(loc="upper right")
plt.xlabel('Rank')
plt.show()

print("*********************************************")
print("all the tokens whose relative frequencies in D2 are higher than those in D1: ")
print("*********************************************")
comparelist2=[]
for r in range(500):
    for q in range(len(rank1)):
        if(rank2[r][1]==rank1[q][1] and rank2[r][3]>rank1[q][3]):
            comparelist2.append([rank1[q][1],round(rank1[q][3],7),round(rank2[r][3],7),round(rank2[r][3]-rank1[q][3],7)])
print("Word,D1 freq,D2 freq, D2-D1freq: ")
for i in range(len(comparelist2)):
    print(comparelist2[i])


