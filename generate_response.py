from groq import Groq
from typing import List
from dotenv import load_dotenv
import os
import json
from models import Metadata, Document, RetrievalResult, OutputModel

load_dotenv()

# Initialize Groq client with API key from environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(query: str, top_k_results: List[dict]) -> str:
    # Prepare the context from the top_k results
    context = "\n".join([f"Title: {result['title']}\nContent: {result['content']}" for result in top_k_results])

    # Define the system message for the response generation
    system_prompt = """You are a helpful AI assistant. 
    Using the provided context, answer the user's question accurately and concisely. 
    If the context doesn't contain relevant information, acknowledge that and provide a general response."""

    # Construct the conversation messages
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Context: {context}\n\nQuestion: {query}\n\nPlease answer the question based on the context provided above."
        }
    ]

    try:
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            temperature=0.7
        )

        # Return only the generated response text
        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error during response generation: {e}")
        return "Could not generate response"