import ollama

# Attempting a chat with Ollama
try:
    response = ollama.chat("Hello, Ollama!")
    print("Response from Ollama:", response)
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
