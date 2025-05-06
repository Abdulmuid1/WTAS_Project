import React, { useEffect, useState } from "react";
import axios from "axios";

function SmsAlerts() {
  const [delays, setDelays] = useState([]);

  useEffect(() => {
    axios.post(`${process.env.REACT_APP_BACKEND_URL}/sms`)  // FastAPI backend URL for sms
      .then(response => {
        setDelays(response.data.data);
      })
      .catch(error => {
        console.error("Error fetching delays:", error);
      });
  }, []);

  return (
    <div style={{ padding: "20px", textAlign: "left", color: "white" }}>
      <h2><span role="img" aria-label="sms">📲</span> Sms Delay Alerts</h2>
      {delays.length === 0 ? (
        <p>No delays at the moment</p>
      ) : (
        <ul>
          {delays.map((item, index) => (
            <li key={index}>
              <strong>{item.type.toUpperCase()}</strong>: {item.message}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SmsAlerts;
