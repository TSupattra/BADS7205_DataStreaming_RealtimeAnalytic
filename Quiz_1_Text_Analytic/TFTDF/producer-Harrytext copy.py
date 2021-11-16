from confluent_kafka import Producer
import time
from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))
# print(stop_words)
from nltk.tokenize import word_tokenize 

p = Producer({'bootstrap.servers': 'localhost:9092,localhost:9192,localhost:9292'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {}'.format(msg.value().decode('utf-8')))
        
i =0      
counter_page = 1
file1 = open('book.txt', 'r', encoding="utf8") 
Lines = file1.readlines()
Temp = ""

def Punc(test_str):
    punc = '''!()-[]{};:'"\,<>/?@#$%^&*_~’“”'''
    for ele in test_str:
        if ele in punc:
            test_str = test_str.replace(ele, "  ")
        
    return test_str.lower()

def stop_word(sentence):
    filtered_sent=[]
    # sentence = "Let's see how it's working."
    tokenized_sent = Punc(sentence.lower()).split(' ')
    # print(tokenized_sent)

    for w in tokenized_sent:
        if w.strip('\n') not in stop_words:
            filtered_sent.append(w)
    # print("Tokenized Sentence:",tokenized_sent)
    # print("Filterd Sentence:",filtered_sent)
    return ' '.join(filtered_sent)


for data in Lines:
 
    p.poll(0)
    time.sleep(0)
    if "Page |" not in data:
        Temp = Temp+stop_word(data)
        Temp =Temp.replace('\n',' ')
   
    else:
        sendMsg = Temp.encode().decode('utf-8').strip('\n')
        p.produce('testtopic', sendMsg , callback=delivery_report)
        print(f'Page {counter_page}')
        counter_page+=1
        Temp = ""
        i=i+1
        time.sleep(1) 
    if i == 5:
        break   
        
p.flush()