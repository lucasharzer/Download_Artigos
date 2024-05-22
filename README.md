# Web Scrapping para Download de artigos
Essa automação acessa o site International Journal of Serious Games (https://journal.seriousgamessociety.org/index.php/IJSG), entra no tópico de arquivos (campo Archives), entra em cada um dos volumes (campo Volumes) de todas as páginas de arquivos e faz download dos artigos e editoriais em arquivos .pdf disponíveis no site. Além disso, o programa cria automaticamente uma pasta para armazenar os arquivos (files) e durante a execução é gerado um arquivo .txt com uma lista dos títulos dos artigos e editoriais baixados.

# Módulos
- beautifulsoup4: Biblioteca leve do python para automação de informações web com parseador HTML;
- requests: Biblioteca simples do python para requisições HTTP.

# Comandos
- Instalação de dependências
```bash
pip install -r requirements.txt
```
- Execução do script
```bash
python main.py
```
