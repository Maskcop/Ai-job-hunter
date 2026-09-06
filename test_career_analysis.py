from career_analysis import generate_learning_plans


matching_skills = [
    "Java",
    "Spring Boot",
    "SQL"
]


missing_skills = [
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
]


plans = generate_learning_plans(
    matching_skills,
    missing_skills
)


for plan in plans:

    print("\n" + "=" * 60)

    print("Skill:", plan["skill"])
    print("Priority:", plan["priority"])
    print("Why:", plan["why_learn"])

    print("\nTopics:")
    for topic in plan["topics"]:
        print("-", topic)

    print("\nPractice:")
    print(plan["practice_task"])

    print("\nMini Project:")
    print(plan["mini_project"])