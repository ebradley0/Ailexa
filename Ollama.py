from ollama import chat 
from ollama import ChatResponse
import ollama

def Querry_AI(query):
    context = {'role': 'system', 'content': 'You are an AI Assistant much like Jarvis from Iron Man. Keep responses human like, but short and concise at the same time.'}
    message = {'role': 'user', 'content': query}
    stream = []
   
    messages = [context, message]
    try:
        stream = chat(model='llama3.2:latest',  messages=messages)
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
    
    for content in stream:
        if 'message' in content:
            return content[1].content
            



Querry_AI('What is the weather like today?') # Output: The weather is sunny today.