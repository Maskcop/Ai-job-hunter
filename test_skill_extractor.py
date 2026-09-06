from skill_extractor import extract_skills


resume_text = """
I am a Full Stack Developer.

I have experience with React.js,
JavaScript, Node.js, Express.js,
SQL, MongoDB, Git and GitHub.

I have also built REST APIs.
"""


skills = extract_skills(
    resume_text
)


print("\nDetected Skills:")

for skill in skills:
    print("✓", skill)