import { useState } from "react";
import { analyzeResume, recommendJobs } from "./services/api";

import {
  Upload,
  FileText,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  Target,
  Brain,
  BookOpen,
  MessageSquare,
  X,
  Briefcase,
  Zap,
} from "lucide-react";

import "./index.css";

function App() {
  const [resume, setResume] = useState(null);

  const [jobDescription, setJobDescription] = useState("");

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const [dragActive, setDragActive] = useState(false);

  const [jobResults, setJobResults] = useState(null);

  const [jobLoading, setJobLoading] = useState(false);

  const handleFile = (file) => {
    if (!file) return;

    if (file.type !== "application/pdf") {
      alert("Please upload a PDF resume.");
      return;
    }

    setResume(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();

    setDragActive(false);

    const file = event.dataTransfer.files[0];

    handleFile(file);
  };

  const handleAnalyze = async () => {
    if (!resume) {
      alert("Please upload your resume.");
      return;
    }

    if (!jobDescription.trim()) {
      alert("Please enter the job description.");
      return;
    }

    try {
      setLoading(true);

      const data = await analyzeResume(resume, jobDescription);

      console.log("REAL API RESPONSE:", data);

      setResult(data);

      setTimeout(() => {
        document.getElementById("results")?.scrollIntoView({
          behavior: "smooth",
        });
      }, 100);
    } catch (error) {
      console.error("Analysis error:", error);

      const message =
        error?.response?.data?.detail ||
        error?.message ||
        "Unable to analyze the resume.";

      alert(message);
    } finally {
      setLoading(false);
    }
  };

  const handleFindJobs = async () => {
    if (!resume) {
      alert("Please upload your resume.");
      return;
    }

    try {
      setJobLoading(true);

      const data = await recommendJobs(resume);

      console.log("JOB RECOMMENDATIONS:", data);

      setJobResults(data);
    } catch (error) {
      console.error("Job recommendation error:", error);

      alert("Unable to find matching jobs.");
    } finally {
      setJobLoading(false);
    }
  };

  const analysis = result?.job_analysis;
  const ats = result?.ats_analysis;
  const career = result?.career_analysis;

  return (
    <div className="app">
      {/* NAVBAR */}

      <nav className="navbar">
        <div className="brand">
          <div className="brand-icon">
            <Sparkles size={19} />
          </div>

          <span>AI Job Hunter</span>
        </div>

        <div className="nav-links">
          <a href="#analyze">Analyze</a>

          <a href="#results">Results</a>

          <a href="#career">Career AI</a>
        </div>

        <div className="nav-status">
          <span></span>
          AI System Online
        </div>
      </nav>

      {/* HERO */}

      <section className="hero" id="analyze">
        <div className="hero-badge">
          <Sparkles size={14} />
          AI-powered career intelligence
        </div>

        <h1>
          Your resume.
          <br />
          <span>Decoded by AI.</span>
        </h1>

        <p>
          Compare your resume with any job description. Discover your match
          score, skill gaps and a personalized plan to become job-ready.
        </p>

        <div className="hero-stats">
          <div>
            <strong>RAG</strong>

            <span>Evidence-based</span>
          </div>

          <div>
            <strong>AI</strong>

            <span>Skill analysis</span>
          </div>

          <div>
            <strong>Agents</strong>

            <span>Career planning</span>
          </div>
        </div>
      </section>

      {/* ANALYZER */}

      <section className="analyzer">
        {/* RESUME */}

        <div className="input-card">
          <div className="card-header">
            <div className="card-title">
              <div className="title-icon">
                <FileText size={18} />
              </div>

              <div>
                <h3>Your Resume</h3>

                <span>Upload PDF</span>
              </div>
            </div>

            <span className="step">01</span>
          </div>

          {!resume ? (
            <div
              className={`drop-zone ${dragActive ? "drag-active" : ""}`}
              onDragOver={(e) => {
                e.preventDefault();

                setDragActive(true);
              }}
              onDragLeave={() => setDragActive(false)}
              onDrop={handleDrop}
            >
              <input
                id="resumeInput"
                type="file"
                accept=".pdf"
                hidden
                onChange={(e) => handleFile(e.target.files[0])}
              />

              <label htmlFor="resumeInput">
                <div className="upload-icon">
                  <Upload size={23} />
                </div>

                <strong>Drop your resume here</strong>

                <span>or click to browse PDF</span>
              </label>
            </div>
          ) : (
            <div className="uploaded-file">
              <div className="file-icon">
                <FileText size={22} />
              </div>

              <div className="file-info">
                <strong>{resume.name}</strong>

                <span>{(resume.size / 1024 / 1024).toFixed(2)} MB · PDF</span>
              </div>

              <button className="remove-btn" onClick={() => setResume(null)}>
                <X size={17} />
              </button>
            </div>
          )}
        </div>

        {/* JOB DESCRIPTION */}

        <div className="input-card">
          <div className="card-header">
            <div className="card-title">
              <div className="title-icon">
                <Briefcase size={18} />
              </div>

              <div>
                <h3>Target Job</h3>

                <span>Job description</span>
              </div>
            </div>

            <span className="step">02</span>
          </div>

          <textarea
            className="job-input"
            placeholder="Paste the complete job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <div className="input-footer">
            <span>{jobDescription.length} characters</span>

            {jobDescription.length > 50 && (
              <span className="ready">
                <CheckCircle2 size={12} />
                Ready
              </span>
            )}
          </div>
        </div>
      </section>

      {/* CTA */}

      <div className="analyze-wrapper">
        <button
          className="analyze-btn"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              AI is analyzing...
            </>
          ) : (
            <>
              <Sparkles size={18} />
              Analyze My Match
              <ArrowRight size={18} />
            </>
          )}
        </button>

        <button
          className="analyze-btn secondary"
          onClick={handleFindJobs}
          disabled={jobLoading}
        >
          {jobLoading ? "Finding jobs..." : "🔥 Find My Jobs"}
        </button>

        <p>
          <Zap size={12} />
          Your resume stays in your session
        </p>
      </div>

      {/* RESULTS */}

      {result && (
        <section className="results" id="results">
          <div className="section-heading">
            <div>
              <span>AI ANALYSIS</span>

              <h2>Your career snapshot</h2>
            </div>

            <div className="analysis-complete">
              <CheckCircle2 size={15} />
              Analysis complete
            </div>
          </div>

          {/* SCORE */}

          <div className="score-card">
            <div className="score-visual">
              <div
                className="score-circle"
                style={{
                  "--score": `${analysis.match_score * 3.6}deg`,
                }}
              >
                <div>
                  <strong>{analysis.match_score}</strong>

                  <span>/ 100</span>
                </div>
              </div>
            </div>

            <div className="score-info">
              <span className="result-label">OVERALL MATCH</span>

              <h2>
                {analysis.match_score >= 70
                  ? "Strong candidate"
                  : "Needs improvement"}
              </h2>

              <p>{analysis.experience_match}</p>

              <div className="recommendation">
                <CheckCircle2 size={16} />

                {analysis.recommendation}
              </div>
            </div>

            <div className="score-side">
              <div>
                <span>MATCH</span>

                <strong>{analysis.match_score}%</strong>
              </div>

              <div>
                <span>SKILLS</span>

                <strong>{analysis.matching_skills.length}</strong>
              </div>

              <div>
                <span>GAPS</span>

                <strong>{analysis.missing_skills.length}</strong>
              </div>
            </div>
          </div>

          {/* SKILLS */}

          <div className="result-grid">
            {/* MATCHING */}

            <div className="result-card">
              <div className="result-card-title">
                <div className="success-icon">
                  <CheckCircle2 size={18} />
                </div>

                <div>
                  <h3>Matching Skills</h3>

                  <span>Strong alignment with the role</span>
                </div>
              </div>

              <div className="skill-list">
                {analysis.matching_skills.map((skill, index) => (
                  <div className="skill-item" key={index}>
                    <CheckCircle2 size={16} />

                    <div>
                      <strong>{skill.skill}</strong>

                      <span>{skill.resume_evidence}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* GAPS */}

            <div className="result-card">
              <div className="result-card-title">
                <div className="warning-icon">
                  <AlertTriangle size={18} />
                </div>

                <div>
                  <h3>Skill Gaps</h3>

                  <span>Prioritized areas to improve</span>
                </div>
              </div>

              <div className="skill-list">
                {analysis.missing_skills.map((skill, index) => (
                  <div className="skill-item missing" key={index}>
                    <AlertTriangle size={16} />

                    <div>
                      <div className="skill-name-row">
                        <strong>{skill.skill}</strong>

                        <span
                          className={`priority ${skill.priority.toLowerCase()}`}
                        >
                          {skill.priority}
                        </span>
                      </div>

                      <span>{skill.reason}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* ATS ANALYSIS */}

          {ats && (
            <section className="ats-section">
              <div className="section-heading">
                <div>
                  <span>ATS INTELLIGENCE</span>
                  <h2>Resume ATS Compatibility</h2>
                </div>

                <div className="analysis-complete">
                  <CheckCircle2 size={15} />
                  AI evaluated
                </div>
              </div>

              {/* ATS SCORE */}

              <div className="ats-score-card">
                <div className="ats-score">
                  <strong>{ats.ats_score}</strong>
                  <span>/ 100</span>
                </div>

                <div className="ats-score-info">
                  <span className="result-label">ATS COMPATIBILITY</span>

                  <h3>
                    {ats.ats_score >= 80
                      ? "ATS-friendly resume"
                      : ats.ats_score >= 60
                      ? "Good, but can be improved"
                      : "Needs ATS optimization"}
                  </h3>

                  <p>
                    Keyword match:{" "}
                    <strong>{ats.keyword_match_percentage}%</strong>
                  </p>
                </div>
              </div>

              {/* KEYWORDS */}

              <div className="ats-grid">
                {/* MATCHED KEYWORDS */}

                <div className="result-card">
                  <div className="result-card-title">
                    <div className="success-icon">
                      <CheckCircle2 size={18} />
                    </div>

                    <div>
                      <h3>Matched Keywords</h3>
                      <span>Keywords supported by your resume</span>
                    </div>
                  </div>

                  <div className="skill-list">
                    {ats.matched_keywords?.map((item, index) => (
                      <div className="skill-item" key={index}>
                        <CheckCircle2 size={16} />

                        <div>
                          <div className="skill-name-row">
                            <strong>{item.keyword}</strong>

                            <span className="priority">{item.importance}</span>
                          </div>

                          <span>Supported by your resume</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* MISSING KEYWORDS */}

                <div className="result-card">
                  <div className="result-card-title">
                    <div className="warning-icon">
                      <AlertTriangle size={18} />
                    </div>

                    <div>
                      <h3>Missing Keywords</h3>
                      <span>Important keywords not found in your resume</span>
                    </div>
                  </div>

                  <div className="skill-list">
                    {ats.missing_keywords?.map((item, index) => (
                      <div className="skill-item missing" key={index}>
                        <AlertTriangle size={16} />

                        <div>
                          <div className="skill-name-row">
                            <strong>{item.keyword}</strong>

                            <span
                              className={`priority ${item.importance?.toLowerCase()}`}
                            >
                              {item.importance}
                            </span>
                          </div>

                          <span>Not supported by the current resume</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* FORMATTING + SECTION ISSUES */}

              <div className="ats-grid">
                <div className="result-card">
                  <div className="result-card-title">
                    <div className="warning-icon">
                      <AlertTriangle size={18} />
                    </div>

                    <div>
                      <h3>Formatting Issues</h3>
                      <span>Potential ATS parsing problems</span>
                    </div>
                  </div>

                  <div className="suggestions">
                    {ats.formatting_issues?.length > 0 ? (
                      ats.formatting_issues.map((issue, index) => (
                        <div className="suggestion" key={index}>
                          <div className="suggestion-number">{index + 1}</div>

                          <span>{issue}</span>
                        </div>
                      ))
                    ) : (
                      <p>No major formatting issues detected.</p>
                    )}
                  </div>
                </div>

                <div className="result-card">
                  <div className="result-card-title">
                    <div className="warning-icon">
                      <AlertTriangle size={18} />
                    </div>

                    <div>
                      <h3>Section Issues</h3>
                      <span>Resume sections that may need improvement</span>
                    </div>
                  </div>

                  <div className="suggestions">
                    {ats.section_issues?.length > 0 ? (
                      ats.section_issues.map((issue, index) => (
                        <div className="suggestion" key={index}>
                          <div className="suggestion-number">{index + 1}</div>

                          <span>{issue}</span>
                        </div>
                      ))
                    ) : (
                      <p>No major section issues detected.</p>
                    )}
                  </div>
                </div>
              </div>

              {/* IMPROVEMENTS */}

              <div className="career-card">
                <div className="career-card-heading">
                  <Sparkles size={20} />

                  <div>
                    <h3>ATS Improvement Suggestions</h3>
                    <p>
                      Practical recommendations to improve your resume for this
                      specific job.
                    </p>
                  </div>
                </div>

                <div className="suggestions">
                  {ats.improvement_suggestions?.map((suggestion, index) => (
                    <div className="suggestion" key={index}>
                      <div className="suggestion-number">{index + 1}</div>

                      <span>{suggestion}</span>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          )}

          {/* CAREER AI */}

          <section className="career-section" id="career">
            <div className="career-header">
              <div className="career-icon">
                <Brain size={21} />
              </div>

              <div>
                <span>CAREER INTELLIGENCE</span>

                <h2>Your AI career plan</h2>
              </div>
            </div>

            {/* LEARNING */}

            <div className="career-card">
              <div className="career-card-heading">
                <BookOpen size={20} />

                <div>
                  <h3>Personalized Learning Roadmap</h3>

                  <p>Your highest-impact skills, ordered by priority.</p>
                </div>
              </div>

              <div className="learning-grid">
                {career.learning_plans.map((plan, index) => (
                  <div className="learning-item" key={index}>
                    <div className="learning-number">0{index + 1}</div>

                    <div className="learning-top">
                      <strong>{plan.skill}</strong>

                      <span>{plan.priority}</span>
                    </div>

                    <p>{plan.why_learn}</p>

                    <div className="topics">
                      {plan.topics.map((topic, i) => (
                        <span key={i}>{topic}</span>
                      ))}
                    </div>

                    <div className="project-box">
                      <span>MINI PROJECT</span>

                      <p>{plan.mini_project}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* INTERVIEW */}

            <div className="career-card">
              <div className="career-card-heading">
                <MessageSquare size={20} />

                <div>
                  <h3>AI Interview Preparation</h3>

                  <p>Questions generated around your target role.</p>
                </div>
              </div>

              <div className="questions">
                {career.interview_questions.map((question, index) => (
                  <div className="question" key={index}>
                    <span>{String(index + 1).padStart(2, "0")}</span>

                    <div>
                      <strong>{question.question}</strong>

                      <small>
                        {question.skill}

                        {" · "}

                        {question.difficulty}
                      </small>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* RESUME */}

            <div className="career-card">
              <div className="career-card-heading">
                <FileText size={20} />

                <div>
                  <h3>Resume Improvements</h3>

                  <p>Practical changes to strengthen your application.</p>
                </div>
              </div>

              <div className="suggestions">
                {career.resume_suggestions.map((suggestion, index) => (
                  <div className="suggestion" key={index}>
                    <div className="suggestion-number">{index + 1}</div>

                    <span>{suggestion}</span>
                  </div>
                ))}
              </div>
            </div>
          </section>
        </section>
      )}

      {/* 👇 ADD THE JOB RESULTS HERE */}

      {jobResults && (
        <section className="job-results">
          <h2>🔥 Recommended Jobs</h2>

          <p>Skills found in your resume:</p>

          <div className="skills-list">
            {jobResults.recommendations.candidate_skills.map((skill) => (
              <span key={skill}>{skill}</span>
            ))}
          </div>

          <div className="job-grid">
            {jobResults.recommendations.jobs.map((job) => (
              <div className="job-card" key={job.job_id}>
                <h3>{job.title}</h3>

                <p>{job.company}</p>

                <p>📍 {job.location}</p>

                {/* MATCH SCORE */}

                <div className="match-score">{job.match_score}% Match</div>

                {/* MATCHING SKILLS */}

                <h4>Matching Skills</h4>

                <div className="job-skill-list">
                  {job.matching_skills.map((skill) => (
                    <span className="job-skill" key={skill}>
                      ✓ {skill}
                    </span>
                  ))}
                </div>

                {/* MISSING SKILLS */}

                {job.missing_skills && job.missing_skills.length > 0 && (
                  <>
                    <h4>Missing Skills</h4>

                    <div className="job-skill-list">
                      {job.missing_skills.map((skill) => (
                        <span className="job-missing-skill" key={skill}>
                          ⚠ {skill}
                        </span>
                      ))}
                    </div>
                  </>
                )}

                {/* WHY YOU ARE A MATCH */}

                {job.match_reasons && job.match_reasons.length > 0 && (
                  <>
                    <h4>Why You're a Match</h4>

                    <div className="match-reasons">
                      {job.match_reasons.map((reason, index) => (
                        <div className="match-reason" key={index}>
                          <CheckCircle2 size={14} />

                          <span>{reason}</span>
                        </div>
                      ))}
                    </div>
                  </>
                )}

                {/* SKILL GAP EXPLANATION */}

                {job.gap_reasons && job.gap_reasons.length > 0 && (
                  <>
                    <h4>Skill Gap</h4>

                    <div className="gap-reasons">
                      {job.gap_reasons.map((reason, index) => (
                        <div className="gap-reason" key={index}>
                          <AlertTriangle size={14} />

                          <span>{reason}</span>
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        </section>
      )}
      {jobResults?.recommendations?.learning_plan &&
        jobResults.recommendations.learning_plan.length > 0 && (
          <section className="learning-results">
            <div className="learning-header">
              <span className="section-badge">AI Career Coach</span>

              <h2>📚 Your Learning Roadmap</h2>

              <p>
                Learn the skills that can improve your chances for your best
                matching job.
              </p>
            </div>

            <div className="learning-grid">
              {jobResults.recommendations.learning_plan.map((plan, index) => (
                <div className="learning-card" key={index}>
                  <div className="learning-card-top">
                    <div>
                      <h3>{plan.skill}</h3>

                      <span className="priority">{plan.priority}</span>
                    </div>
                  </div>

                  <div className="learning-section">
                    <h4>Why Learn This?</h4>

                    <p>{plan.why_learn}</p>
                  </div>

                  <div className="learning-section">
                    <h4>Topics to Learn</h4>

                    <ul>
                      {plan.topics.map((topic, topicIndex) => (
                        <li key={topicIndex}>{topic}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="learning-section">
                    <h4>Practice Task</h4>

                    <p>{plan.practice_task}</p>
                  </div>

                  <div className="learning-project">
                    <span>🚀 Mini Project</span>

                    <p>{plan.mini_project}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

      {jobResults?.recommendations?.interview_questions &&
        jobResults.recommendations.interview_questions.length > 0 && (
          <section className="interview-results">
            <div className="interview-header">
              <span className="section-badge">AI Interview Coach</span>

              <h2>🎯 Interview Preparation</h2>

              <p>
                Practice questions based on your strongest skills and skill
                gaps.
              </p>
            </div>

            <div className="interview-grid">
              {jobResults.recommendations.interview_questions.map(
                (question, index) => (
                  <div className="interview-card" key={index}>
                    <div className="question-number">Question {index + 1}</div>

                    <h3>{question.question}</h3>

                    <div className="question-meta">
                      <span className="question-skill">{question.skill}</span>

                      <span
                        className={`difficulty ${question.difficulty
                          ?.toLowerCase()
                          .replace(/\s+/g, "-")}`}
                      >
                        {question.difficulty}
                      </span>
                    </div>

                    <div className="question-reason">
                      <strong>Why this question?</strong>

                      <p>{question.reason}</p>
                    </div>
                  </div>
                )
              )}
            </div>
          </section>
        )}

      {/* FOOTER */}

      <footer>
        <div className="brand">
          <div className="brand-icon">
            <Sparkles size={16} />
          </div>
          AI Job Hunter
        </div>

        <span>RAG · ChromaDB · LangGraph · Gemini · FastAPI · React</span>
      </footer>
    </div>
  );
}

export default App;
