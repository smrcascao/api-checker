# Usa uma imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências (caso queira usar requirements.txt)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do app
COPY app.py .

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Comando para iniciar o app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]