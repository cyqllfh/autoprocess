import os
from kafka import KafkaConsumer

if __name__ == "__main__":
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer('spark',
                             group_id='my-group',
                             bootstrap_servers=['192.168.1.15:9092'])
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                              message.offset, message.key,
                                              message.value))
        if "deal" in message.key:
            result = message.value[:-5] + '_result'
            deal_cmd = "/opt/spark/bin/spark-submit --master yarn-client /opt/code/python/SparkNuomiDealer.py " \
                       + message.value \
                       + ' ' + result
            print deal_cmd
            os.system(deal_cmd)