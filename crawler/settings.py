import sys
import os

# Permite que o Scrapy importe módulos das pastas 'bigquery' e 'config'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

BOT_NAME = "crawler"

# Localização das spiders (scripts de coleta)
SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

# Ignora o robots.txt para garantir a coleta no ambiente de teste
ROBOTSTXT_OBEY = False

# Configurações de Cortesia: Evita sobrecarregar o site e ser bloqueado
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Garante a codificação correta de acentos e caracteres especiais
FEED_EXPORT_ENCODING = "utf-8"

# Pipeline que envia os dados coletados diretamente para o BigQuery
ITEM_PIPELINES = {
    "crawler.pipelines.BigQueryPipeline": 300,
}