# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos primeiro para otimizar o cache de camadas
COPY requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Descobre o caminho de instalação do Streamlit e o armazena em uma variável
# Isso torna o script robusto a diferentes versões do Python
ARG STREAMLIT_PATH=/usr/local/lib/python3.10/site-packages/streamlit/static
ENV STREAMLIT_STATIC_PATH=${STREAMLIT_PATH}

# Copia seu index.html modificado para SOBRESCREVER o original do Streamlit
# Esta é a etapa mágica!
COPY index.html ${STREAMLIT_STATIC_PATH}/index.html

# Copia todo o resto do seu projeto para o diretório de trabalho
COPY . .

# Expõe a porta que o Streamlit usará
EXPOSE 8501

# Define o comando para iniciar a aplicação
# O Render irá sobrescrever a porta com a variável $PORT
CMD ["streamlit", "run", "app_11.py", "--server.port=8501", "--server.address=0.0.0.0"]
