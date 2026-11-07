import os
from xmlrpc import client
from dotenv import load_dotenv

import chromadb
from sentence_transformers import SentenceTransformer

# Optional Grok import
try:
    from grok import Grok
    GROK_AVAILABLE = True
except ImportError:
    GROK_AVAILABLE = False


docs = [
    {
        "id": "p1",
        "text": "BharatPe processes UPI payments instantly. Failures are auto-reversed within 24 hours.",
        "category": "payments"
    },
    {
        "id": "r1",
        "text": "Refunds for failed transactions are processed within 5-7 business days.",
        "category": "refunds"
    },
    {
        "id": "a1",
        "text": "Two-factor authentication is mandatory for all merchant accounts.",
        "category": "account_security"
    },
    {
        "id": "m1",
        "text": "New merchants must submit GST certificate and Aadhaar for onboarding.",
        "category": "merchant_onboarding"
    }
]

load_dotenv()


def load_embedding_model():
    return SentenceTransformer("BAAI/bge-small-en")


embedding_model = load_embedding_model()



def create_collection():
    client = chromadb.PersistentClient(path="./bharatpe_chroma")

    collection = client.get_or_create_collection(
        name="bharatpe_policies"
    )

    return collection


collection = create_collection()


def index_documents(collection, documents):
    for doc in documents:
        embedding = embedding_model.encode(doc["text"]).tolist()

        collection.upsert(
            ids=[doc["id"]],
            documents=[doc["text"]],
            embeddings=[embedding],
            metadatas=[{"category": doc["category"]}]
        )


index_documents(collection, docs)


def retrieve(query, category):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1,
        where={"category": category}
    )

    retrieved_docs = results.get("documents", [[]])[0]

    return retrieved_docs



SYSTEM_PROMPT = """
You are a BharatPe policy assistant.

Rules:
1. Answer ONLY using the information present in the provided context.
2. Do not use external knowledge.
3. Do not make assumptions or infer facts not explicitly stated.
4. If the context does not contain the answer, respond exactly with:

I do not have information on this topic.

5. Keep answers concise and factual.
"""


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(query, context):

    if not context:
        return "I do not have information on this topic."

    prompt = f"""
Context:
{context}

User Question:
{query}
"""

    # -------------------------------
    # GROK IMPLEMENTATION
    # -------------------------------
    if GROK_AVAILABLE and os.getenv("GROK_API_KEY"):

        client = Grok(api_key=os.getenv("GROK_API_KEY"))

        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    return f"Mock answer based on context: {context[:100]}"


if __name__ == "__main__":

    user_query = "How long does a refund take?"
    category = "refunds"

    retrieved_context = retrieve(user_query, category)

    if retrieved_context:
        context_text = "\n".join(retrieved_context)
    else:
        context_text = ""

    answer = generate_answer(user_query, context_text)

    print("Retrieved Context:")
    print(context_text)

    print("\nAnswer:")
    print(answer)