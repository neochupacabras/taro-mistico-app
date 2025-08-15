# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Instala o 'sed', uma ferramenta para editar arquivos
RUN apt-get update && apt-get install -y sed

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala os requisitos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- A ETAPA MÁGICA ---
# Pega o index.html oficial do Streamlit que acabamos de instalar e injeta nossas meta tags nele.
# Ele encontra a tag </head> e insere nosso bloco de código logo antes dela.
RUN sed -i '/<\/head>/i \
    <!-- Meta Tags Injetadas para Preview em Redes Sociais -->\
    <meta property="og:title" content="🔮 Tarô Místico - Sua Revelação Sagrada">\
    <meta property="og:description" content="Um portal para o autoconhecimento através dos arquétipos universais. Receba uma leitura de tarô personalizada e profunda.">\
    <meta property="og:image" content="https://raw.githubusercontent.com/neochupacabras/taro-mistico-app/main/images/spread_celtic_cross.png">\
    <meta property="og:url" content="https://taromistico.onrender.com/">\
    <meta name="twitter:card" content="summary_large_image">\
    ' /usr/local/lib/python3.10/site-packages/streamlit/static/index.html

# Copia todo o resto do seu projeto para o diretório de trabalho
COPY . .

# Expõe a porta e define o comando de início
EXPOSE 8501
CMD ["streamlit", "run", "app_11.py", "--server.port=8501", "--server.address=0.0.0.0"]
