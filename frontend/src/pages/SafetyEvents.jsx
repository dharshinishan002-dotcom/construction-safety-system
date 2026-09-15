
import { useEffect, useState } from "react";
import axios from "axios";

const API_URL ="https://construction-safety-system-cvd2.onrender.com/api/safety-events";

function SafetyEvents() {

  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  const fetchEvents = async () => {

    try {

      const response = await axios.get(API_URL);

      if (response.data.success) {
        setEvents(response.data.data);
      }

      setError("");

    } catch (err) {

      console.error(err);

      setError("Unable to load safety events");

    } finally {

      setLoading(false);

    }

  };


  useEffect(() => {

    fetchEvents();

  }, []);


  const resolveEvent = async (id) => {

    try {

      await axios.patch(
        API_URL + "/" + id + "/resolve"
      );

      fetchEvents();

    } catch (err) {

      console.error(
        "Error resolving event:",
        err
      );

      alert("Unable to resolve event");

    }

  };


  return (

    <div className="events-page">

      <h1>Safety Events</h1>

      <p>
        Monitor detected construction safety violations.
      </p>


      <button onClick={fetchEvents}>
        🔄 Refresh
      </button>


      {loading && (

        <p>
          Loading safety events...
        </p>

      )}


      {error && (

        <p>
          ⚠️ {error}
        </p>

      )}


      {!loading &&
        !error &&
        events.length === 0 && (

          <p>
            🟢 No safety events found.
          </p>

        )}


      {!loading &&
        !error &&
        events.length > 0 && (

          <div>

            {events.map((event) => (

              <div
                key={event._id}
                className="event"
              >

                <h3>
                  🚨{" "}
                  {event.eventType.replaceAll(
                    "_",
                    " "
                  )}
                </h3>


                <p>
                  Camera: {event.cameraId}
                </p>


                <p>
                  Worker: {event.workerId}
                </p>


                <p>
                  Severity: {event.severity}
                </p>


                <p>
                  Status: {event.status}
                </p>


                <p>
                  Time:{" "}
                  {new Date(
                    event.timestamp
                  ).toLocaleString()}
                </p>


                {event.status === "OPEN" && (

                  <button
                    onClick={() =>
                      resolveEvent(event._id)
                    }
                  >
                    ✓ Resolve
                  </button>

                )}

              </div>

            ))}

          </div>

        )}

    </div>

  );

}

export default SafetyEvents;

