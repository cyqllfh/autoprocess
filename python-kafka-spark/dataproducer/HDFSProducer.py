import sys
from kafka import KafkaProducer
from kafka.errors import KafkaError

def produce_message(filename):
    producer = KafkaProducer(bootstrap_servers=['192.168.1.13:9092'])

    # Asynchronous by default
    value = '/opt/nuomi/' + filename
    future =producer.send('hdfs', key=b'upload', value=value)
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        pass

    # Successful result returns assigned partition and offset
    print (record_metadata.topic)
    print (record_metadata.partition)
    print (record_metadata.offset)


if __name__=='__main__':
    filename = sys.argv[1]
    produce_message(filename)
