from job_vector_db import get_job_retriever


retriever = get_job_retriever()


query = """
I am looking for a job where I can
build web applications using React,
JavaScript, Python and REST APIs.
"""


results = retriever.invoke(query)


print("\n🔥 TOP MATCHING JOBS\n")


for index, doc in enumerate(
    results,
    start=1
):

    print(
        f"\n#{index}"
    )

    print(
        "Job:",
        doc.metadata["title"]
    )

    print(
        "Company:",
        doc.metadata["company"]
    )

    print(
        "Location:",
        doc.metadata["location"]
    )

    print(
        "\nContent:"
    )

    print(
        doc.page_content[:300]
    )