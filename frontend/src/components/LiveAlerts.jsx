function LiveAlerts({ events, loading }) {
  const latestEvents = events.slice(0, 5);

  return (
    <section className="section">
      <h2 className="live-alert-title">
        🚨 Live Safety Alerts
      </h2>

      <div className="live-alerts">

        {loading ? (
          <div className="live-alert-empty">
            Loading alerts...
          </div>
        ) : latestEvents.length === 0 ? (
          <div className="live-alert-empty">
            🟢 No active safety alerts
          </div>
        ) : (
          latestEvents.map((event) => {

            const severity =
              event.severity?.toLowerCase() || "medium";

            return (
              <div
                className={`live-alert ${severity}`}
                key={event._id}
              >

                <div className="alert-icon">
                  🚨
                </div>

                <div className="alert-details">

                  <strong>
                    {event.eventType.replaceAll("_", " ")}
                  </strong>

                  <p>
                    {event.cameraId} • Worker {event.workerId}
                  </p>

                </div>

                <span className="alert-severity">
                  {event.severity}
                </span>

              </div>
            );
          })
        )}

      </div>
    </section>
  );
}

export default LiveAlerts;