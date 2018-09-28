import speech_recognition as sr
from nltk.corpus import stopwords
import numpy as np
import sklearn.cluster
import distance
import Levenshtein

r = sr.Recognizer()





#LISTENING TO SPEECH
try:
    with sr.Microphone() as source:
        print('What Do You Wanna Search For? LISTENING.....')
        audio = r.listen(source)
        print('Calculating')

    text = r.recognize_google(audio)

except:
    print("could not connect")





#REMOVING STOP WORDS
cachedStopWords = stopwords.words("english")
new=[]
newlist=text.split()
print(newlist)


for x in range(0,len(newlist)):
     if newlist[x] not in cachedStopWords:
        new.append(newlist[x])





#STEMMING THE WORDS
from nltk.stem.porter import PorterStemmer
stem = PorterStemmer()

def steming(word):

    stem_free_word = stem.stem(word)
    return stem_free_word

for i in range(0,len(new)):
    new[i]=steming(new[i])





#PRINTING FINAL WORD LIST
print(new)




#CREATING THE CLUSTER
words_orgn = ["classes","courses","teachers","timings"]

words = ["classes","courses","teachers","timings"]
for i in range(0,len(new)):
    words.append(new[i])
words = np.asarray(words)
lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])
affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.80)
affprop.fit(lev_similarity)





#CONNECTING TO DATABASE (MYSQL)
import mysql.connector

try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="YOURPASSWORD",
        database="test1"
    )





    #PRINTING THE OUTPUT
    for cluster_id in np.unique(affprop.labels_):
        exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(affprop.labels_ == cluster_id)])
        for i in range(0,len(cluster)):
            mycursor = mydb.cursor()
            if cluster[i] in words_orgn :
                for j in range(0,len(new)):
                    if(Levenshtein.ratio(cluster[i], new[j]) > 0.5):
                        str1="select * from newtable where name="
                        str2 = "\'"+str(cluster[i])+"\'"
                        str3=str1+str2
                        mycursor.execute(str3)
                        myresult = mycursor.fetchone()
                        if(mycursor.fetchone()!=False):
                            print("-----------------------THE RESULT---------------------")
                            print(myresult)
                        else:
                            print("Unable to find record")
except:
    print("could not connect to database")

