
import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = `${import.meta.env.VITE_API_URL}/api/safety-events`;

function Workers() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await axios.get(API_URL);

      if (response.data.success) {
        setEvents(response.data.data);
      }
    } catch (error) {
      console.error("Error fetching workers:", error);
    } finally {
      setLoading(false);
    }
  };

  // Create worker summary from safety events
  const workers = {};

  events.forEach((event) => {
    const workerId = event.workerId;

    if (!workers[workerId]) {
      workers[workerId] = {
        workerId: workerId,
        cameras: new Set(),
        violations: [],
      };
    }

    workers[workerId].cameras.add(event.cameraId);
    workers[workerId].violations.push(event.eventType);
  });

  const workerList = Object.values(workers);

  if (loading) {
    return <h2>Loading workers...</h2>;
  }

  return (
    <div className="page">

      <h1>Workers</h1>

      <p>Workers detected with safety violations</p>

      {workerList.length === 0 ? (
        <div className="card">
          <h3>No unsafe workers found</h3>
        </div>
      ) : (
        <div className="workers-grid">

          {workerList.map((worker) => (
            <div className="card" key={worker.workerId}>

              <h2>👷 Worker {worker.workerId}</h2>

              <p>
                <strong>Camera:</strong>{" "}
                {[...worker.cameras].join(", ")}
              </p>

              <p>
                <strong>Violations:</strong>{" "}
                {worker.violations.length}
              </p>

              <p>
                <strong>Types:</strong>{" "}
                {[
                  ...new Set(worker.violations)
                ].join(", ")}
              </p>

              <span className="unsafe">
                🔴 Unsafe
              </span>

            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default Workers;