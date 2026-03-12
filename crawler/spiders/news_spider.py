"""
    Spider responsável por navegar pelo site de notícias da BBC,
    descobrir links de artigos e extrair informações relevantes
    como título, autor, conteúdo e data de publicação.

    Os dados coletados são enviados para o pipeline para
    processamento e armazenamento no BigQuery.
"""

import scrapy
from crawler.items import NewsItem

class NewsSpider(scrapy.Spider):
    """
        Spider Responsável por navegar pelo site de notícias,
        descobrir links de artigos e extrair informações relevantes
        como título, autor, conteúdo e data de publicação.
    """
    
    # Nome do spider usado no comando scrapy crawl
    name = "news_spider"

    # Páginas iniciais que o crawler irá visitar
    start_urls = [
        "https://www.bbc.com/news",
        "https://www.bbc.com/news/world",
        "https://www.bbc.com/news/business",
        "https://www.bbc.com/news/technology",
        "https://www.bbc.com/news/science_and_environment",
    ]

    def parse(self, response):
        """
            Método responsável por explorar páginas de listagem
            e identificar links de artigos ou outras páginas
            relevantes para continuar o crawling.
        """
        
        # Coleta todos os links da página.
        links = response.css("a::attr(href)").getall()

        for link in links:

            # Converte links relativos para links completos
            if link.startswith("/"):
                link = "https://www.bbc.com" + link

            # Se o link for de um artigo, envia para o parser de artigo
            if "/news/articles/" in link:
                yield response.follow(link, callback=self.parse_article)

            # Caso contrário, continua explorando algumas seções do site
            elif any(section in link for section in [
                "/news/world",
                "/news/business",
                "/news/technology",
                "/news/science",
            ]):
                yield response.follow(link, callback=self.parse)

    def parse_article(self, response):
        
        """
            Extrai os dados principais de um artigo individual
        """

        # Título do artigo 
        title = response.css("h1::text").get()

        # Log para acompanhar o progresso do crawler
        self.logger.info(f"Scraping article: {response.url}")

        # Conteúdo principal do artigo
        content = " ".join(response.css("article p::text").getall())

        # Ignora páginas que não possuem conteúdo
        if not content:
            return

        # Coleta possíveis nomes de autores 
        authors = response.css('[data-testid="byline-contributors"] span::text').getall()

        # Limpeza do nome dos autores
        authors = [
            a.strip() for a in authors
            if a.strip() not in [",", "and"] and "BBC" not in a
        ]

        # Junta múltiplos autores em uma única string 
        author = ", ".join(authors) if authors else None

        # Data de publicação do artigo
        published_at = response.css("time::attr(datetime)").get()

        # Cria um item do Scrapy para estruturar os dados do artigo
        item = NewsItem()
        
        # Preenche os campos do item com as informações extraídas da página
        item["title"] = title
        item["author"] = author
        item["content"] = content
        item["url"] = response.url
        item["published_at"] = published_at
        
        # Envia o item para o pipeline de processamento do Scrapy
        yield item

    # Configurações específicas deste spider
    custom_settings = {
        
        # Limita profundidade de navegação do crawler
        "DEPTH_LIMIT": 2,
        
        # Encerra após coletar 50 itens
        "CLOSESPIDER_ITEMCOUNT": 50,
        
        # Ativa controle automático de velocidade
        "AUTOTHROTTLE_ENABLED": True
    }