const mongoose = require("mongoose");

const safetyEventSchema = new mongoose.Schema(
  {
    cameraId: {
      type: String,
      required: true,
      trim: true,
    },

    workerId: {
      type: String,
      required: true,
      trim: true,
    },

    eventType: {
      type: String,
      required: true,
      enum: [
        "NO_HELMET",
        "NO_GOGGLES",
        "NO_GLOVES",
        "NO_BOOTS",
        "FALL",
      ],
    },

    severity: {
      type: String,
      enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
      default: "HIGH",
    },

    timestamp: {
      type: Date,
      default: Date.now,
    },

    snapshotPath: {
      type: String,
      default: null,
    },

    status: {
      type: String,
      enum: ["OPEN", "RESOLVED"],
      default: "OPEN",
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model(
  "SafetyEvent",
  safetyEventSchema
);