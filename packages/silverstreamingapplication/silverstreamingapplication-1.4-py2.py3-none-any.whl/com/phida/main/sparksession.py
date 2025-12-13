from pyspark.sql import SparkSession

from com.phida.main import logging

spark = (SparkSession.builder
         .getOrCreate())

logger = logging.Log4j(spark)
