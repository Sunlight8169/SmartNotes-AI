from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.embeddings import load_vectorstore
from config import LLM_MODEL, TOP_K_RESULTS

def get_llm():
    llm = OllamaLLM(
        model=LLM_MODEL,
        temperature=0.1
    )
    return llm

def build_rag_chain():
    llm = get_llm()
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": TOP_K_RESULTS}
    )

    template = """You are a helpful academic assistant.
    Answer the question based on the context below.
    IMPORTANT: Reply in the same language as the question. If question is in Hindi, answer in Hindi. If question is in English, answer in English.
    If the answer is not in the context, say "I could not find this information in the document."

    Context:
    {context}

    Question: {question}

    Answer:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever

def get_answer(query: str):
    chain, retriever = build_rag_chain()

    answer = chain.invoke(query)
    docs = retriever.invoke(query)

    source_pages = list(set([
        doc.metadata.get("page", "unknown")
        for doc in docs
    ]))

    return {
        "answer": answer,
        "source_pages": source_pages
    }