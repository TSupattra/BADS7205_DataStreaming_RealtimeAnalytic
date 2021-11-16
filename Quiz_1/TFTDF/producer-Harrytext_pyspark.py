from confluent_kafka import Producer
import time

p = Producer({'bootstrap.servers': 'localhost:9092,localhost:9192,localhost:9292'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {}'.format(msg.value().decode('utf-8')))
        
        

file1 = open('book.txt', 'r', encoding="utf8") 
Lines = file1.readlines()
for data in Lines:
 
    p.poll(0)

   
    sendMsg = data.encode().decode('utf-8').strip('\n')
    p.produce('my-first-topic', sendMsg , callback=delivery_report)
        
    time.sleep(0)

   

        
        
p.flush()