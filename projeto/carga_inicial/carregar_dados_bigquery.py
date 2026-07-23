# Bibliotecas
from google.cloud import bigquery
import os

# Configurações
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../chave/projeto-loja-x-126b309b3360.json"
project_id = "projeto-loja-x"
dataset_id = "raw"

# Diretório onde os arquivos CSV estão salvos
csv_directory = "dados" 

# Inicializa o cliente do BigQuery
client = bigquery.Client(project=project_id)

# Função para criar o dataset (banco de dados) se ele não existir
def cria_dataset(dataset_id):
    # Nome do projeto e do dataset no BigQuery
    dataset_ref = f"{project_id}.{dataset_id}"
    # Define o dataset
    dataset = bigquery.Dataset(dataset_ref)
    # Você pode ajustar a região conforme necessário
    dataset.location = "US"  
    try:
        client.get_dataset(dataset_ref)  # Verifica se o dataset já existe
        print(f"Dataset '{dataset_id}' já existe.")
    except Exception:
        # Se não existir, cria o dataset
        dataset = client.create_dataset(dataset)
        print(f"Dataset '{dataset_id}' criado com sucesso.")

# Função para carregar cada CSV como uma tabela no BigQuery
def carrega_bigquery(table_name, csv_file_path):
    # Define o nome da tabela
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    # Configuração do job de carregamento
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True
    )
    with open(csv_file_path, "rb") as file:
        load_job = client.load_table_from_file(file, table_id, job_config=job_config)
        load_job.result()
    print(f"Tabela {table_name} criada com sucesso.")

# Primeiro, cria o dataset se ele ainda não existir
cria_dataset(dataset_id)

# Arquivos CSV e nomes das tabelas correspondentes
csv_files = {
    "raw_clientes": os.path.join(csv_directory, "raw_clientes.csv"),
    "raw_produtos": os.path.join(csv_directory, "raw_produtos.csv"),
    "raw_pedidos": os.path.join(csv_directory, "raw_pedidos.csv"),
    "raw_itens_pedido": os.path.join(csv_directory, "raw_itens_pedido.csv"),
}
# Carrega cada CSV no BigQuery
for table_name, csv_file_path in csv_files.items():
    carrega_bigquery(table_name, csv_file_path)