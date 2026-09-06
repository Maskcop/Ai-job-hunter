from career_graph import career_graph


def run_career_analysis(analysis):

    matching_skills = [
        item.skill
        for item in analysis.matching_skills
    ]

    missing_skills = [
        {
            "skill": item.skill,
            "priority": item.priority,
            "reason": item.reason
        }
        for item in analysis.missing_skills
    ]

    initial_state = {
        "match_score": analysis.match_score,

        "matching_skills": matching_skills,

        "missing_skills": missing_skills,

        "learning_plans": [],

        "interview_questions": [],

        "resume_suggestions": []
    }

    result = career_graph.invoke(initial_state)

    return result