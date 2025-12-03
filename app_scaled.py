import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Configuration
DB_PATH = "./chroma_db"
COLLECTION_NAME = "policies"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"

# --- Setup LangChain Components ---

@st.cache_resource
def load_vector_store():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_store = Chroma(
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )
    return vector_store

vector_store = load_vector_store()

# Create a "Retriever"
# k=5 means retrieve top 5 chunks (increased from 3 for better accuracy)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Define the Prompt Template
template = """
You are a senior policy expert. Answer the question based ONLY on the following context. 
If the context doesn't contain the answer, strictly say "I cannot find this in the policy documents."

Context:
{context}

Question:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)

# Initialize LLM
llm = ChatOllama(model=LLM_MODEL, temperature=0)

# Build the Chain (The "Pipeline")
# 1. Retriever gets docs -> 2. format_docs cleans them -> 3. Prompt -> 4. LLM
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- Streamlit UI ---
st.title("🏢 Enterprise Policy Search (500+ Docs)")

query = st.chat_input("Search company policies...")

if query:
    # Add user message
    st.chat_message("user").write(query)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing policies..."):
            # Stream the response
            response_generator = rag_chain.stream(query)
            st.write_stream(response_generator)
            
    # Source retrieval (Optional: for debugging)
    with st.expander("View Source Documents"):
        docs = retriever.invoke(query)
        for i, doc in enumerate(docs):
            st.markdown(f"**Source {i+1}:** `{doc.metadata.get('source', 'Unknown')}`")
            st.text(doc.page_content[:200] + "...")