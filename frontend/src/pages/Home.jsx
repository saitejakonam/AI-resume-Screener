import React from "react";
import { useNavigate } from "react-router-dom";
import "./PageStyles.css";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="page-container">
      <div className="hero-section">
        <h1>Welcome to Resume Screener</h1>
        <p>
          Upload resumes, analyze candidates, and rank them based on job relevance using AI.
        </p>
        <div className="button-group">
          <button className="primary-btn" onClick={() => navigate("/create-job")}>
            Create Job
          </button>
          <button className="secondary-btn" onClick={() => navigate("/view-jobs")}>
            View Jobs
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
