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


  const handleSendSms = () => {
    axios.post(`${process.env.REACT_APP_BACKEND_URL}/sms`, {})
      .then((response) => setSmsDelays(response.data.data))
      .catch((error) => console.error("Error sending SMS alerts:", error));
    setShowSMS(true); // show the section after clicking
  };

  const handleAnnounce = () => {
    axios.post(`${process.env.REACT_APP_BACKEND_URL}/speaker`, {})
      .then((response) => setSpeakerDelays(response.data.data))
      .catch((error) => console.error("Error sending speaker announcements:", error));
    setShowSpeaker(true); // show the section after clicking
  };


  return (
    <div className="App">
      <header className="App-header">
        <h1>Winter Transit Alert System (WTAS)</h1>
        <p>Stay updated on real-time delays for buses and trains.</p>
      </header>

      <DelayAlerts />

      <div style={{ margin: "20px" }}>
        <button className="attention-button" onClick={handleSendSms}>
          <FaSms /> Send SMS Alerts
        </button>
        <button className="attention-button" onClick={handleAnnounce}>
          <FaBullhorn /> Announce via Speaker
        </button>
      </div>


      {showSMS && <SmsAlerts delays={smsDelays} />}
      {showSpeaker && <SpeakerAnnouncements delays={speakerDelays} />}

      <footer>
      <p>&copy; {new Date().getFullYear()} Winter Transit Alert System - Edmonton</p>
     </footer>
     
    </div>
    
  );
}

export default App;
