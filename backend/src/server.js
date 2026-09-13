require("dotenv").config();

const express = require("express");
const cors = require("cors");

const connectDatabase = require("./config/database");
const safetyEventRoutes = require("./routes/safetyEventRoutes");

const app = express();


// Middleware
app.use(cors());
app.use(express.json());


// Test route
app.get("/", (req, res) => {
    res.json({
        success: true,
        message: "Construction Safety Backend is running"
    });
});


// Safety Event API
app.use(
    "/api/safety-events",
    safetyEventRoutes
);


// Start server
const PORT = process.env.PORT || 5000;

const startServer = async () => {

    await connectDatabase();

    app.listen(PORT, () => {
        console.log(
            `🚧 Construction Safety Backend running on port ${PORT}`
        );
    });

};

startServer();