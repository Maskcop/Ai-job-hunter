import re


SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "React",
    "React.js",
    "Node.js",
    "Express.js",
    "Spring Boot",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "REST APIs",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Kafka",
    "Redis",
    "HTML",
    "CSS",
    "Next.js",
    "Linux",
    "CI/CD",
]


def extract_skills(resume_text):

    text = resume_text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = re.escape(
            skill.lower()
        )

        if re.search(
            pattern,
            text
        ):
            found_skills.append(skill)

    return found_skills