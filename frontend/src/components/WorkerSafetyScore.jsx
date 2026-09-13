function WorkerSafetyScore({ events }) {

  const workers = {};

  events.forEach((event) => {
    const workerId = event.workerId;

    if (!workers[workerId]) {
      workers[workerId] = {
        workerId,
        violations: 0,
        penalty: 0
      };
    }

    workers[workerId].violations++;

    const severity = event.severity?.toLowerCase();

    if (severity === "critical") {
      workers[workerId].penalty += 20;
    } else if (severity === "high") {
      workers[workerId].penalty += 15;
    } else {
      workers[workerId].penalty += 10;
    }
  });

  const workerScores = Object.values(workers).map((worker) => {

    const score = Math.max(
      100 - worker.penalty,
      0
    );

    let status = "Safe";

    if (score < 70) {
      status = "Warning";
    }

    if (score < 40) {
      status = "High Risk";
    }

    return {
      ...worker,
      score,
      status
    };
  });

  return (
    <section className="section">

      <h2 className="worker-score-title">
        👷 Worker Safety Score
      </h2>

      <div className="worker-score-grid">

        {workerScores.length === 0 ? (

          <div className="worker-score-empty">
            🟢 No worker violations detected
          </div>

        ) : (

          workerScores.map((worker) => (

            <div
              className="worker-score-card"
              key={worker.workerId}
            >

              <div className="worker-info">

                <h3>
                  Worker {worker.workerId}
                </h3>

                <p>
                  {worker.violations} safety violation(s)
                </p>

              </div>

              <div className="score">
                {worker.score}
              </div>

              <span
                className={`score-status ${
                  worker.status
                    .toLowerCase()
                    .replace(" ", "-")
                }`}
              >
                {worker.status}
              </span>

            </div>

          ))

        )}

      </div>

    </section>
  );
}

export default WorkerSafetyScore;