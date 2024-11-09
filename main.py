from search_documents import search_documents
from generate_response import generate_response

def main():
    try:
        # Example query
        query = input("Enter your question: ")
        
        # Search for relevant documents
        print("Searching for relevant documents...")
        top_k_results = search_documents(query, top_k=3)
        
        if not top_k_results:
            print("No relevant documents found in the knowledge base.")
            return
            
        # Generate response
        print("Generating response...")
        response = generate_response(query, top_k_results)
        print("\nGenerated Response:")
        print(response)

    except Exception as e:
        print(f"Error in main application: {e}")

if __name__ == "__main__":
    main()