# Pipeline  de Dados com Python, DBT e BigQuery

Projeto de Engenharia de Dados desenvolvido para simular um ambiente de análise em nuvem  de um e-commerce utilizando **Python**, **Faker**, **Docker**, **dbt** e **Google BigQuery**.

O projeto contempla desde a geração de dados sintéticos até a construção de um Data Warehouse analítico, incluindo modelagem dimensional, criação de relatórios e KPIs para apoio à tomada de decisão.

---

## Tecnologias utilizadas

- Python 3.11
- Docker
- dbt Core
- Google BigQuery
- SQL

---

## Funcionalidades

- Geração de dados sintéticos utilizando Faker em CSV ou JSON.
- Carga inicial para o Google BigQuery com script python.
- Construção de Data Warehouse em camadas.
- Modelagem dimensional utilizando dbt.
- Criação de relatórios analíticos.
- Desenvolvimento de KPIs de negócio.

---

# Geração de dados

Os dados utilizados foram gerados utilizando python e a biblioteca Faker.

O script permite gerar:

- Clientes
- Produtos
- Pedidos
- Itens dos pedidos

Características:

- Quantidade de registros configurável.
- Produtos carregados a partir de um arquivo JSON.
- Exportação em CSV ou JSON.

Os pedidos são gerados de forma a simular um ambiente real de e-commerce, incluindo informações como:

- Status do pedido
- Forma de pagamento
- Canal de venda
- Origem da venda
- Transportadora
- Código de rastreio
- Prazo de entrega
- Valor total do pedido

---

## Ambiente Docker

O ambiente do projeto é executado em um container Docker baseado em:

- Python 3.11
- dbt Core 1.8.8
- dbt-bigquery 1.8.3

O Dockerfile prepara um ambiente contendo todas as dependências necessárias para executar o projeto dbt, evitando diferenças entre ambientes de desenvolvimento.

---

# Arquitetura do Projeto

O pipeline foi desenvolvido seguindo uma arquitetura em camadas utilizando o dbt.

```text
Dados Sintéticos
        │
        ▼
      RAW
        │
        ▼
    STAGING
        │
        ▼
 INTERMEDIATE
        │
        ▼
      MARTS
   ├── CORE
   ├── REPORTS
   └── KPIs
```

---

## Camada RAW

A camada **Raw** recebe os dados gerados pelo script Python através de uma carga inicial no Google BigQuery.
Depois será automatizado a inserção de novos registros através do serviço Cloud Run.

Essa camada representa os dados em seu estado original, sem qualquer transformação.

---

## Camada STAGING

Responsável pela padronização e tratamento inicial dos dados.

Nesta etapa são realizadas atividades como:

* seleção das colunas relevantes;
* padronização dos tipos de dados;
* limpeza de informações;
* renomeação de campos;
* preparação dos dados para as próximas etapas do pipeline.

---

## Camada INTERMEDIATE

Nesta camada são implementadas regras de negócio, agregações e enriquecimento dos dados.

Os modelos desenvolvidos são:

| Modelo                         | Objetivo                                                                                           |
| ------------------------------ | -------------------------------------------------------------------------------------------------- |
| `int_cliente_metricas`         | Consolida métricas por cliente, como quantidade de pedidos, valor gasto, primeira e última compra. |
| `int_pedido_valores`           | Calcula os valores consolidados de cada pedido.                                                    |
| `int_produto_metricas`         | Consolida métricas agregadas por produto.                                                          |
| `int_itens_pedidos_detalhados` | Enriquece os itens do pedido através da junção entre pedidos, clientes e produtos.                 |

---

## Camada MARTS

A camada **Marts** representa a camada analítica utilizada pelos analistas.

Ela está dividida em três grupos.

## Core

Responsável pela modelagem dimensional do Data Warehouse.

Os modelos disponíveis são:

* `dim_cliente`
* `dim_produto`
* `dim_data`
* `fato_venda`

Esses modelos representam a fonte oficial para consultas analíticas e construção de dashboards.

---

## Reports

Contém consultas recorrentes utilizadas na construção de relatórios de negócio.

Exemplos:

* Clientes ativos nos últimos 90 dias;
* Receita por categoria;
* Receita por origem;
* Vendas da última semana;
* Vendas dos últimos 30 dias.

Esses modelos disponibilizam consultas prontas para consumo por ferramentas de Business Intelligence.

---

## KPIs

Contém indicadores de desempenho utilizados para monitoramento da saúde do negócio.

Entre os KPIs desenvolvidos estão:

* Receita Total;
* Ticket Médio;
* Clientes Ativos;
* Novos Clientes do Mês;
* Categoria Mais Vendida;
* Taxa de Cancelamento;
* Receita MTD Comparativa;
* Receita YTD Comparativa.

Esses modelos retornam indicadores prontos para utilização em dashboards executivos.

---

# Documentação

O projeto utiliza o **dbt Docs**, permitindo visualizar:

* documentação dos modelos;
* documentação das colunas;
* dependências entre modelos;
* Data Lineage completo do pipeline.

---

# Próximos Passos

* Ampliação dos testes automatizados do dbt;
* Automatização da carga de dados;
* Passar a executar o dbt no docker na núvem ao invés localmente.

---

# Autor

**Gregory Nicholas Mayer**

