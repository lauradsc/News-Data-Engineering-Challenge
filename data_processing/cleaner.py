"""
    Módulo responsável pela limpeza e extração de texto a partir
    do HTML bruto das páginas de notícias.

    Utiliza a biblioteca Readability para identificar o conteúdo
    principal do artigo e o BeautifulSoup para remover tags HTML,
    retornando apenas o texto limpo.
"""

from readability import Document
from bs4 import BeautifulSoup


def clean_html(html):
    """
        Remove elementos irrelevantes do HTML como anúncios, menus e scripts.
        
        Args: 
            html: conteúdo HTML da página.
        Returns: 
            Texto limpo contendo apenas o conteúdo principal do artigo.
    """
    
    doc = Document(html)
    
    cleaned_html = doc.summary()
    
    soup = BeautifulSoup(cleaned_html, "html.parser")
    
    text = soup.get_text(separator=" ")
    
    return text.strip()
    