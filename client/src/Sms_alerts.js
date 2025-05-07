import React from "react";

function SmsAlerts({ delays }) {
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
