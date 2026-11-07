Q: 26
Problem Statement
You are building a customer support chatbot for BharatPe, a fintech platform. The chatbot must answer questions about four policy categories: payments, refunds, account_security, and merchant_onboarding. You have access to:

A BAAI/bge-small-en embedding model (from sentence-transformers)
ChromaDB as the vector store
A Grok LLM (install: pip install grok; import: from grok import Grok; API key stored in a .env file as GROK_API_KEY)
Dataset
You have the following pre-chunked policy documents (each is one chunk):

docs = [
    {"id": "p1", "text": "BharatPe processes UPI payments instantly. Failures are auto-reversed within 24 hours.", "category": "payments"},
    {"id": "r1", "text": "Refunds for failed transactions are processed within 5-7 business days.", "category": "refunds"},
    {"id": "a1", "text": "Two-factor authentication is mandatory for all merchant accounts.", "category": "account_security"},
    {"id": "m1", "text": "New merchants must submit GST certificate and Aadhaar for onboarding.", "category": "merchant_onboarding"}
]
Tasks
Write Python code to: (a) load the BAAI/bge-small-en embedding model, (b) create a persistent ChromaDB client and collection, (c) embed each document chunk and upsert it into ChromaDB with its category as metadata.

Write a retrieve(query, category) function that: (a) embeds the user query, (b) retrieves the top-1 most relevant chunk from ChromaDB filtered to the specified category using a metadata where filter, (c) returns the retrieved text chunks.

Write a strict system prompt string that: (a) instructs the LLM to answer only from the provided context, (b) explicitly tells the LLM to respond with 'I do not have information on this topic.' when the retrieved context does not contain a relevant answer.

Write a generate_answer(query, context) function that combines the system prompt with the retrieved context and user query, calls the Grok LLM, and returns the final answer.

Submission Format
Paste your complete Python code as a single script in the input box. Ensure each task is handled in logically named functions or code blocks. No URLs or external notebooks.

API Key: Task 4 requires a live LLM call. You may use any of the following:

Grok (as specified): Create a key at console.x.ai → Sign In → API Keys → Create Key. Store it as GROK_API_KEY in your .env file.
Gemini alternative: Create a free key at aistudio.google.com → Sign in with Google → Get API key → Create API key. Store it as GEMINI_API_KEY in your .env file. Use pip install google-generativeai instead of pip install grok, and adapt generate_answer() to use the Gemini SDK — keep the function signature generate_answer(query, context) unchanged.
No key available: In generate_answer(), skip the LLM call and return a mock string such as f"Mock answer based on context: {context[:100]}". Grading focuses on your retrieval logic, system prompt construction, and function structure — not live LLM output.
Note: You may use any IDE (online: Google Colab, Jupyter Notebook; offline: VS Code, PyCharm, or similar) to write, run, and test your code. You must disable all AI-based extensions (GitHub Copilot, Tabnine, Codeium, etc.) before starting. AI tools of any kind are not permitted and will lead to disqualification. Submit your complete code as a copy-pasted snippet in the input box — do not submit a URL, notebook link, GitHub repository, or Google Drive file.



def load_and_store_documents(docs):
    from sentence_transformers import SentenceTransformer
    import chromadb
    # Load embedding model
    model = SentenceTransformer("BAAI/bge-small-en")
    # Create ChromaDB client and collection
    client = chromadb.PersistentClient(path="./chroma_store")
    collection = client.get_or_create_collection(name="bharatpe_policies", embedding_function=None)
    # Embed and upsert documents
    for doc in docs:
        embedding = model.encode(doc["text"], convert_to_numpy=True).tolist()
        collection.upsert(ids=[doc["id"]], documents=[doc["text"]], metadatas=[{"category": doc["category"]}], embeddings=[embedding])
    
def retrieve(query, category):
    from sentence_transformers import SentenceTransformer
    import chromadb
    # Load embedding model  
    model = SentenceTransformer("BAAI/bge-small-en")
    # Create ChromaDB client and collection
    client = chromadb.PersistentClient(path="./chroma_store")
    collection = client.get_or_create_collection(name="bharatpe_policies", embedding_function=None)
    # Embed query
    query_embedding = model.encode(query, convert_to_numpy=True).tolist()
    # Retrieve top-1 relevant chunk filtered by category
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1,
        where={"category": category}
    )
    return results.get("documents", [[]])[0]    