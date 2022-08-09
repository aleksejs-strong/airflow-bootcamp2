from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import sys

def init_spark():
  spark = SparkSession.builder.appName("air-quality-data-partitioning").getOrCreate()
  sc = spark.sparkContext
  return spark,sc

def main():
  spark,sc = init_spark()
  source = sys.argv[1]
  target = sys.argv[2]
  print("Source: {}".format(source))
  print("Target: {}".format(target))
  df = spark.read.option("header", True).option("delimiter", ";").csv(source)
  df.show()
  df.printSchema()

  df_filtered = df.filter(col("Measurement Year") > "2015")

  df_filtered.write.option("header", True).partitionBy("Measurement Year").mode("overwrite").csv(target)


if __name__ == '__main__':
  main()