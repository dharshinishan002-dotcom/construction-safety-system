# AI-Based Intelligent Construction Site Safety Monitoring and Fall Prevention System

A full-stack platform that treats 5 prerecorded construction videos as simulated live CCTV
feeds, runs computer vision (YOLO + OpenCV) on them to detect workers, falls, PPE compliance,
and restricted-zone violations, scores site/worker risk, and surfaces everything on a
real-time dashboard.

## Architecture

```
React Frontend
      |
Node.js / Express Backend  <---->  MongoDB
      |
Python AI Detection Service (YOLO + OpenCV + Tracking)
      |
5 Construction CCTV Videos (videos/CAM-01.mp4 ... CAM-05.mp4)
```

## Project structure

```
construction-safety-system/
├── frontend/          # React dashboard (built in Phase 10)
├── backend/           # Node.js/Express API + Socket.IO + MongoDB models
├── ai-service/        # Python computer vision service (YOLO/OpenCV)
├── videos/            # Put CAM-01.mp4 ... CAM-05.mp4 here
├── snapshots/          # Auto-captured incident frames land here
├── database/           # Mongo seed/migration scripts, ER notes
├── documentation/       # Phase write-ups, API docs, architecture notes
└── README.md
```

## Build plan (we go one phase at a time — see documentation/PHASES.md)

1. Project structure + verify all 5 videos can be read **(you are here)**
2. Person detection
3. Worker tracking
4. Fall detection
5. PPE detection
6. Danger-zone detection
7. Risk scoring
8. Incident + alert system
9. Node.js backend + MongoDB integration
10. React dashboard
11. Connect Python AI service to backend
12. Real-time alerts
13. Analytics
14. Full system test with all 5 videos

## Important note on "live" video

The 5 videos are **prerecorded** files played back and processed continuously to *simulate*
a live CCTV feed (looping playback, "LIVE" badge, continuous frame processing, alerts firing
as the video plays). The system never claims to be connected to real camera hardware.
