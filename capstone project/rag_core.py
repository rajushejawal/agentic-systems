import numpy as np
import re
from knowledge_base import KB_DOCUMENTS

class MockVectorStore:
    def __init__(self):
        self.collections = {"fixed": [], "sentence": []}

    def index_documents(self):
        # Strategy A: Fixed-size with Overlap
        for topic, text in KB_DOCUMENTS.items():
            words = text.split()
            chunk1 = " ".join(words[:20])
            chunk2 = " ".join(words[10:30])
            self.collections["fixed"].append({"topic": topic, "text": chunk1})
            self.collections["fixed"].append({"topic": topic, "text": chunk2})
            
            # Strategy B: Sentence-based Chunking
            sentences = text.split(". ")
            for s in sentences:
                if s:
                    self.collections["sentence"].append({"topic": topic, "text": s.strip()})

    def mock_similarity_search(self, query: str, collection_name: str):
        # Clean punctuation out of the query string
        clean_query = re.sub(r'[?!\.,]', '', query.lower())
        query_words = set(clean_query.split())
        
        # Core banking keywords that prove a query is in-scope
        banking_keywords = {
            "interest", "rate", "slab", "slabs", "kyc", "document", "requirements", 
            "emi", "calculation", "formula", "fee", "structure", "tiered", "card", 
            "fraud", "dispute", "resolution", "closure", "prepayment", "penalty", 
            "minimum", "balance", "premium", "savings", "credit", "score", "joint", 
            "account", "nri", "eligibility", "fema", "loan", "criteria"
        }
        
        results = []
        for item in self.collections[collection_name]:
            clean_item_text = re.sub(r'[?!\.,]', '', item["text"].lower())
            item_words = set(clean_item_text.split())
            
            intersection = query_words.intersection(item_words)
            
            # Calculate standard overlap similarity weight
            base_score = len(intersection) / (np.sqrt(len(query_words)) * np.sqrt(len(item_words)) + 1e-5)
            
            # Guardrail: Check if the user is using any official banking keyword
            has_banking_term = any(term in query_words for term in banking_keywords)
            
            # If it's a generic conversational phrase with no policy keywords, force score to 0
            if not has_banking_term:
                score = 0.0
            else:
                score = base_score
                
            results.append((item, score))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results[0] if results else (None, 0.0)

# Initialize vector spaces locally
RAG_DB = MockVectorStore()
RAG_DB.index_documents()

# Task 4: Calibrated safety fallback threshold
THRESHOLD = 0.12

def grounded_rag_lookup(query: str) -> str:
    best_match_tuple = RAG_DB.mock_similarity_search(query, "sentence")
    
    if not best_match_tuple or not best_match_tuple[0] or best_match_tuple[1] < THRESHOLD:
        return "I am sorry, but the retrieved context does not provide sufficient information to safely answer this question."
        
    # Unpack the document dictionary from the tuple match context safely
    return best_match_tuple[0]["text"]
