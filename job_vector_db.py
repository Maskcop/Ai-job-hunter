import json

from dotenv import load_dotenv

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)

from langchain_chroma import Chroma
from langchain_core.documents import Document


load_dotenv()


# --------------------------------
# Embedding model
# --------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview"
)


# --------------------------------
# Load jobs
# --------------------------------

def load_jobs():

    with open(
        "jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# --------------------------------
# Create Job Vector Database
# --------------------------------

def create_job_vector_db():

    jobs = load_jobs()

    documents = []


    for job in jobs:

        text = f"""
Job Title: {job["title"]}

Company: {job["company"]}

Location: {job["location"]}

Description:
{job["description"]}

Required Skills:
{", ".join(job["required_skills"])}

Preferred Skills:
{", ".join(job["preferred_skills"])}
"""


        document = Document(

            page_content=text,

            metadata={
    "job_id": job["id"],
    "title": job["title"],
    "company": job["company"],
    "location": job["location"],
    "required_skills": ", ".join(
        job["required_skills"]
    ),
    "preferred_skills": ", ".join(
        job["preferred_skills"]
    )
}
        )

        documents.append(document)


    vector_store = Chroma.from_documents(

        documents=documents,

        embedding=embeddings,

        persist_directory="./job_chroma_db",

        collection_name="jobs"
    )


    print(
        f"Job Vector DB created with {len(documents)} jobs!"
    )


    return vector_store


# --------------------------------
# Retriever
# --------------------------------

def get_job_retriever():

    vector_store = Chroma(

        persist_directory="./job_chroma_db",

        embedding_function=embeddings,

        collection_name="jobs"
    )


    return vector_store.as_retriever(
        search_kwargs={
            "k": 5
        }
    )