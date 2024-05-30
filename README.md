# Web Scrapping para Download de artigos
Essa automação acessa o site International Journal of Serious Games (https://journal.seriousgamessociety.org/index.php/IJSG), entra no tópico de arquivos (campo Archives), entra em cada um dos volumes (campo Volumes) de todas as páginas de arquivos e faz download dos artigos/editoriais em arquivos .pdf disponíveis no site de forma simultânea. Além disso, o programa cria automaticamente uma pasta para armazenar os arquivos (files) e durante a execução é gerado um arquivo .txt com uma lista dos títulos dos artigos e editoriais baixados.

Obs: O programa funciona de forma assíncrona para acelerar e agilizar o processo de download.

# Módulos
- aiohttp: Biblioteca do python para fazer requisições HTTP cliente/servidor de forma assíncrona;
- asyncio: Biblioteca do python para escrever código assíncrono e concorrente usando "async" e "await";
- beautifulsoup4: Biblioteca leve do python para automação de informações web com parseador HTML;
- python-dotenv: Bilioteca do python ler variáveis de ambiente no arquivo .env

# Comandos
Obs: Execute esses comandos na raiz do projeto.

- Renomear o arquivo .env.example para .env (manualmente ou com o comando)
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
    <img src="https://github.com/lucasharzer/Download_Artigos/assets/85804895/1ae439cb-aa62-48bd-b725-25e25145a004">
</span>
