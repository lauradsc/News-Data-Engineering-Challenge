"""
    Serviço FastAPI responsável por expor um endpoint 
    de busca que consulta artigos de notícias armazenados no BigQuery.
"""

import os

from fastapi import FastAPI
from google.cloud import bigquery
from config.config import GOOGLE_APPLICATION_CREDENTIALS

# Configuração das credenciais do Google Cloud
os.environ.setdefault(
    "GOOGLE_APPLICATION_CREDENTIALS",
    GOOGLE_APPLICATION_CREDENTIALS
)

# Inicialização da aplicação FastAPI
app = FastAPI()

# Inicialização do cliente do BigQuery
client = bigquery.Client()

@app.get("/search")
def search_articles(keyword: str):
    """
        Busca artigos contendo a palavra-chave informada.
        
        A busca é realizada nos campos 'title' e 'content' 
        da tabela de artigos já processados (articles_clean)
        armazenada no BigQuery.
        
        Args: 
            keyword (str): palavra-chave utilizada na busca.
        Returns:
            Dicionário com a chave "results", contendo 
            os artigos encontrados (título, url e conteúdo).
    """
    
    query = """
        SELECT title, url, content 
        FROM news-data-project-489813.news_dataset.articles_clean 
        WHERE 
            SEARCH(title, @keyword) 
            OR SEARCH(content, @keyword) 
        LIMIT 30
    """
    
    # Configuração da query com parâmetro 
    # Usar parâmetros evita SQL injection e melhora a segurança
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "keyword",
                "STRING",
                keyword.lower()
            )
        ]
    )

    # Executa a consulta no BigQuery
    results = client.query(query, job_config=job_config)

    # Converte os resultados da consulta em uma lista de dicionários
    articles = []

    for row in results:
        articles.append({
            "title": row.title,
            "url": row.url,
            "content": row.content
        })

    # Retorna os resultados no formato esperado pela API
    return {"results": articles}