import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./PageStyles.css";

const ViewJobs = () => {
  const [jobs, setJobs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/jobs/`)
      .then((res) => {
        console.log("Job API response:", res.data);
        const jobList = Array.isArray(res.data) ? res.data : res.data?.jobs || [];
        setJobs(jobList);
      })
      .catch((err) => {
        console.error("Failed to fetch jobs:", err);
        setJobs([]); // fallback to empty array
      });
  }, []);

  return (
    <div className="page-container">
      <h2>Job Dashboard</h2>
      <div className="job-grid">
        {jobs.length === 0 ? (
          <p className="no-data-text">No jobs found.</p>
        ) : (
          jobs.map((job) => (
            <div key={job.id} className="job-card">
              <h4>{job.title}</h4>
              <p><strong>Skills:</strong> {job.required_skills}</p>
              <p><strong>Location:</strong> {job.location}</p>
              <div className="button-group">
                <button className="secondary-btn" onClick={() => navigate(`/apply/${job.id}`)}>
                  Upload
                </button>
                <button className="primary-btn" onClick={() => navigate(`/ranked/${job.id}`)}>
                  View Ranks
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ViewJobs;
