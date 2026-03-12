"""
    Módulo de configuração da aplicação.

    Responsável por carregar variáveis de ambiente a partir
    do arquivo .env, utilizadas para autenticação e configuração
    de serviços externos como o Google Cloud e o BigQuery.
"""

from dotenv import load_dotenv
import os

# Carrega as variáveis definidas no arquivo .env para o ambiente da aplicação.
load_dotenv()

# Caminho para o arquivo de credenciais do Google Cloud
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# ID do projeto no Google Cloud onde o BigQuery está configurado
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

# Nome do dataset no BigQuery que armazena as tabelas do projeto
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")