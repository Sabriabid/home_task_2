from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp
import uuid

def ingest_csv_to_deltalake(file_path, has_header=True):
    spark = SparkSession.builder \
        .appName("CSV to DeltaLake Ingestion Job") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:0.8.0") \
        .getOrCreate()

    # Lecture du CSV avec ou sans en-tête
    df = spark.read.option("header", has_header).csv(file_path)

    # Ajout des colonnes supplémentaires
    df = df.withColumn("ingestion_tms", current_timestamp().cast("timestamp").alias("ingestion_tms")) \
           .withColumn("batch_id", lit(str(uuid.uuid4())))

    # Écriture dans DeltaLake en mode append
    df.write.format("delta").mode("append").save("/data/table")

    spark.stop()

# Exemple d'utilisation
ingest_csv_to_deltalake("test.csv", True)
