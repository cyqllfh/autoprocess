# from pyspark import SparkContext
# from pyspark.sql import SQLContext
#
# if __name__ == "__main__":
#     sc = SparkContext(appName="TestJson")
#     sqlContext = SQLContext(sc)
#     jsons = sqlContext.read.json("hdfs://master1:9000/chu/nuomi_20160516180247653497.json")
#     jsons.printSchema()
#     #rows = jsons.flatMap(lambda line: [line.name[0], line.link[0], line.cinema[0], line.g_price, line.b_price])
#     rows = jsons.map(lambda line: (
#         line.name[0].encode('utf8'),
#         line.cinema[0].encode('utf8'),
#         line.link[0].encode('utf8'),
#         line.g_price[0].encode('utf8') if line.g_price else '1000',
#         line.b_price[0].encode('utf8') if line.b_price else '1000'))\
#         .groupBy(lambda line: line[0])\
#         .sortBy(lambda line: float(line[4])).map(lambda line: '%s\t%s\t%s\t%s\t%s' % line)
#
#     rows.saveAsTextFile("hdfs://master1:9000/chu/result")
#
#     sc.stop()
from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.sql import SQLContext

def f(x):
    min_price, it = 1000, None
    value_list = [item for item in x]
    for item in x:
        if float(item[4]) < min_price:
            min_price = float(item[4])
            it = item
    return it


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: wordcount <input> <output>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="ComputeNuomi")
    sqlContext = SQLContext(sc)
    jsons = sqlContext.read.json(sys.argv[1])
    jsons.printSchema()
    rows = jsons.map(lambda line: (
        line.name[0],
        line.cinema[0],
        line.link[0],
        line.g_price[0] if line.g_price else '1000',
        line.b_price[0] if line.b_price else '1000')) \
        .groupBy(lambda line: line[0]) \
        .mapValues(f) \
        .map(lambda line: '%s\t%s\t%s\t%s\t%s' % line[1])
    rows.saveAsTextFile(sys.argv[2])
    sc.stop()