const SafetyEvent = require("../models/SafetyEvent");

// Create a new safety event
const createSafetyEvent = async (req, res) => {
  try {
    const {
      cameraId,
      workerId,
      eventType,
      severity,
      timestamp,
      snapshotPath,
    } = req.body;

    const event = await SafetyEvent.create({
      cameraId,
      workerId,
      eventType,
      severity,
      timestamp,
      snapshotPath,
    });

    res.status(201).json({
      success: true,
      message: "Safety event created successfully",
      data: event,
    });
  } catch (error) {
    console.error("Create safety event error:", error);

    res.status(500).json({
      success: false,
      message: "Failed to create safety event",
      error: error.message,
    });
  }
};


// Get all safety events
const getSafetyEvents = async (req, res) => {
  try {
    const events = await SafetyEvent.find()
      .sort({ createdAt: -1 });

    res.status(200).json({
      success: true,
      count: events.length,
      data: events,
    });
  } catch (error) {
    console.error("Get safety events error:", error);

    res.status(500).json({
      success: false,
      message: "Failed to fetch safety events",
      error: error.message,
    });
  }
};


// Get one safety event
const getSafetyEventById = async (req, res) => {
  try {
    const event = await SafetyEvent.findById(
      req.params.id
    );

    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Safety event not found",
      });
    }

    res.status(200).json({
      success: true,
      data: event,
    });
  } catch (error) {
    console.error("Get safety event error:", error);

    res.status(500).json({
      success: false,
      message: "Failed to fetch safety event",
      error: error.message,
    });
  }
};


// Resolve a safety event
const resolveSafetyEvent = async (req, res) => {
  try {
    const event = await SafetyEvent.findByIdAndUpdate(
      req.params.id,
      {
        status: "RESOLVED",
      },
      {
        new: true,
      }
    );

    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Safety event not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Safety event resolved",
      data: event,
    });
  } catch (error) {
    console.error("Resolve safety event error:", error);

    res.status(500).json({
      success: false,
      message: "Failed to resolve safety event",
      error: error.message,
    });
  }
};


module.exports = {
  createSafetyEvent,
  getSafetyEvents,
  getSafetyEventById,
  resolveSafetyEvent,
};