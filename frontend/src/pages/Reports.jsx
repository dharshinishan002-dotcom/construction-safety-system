import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "https://construction-safety-system-cvd2.onrender.com/api/safety-events";

function Reports() {
const [events, setEvents] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
const fetchReports = async () => {
try {
const response = await axios.get(API_URL);


    if (response.data.success) {
      setEvents(response.data.data);
    }
  } catch (error) {
    console.error("Reports error:", error);
  } finally {
    setLoading(false);
  }
};

fetchReports();


}, []);

const helmetViolations = events.filter(
(event) => event.eventType === "NO_HELMET"
).length;

const gloveViolations = events.filter(
(event) => event.eventType === "NO_GLOVES"
).length;

const goggleViolations = events.filter(
(event) => event.eventType === "NO_GOGGLE"
).length;

const bootViolations = events.filter(
(event) => event.eventType === "NO_BOOTS"
).length;

const unsafeWorkers = new Set(
events.map((event) => event.workerId)
).size;

const cameraCounts = {};

events.forEach((event) => {
cameraCounts[event.cameraId] =
(cameraCounts[event.cameraId] || 0) + 1;
});

if (loading) {
return ( <main className="main"> <div className="card"> <h2>Safety Reports</h2> <p>Loading reports...</p> </div> </main>
);
}

return ( <main className="main">

```
  <header className="header">
    <div>
      <h1>Safety Reports</h1>
      <p>Construction site safety analysis</p>
    </div>

    <div className="status">
      🟢 Report Generated
    </div>
  </header>

  <section className="stats">

    <div className="card">
      <h3>Total Events</h3>
      <strong>{events.length}</strong>
      <p>Detected violations</p>
    </div>

    <div className="card">
      <h3>Unsafe Workers</h3>
      <strong>{unsafeWorkers}</strong>
      <p>Workers requiring attention</p>
    </div>

    <div className="card">
      <h3>No Helmet</h3>
      <strong>{helmetViolations}</strong>
      <p>Helmet violations</p>
    </div>

    <div className="card">
      <h3>No Gloves</h3>
      <strong>{gloveViolations}</strong>
      <p>Glove violations</p>
    </div>

  </section>

  <section className="section">

    <h2>PPE Violation Summary</h2>

    <div className="events">

      <div className="event">
        <span>🪖</span>
        <div>
          <strong>NO HELMET</strong>
          <p>Missing safety helmet</p>
        </div>
        <span className="high">
          {helmetViolations}
        </span>
      </div>

      <div className="event">
        <span>🧤</span>
        <div>
          <strong>NO GLOVES</strong>
          <p>Missing safety gloves</p>
        </div>
        <span className="high">
          {gloveViolations}
        </span>
      </div>

      <div className="event">
        <span>🥽</span>
        <div>
          <strong>NO GOGGLE</strong>
          <p>Missing safety goggles</p>
        </div>
        <span className="high">
          {goggleViolations}
        </span>
      </div>

      <div className="event">
        <span>🥾</span>
        <div>
          <strong>NO BOOTS</strong>
          <p>Missing safety boots</p>
        </div>
        <span className="high">
          {bootViolations}
        </span>
      </div>

    </div>

  </section>

  <section className="section">

    <h2>Camera-wise Violations</h2>

    <div className="events">

      {[
        "CAM-01",
        "CAM-02",
        "CAM-03",
        "CAM-04",
        "CAM-05"
      ].map((camera) => (
        <div className="event" key={camera}>

          <div>
            <strong>{camera}</strong>
            <p>Safety violations detected</p>
          </div>

          <span className="high">
            {cameraCounts[camera] || 0}
          </span>

        </div>
      ))}

    </div>

  </section>

</main>


);
}

export default Reports;
