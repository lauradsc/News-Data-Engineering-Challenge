"""
    Cliente responsável por gerenciar a comunicação com o BigQuery.

    Este módulo centraliza operações relacionadas ao banco de dados,
    como verificação de duplicidade de artigos e inserção de novos
    registros nas tabelas do dataset.
"""

import os
from google.cloud import bigquery
from config.config import GCP_PROJECT_ID, BIGQUERY_DATASET


class BigQueryClient:
    """
        Classe responsável por centralizar as operações 
        de comunicação com o BigQuery.
    """
    
    def __init__(self, project_id=GCP_PROJECT_ID, dataset=BIGQUERY_DATASET):
        """
        Inicializa cliente BigQuery.
        
        Args: 
            project_id = ID do projeto no Google Cloud.
            dataset = Dataset onde as tabelas estão armazenadas.
        """
        
        # cria conexão com o BigQuery
        self.client = bigquery.Client(project=project_id)
        
        # dataset padrão usado nas consultas
        self.dataset = dataset
        
    def article_exists(self, table, url):
        """
        Verifica se um artigo já existe na tabela com base na URL.
        
        Isso evita inserir artigos duplicados durante o processo
        de ingestão de dados.
        
        Args: 
            table: nome da tabela onde será feita a verificação.
            url: URL do artigo.
        
        Returns: 
            True se o artigo já existir, False caso contrário.
        """

        query = f"""
        SELECT COUNT(1) as total
        FROM `{self.client.project}.{self.dataset}.{table}`
        WHERE url = @url
        """

        # Parâmetro seguro para evitar SQL injection
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("url", "STRING", url)
            ]
        )

        # Executa a query
        query_job = self.client.query(query, job_config=job_config)

        result = query_job.result()

        # Verifica se a contagem é maior que zero
        for row in result:
            return row.total > 0

        return False


    def load_articles(self, table, rows):
        """
            Insere artigos no BigQuery.

        Args:
            table: nome da tabela destino.
            rows: lista de dicionários contendo os artigos.
        """

        table_id = f"{self.client.project}.{self.dataset}.{table}"

        # Envia os dados para o BigQuery
        job = self.client.load_table_from_json(
            rows,
            table_id
        )

        # Aguarda a finalização do Job
        job.result()

        print(f"{len(rows)} rows inserted into {table_id}")