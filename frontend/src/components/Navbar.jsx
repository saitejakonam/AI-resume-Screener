import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <Link to="/" className="logo">Resume Screener</Link>
      <div className="nav-links">
        <Link to="/create-job">Create Job</Link>
        <Link to="/view-jobs">View Jobs</Link>
        <Link to="/search">Search</Link>
      </div>
    </nav>
  );
};

export default Navbar;
