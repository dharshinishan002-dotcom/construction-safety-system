# Build Phases

| Phase | Scope | Status |
|-------|-------|--------|
| 1 | Project structure + verify all 5 videos can be read | ✅ In progress (this delivery) |
| 2 | Person detection (YOLO) | ⏳ Not started |
| 3 | Worker tracking | ⏳ Not started |
| 4 | Fall detection | ⏳ Not started |
| 5 | PPE detection | ⏳ Not started |
| 6 | Danger-zone detection | ⏳ Not started |
| 7 | Risk scoring engine | ⏳ Not started |
| 8 | Incident + alert system | ⏳ Not started |
| 9 | Node.js backend + MongoDB | ⏳ Not started |
| 10 | React dashboard | ⏳ Not started |
| 11 | Connect AI service <-> backend | ⏳ Not started |
| 12 | Real-time alerts (Socket.IO) | ⏳ Not started |
| 13 | Analytics | ⏳ Not started |
| 14 | Full system test | ⏳ Not started |

Each phase gets its own section below once complete, with what was built, how to test it,
and how to troubleshoot it.

## Phase 1 — Project structure + video verification

**Goal:** Confirm the folder layout is correct and that OpenCV can open and read frames from
each of the 5 CCTV videos before any AI logic is written on top of them.

**What was built:**
- Top-level folder structure (`frontend/`, `backend/`, `ai-service/`, `videos/`, `snapshots/`,
  `database/`, `documentation/`).
- `ai-service/requirements.txt` — Python dependencies for the CV service.
- `ai-service/utils/verify_videos.py` — reads each `CAM-0X.mp4` in `videos/`, reports
  resolution, FPS, frame count, duration, and pulls a sample frame to confirm decoding works.
- `backend/package.json` — Node/Express dependency manifest (not run yet — that's Phase 9).

**How to test:**
1. Drop your 5 video files into `videos/` named exactly `CAM-01.mp4` through `CAM-05.mp4`.
2. `cd ai-service && pip install -r requirements.txt`
3. `python utils/verify_videos.py`
4. You should see a per-camera report (resolution/FPS/frame count/duration) and a sample
   frame saved to `ai-service/utils/verify_output/`.

**Troubleshooting:**
- `ModuleNotFoundError: cv2` → `pip install opencv-python`
- "Could not open video" → check the filename matches exactly (case-sensitive on
  Linux/Mac) and that the codec is a common one (H.264/mp4). Re-encode with
  `ffmpeg -i input.mov -c:v libx264 -c:a aac CAM-01.mp4` if needed.
- 0 frames read → the file may be corrupted or only contain audio; try re-downloading /
  re-exporting it.
