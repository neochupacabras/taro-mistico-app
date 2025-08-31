# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Instala o 'sed', uma ferramenta para editar arquivos de texto
RUN apt-get update && apt-get install -y sed

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as bibliotecas Python necessárias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- ETAPA DE INJEÇÃO DAS META TAGS ---
# Injeta as meta tags genéricas do "Santuário das Revelações" no HTML do Streamlit.
# A tag </head> é encontrada, e o bloco de código é inserido antes dela.
RUN sed -i '/<\/head>/i \
    <!-- Meta Tags Injetadas para o Santuário das Revelações -->\
    <meta property="og:title" content="🔮 Santuário das Revelações">\
    <meta property="og:description" content="Um portal sagrado com três oráculos: Tarô Místico, Ecos Estelares e o Intérprete Xamânico. Desvende os mistérios da sua alma.">\
    <meta property="og:image" content="https://raw.githubusercontent.com/seu-usuario-github/seu-repositorio/main/images/santuario_preview.png">\
    <meta property="og:url" content="https://taromistico.onrender.com/">\
    <meta name="twitter:card" content="summary_large_image">\
    ' /usr/local/lib/python3.10/site-packages/streamlit/static/index.html

# Copia todo o resto do seu projeto para o diretório de trabalho
COPY . .

# Expõe a porta que o Streamlit usa
EXPOSE 8501

# <<< MUDANÇA CRUCIAL AQUI >>>
# Define o comando de início para executar o arquivo principal do Santuário.
# O nome do arquivo com emoji precisa estar entre aspas.
CMD ["streamlit", "run", "🔮_Santuario_Principal.py", "--server.port=8501", "--server.address=0.0.0.0"]
