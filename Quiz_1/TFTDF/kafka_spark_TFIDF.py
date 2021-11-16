import findspark
import re
import math
findspark.init()
from operator import add

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize
# from pyspark.mllib.feature import HashingTF, IDF
from pyspark.sql.functions import *
from operator import itemgetter
import ast
from confluent_kafka import Producer
import time
stop_words=set(stopwords.words("english"))


# Num_sentence = []

# Num_word_sentence = []
# i = 0

# Tuple_sentence = ()
# Tuple_countword = ()



# def delivery_report(err, msg):
#     """ Called once for each message produced to indicate delivery result.
#         Triggered by poll() or flush(). """
#     if err is not None:
#         print('Message delivery failed: {}'.format(err))
#     else:
#         print('Message delivered to {}'.format(msg.value().decode('utf-8')))

def stop_word(sentence):
    # stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    # sentence = "Let's see how it's working."
    tokenized_sent = sentence.lower().split(' ')
    # print(tokenized_sent)

    for w in tokenized_sent:
        if w.strip('\n') not in stop_words:
            filtered_sent.append(w)
    # print("Tokenized Sentence:",tokenized_sent)
    # print("Filterd Sentence:",filtered_sent)
    return ' '.join(filtered_sent)

def update_Num_page(msg):
    global Num_sentence
    # docs = ast.literal_eval(msg)
    # print(msg)
    Num_sentence = []

    Num_word_sentence = []
 
    text = msg.replace('miss','').replace('mrs.','').replace('mr.','')
    split_sentence = text.lower().split(".")
    num_total_sen = len(text.lower().split(" "))

    # print(split_sentence)
    for s in range(len(split_sentence)) :
        st = stop_word(split_sentence[s])
        # print(st)
        Tuple_sentence = (s,st,len(st.split(' ')))
        if split_sentence[s] is not '':
            Num_sentence.append(Tuple_sentence)


def Tfidf(masseage):
    try:
        global Num_page
        # Rdd from stream
        records = masseage.collect()
        doc = records[0][1]

        update_Num_page(doc)

        # print(f'Total Sentence: {Num_sentence}')

        line = sc.parallelize(Num_sentence)
        
        #Find TF
        linecount = line.map(lambda x : (x[0] ,x[2]))#.reduceByKey(lambda x,y:x+y)
        # print(linecount.take(10))

        map_0 = line.flatMap(lambda x: [((x[0],i.strip()),1) for i in x[1].split()])
        # print(map_0.take(10))
        
        reduce = map_0.reduceByKey(lambda x,y:x+y)
        # print(reduce.take(10))
        # test = reduce.collect()

        #Find TF
        mapForTf = reduce.map(lambda x : (x[0][0],(x[0][1], x[1])))
        # print(mapForTf.take(10)) 


        #join mapForTf with linecount
        joinmapForTF_linecount = mapForTf.join(linecount)
        # print(joinmapForTF_linecount.take(10)) 

        TFcal = joinmapForTF_linecount.map(lambda x: (x[1][0][0],(x[0],x[1][0][1]/x[1][1])))
        # print(TFcal.take(10)) 


        map3 = reduce.map(lambda x: (x[0][1],(x[0][0],x[1],1))).map(lambda x:(x[0],x[1][2])).reduceByKey(lambda x,y:x+y)
        # print(map3.take(10))


        # map4 = map3.map(lambda x:(x[0],x[1][2])).reduceByKey(lambda x,y:x+y)
        # print(map4.take(10))
        # reduce2 = map4.reduceByKey(lambda x,y:x+y)
        # print(reduce2.take(10))

        # print(len(Num_sentence))
        idf = map3.map(lambda x: (x[0],math.log10((1+len(Num_sentence))/(1+x[1]))+1))
        # print(idf.take(10))

        tfidf = TFcal.join(idf)
        # print(tfidf.take(10))

        tfidf = tfidf.map(lambda x: (x[1][0][0],(x[0],x[1][0][1],x[1][1],x[1][0][1]*x[1][1]))).sortByKey()
        # print(tfidf.take(10))

        tfidf = tfidf.map(lambda x: (x[0],x[1][0],x[1][1],x[1][2],x[1][3])).sortBy(lambda a: -a[4])
        print(tfidf.take(10))

        # for_produce = tfidf.collect()
        # ms = "word :" + str(for_produce[0][1])

        # p = Producer({'bootstrap.servers': 'localhost:9092,localhost:9192,localhost:9292'})
        # sendMsg = ms.encode().decode('utf-8').strip('\n')
        # p.produce('streams-plaintext-input', sendMsg , callback=delivery_report)

        # time.sleep(1)
        # p.flush()

        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")


    
    except Exception as e:
        print(f'error: {e}')

if __name__=="__main__":
    sc = SparkContext(appName="Kafka Spark Demo")
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sc,1)

    msg = KafkaUtils.createDirectStream(ssc, topics=["testtopic"],kafkaParams={"metadata.broker.list":"localhost:9092"})
    msg.foreachRDD(Tfidf)

    ssc.start()
    ssc.awaitTermination()
