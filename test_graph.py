from career_graph import career_graph


initial_state = {

    "match_score": 82,

    "matching_skills": [
        "Java",
        "Spring Boot",
        "SQL"
    ],

    "missing_skills": [
        {
            "skill": "AWS",
            "priority": "HIGH",
            "reason": "AWS is required for cloud deployment"
        },
        {
            "skill": "Kafka",
            "priority": "MEDIUM",
            "reason": "Kafka is mentioned in the job requirements"
        }
    ],

    "learning_plans": [],

    "interview_questions": [],

    "resume_suggestions": []
}


result = career_graph.invoke(initial_state)


print("\n===== MATCH SCORE =====")
print(result["match_score"])


print("\n===== LEARNING PLANS =====")

for plan in result["learning_plans"]:

    print("\nSkill:", plan["skill"])
    print("Priority:", plan["priority"])


if result["interview_questions"]:

    print("\n===== INTERVIEW QUESTIONS =====")

    for question in result["interview_questions"]:

        print("\nQuestion:", question["question"])
        print("Skill:", question["skill"])
        print("Difficulty:", question["difficulty"])


if result["resume_suggestions"]:

    print("\n===== RESUME SUGGESTIONS =====")

    for suggestion in result["resume_suggestions"]:

        print("-", suggestion)