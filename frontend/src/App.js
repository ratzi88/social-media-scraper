import React, { useState } from "react";
import "./App.css";
import axios from "axios"; // To make API requests

function App() {
  // States for handling input, loading, results, and error
  const [inputName, setInputName] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState({});
  const [error, setError] = useState(null);

  // Helper function to truncate URLs
  const truncateURL = (url, maxLength = 50) => {
    if (url.length > maxLength) {
      return `${url.substring(0, maxLength)}...`;
    }
    return url;
  };

  // Function to handle API call
  const fetchSocialAccounts = async () => {
    setLoading(true); // Set loading state
    setResults({}); // Clear previous results
    setError(null); // Clear previous errors

    try {
      const response = await axios.post(`https://backend.graber.live/search`, {
        name: inputName,
      });
      console.log("API Response:", response.data); // Log the API response
      setResults(response.data);
    } catch (err) {
      console.error("Error:", err); // Log the error
      setError("An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Function to reset everything
  const resetSearch = () => {
    setInputName("");
    setResults({});
    setError(null);
  };

  // Render Font Awesome Icons
  const renderSocialIcon = (platform) => {
    const iconClassMap = {
      facebook: "fa-brands fa-facebook",
      instagram: "fa-brands fa-instagram",
      x: "fa-brands fa-x-twitter", // X (formerly Twitter)
      linkedin: "fa-brands fa-linkedin",
    };

    return (
      <i
        className={iconClassMap[platform]}
        style={{
          color: "#4da8da", // Icon color
          marginRight: "8px",
          fontSize: "20px", // Icon size
        }}
      ></i>
    );
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>GrABer</h1>
        <img src="/favicon.png" className="App-logo" alt="favicon" />
        <p>
          Enter a name below, and GrABer will fetch any linked social media
          accounts from Facebook, Instagram, X, and LinkedIn.
        </p>

        {/* Input Box */}
        {Object.keys(results).length === 0 && !loading ? (
          <>
            <input
              type="text"
              placeholder="Enter a name..."
              value={inputName}
              onChange={(e) => setInputName(e.target.value)}
              style={{
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
                marginBottom: "10px",
              }}
            />
            <button
              onClick={fetchSocialAccounts}
              disabled={!inputName}
              style={{
                fontFamily: "'Poppins', Arial, sans-serif;",
                padding: "10px 20px",
                border: "none",
                borderRadius: "5px",
                backgroundColor: "#28a745",
                color: "#fff",
                cursor: "pointer",
              }}
            >
              Search
            </button>
          </>
        ) : null}

        {/* Loading State */}
        {loading && <p>Loading Social Accounts...</p>}

        {/* Display Results */}
        {!loading && Object.keys(results).length > 0 && (
          <div>
            <h2>Results:</h2>
            {["facebook", "instagram", "x", "linkedin"].map((platform) => (
              <div
                key={platform}
                style={{
                  fontFamily: "'Poppins', Arial, sans-serif;",
                  margin: "10px 0",
                  display: "flex",
                  alignItems: "center",
                  fontSize: "30px",
                }}
              >
                {renderSocialIcon(platform)}
                {results[platform] ? (
                  <a
                    href={results[platform]}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      fontFamily: "'Poppins', Arial, sans-serif",
                      color: "#4da8da", // Link color
                      textDecoration: "none",
                      fontWeight: "bold",
                      fontSize: "25px",
                    }}
                  >
                    {truncateURL(results[platform])}
                  </a>
                ) : (
                  <span style={{ color: "#000000" }}>No Accounts Found</span>
                )}
              </div>
            ))}
            <button
              onClick={resetSearch}
              style={{
                fontFamily: "'Poppins', Arial, sans-serif;",
                marginTop: "20px",
                padding: "10px 20px",
                backgroundColor: "#007bff",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Search Another Name
            </button>
          </div>
        )}

        {/* Error Handling */}
        {error && <p style={{ color: "red" }}>{error}</p>}
      </header>
    </div>
  );
}

export default App;
