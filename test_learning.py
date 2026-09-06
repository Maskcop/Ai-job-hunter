print("Starting learning agent...")

from learning_agent import create_learning_plan

print("Learning agent imported successfully!")


result = create_learning_plan(
    matching_skills=[
        "Java",
        "Spring Boot",
        "SQL"
    ],
    skill="AWS",
    priority="HIGH",
    job_requirement="Experience deploying applications on AWS"
)

print("AI response received!")

print("\nLearning Plan:")
print(result)

print("\nAs JSON:")
print(result.model_dump())