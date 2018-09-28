import speech_recognition as sr
from nltk.corpus import stopwords


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
    for i in range(0,len(new)):
            mycursor = mydb.cursor()

            str1="select * from newtable where name="
            str2 = "\'"+str(new[i])+"\'"
            str3=str1+str2
            mycursor.execute(str3)

            myresult = mycursor.fetchone()
            print("-----------------------THE RESULT---------------------")
            print(myresult)
except:
    print("could not connect to database")


