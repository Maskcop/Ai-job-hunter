import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview"
)


def calculate_similarity(
    resume_text,
    job_description
):

    resume_vector = embeddings.embed_query(
        resume_text
    )

    job_vector = embeddings.embed_query(
        job_description
    )

    # Cosine similarity
    dot_product = sum(
        a * b
        for a, b in zip(
            resume_vector,
            job_vector
        )
    )

    resume_magnitude = sum(
        a * a
        for a in resume_vector
    ) ** 0.5

    job_magnitude = sum(
        b * b
        for b in job_vector
    ) ** 0.5

    if (
        resume_magnitude == 0
        or job_magnitude == 0
    ):
        return 0

    similarity = (
        dot_product
        / (
            resume_magnitude
            * job_magnitude
        )
    )

    # Convert 0-1 to 0-100
    score = round(
        similarity * 100
    )

    return score