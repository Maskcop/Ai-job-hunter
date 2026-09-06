from typing import TypedDict, List


class CareerState(TypedDict):

    match_score: int

    matching_skills: List[str]

    missing_skills: List[dict]

    learning_plans: List[dict]

    interview_questions: List[dict]

    resume_suggestions: List[str]