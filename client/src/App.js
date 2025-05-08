import React, {useState} from "react";
import { FaSms, FaBullhorn } from "react-icons/fa";
import "./App.css";
import DelayAlerts from "./Delay_alerts";  // render the DelayAlerts component
import SpeakerAnnouncements from "./Speaker_announce"; // render the Speaker component
import SmsAlerts from "./Sms_alerts"; // render the Sms component
import axios from "axios";

console.log("Backend URL:", process.env.REACT_APP_BACKEND_URL);

function App() {
  const [showSMS, setShowSMS] = useState(false);
  const [showSpeaker, setShowSpeaker] = useState(false);
  const [smsDelays, setSmsDelays] = useState([]);
  const [speakerDelays, setSpeakerDelays] = useState([]);
  const [smsLastUpdated, setSmsLastUpdated] = useState(null);
  const [speakerLastUpdated, setSpeakerLastUpdated] = useState(null);
  
  // Toggles the SMS Alerts section visibility
  const handleToggleSms = () => setShowSMS(!showSMS);

  // Toggles the Speaker Announcements section visibility
  const handleToggleSpeaker = () => setShowSpeaker(!showSpeaker);

  // Fetches updated SMS delays and sets the last updated time
  const handleRefreshSms = () => {
    axios.post(`${process.env.REACT_APP_BACKEND_URL}/api/sms`, {})
      .then((response) => {
        setSmsDelays(response.data.data);
        setSmsLastUpdated(new Date());
      })
      .catch((error) => console.error("Error fetching SMS alerts:", error));
  };

  // Fetches updated Speaker delays and sets the last updated time
  const handleRefreshSpeaker = () => {
    axios.post(`${process.env.REACT_APP_BACKEND_URL}/api/speaker`, {})
      .then((response) => {
        setSpeakerDelays(response.data.data);
        setSpeakerLastUpdated(new Date());
      })
      .catch((error) => console.error("Error fetching speaker announcements:", error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Winter Transit Alert System (WTAS)</h1>
        <p>Stay updated on real-time delays for buses and trains.</p>
      </header>

      <DelayAlerts />

      <div style={{ margin: "20px" }}>
        <button className="attention-button" onClick={handleToggleSms}>
          <FaSms /> {showSMS ? "Hide" : "Show"} SMS Alerts
        </button>
        <button className="attention-button" onClick={handleRefreshSms}>
        <span role="img" aria-label="refresh">🔄 Refresh SMS Alerts</span>
        </button>
        <br /><br />
        <button className="attention-button" onClick={handleToggleSpeaker}>
          <FaBullhorn /> {showSpeaker ? "Hide" : "Show"} Speaker Announcements
        </button>
        <button className="attention-button" onClick={handleRefreshSpeaker}>
        <span role="img" aria-label="refresh">🔄 Refresh Speaker Announcements</span>
        </button>
      </div>

      {showSMS && (
        <SmsAlerts delays={smsDelays} lastUpdated={smsLastUpdated} />
      )}

      {showSpeaker && (
        <SpeakerAnnouncements delays={speakerDelays} lastUpdated={speakerLastUpdated} />
      )}

      <footer>
      <p>&copy; {new Date().getFullYear()} Winter Transit Alert System - Edmonton</p>
     </footer>
     
    </div>
    
  );
}

export default App;
