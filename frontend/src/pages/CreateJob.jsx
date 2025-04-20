import React, { useState } from "react";
import axios from "axios";
import "./PageStyles.css";

const CreateJob = () => {
  const [job, setJob] = useState({
    title: "",
    description: "",
    required_skills: "",
    experience: "",
    location: "",
  });

  const handleSubmit = async () => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/jobs/`, job);
      console.log("API URL:", process.env.REACT_APP_API_URL);
      alert("Job Created Successfully");
    } catch (error) {
      console.error("Error creating job:", error);
      alert("Failed to create job. Check API or browser console for details.");
    }
  };

  return (
    <div className="page-container">
      <div className="form-card">
        <h2>Create New Job</h2>
        <input
          type="text"
          placeholder="e.g. Python Developer"
          value={job.title}
          onChange={(e) => setJob({ ...job, title: e.target.value })}
        />
        <textarea
          placeholder="Describe the job..."
          value={job.description}
          onChange={(e) => setJob({ ...job, description: e.target.value })}
        />
        <input
          type="text"
          placeholder="e.g. Python, ML"
          value={job.required_skills}
          onChange={(e) =>
            setJob({ ...job, required_skills: e.target.value })
          }
        />
        <input
          type="text"
          placeholder="e.g. 1-3 years"
          value={job.experience}
          onChange={(e) => setJob({ ...job, experience: e.target.value })}
        />
        <input
          type="text"
          placeholder="e.g. Remote"
          value={job.location}
          onChange={(e) => setJob({ ...job, location: e.target.value })}
        />
        <button className="primary-btn" onClick={handleSubmit}>
          Create & Upload
        </button>
      </div>
    </div>
  );
};

export default CreateJob;
