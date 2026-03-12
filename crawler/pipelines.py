"""
    Pipeline do Scrapy responsável por processar os itens
    extraídos pelos spiders e enviá-los para o BigQuery.

    O pipeline também realiza verificações para evitar
    inserção de artigos duplicados na base de dados.
"""

from itemadapter import ItemAdapter
from bigquery.bigquery_client import BigQueryClient
from datetime import datetime
import uuid


class BigQueryPipeline:
    """
        Pipeline responsável por processar os itens extraídos pelo spider
        e enviá-los para o BigQuery.
        
        Também realiza uma verificação para evitar inserção de artigos duplicados.
    """
    def __init__(self):
        """
            Inicializa o cliente de conexão com o BigQuery.
        """

        # Cria instância do cliente responsável pelas operações no BigQuery
        self.bq_client = BigQueryClient(
            project_id="news-data-project-489813",
            dataset="news_dataset"
        )

    def process_item(self, item, spider):
        """
            Processa cada item extraído pelo spider.

            Etapas:
            1. Converte o item em um adapter para facilitar acesso aos campos
            2. Verifica se o artigo já existe no BigQuery
            3. Caso não exista, prepara os dados
            4. Insere o registro na tabela
        """

        # Adapta o item Scrapy para facilitar acesso aos campos
        adapter = ItemAdapter(item)

        # Obtém URL do artigo
        url = adapter.get("url")
        
        if not url:
            return item

        # Verifica se o artigo já existe na tabela
        if self.bq_client.article_exists("articles", url):
            spider.logger.info(f"Duplicate article skipped: {url}")
            return item

        # Estrutura os dados que serão enviados ao BigQuery
        row = {
            # Gera identificador único para o artigo
            "id": str(uuid.uuid4()),
            
            # Campos extraídos pelo spider
            "title": adapter.get("title"),
            "author": adapter.get("author"),
            "content": adapter.get("content"),
            "url": url,
            "published_at": adapter.get("published_at"),
            
            # Data em que o artigo foi coletado pelo crawler
            "scraped_at": datetime.utcnow().isoformat()
        }

        # envia o registro para o BigQuery
        self.bq_client.load_articles("articles", [row])

        return item