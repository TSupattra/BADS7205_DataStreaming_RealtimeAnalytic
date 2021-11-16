from confluent_kafka import Consumer

c = Consumer({
    'bootstrap.servers': 'localhost:9092,localhost:9192,localhost:9292',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['streams-wordcount-output'])

# print(c)

while True:
    msg = c.poll(5)
  

    if msg is None:
        print('Received message: Harry  , 0')
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    value = msg.value()
    # print(msg.value().decode("utf-8"))
    # print(msg.key())

    if value is None:
        value = -1
    else:
        value = int.from_bytes(msg.value(), byteorder="big")

    # index_kvalue = msg.key().decode("utf-8", "ignore").find('y')
    kvalue = msg.key().decode("utf-8", "ignore")[:6]
    # print(type(value))

    print('Received message: {0} , {1}'.format(kvalue, value))
    
c.close()

