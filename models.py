from pydantic import BaseModel
from typing import List


class SkillEvidence(BaseModel):
    skill: str
    resume_evidence: str
    job_requirement: str


class MissingSkill(BaseModel):
    skill: str
    reason: str
    priority: str


class LearningStep(BaseModel):
    skill: str
    priority: str
    why_learn: str
    topics: List[str]
    practice_task: str
    mini_project: str


class JobAnalysis(BaseModel):
    match_score: int
    matching_skills: List[SkillEvidence]
    missing_skills: List[MissingSkill]
    experience_match: str
    recommendation: str

class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    required_skills: List[str]
    preferred_skills: List[str] = []
