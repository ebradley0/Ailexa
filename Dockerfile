FROM ollama/ollama:latest

WORKDIR /app

#Pip install dependencies if needed

COPY . /app

RUN ollama pull llama3.2

EXPOSE 11434

CMD ["ollama", "serve"]