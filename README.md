# Web Scrapping para Download de artigos
Essa automação acessa o site International Journal of Computer Games Technology (https://www.hindawi.com/journals/ijcgt), entra no tópico de conteúdos (campo Table of Contents), acessa todas as páginas de arquivos e faz download dos artigos em arquivos .pdf disponíveis no site de forma simultânea. Além disso, o programa cria automaticamente uma pasta para armazenar os arquivos (files) e durante a execução é gerado um arquivo .txt com uma lista dos títulos dos artigos baixados.

Obs: O programa funciona de forma assíncrona para acelerar e agilizar o processo de download. Exceto as requisições para acessar o site que é feita de forma síncrona, utilizando um header com User-Agent e com uma espera de 3 segundos entre as requisições para evitar problemas de conexão ou rejeição do site.

# Módulos
- aiohttp: Biblioteca do python para fazer requisições HTTP cliente/servidor de forma assíncrona;
- asyncio: Biblioteca do python para escrever código assíncrono e concorrente usando "async" e "await";
- beautifulsoup4: Biblioteca leve do python para automação de informações web com parseador HTML;
- requests: Biblioteca simples do python para fazer requisições HTTP.

# Comandos
- Instalação de dependências
```bash
pip install -r requirements.txt
```
- Execução do script
```bash
python main.py
```
