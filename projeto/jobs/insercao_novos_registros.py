# Bibliotecas
from datetime import date, datetime
import random
import json
from faker import Faker
from google.cloud import bigquery

fake = Faker("pt_BR")
bq_cliente = bigquery.Client()

# Gerar novos clientes
def gerar_clientes():
  quantidade = random.randint(4, 10)
  clientes = []

  for _ in range(quantidade):
    clientes.append(
      {
        "cliente_id": fake.uuid4(),
        "nome": fake.name(),
        "email": fake.email(),
        "celular": fake.phone_number(),
        "sexo": random.choice(
            ["Masculino", "Feminino"]
        ),
        "data_nascimento": fake.date_of_birth(
            minimum_age=18,
            maximum_age=60,
        ).isoformat(),
        "documento": fake.cpf(),
        "cidade": fake.city(),
        "estado": fake.estado_sigla(),
        "cep": fake.postcode(),
        "endereco": fake.street_address(),
        "data_cadastro": date.today().isoformat(),
        "atualizado_em": date.today().isoformat(),
      }
    )

  return clientes

# Carregar produtos do arquivo JSON
def carregar_produtos():
  with open("produtos.json", "r", encoding="utf-8") as f:
    return json.load(f)

# Gerar pedidos e itens de pedido
def gerar_pedidos(clientes, produtos):

  clientes_ids = []
  for cliente in clientes:
    clientes_ids.append(cliente["cliente_id"])

  pedidos = []

  quantidade = random.randint(5,10)

  for _ in range(quantidade):
    pedido_id = fake.uuid4()
    status = random.choices(["Entregue", "Cancelado"], weights=[90, 10], k=1)[0]
    if status == "Entregue":
      codigo_rastreio = fake.bothify(text="BR##########")
      transportadora = random.choice(["Correios", "Loggi", "Jadlog", "Total Express"])
      prazo_entrega_dias = random.randint(2,10)
    else:
      codigo_rastreio = None
      transportadora = None
      prazo_entrega_dias = None
    forma_pagamento = random.choices(["PIX", "Cartão de Crédito", "Crédito de Débito"], weights=[35,50,15], k=1)[0]
    if forma_pagamento == "PIX":
      pix_qr_code = fake.uuid4()
    else:
      pix_qr_code = None
    pedidos.append(
      {
        "pedido_id": pedido_id,
        "cliente_id": random.choice(clientes_ids),
        "data_pedido": datetime.now().isoformat(),
        "forma_pagamento": forma_pagamento,
        "pix_qr_code": pix_qr_code,
        "status": status,
        "canal": random.choices(
            ["Site","Marketplace","Aplicativo"], weights=[50, 20, 30], k=1)[0],
        "origem": random.choices(["Orgânico","Google Ads","Instagram","Facebook","E-mail Marketing"], weights=[40, 20, 15, 15, 10], k=1)[0],
        "transportadora": transportadora,
        "codigo_rastreio": codigo_rastreio,
        "prazo_entrega_dias": prazo_entrega_dias,
        "valor_total": 0
      }
    )

  itens_pedido = gerar_itens_pedido(pedidos, produtos)
  pedidos = atualizar_valor_total_pedidos(pedidos, itens_pedido)

  return pedidos, itens_pedido

def gerar_itens_pedido(pedidos, produtos):
  itens_pedido = []
  for pedido in pedidos:
    quantidade_produtos = random.randint(1,3)
    produtos_pedido = random.sample(produtos, quantidade_produtos)

    for produto in produtos_pedido:
      quantidade = random.randint(1,2)
      subtotal = (quantidade * produto["preco"])
      itens_pedido.append(
        {
          "item_id": fake.uuid4(),
          "pedido_id": pedido["pedido_id"],
          "produto_id": produto["produto_id"],
          "quantidade": quantidade,
          "valor_unitario": produto["preco"],
          "subtotal": round(subtotal, 2)
        }
      )
  return itens_pedido

# Atualizar o valor total dos pedidos com base nos itens do pedido
def atualizar_valor_total_pedidos(pedidos, itens_pedido):
  totais = {}
  for item in itens_pedido:
    pedido_id = item["pedido_id"]
    totais[pedido_id] = (totais.get(pedido_id, 0) + item["subtotal"])
  for pedido in pedidos:
    pedido["valor_total"] = round(totais.get(pedido["pedido_id"], 0), 2)
    
  return pedidos

# Função para inserir dados no BigQuery
def inserir_bigquery(json_data, tabela):
  job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
  )
  job = bq_cliente.load_table_from_json(
    json_data,
    tabela,
    job_config=job_config,
  )
  job.result()
  print(
    f"{len(json_data)} registros inseridos em {tabela}."
  )

def main():
  print("Gerando novos registros...")
  clientes = gerar_clientes()
  produtos = carregar_produtos()
  pedidos, itens_pedido = gerar_pedidos(clientes, produtos)

  inserir_bigquery(
    clientes,
    "projeto-loja-x.raw.raw_clientes",
  )

  inserir_bigquery(
    pedidos,
    "projeto-loja-x.raw.raw_pedidos"
  )

  inserir_bigquery(
    itens_pedido,
    "projeto-loja-x.raw.raw_itens_pedido"
  )

  print("Execução concluída com sucesso.")

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(f"Erro durante a execução: {e}")
    raise