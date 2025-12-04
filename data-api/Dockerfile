# Usa a versão 3.11-slim, que é compatível com o PySUS 1.0.1
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para a instalação
COPY requirements.txt .

# 1. Instala ferramentas de build e o Git (essenciais para compilar o PySUS do código-fonte)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Atualiza o pip para garantir a resolução correta de dependências
RUN pip install --upgrade pip

# 2. Instala o PySUS e as demais dependências
# Instalamos o PySUS diretamente do repositório GitHub (versão v1.0.1) para evitar a falha de distribuição do PyPI.
# Depois, instalamos os outros pacotes do requirements.txt que não são o PySUS.
RUN pip install --no-cache-dir "git+https://github.com/AlertaDengue/PySUS.git" \
    && pip install --no-cache-dir pandas fastapi uvicorn python-multipart orjson requests

# 3. Copia o código da sua aplicação (data_extractor.py e api_server.py)
COPY . .

# 4. Comando para executar o extrator e gerar o JSON inicial
# Se a extração falhar, ele salva o JSON de erro, mas o container não quebra.
#RUN python data_extractor.py

# Expõe a porta 8000, usada pelo servidor FastAPI
EXPOSE 8000

# Define o comando que será executado quando o container for iniciado (roda o servidor Uvicorn)
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]