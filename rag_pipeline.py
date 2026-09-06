import os
from dotenv import load_dotenv
from models import JobAnalysis

load_dotenv()
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
structured_llm = llm.with_structured_output(JobAnalysis)

prompt = ChatPromptTemplate.from_template("""
You are an expert technical recruiter and career advisor.

Analyze the candidate's resume against the job description.

RESUME EVIDENCE:
{resume_context}

JOB DESCRIPTION:
{job_description}

Rules:

1. Give a match score from 0 to 100.
2. Identify skills that match the job requirements.
3. For every matching skill, provide:
   - skill name
   - evidence from the resume
   - related job requirement
4. Identify skills required by the job but not supported by the resume.
5. For every missing skill:
   - explain why it is missing
   - assign a priority: HIGH, MEDIUM, or LOW
6. Priority rules:
   - HIGH = important skill directly required by the job
   - MEDIUM = useful skill mentioned in the job
   - LOW = optional or less important skill
7. Evaluate experience match.
8. Give an application recommendation.
9. NEVER invent resume experience.
10. Use only information supported by the resume evidence and job description.
""")  
def analyze_resume(resume_documents, job_description):

    # 1. Split resume
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(resume_documents)

    # 2. Create vector database
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="uploaded_resume"
    )

    # 3. Retriever
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

    # 4. Retrieve relevant resume information
    query = f"""
    Find resume information relevant to this job:

    {job_description}
    """

    relevant_documents = retriever.invoke(query)

    # 5. Build context
    resume_context = "\n\n".join(
        doc.page_content
        for doc in relevant_documents
    )

    # 6. Create prompt
    messages = prompt.invoke({
        "resume_context": resume_context,
        "job_description": job_description
    })

    # 7. Ask Gemini
    response = structured_llm.invoke(messages)

    return response