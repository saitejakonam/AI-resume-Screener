const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// Create a new job
export async function createJob(jobData) {
  const res = await fetch(`${BASE_URL}/jobs/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(jobData),
  });
  return await res.json();
}

// Fetch all jobs
export async function getJobs() {
  const res = await fetch(`${BASE_URL}/jobs/`);
  return await res.json();
}

// Upload resumes for a job
export async function uploadResumes(jobId, files) {
  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }

  const res = await fetch(`${BASE_URL}/resumes/upload/${jobId}`, {
    method: "POST",
    body: formData,
  });
  return await res.json();
}

// Fetch ranked resumes for a job
export async function getRankedResumes(jobId) {
  const res = await fetch(`${BASE_URL}/resumes/rank_candidates?job_id=${jobId}`);
  return await res.json(); // Let RankedResumes.jsx handle structure
}

// Search resumes based on filters
export async function searchCandidates(skills = "", experience = "", location = "") {
  const query = new URLSearchParams({ skills, experience, location }).toString();
  const res = await fetch(`${BASE_URL}/resumes/search?${query}`);
  return await res.json();
}

// Fetch a single resume and its metadata by candidate_id
export async function getResumeDetails(candidateId) {
  const res = await fetch(`${BASE_URL}/resumes/${candidateId}`);
  return await res.json(); // expected: { metadata: {...}, resume_url: "..." }
}
