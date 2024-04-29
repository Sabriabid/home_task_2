import os
import uuid
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp

# Create Spark session
spark = SparkSession.builder \
    .appName("CSV to DeltaLake Ingestion Job") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def ingest_csv_to_deltalake(file_paths, has_header=True):
    # Ensure the output directory exists within /tmp which typically has write permissions
    output_dir = "/tmp/data/delta_table"
    ensure_directory(output_dir)

    for file_path in file_paths:
        full_path = os.path.join("/opt/spark/work-dir", file_path)
        print("Attempting to read from:", full_path)
        if not os.path.exists(full_path):
            raise Exception(f"File not found: {full_path}")

        df = spark.read.option("header", has_header).csv(full_path)

        df = df.withColumn("ingestion_tms", current_timestamp()) \
               .withColumn("batch_id", lit(str(uuid.uuid4())))

        df.write.format("delta").mode("append").save(output_dir)
        delta_df = spark.read.format("delta").load(output_dir)
        delta_df.show()

    spark.stop()

if __name__ == "__main__":
    file_paths = ["test.csv"]  # Ensure this is a list
    ingest_csv_to_deltalake(file_paths, has_header=True)
