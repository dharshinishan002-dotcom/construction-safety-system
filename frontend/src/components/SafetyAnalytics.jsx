import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function SafetyAnalytics({ events }) {

  const cameraData = [
    "CAM-01",
    "CAM-02",
    "CAM-03",
    "CAM-04",
    "CAM-05"
  ].map((camera) => ({
    camera,
    events: events.filter(
      (event) => event.cameraId === camera
    ).length
  }));

  return (
    <section className="section">

      <h2 className="analytics-title">
        📊 Safety Analytics
      </h2>

      <div className="analytics-card">

        <h3>Safety Events by Camera</h3>

        <ResponsiveContainer width="100%" height={300}>

          <BarChart data={cameraData}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="camera" />

            <YAxis allowDecimals={false} />

            <Tooltip />

            <Bar
              dataKey="events"
              fill="#e74c3c"
              radius={[6, 6, 0, 0]}
            />

          </BarChart>

        </ResponsiveContainer>

      </div>

    </section>
  );
}

export default SafetyAnalytics;