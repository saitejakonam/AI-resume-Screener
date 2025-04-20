import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import "./PageStyles.css";

const ViewResume = () => {
  const { candidateId } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCandidate = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_URL}/resumes/view/${candidateId}`
        );
        setCandidate(res.data);
      } catch (err) {
        console.error("Error fetching candidate:", err);
        setError("Failed to load resume.");
      } finally {
        setLoading(false);
      }
    };

    fetchCandidate();
  }, [candidateId]);

  if (loading) return <p className="loading-text">Loading resume...</p>;
  if (error) return <p className="error-text">{error}</p>;
  if (!candidate) return <p className="error-text">Candidate not found.</p>;

  return (
    <div className="page-container">
      <h2 className="page-title">Resume Details</h2>
      <div className="resume-view-container">
        <iframe
          src={candidate.resume_url}
          title="Resume PDF"
          width="100%"
          height="600px"
        />
        <div className="structured-metadata">
          <h3>Structured Metadata</h3>
          <p><strong>Name:</strong> {candidate.metadata.name}</p>
          <p><strong>Email:</strong> {candidate.metadata.email}</p>
          <p><strong>Skills:</strong> {candidate.metadata.skills}</p>
          <p><strong>Experience:</strong> {candidate.metadata.experience}</p>
          <p><strong>Location:</strong> {candidate.metadata.location}</p>
        </div>
      </div>
    </div>
  );
};

export default ViewResume;
