# News Data Engineering Pipeline 💻

Este projeto foi desenvolvido como parte de um desafio técnico para a vaga de Estágio em Engenharia de Dados e Analytics.

O objetivo principal foi criar um fluxo que automatiza todo o caminho da informação, desde a captura até a entrega:

Coleta: Um crawler que acessa um site de notícias e busca os artigos.

Tratamento: Limpeza do texto e extração apenas do que é importante.

Armazenamento: Envio dos dados estruturados para o Google BigQuery.

Consulta: Criação de uma API para pesquisar os artigos salvos no banco.

Esse projeto me permitiu aplicar conceitos de ciclo de vida do dado, lidando com ingestão, processamento e disponibilização (ponta a ponta).

Muito obrigado pela oportunidade! 😄
---

# Arquitetura do Projeto 🗃️

O pipeline segue o seguinte fluxo:

```
Web Scraping (Scrapy)
        ↓
Extração de artigos
        ↓
Pipeline de processamento
        ↓
Armazenamento no BigQuery
        ↓
API de busca (FastAPI)
        ↓
Consulta por palavras-chave
```

---

# Tecnologias Utilizadas

* Python
* Scrapy
* FastAPI
* Google BigQuery
* BeautifulSoup
* Readability
* Uvicorn
* dotenv

---

# Estrutura do Projeto 📁

```
news-data-engineering
│
├── api
│   └── main.py              # API de busca com FastAPI
│
├── bigquery
│   └── bigquery_client.py   # Cliente para comunicação com BigQuery
│
├── config
│   └── config.py           # Configurações e variáveis de ambiente
│
├── crawler
│   ├── items.py
│   ├── pipelines.py
│   └── spiders
│       └── news_spider.py   # Spider responsável pelo scraping
│
├── data_processing
│   └── cleaner.py           # Limpeza de HTML dos artigos
│
├── scrapy.cfg
├── requirements.txt
└── README.md
```

---

# Funcionalidades

* Coleta automática de artigos de notícias
* Extração de título, autor, conteúdo e data
* Limpeza de HTML para obter texto puro
* Armazenamento estruturado no BigQuery
* API para busca por palavras-chave

---

# Como Executar o Projeto 🖱️

## 1. Clonar o repositório

```
git clone https://github.com/seu-usuario/news-data-engineering.git
cd news-data-engineering
```

---

## 2. Criar ambiente virtual

Linux / Mac:

```
python -m venv venv
source venv/bin/activate
```

Windows:

```
python -m venv venv
venv\Scripts\activate
```

---

## 3. Instalar dependências

```
pip install -r requirements.txt
```

---

## 4. Configurar variáveis de ambiente ⚙️

Crie um arquivo `.env` na raiz do projeto:

```
GOOGLE_APPLICATION_CREDENTIALS=path/to/gcp-key.json
GCP_PROJECT_ID=seu-project-id
BIGQUERY_DATASET=news_dataset
```

---

# Executando o Web Scraper

Para coletar artigos de notícias:

```
scrapy crawl news_spider
```

O spider irá:

1. navegar pelas páginas de notícias
2. extrair links de artigos
3. coletar informações relevantes
4. enviar os dados para o BigQuery

---

# Executando a API de Busca 🔎

Inicie a API com:

```
uvicorn api.main:app --reload
```

A API ficará disponível em:

```
http://127.0.0.1:8000
```

---

# Endpoint de Busca

Buscar artigos contendo uma palavra-chave:

```
GET /search?keyword=economy
```

Exemplo:

```
http://127.0.0.1:8000/search?keyword=politics
```

Resposta esperada:

```json
{
  "results": [
    {
      "title": "Example News Title",
      "url": "https://example.com/article",
      "content": "Article content..."
    }
  ]
}
```

---

# Documentação Interativa da API

FastAPI gera documentação automaticamente:

```
http://127.0.0.1:8000/docs
```

## 📺 Demonstração (API em funcionamento)
<video src="https://github.com/user-attachments/assets/12b52753-c9cc-4076-bc9d-a0ca3f5d232c" controls="controls" style="max-width: 100%;">
</video>

---

# Estrutura dos Dados 

Cada artigo armazenado no BigQuery possui os seguintes campos:

* id
* title
* author
* content
* url
* published_at
* scraped_at

<img width="1601" height="579" alt="Captura de tela 2026-03-12 094220" src="https://github.com/user-attachments/assets/1a01e6d5-8a17-48fb-9dc9-bdcdc6456728" />
---

## Estrutura de Dados no BigQuery 

O projeto utiliza duas tabelas no BigQuery para separar diferentes etapas do pipeline de dados:

* **`articles`**: contém os dados coletados diretamente pelo crawler (camada bruta).
* **`articles_clean`**: contém os dados já processados e preparados para consulta.

Essa separação segue uma prática comum em engenharia de dados, onde os dados brutos são preservados para possibilitar reprocessamento ou auditoria, enquanto a tabela limpa é utilizada pela API de busca para garantir melhor qualidade e consistência nos resultados.

<img width="1600" height="573" alt="Captura de tela 2026-03-12 094355" src="https://github.com/user-attachments/assets/723fd512-6a5a-4a46-881e-0fd0943c3c3f" />
<img width="1598" height="721" alt="Captura de tela 2026-03-12 094444" src="https://github.com/user-attachments/assets/6aee2691-0af6-4ec1-aac4-45e7f968df0e" />

# 🚀 Próximos Passos & Melhorias

* Adicionar ranking de relevância na busca
* Implementar cache de consultas
* Expandir coleta para múltiplas fontes de notícias

---
