#!/bin/bash

# Chemin d'accès au répertoire d'installation de Spark
SPARK_HOME=/opt/bitnami/spark

# Démarrer le serveur d'historique Spark
$SPARK_HOME/sbin/start-history-server.sh

# Afficher le message de démarrage
echo "Spark History Server started."
