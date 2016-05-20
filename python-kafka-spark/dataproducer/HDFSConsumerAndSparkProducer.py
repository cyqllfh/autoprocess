import os
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError


def produce_message(filename):
    producer = KafkaProducer(bootstrap_servers=['192.168.1.13:9092'])

    # Asynchronous by default
    value = 'hdfs://master1:9000/chu/nuomi/' + filename
    future =producer.send('spark', key=b'deal', value=value)
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        pass

    # Successful result returns assigned partition and offset
    print (record_metadata.topic)
    print (record_metadata.partition)
    print (record_metadata.offset)

if __name__ == "__main__":
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer('hdfs',
                             group_id='my-group',
                             bootstrap_servers=['192.168.1.15:9092'])
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                              message.offset, message.key,
                                              message.value))
        if "upload" in message.key:
            upload_cmd = "hadoop fs -put " + message.value + " /chu/nuomi"
            os.system(upload_cmd)
            print upload_cmd
            rm_cmd = 'rm ' + message.value
            print rm_cmd
            os.system(rm_cmd)

            # produce a message
            filename = message.value.split('/')[-1]
            produce_message(filename)
