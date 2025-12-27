from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()
def build_rag_chain(transcript_text:str):
    """
    Build a simple rag pipeline
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
    )
    documents = splitter.split_documents([
        Document(page_content = transcript_text)
    ])
    embeddings = HuggingFaceEmbeddings(
        model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    )
    vectorstore = FAISS.from_documents(documents,embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k":4})
    llm = init_chat_model(
        model = 'llama-3.1-8b-instant',
        temperature = 0,
        model_provider = 'groq',
        api_key = os.getenv('GROQ_API_KEY')
    )
    
    def ask(question:str)->str:
        docs = retriever.invoke(question)
        context = '\n\n'.join(d.page_content for d in docs)

        prompt = f"""
        Answer the question using ONLY the context below.
        If the answer is not present, say:
        "I don't have enough information from the video."

        Context:
        {context}

        Question:
        {question}

        Answer:
        """ 
        return llm.invoke(prompt).content
    
    return ask