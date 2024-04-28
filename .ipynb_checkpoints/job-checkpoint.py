from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp
import uuid

def ingest_csv_to_deltalake(file_paths, has_header=True):
    spark = SparkSession.builder \
        .appName("CSV to DeltaLake Ingestion Job") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.HDFSLogStore") \
        .getOrCreate()

    for file_path in file_paths:
        full_path = f"/opt/spark/work-dir/{file_path}"
        print("Attempting to read from:", full_path)
        df = spark.read.option("header", has_header).csv(full_path)

        df = df.withColumn("ingestion_tms", current_timestamp()) \
               .withColumn("batch_id", lit(str(uuid.uuid4())))

        df.write.format("delta").mode("append").save("/data/delta_table")
        delta_df = spark.read.format("delta").load("/data/delta_table")
        delta_df.show()

    spark.stop()

if __name__ == "__main__":
    file_paths = ["test.csv"]
    ingest_csv_to_deltalake(file_paths, has_header=True)
