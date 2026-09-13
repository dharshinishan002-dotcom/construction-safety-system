import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

import SafetyEvents from "./pages/SafetyEvents";
import Workers from "./pages/Workers";
import Reports from "./pages/Reports";
import LiveAlerts from "./components/LiveAlerts";
import SafetyAnalytics from "./components/SafetyAnalytics";
import WorkerSafetyScore from "./components/WorkerSafetyScore";

const API_URL = `${import.meta.env.VITE_API_URL}/api/safety-events`;

function App() {
  const [events, setEvents] = useState([]);
  const [currentPage, setCurrentPage] = useState("dashboard");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchEvents = async () => {
    try {
      const response = await axios.get(API_URL);

      if (response.data.success) {
        setEvents(response.data.data);
        setError("");
      }
    } catch (err) {
      console.error("Backend error:", err);
      setError("Unable to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();

    const interval = setInterval(fetchEvents, 5000);

    return () => clearInterval(interval);
  }, []);

  const unsafeWorkers = new Set(
    events.map((event) => event.workerId)
  ).size;

  const renderPage = () => {
    if (currentPage === "events") {
      return <SafetyEvents />;
    }

    if (currentPage === "workers") {
      return <Workers />;
    }

    if (currentPage === "reports") {
      return <Reports />;
    }

    return (
      <>
        <header className="header">
          <div>
            <h1>Construction Safety Dashboard</h1>
            <p>AI-powered construction site monitoring</p>
          </div>

          <div className="status">
            🟢 System Online
          </div>
        </header>

        {error && (
          <div className="error">
            ⚠️ {error}
          </div>
        )}

        <section className="stats">

          <div className="card">
            <h3>Total Cameras</h3>
            <strong>5</strong>
            <p>CAM-01 to CAM-05</p>
          </div>

          <div className="card">
            <h3>Safety Events</h3>
            <strong>
              {loading ? "..." : events.length}
            </strong>
            <p>Detected by AI</p>
          </div>

          <div className="card">
            <h3>Unsafe Workers</h3>
            <strong>
              {loading ? "..." : unsafeWorkers}
            </strong>
            <p>Require attention</p>
          </div>

          <div className="card">
            <h3>System Status</h3>
            <strong>
              {error ? "OFFLINE" : "SAFE"}
            </strong>
            <p>
              {error
                ? "Backend disconnected"
                : "Monitoring active"}
            </p>
          </div>

        </section>
               <LiveAlerts
                   events={events}
                  loading={loading}
               />
               <SafetyAnalytics events={events} />
               <WorkerSafetyScore events={events} />

        <section className="section">

          <h2>Camera Monitoring</h2>

          <div className="camera-grid">

            {[
              "CAM-01",
              "CAM-02",
              "CAM-03",
              "CAM-04",
              "CAM-05"
            ].map((camera) => {

              const cameraEvents = events.filter(
                (event) => event.cameraId === camera
              );

              return (
                <div
                  className="camera-card"
                  key={camera}
                >

                  <video
                    className="camera-video"
                    src={`/videos/${camera}_browser.mp4`}
                    controls
                    muted
                    playsInline
                    preload="metadata"
                  >
                    Your browser does not support the video tag.
                  </video>

                  <h3>{camera}</h3>

                   {cameraEvents.length > 0 ? (
                <span className="unsafe">
                 🔴 Attention Required
                 <small>
                   {cameraEvents.length} event(s) detected
                  </small>
               </span>
                  ) : (
                <span className="safe">
                  🟢 Monitoring
               <small>
                 No violations detected
               </small>
              </span>
              )}

                </div>
              );
            })}

          </div>

        </section>

        <section className="section">

          <h2>Recent Safety Events</h2>

          <div className="events">

            {loading ? (
              <div className="event">
                Loading safety events...
              </div>
            ) : events.length === 0 ? (
              <div className="event">
                No safety events found.
              </div>
            ) : (
              events.slice(0, 10).map((event) => (

                <div
                  className="event"
                  key={event._id}
                >

                  <span className="danger">
                    🚨
                  </span>

                  <div>
                    <strong>
                      {event.eventType.replaceAll("_", " ")}
                    </strong>

                    <p>
                      {event.cameraId} • Worker{" "}
                      {event.workerId}
                    </p>
                  </div>

                  <span className="high">
                    {event.severity}
                  </span>

                </div>

              ))
            )}

          </div>

        </section>
      </>
    );
  };

  return (
    <div className="app">

      <aside className="sidebar">

        <h2>🦺 SafetyAI</h2>

        <nav>

          <button
            className={
              currentPage === "dashboard"
                ? "active"
                : ""
            }
            onClick={() =>
              setCurrentPage("dashboard")
            }
          >
            Dashboard
          </button>

          <button
            className={
              currentPage === "events"
                ? "active"
                : ""
            }
            onClick={() =>
              setCurrentPage("events")
            }
          >
            Safety Events
          </button>

          <button
            className={
              currentPage === "workers"
                ? "active"
                : ""
            }
            onClick={() =>
              setCurrentPage("workers")
            }
          >
            Workers
          </button>

          <button
            className={
              currentPage === "reports"
                ? "active"
                : ""
            }
            onClick={() =>
              setCurrentPage("reports")
            }
          >
            Reports
          </button>

        </nav>

      </aside>

      <main className="main">
        {renderPage()}
      </main>

    </div>
  );
}

export default App;