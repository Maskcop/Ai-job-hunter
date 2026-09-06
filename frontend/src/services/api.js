import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});


// Analyze resume against a job description
export const analyzeResume = async (
  resume,
  jobDescription
) => {

  const formData = new FormData();

  formData.append("resume", resume);

  formData.append(
    "job_description",
    jobDescription
  );

  const response = await API.post(
    "/analyze",
    formData
  );

  return response.data;
};


// Find jobs matching the resume
export const recommendJobs = async (resume) => {

  const formData = new FormData();

  formData.append(
    "resume",
    resume
  );

  const response = await API.post(
    "/recommend-jobs",
    formData
  );

  return response.data;
};