import os
import pandas as pd
import streamlit as st
import json
from google.cloud import bigquery

st.set_page_config(
    page_title="APP export",
    page_icon="📊",
    layout="wide",  # Habilita o Wide Mode
    initial_sidebar_state="expanded"  # Opções: "expanded", "collapsed", "auto"
)


# Lê o JSON da variável de ambiente e salva como arquivo temporário
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

with open("temp_cred.json", "w") as f:
    json.dump(creds_dict, f)

# Autenticação BigQuery via JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_cred.json"

# Cliente BigQuery
client = bigquery.Client()

lojas = [
    "ARES MOTOS - JUAZEIRO",
    "ARES MOTOS - BREJO SANTO",
    "ARES MOTOS - IGUATU",
    "ARES MOTOS - ICÓ",
    "ARES MOTOS - CAMPO SALES",
    "ARES MOTOS - CRATO",
    "ARES MOTOS - JAGUARIBE",
    "ARES MOTOS - TIANGUÁ",
    "ARES MOTOS - IPU",
    "ARES MOTOS - ITAPAJE",
    "ARES MOTOS - ITAPIPOCA",
    "ARES MOTOS - PARAIPABA",
    "ARES MOTOS - VIÇOSA",
    "ARES MOTOS - SALVADOR",
    "ARES MOTOS - ACM",
    "ARES MOTOS - CALÇADA",
    "ARES MOTOS - LITORAL",
    "ARES MOTOS - SIMOES FILHO",
    "NOVA ONDA - IGUATU",
    "NOVA ONDA - LIMOEIRO",
    "NOVA ONDA - ARACATI",
    "TERRA SANTA - BYD",
    "TERRA SANTA - NATAL",
    "TERRA SANTA - MOSSORÓ",
    "TERRA SANTA - ARACAJU",
    "TERRA SANTA - JUAZEIRO",
    "TERRA SANTA - JUAZEIRO",
    "TERRA SANTA - RENAULT",
    "TERRA SANTA SEMINOVOS - NATAL",
    "TERRA SANTA SEMINOVOS - JUAZEIRO",
    "TERRA SANTA - CANINDÉ",
    "ARES MOTOS - CRUZ DAS ALMAS",
    "ARES MOTOS - VALENÇA"
]

st.title("Consulta BigQuery com Filtros")

# Filtros de entrada
dta_inicio = st.date_input("Data Início")
dta_fim = st.date_input("Data Fim")
opcao_estado = st.selectbox("Novo ou Usado", ["Todos", "NOVO", "USADO"])
loja = st.selectbox("Selecione a loja:", lojas)

# Botão para gerar
if st.button("Gerar"):

    # Montagem dinâmica do WHERE
    where_clauses = []
    if dta_inicio and dta_fim:
        where_clauses.append(f"DATE(dta_entrada_saida) BETWEEN DATE('{dta_inicio}') AND DATE('{dta_fim}')")

    if opcao_estado != "Todos":
        where_clauses.append(f"Novo_Usado_CC = '{opcao_estado}'")

    if loja:
        where_clauses.append(f"Loja = '{loja}'")

    # Unir os filtros
    where_sql = " AND ".join(where_clauses)
    if where_sql:
        where_sql = "WHERE " + where_sql

    # Query final
    query = f"""
        SELECT Loja, nome_Vend, modelo, tipo_transacao, dta_entrada_saida, QTE, val_total, FRETE, valdesconto, val_custo, val_pis, val_cofins, val_icms, BONUS_TRADEIN, BONUS_MONTADORA, BONUS_VAREJO, Bonus_CaixaDagua, REBATE, cliente, nome_CLI, cidade, numero_nota_fiscal, serie_nota_fiscal, chassi
        FROM `delivery.drvy_VeiculosVendas`
        {where_sql}
    """

    # Execução da consulta
    df = client.query(query).to_dataframe()

    # Exibição
    st.success(f"{len(df)} registros encontrados.")
    st.dataframe(df, use_container_width=True)