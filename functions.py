import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

load_dotenv()
    
class RAG:
    def __init__(self):
        self.faiss_db=FAISS.load_local(os.getenv('index_name'),HuggingFaceEmbeddings(model_name=os.getenv('embedding_model')),allow_dangerous_deserialization=True)

    def answer(self,query):
        similar_docs=self.search_faiss(query)
        context=self.context_and_url(similar_docs)
        return context

    def context_and_url(self,docs_and_scores):
        context=""
        for data in docs_and_scores:
            text,score=data
            context+=text.page_content
        return context
    
    def search_faiss(self,query):
        docs_and_scores = self.faiss_db.similarity_search_with_score(query)
        return docs_and_scores