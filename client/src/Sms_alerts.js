import React from "react";

// Renders delay data passed from App.js
// Displays last updated time if available
function SmsAlerts({ delays, lastUpdated }) {
  return (
    <div style={{ padding: "20px", textAlign: "left", color: "white" }}>
      <h2><span role="img" aria-label="refresh">📲 SMS Delay Alerts</span></h2>
      {lastUpdated && <p>Last updated: {lastUpdated.toLocaleTimeString()}</p>}
      {delays.length === 0 ? <p>No delays</p> : (
        <ul>{delays.map((d, i) => <li key={i}>{d.message}</li>)}</ul>
      )}
    </div>
  );
}

export default SmsAlerts;
