FROM jupyter/pyspark-notebook:spark-3.4.1

# COPY notebooks/example.ipynb .
USER root
RUN mkdir -p /var/lib/apt/lists/partial && \
    chmod -R 775 /var/lib/apt/lists && \
    apt-get update && apt-get install -y openjdk-8-jdk


RUN pip install delta-spark==2.4.0
RUN pip install deltalake
RUN pip install jupyterlab 
RUN pip install pandas
RUN pip install pyspark==3.4.1

ARG NB_USER=jovyan
ARG NB_UID=1000
ARG NB_GID=100

ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}
RUN groupadd -f ${USER} && \
    chown -R ${USER}:${USER} ${HOME}

USER ${NB_USER}

RUN export PACKAGES="io.delta:delta-core_2.12:0.7.0"
RUN export PYSPARK_SUBMIT_ARGS="--packages ${PACKAGES} pyspark-shell"

# Copy your Spark job script into the container
COPY job.py /opt/spark/work-dir/

# Set the working directory
WORKDIR /opt/spark/work-dir

# Command to run your Spark job
CMD ["spark-submit", "--master", "local[*]", "job.py"]
