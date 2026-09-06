from langgraph.graph import StateGraph, START, END

from graph_state import CareerState

from career_analysis import generate_learning_plans
from interview_agent import generate_interview_questions
from resume_optimizer import optimize_resume


def learning_node(state: CareerState):

    plans = generate_learning_plans(
        matching_skills=state["matching_skills"],
        missing_skills=state["missing_skills"]
    )

    return {
        "learning_plans": plans
    }


def interview_node(state: CareerState):

    questions = generate_interview_questions(
        matching_skills=state["matching_skills"],
        missing_skills=state["missing_skills"],
        learning_plans=state["learning_plans"]
    )

    return {
        "interview_questions": [
            question.model_dump()
            for question in questions
        ]
    }


def resume_optimizer_node(state: CareerState):

    suggestions = optimize_resume(
        matching_skills=state["matching_skills"],
        missing_skills=state["missing_skills"]
    )

    return {
        "resume_suggestions": suggestions
    }


# -----------------------------
# Routing function
# -----------------------------

def route_after_learning(state: CareerState):

    if state["match_score"] >= 70:
        return "interview_agent"

    return "resume_optimizer"


# -----------------------------
# Create graph
# -----------------------------

builder = StateGraph(CareerState)


builder.add_node(
    "learning_agent",
    learning_node
)

builder.add_node(
    "interview_agent",
    interview_node
)

builder.add_node(
    "resume_optimizer",
    resume_optimizer_node
)


# START → Learning
builder.add_edge(
    START,
    "learning_agent"
)


# Conditional routing
builder.add_conditional_edges(
    "learning_agent",
    route_after_learning,
    {
        "interview_agent": "interview_agent",
        "resume_optimizer": "resume_optimizer"
    }
)


# End paths

builder.add_edge(
    "interview_agent",
    END
)

builder.add_edge(
    "resume_optimizer",
    END
)


career_graph = builder.compile()