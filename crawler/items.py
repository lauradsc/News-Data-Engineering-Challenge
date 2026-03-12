"""
    Definição da estrutura dos itens extraídos pelo crawler.

    Este módulo define o formato padrão dos dados coletados
    pelos spiders, garantindo consistência nas informações
    processadas pelos pipelines.
"""

import scrapy


class NewsItem(scrapy.Item):
    """
    Estrutura de dados que representa um artigo.
    """
    
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    published_at = scrapy.Field()
