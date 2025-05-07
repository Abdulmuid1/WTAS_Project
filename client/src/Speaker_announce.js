import React from "react";

function SpeakerAnnouncements({ delays }) {
  return (
    <div style={{ padding: "20px", textAlign: "left", color: "white" }}>
      <h2><span role="img" aria-label="speaker">📢</span> Speaker Announcements</h2>
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

export default SpeakerAnnouncements;
