from learning_agent import create_learning_plans


def generate_learning_plans(
    matching_skills,
    missing_skills
):

    plans = create_learning_plans(
        matching_skills=matching_skills,
        missing_skills=missing_skills
    )

    return [
        plan.model_dump()
        for plan in plans
    ]