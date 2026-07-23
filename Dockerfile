FROM python:3.11-slim

LABEL maintainer="Gregory"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    vim \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /projeto
VOLUME /projeto

# Criando um diretório de trabalho
WORKDIR /projeto

# Instalando DBT e adaptador para o BigQuery
RUN pip install dbt-core==1.8.8
RUN pip install dbt-bigquery==1.8.3

# Expor a porta
EXPOSE 8080

# Definir o comando padrão para execução quando o container for iniciado
CMD ["/bin/bash"]
