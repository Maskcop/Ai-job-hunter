import os 
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

pdf_path = "data/AdityaSuryawanshiResume24Company.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()
print("Pages:", len(documents))


from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

print("Number of chunks:", len(chunks))


from langchain_google_genai import GoogleGenerativeAIEmbeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
)
print("Embedding model ready")


from langchain_chroma import Chroma
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="resume"
)

print("Vector DB created!")

retriever = vector_store.as_retriever(
    search_kwargs={"k":3}
) 
print("retriever ready")

results = retriever.invoke(
    "What are my technical skills?"
)

for i, doc in enumerate(results, 1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content)


question = "What are Aditya's technical skills?"

results = retriever.invoke(question)

for i, doc in enumerate(results, 1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content)

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
print("LLM model ready")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant 
answers questions about a resume. information provided in the context.
If the answer is not present in the context ,say:
"I could not find this information in the resume.
Context:
{context}

Question:
{question}

Answer:
""" )
######Create the RAG chain
def ask_resume(question):
    documents = retriever.invoke(question)
    context = "\n\n".join(
        doc.page_content for doc in documents
    )
    messages = prompt.invoke({
        "context": context,
        "question": question
    })
    response = llm.invoke(messages)

    return response.content


question = "What are Aditya's technical skills?"
answer = ask_resume(question)
print("\nAnswer:")
print(answer)




