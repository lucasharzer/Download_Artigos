# Web Scrapping para Download de artigos
Essa automação acessa o site International Journal of Serious Games, entra no tópico de arquivos (campo Archives), entra em cada um dos Volumes de todas as páginas de arquivos, cria pasta para armazenar os arquivos e faz download dos artigos e editoriais em arquivos .pdf disponíveis no site. Além disso, durante a execução é gerado um arquivo .txt com uma lista dos títulos dos artigos e editoriais baixados.

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
