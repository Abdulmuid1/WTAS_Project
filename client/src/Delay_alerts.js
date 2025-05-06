import React, { useEffect, useState } from "react";
import axios from "axios";

function DelayAlerts() {
  const [hasDelays, setHasDelays] = useState(false);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/delays`) // FastAPI backend URL
      .then(response => {
        if (response.data && response.data.data && response.data.data.length > 0) {
          setHasDelays(true);
        } else {
          setHasDelays(false);
        }
      })
      .catch(error => {
        console.error("Error fetching delays:", error);
        setHasDelays(false);
      });
  }, []);

  return (
    <div style={{ padding: "20px", textAlign: "left", color: "white" }}>
      <h2><span role="img" aria-label="live-alerts">🧊</span> Live Delay Alerts</h2>
      {hasDelays ? (
        <ul>
          <li><strong>ALERT!</strong></li>
        </ul>
      ) : (
        <p>No delays at the moment</p>
      )}
    </div>
  );
}

export default DelayAlerts;
