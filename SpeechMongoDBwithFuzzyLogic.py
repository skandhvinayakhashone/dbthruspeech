import speech_recognition as sr
from nltk.corpus import stopwords
import numpy as np
import sklearn.cluster
import distance
import Levenshtein
import pymongo
from nltk.corpus import words
from gtts import gTTS
import os
word_list = words.words()


#LISTENING TO SPEECH
r = sr.Recognizer()
try:
    with sr.Microphone() as source:
        print('what do you want to search for?')
        audio = r.listen(source)
        print('Calculating.......................')

        text = r.recognize_google(audio)
        print(text)
except:

        print("could not connect")



#REMOVING STOP WORDS
cachedStopWords = stopwords.words("english")
cachedStopWords.remove("it")
new=[]
newlist=text.split()
#print(newlist)


for x in range(0,len(newlist)):
     if newlist[x] not in cachedStopWords:
        new.append(newlist[x])


for i in range(0,len(new)):
    new[i]=new[i].lower()



#PRINTING FINAL WORD LIST
#print(new)


#CREATING THE CLUSTER
words_orgn = word_list
final_word_list=[]
for i in range(0,len(new)):
    if new[i] in word_list:
        final_word_list.append(new[i])

words = final_word_list
for i in range(0,len(new)):
    words.append(new[i])
words = np.asarray(words)
lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])
affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.80)
affprop.fit(lev_similarity)


data=[]
for cluster_id in np.unique(affprop.labels_):
    exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
    cluster = np.unique(words[np.nonzero(affprop.labels_ == cluster_id)])
    for i in range(0, len(cluster)):
        if cluster[i] in words_orgn:
            for j in range(0, len(new)):
                if Levenshtein.ratio(cluster[i], new[j]) > 0.5:
                    print(cluster[i])
                    data.append(cluster[i])

#print(data)
data.reverse()
#print(data[0])
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["monty"]
mycol = mydb[data[0]]

x = list(mycol.find({},{data[1]:1}))
x=str(x)
my_list = x.split(",")
my_list=my_list[1].split("{")
my_list=my_list[1].replace(',','')
my_list=my_list.replace('\'','')
print(my_list)

myobj = gTTS(text=my_list, lang='en', slow=False)

myobj.save("speech.mp3")

os.system("afplay speech.mp3")
#replace afplay with mpg123 for Linux Operating Systems and replace the entire thing in the pranthesis with "powershell -c (New-Object Media.SoundPlayer 'speech.mp3').PlaySync() for windows operating system"

os.remove("speech.mp3")

