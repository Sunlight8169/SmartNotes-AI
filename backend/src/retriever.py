from src.embeddings import load_vectorstore
from config import TOP_K_RESULTS

def get_retriever():
    vectorstore = load_vectorstore()
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K_RESULTS}
    )
    return retriever

def retrieve_docs(query: str):
    retriever = get_retriever()
    docs = retriever.invoke(query)
    
    print(f"Retrieved {len(docs)} chunks query ke liye: '{query}'")
    return docs