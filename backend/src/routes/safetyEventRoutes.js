const express = require("express");

const {
  createSafetyEvent,
  getSafetyEvents,
  getSafetyEventById,
  resolveSafetyEvent,
} = require("../controllers/safetyEventController");

const router = express.Router();


// Create safety event
router.post(
  "/",
  createSafetyEvent
);


// Get all safety events
router.get(
  "/",
  getSafetyEvents
);


// Get one safety event
router.get(
  "/:id",
  getSafetyEventById
);


// Resolve safety event
router.patch(
  "/:id/resolve",
  resolveSafetyEvent
);


module.exports = router;