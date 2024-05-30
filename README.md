# Web Scrapping para Download de artigos
Essa automação acessa o site International Journal of Computer Games Technology (https://www.hindawi.com/journals/ijcgt), entra no tópico de conteúdos (campo Table of Contents) que já abrange todos os artigos, acessa todas as páginas de arquivos e faz download dos artigos em arquivos .pdf disponíveis no site de forma simultânea. Além disso, o programa cria automaticamente uma pasta para armazenar os arquivos e durante a execução é gerado um arquivo .txt com uma lista dos títulos dos artigos baixados.

Obs: O programa funciona de forma assíncrona para acelerar e agilizar o processo de download. Exceto as requisições para acessar o site que é feita de forma síncrona, utilizando um header com User-Agent e com uma espera de 3 segundos entre as requisições para evitar problemas de conexão ou rejeição do site.

# Módulos
- `aiohttp`: Biblioteca do python para fazer requisições HTTP cliente/servidor de forma assíncrona;
- `asyncio`: Biblioteca do python para escrever código assíncrono e concorrente usando "async" e "await";
- `beautifulsoup4`: Biblioteca leve do python para automação de informações web com parseador HTML;
- `python-dotenv`: Biblioteca do python para ler variáveis de ambiente do arquivo `.env`;
- `requests`: Biblioteca simples do python para fazer requisições HTTP.

# Comandos
Obs: Execute esses comandos na raiz do projeto. Após renomear o arquivo `.env.example`, pode modificar as variáveis FOLDER e TITLE para o nome que preferirem exceto a variável LINK.

- Renomear o arquivo `.env.example` para `.env` (manualmente ou com comando)
```bash
ren .env.example .env
```
- Instalação de dependências
```bash
pip install -r requirements.txt
```
- Execução do script
```bash
python main.py
```

# Resultados
Demonstração da execução do programa no terminal, pasta de downloads e arquivo de títulos: 

<span>
    <img src="https://github.com/lucasharzer/Download_Artigos/assets/85804895/4a6d25a0-e921-453b-acac-e095d24d447b">
</span>
