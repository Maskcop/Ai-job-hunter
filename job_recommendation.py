from skill_extractor import extract_skills
from job_matcher import calculate_match
from job_vector_db import get_job_retriever
from learning_agent import create_learning_plans
from interview_agent import generate_interview_questions


def recommend_jobs(
    resume_text,
    keyword=None,
    location=None
):

    # --------------------------------
    # 1. Extract candidate skills
    # --------------------------------

    candidate_skills = extract_skills(
        resume_text
    )


    # --------------------------------
    # 2. Semantic job retrieval
    # --------------------------------

    retriever = get_job_retriever()

    relevant_documents = retriever.invoke(
        resume_text
    )


    results = []


    # --------------------------------
    # 3. Match retrieved jobs
    # --------------------------------

    for doc in relevant_documents:

        job = {
            "id": doc.metadata["job_id"],

            "title": doc.metadata["title"],

            "company": doc.metadata["company"],

            "location": doc.metadata["location"],

            "description": doc.page_content,

            "required_skills": (
                doc.metadata[
                    "required_skills"
                ].split(", ")
            ),

            "preferred_skills": (
                doc.metadata[
                    "preferred_skills"
                ].split(", ")
            )
        }


        # --------------------------------
        # Location filter
        # --------------------------------

        if location:

            if (
                location.lower()
                not in job["location"].lower()
            ):
                continue


        # --------------------------------
        # Keyword filter
        # --------------------------------

        if keyword:

            searchable_text = (
                job["title"]
                + " "
                + job["description"]
            ).lower()

            if (
                keyword.lower()
                not in searchable_text
            ):
                continue


        # --------------------------------
        # Skill matching
        # --------------------------------

        match = calculate_match(
            candidate_skills,
            job
        )


        # --------------------------------
        # Semantic score
        # --------------------------------

        semantic_score = 0

        if relevant_documents:

            position = (
                relevant_documents.index(doc)
            )

            semantic_score = max(
                100 - (position * 10),
                50
            )


        # --------------------------------
        # Final score
        # --------------------------------

        skill_score = match[
            "match_score"
        ]

        final_score = round(
            skill_score * 0.6
            +
            semantic_score * 0.4
        )


        # --------------------------------
        # Add scores
        # --------------------------------

        match["semantic_score"] = (
            semantic_score
        )

        match["skill_score"] = (
            skill_score
        )

        match["final_score"] = (
            final_score
        )


        results.append(match)


    # --------------------------------
    # 4. Sort results
    # --------------------------------

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )


    # --------------------------------
    # 5. Learning roadmap
    # --------------------------------

    learning_plan = None

    interview_questions = []


    if results:

        top_job = results[0]

        matching_skills = (
            top_job["matching_skills"]
        )

        missing_skills = (
            top_job["missing_skills"]
        )


        # --------------------------------
        # Create learning roadmap
        # --------------------------------

        if missing_skills:

            learning_plan = create_learning_plans(

                matching_skills=matching_skills,

                missing_skills=missing_skills

            )


        # --------------------------------
        # Create interview questions
        # --------------------------------

        interview_questions = (
            generate_interview_questions(

                matching_skills=matching_skills,

                missing_skills=missing_skills,

                learning_plans=str(
                    learning_plan
                )

            )
        )


    # --------------------------------
    # 6. Return results
    # --------------------------------

    return {

        "candidate_skills":
            candidate_skills,

        "total_jobs":
            len(results),

        "jobs":
            results,

        "learning_plan":
            learning_plan,

        "interview_questions":
            interview_questions

    }