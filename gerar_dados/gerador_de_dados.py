import argparse
import pandas as pd
from faker import Faker
import random
import json

fake = Faker("pt_BR")

# Função para gerar dados de clientes
def gerar_clientes(quantidade=100):

  clientes = []
  for _ in range(quantidade):

    data_cadastro = fake.date_between(start_date="-4y", end_date="today")
    atualizado_em = fake.date_between(start_date=data_cadastro, end_date="today")

    clientes.append({
      "cliente_id": fake.uuid4(),
      "nome": fake.name(),
      "email": fake.email(),
      "celular": fake.phone_number(),
      "sexo": random.choice(["Masculino", "Feminino"]),
      "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=60),
      "documento": fake.cpf(),
      "cidade": fake.city(),
      "estado": fake.estado_sigla(),
      "cep": fake.postcode(),
      "endereco": fake.street_address(),
      "data_cadastro": data_cadastro,
      "atualizado_em": atualizado_em
    })
  return pd.DataFrame(clientes)

# Função para gerar produtos a partir de um arquivo JSON
def carregar_produtos(arquivo="produtos.json"):
  with open(arquivo, "r", encoding="utf-8") as f:
    produtos = json.load(f)
  return pd.DataFrame(produtos)

# Função para gerar pedidos com base nos clientes existentes
def gerar_pedidos(clientes, produtos, quantidade=100):

  clientes_ids = clientes["cliente_id"].tolist()
  pedidos = []

  for _ in range(quantidade):
    pedido_id = fake.uuid4()
    status = random.choices(
      ["Entregue", "Cancelado"],
      weights=[90, 10],
      k=1
    )[0]
    if status == "Entregue":
      codigo_rastreio = fake.bothify(text="BR##########")
      transportadora = random.choice([
        "Correios",
        "Loggi",
        "Jadlog",
        "Total Express"
      ])
      prazo_entrega_dias = random.randint(2, 10)
    else:
      codigo_rastreio = None
      transportadora = None
      prazo_entrega_dias = None
    
    forma_pagamento = random.choices(
      ["PIX", "Cartão de Crédito", "Cartão de Débito"],
      weights=[35, 40, 15],
      k=1
    )[0]

    if forma_pagamento == "PIX":
      pix_qr_code = fake.uuid4()
    else:
      pix_qr_code = None

    pedidos.append({
      "pedido_id": pedido_id,
      "cliente_id": random.choice(clientes_ids),
      "data_pedido": fake.date_time_between("-4y", "now"),
      "forma_pagamento": forma_pagamento,
      "pix_qr_code": pix_qr_code,
      "status": status,
      "canal": random.choices(
        ["Site", "Marketplace", "Aplicativo"],
        weights=[50, 20, 30],
        k=1
      )[0],
      "origem": random.choices(
        ["Orgânico", "Google Ads", "Instagram", "Facebook", "E-mail Marketing"],
        weights=[40, 20, 15, 15, 10],
        k=1
      )[0],
      "transportadora": transportadora,
      "codigo_rastreio": codigo_rastreio,
      "prazo_entrega_dias": prazo_entrega_dias,
      "valor_total": 0
    })

  pedidos = pd.DataFrame(pedidos)

  itens_pedido = gerar_itens_pedido(pedidos, produtos)

  pedidos = atualizar_valor_total_pedidos(
      pedidos,
      itens_pedido
  )

  return pedidos, itens_pedido

def gerar_itens_pedido(pedidos, produtos):
  produtos = produtos.to_dict("records")
  itens = []

  for pedido_id in pedidos["pedido_id"]:
    quantidade_produtos = random.randint(1, 3)
    produtos_pedido = random.sample(produtos, quantidade_produtos)
    for produto in produtos_pedido:
      quantidade = random.randint(1, 2)
      subtotal = quantidade * produto["preco"]
      itens.append({
        "item_id": fake.uuid4(),
        "pedido_id": pedido_id,
        "produto_id": produto["produto_id"],
        "quantidade": quantidade,
        "valor_unitario": produto["preco"],
        "subtotal": round(subtotal, 2)
      })
  return pd.DataFrame(itens)

def atualizar_valor_total_pedidos(pedidos, itens_pedidos):
  totais = (itens_pedidos.groupby("pedido_id")["subtotal"].sum())
  pedidos["valor_total"] = (pedidos["pedido_id"].map(totais).fillna(0).round(2))
  return pedidos

# Função para salvar os dados em diferentes formatos
def salvar_dados(df: pd.DataFrame, out: str, fmt: str):
  if fmt == "csv":
    df.to_csv(out, index=False, encoding="utf-8-sig")
  elif fmt == "excel":
    df.to_excel(out, index=False)
  elif fmt == "json":
    df.to_json(out, orient="records", indent=4, date_format="iso")
  else:
    raise ValueError(f"Formato de saída '{fmt}' não suportado. Use 'csv', 'excel' ou 'json'.")

def main():
  parser = argparse.ArgumentParser(description="Gerador de Dados v1.0")
  subparsers = parser.add_subparsers(dest="tipo", required=True)
  # Clientes
  parser_clientes = subparsers.add_parser("clientes", help="Gerar dados de clientes")
  parser_clientes.add_argument("--quantidade", type=int, default=100)
  parser_clientes.add_argument("--arquivo", default="clientes.csv")
  parser_clientes.add_argument("--formato", choices=["csv", "excel", "json"], default="csv")
  # Produtos
  parser_produtos = subparsers.add_parser("produtos", help="Gerar dados de produtos")
  parser_produtos.add_argument("--arquivo", default="produtos.csv")
  parser_produtos.add_argument("--formato", choices=["csv", "excel", "json"], default="csv")
  # Pedidos
  parser_pedidos = subparsers.add_parser("pedidos", help="Gerar dados de pedidos")
  parser_pedidos.add_argument("--quantidade", type=int, default=100)
  parser_pedidos.add_argument("--clientes", default="clientes.csv", help="Arquivo de clientes")
  parser_pedidos.add_argument("--arquivo-pedidos", default="pedidos.csv")
  parser_pedidos.add_argument("--arquivo-itens", default="itens_pedido.csv")
  parser_pedidos.add_argument("--formato", choices=["csv", "excel", "json"], default="csv")

  args = parser.parse_args()

  if args.tipo == "clientes":
    clientes = gerar_clientes(args.quantidade)
    salvar_dados(clientes, args.arquivo, args.formato)
  elif args.tipo == "produtos":
    produtos = carregar_produtos()
    salvar_dados(produtos, args.arquivo, args.formato)
  elif args.tipo == "pedidos":
    clientes = pd.read_csv(args.clientes)
    produtos = carregar_produtos()
    pedidos, itens_pedido = gerar_pedidos(clientes, produtos, args.quantidade)
    salvar_dados(pedidos, args.arquivo_pedidos, args.formato)
    salvar_dados(itens_pedido, args.arquivo_itens, args.formato)

if __name__ == "__main__":
    main()
