# Utiliser une image de base qui contient déjà Apache Spark
FROM bitnami/spark:3.4.3

# Copier les scripts de votre job Spark dans le conteneur
COPY job.py /opt/spark/work-dir/

# Définir le répertoire de travail
WORKDIR /opt/spark/work-dir

# Commande pour exécuter le job Spark
CMD ["spark-submit", "--master", "local[*]", "job.py"]
