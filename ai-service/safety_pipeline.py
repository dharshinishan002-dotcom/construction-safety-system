# import os
# import cv2
# from ultralytics import YOLO
#
#
# # ============================================================
# # PROJECT PATHS
# # ============================================================
#
# PROJECT_ROOT = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "..")
# )
#
# CAMERAS = [
#     "CAM-01",
#     "CAM-02",
#     "CAM-03",
#     "CAM-04",
#     "CAM-05"
# ]
# PPE_MODEL_PATH = os.path.join(
#     PROJECT_ROOT,
#     "models",
#     "ppe_best.pt"
# )
#
# OUTPUT_DIR = os.path.join(
#     PROJECT_ROOT,
#     "snapshots",
#     "pipeline"
# )
#
# SNAPSHOT_DIR = os.path.join(
#     OUTPUT_DIR,
#     "violations"
# )
#
# OUTPUT_VIDEO = os.path.join(
#     OUTPUT_DIR,
#     "CAM-01_safety_pipeline.mp4"
# )
#
# os.makedirs(OUTPUT_DIR, exist_ok=True)
# os.makedirs(SNAPSHOT_DIR, exist_ok=True)
#
#
# # ============================================================
# # SETTINGS
# # ============================================================
#
# PERSON_CONFIDENCE = 0.5
# PPE_CONFIDENCE = 0.4
#
# # Fall detection
# FALL_ASPECT_RATIO = 1.2
# FALL_CONFIRMATION_FRAMES = 8
#
#
# # ============================================================
# # LOAD MODELS
# # ============================================================
#
# print("\n==============================================")
# print("       CONSTRUCTION SAFETY PIPELINE")
# print("==============================================")
#
# print("\nLoading person model...")
#
# person_model = YOLO("yolov8n.pt")
#
# print("✅ Person model loaded")
#
#
# print("\nLoading PPE model...")
#
# ppe_model = YOLO(PPE_MODEL_PATH)
#
# print("✅ PPE model loaded")
#
# print("\nPPE classes:")
# print(ppe_model.names)
#
#
# # ============================================================
# # VIDEO CHECK
# # ============================================================
#
# if not os.path.exists(VIDEO_PATH):
#
#     print("\n❌ ERROR: CAM-01 video not found!")
#     print(VIDEO_PATH)
#     exit(1)
#
#
# # ============================================================
# # OPEN VIDEO
# # ============================================================
#
# cap = cv2.VideoCapture(VIDEO_PATH)
#
# if not cap.isOpened():
#
#     print("\n❌ ERROR: Could not open CAM-01")
#     exit(1)
#
#
# width = int(
#     cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# )
#
# height = int(
#     cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# )
#
# fps = cap.get(
#     cv2.CAP_PROP_FPS
# )
#
# if fps <= 0:
#     fps = 25
#
#
# total_frames = int(
#     cap.get(cv2.CAP_PROP_FRAME_COUNT)
# )
#
#
# # ============================================================
# # VIDEO WRITER
# # ============================================================
#
# fourcc = cv2.VideoWriter_fourcc(
#     *"mp4v"
# )
#
# out = cv2.VideoWriter(
#     OUTPUT_VIDEO,
#     fourcc,
#     fps,
#     (width, height)
# )
#
#
# # ============================================================
# # TRACKING / FALL DATA
# # ============================================================
#
# fall_counters = {}
#
# fall_alerted = set()
#
# snapshot_count = 0
#
# frame_number = 0
#
#
# # ============================================================
# # MAIN PROCESSING LOOP
# # ============================================================
#
# print("\n==============================================")
# print("🚧 PROCESSING CAM-01")
# print("==============================================")
#
# print(f"Input : {VIDEO_PATH}")
# print(f"Output: {OUTPUT_VIDEO}")
# print(f"Frames: {total_frames}")
#
#
# while True:
#
#     ret, frame = cap.read()
#
#     if not ret:
#         break
#
#     frame_number += 1
#
#
#     # ========================================================
#     # PERSON DETECTION + TRACKING
#     # ========================================================
#
#     tracking_results = person_model.track(
#         frame,
#         persist=True,
#         classes=[0],
#         tracker="bytetrack.yaml",
#         verbose=False
#     )
#
#
#     # Store workers detected in current frame
#
#     workers = []
#
#
#     for result in tracking_results:
#
#         if result.boxes is None:
#             continue
#
#
#         for box in result.boxes:
#
#             confidence = float(
#                 box.conf[0]
#             )
#
#             if confidence < PERSON_CONFIDENCE:
#                 continue
#
#
#             x1, y1, x2, y2 = map(
#                 int,
#                 box.xyxy[0]
#             )
#
#
#             if box.id is not None:
#
#                 track_id = int(
#                     box.id[0]
#                 )
#
#             else:
#
#                 track_id = -1
#
#
#             workers.append(
#                 (
#                     track_id,
#                     x1,
#                     y1,
#                     x2,
#                     y2
#                 )
#             )
#
#
#     # ========================================================
#     # PROCESS EACH WORKER
#     # ========================================================
#
#     for (
#         track_id,
#         x1,
#         y1,
#         x2,
#         y2
#     ) in workers:
#
#
#         # ----------------------------------------------------
#         # FALL DETECTION
#         # ----------------------------------------------------
#
#         box_width = x2 - x1
#         box_height = y2 - y1
#
#         aspect_ratio = (
#             box_width / box_height
#             if box_height > 0
#             else 0
#         )
#
#         possible_fall = (
#             aspect_ratio >= FALL_ASPECT_RATIO
#         )
#
#
#         if track_id != -1:
#
#             if track_id not in fall_counters:
#                 fall_counters[track_id] = 0
#
#
#             if possible_fall:
#
#                 fall_counters[track_id] += 1
#
#             else:
#
#                 fall_counters[track_id] = 0
#
#
#         fall_detected = False
#
#
#         if (
#             track_id != -1
#             and fall_counters.get(track_id, 0)
#             >= FALL_CONFIRMATION_FRAMES
#         ):
#
#             fall_detected = True
#
#             fall_alerted.add(
#                 track_id
#             )
#
#
#         # ----------------------------------------------------
#         # PPE DETECTION
#         # ----------------------------------------------------
#
#         # Crop the worker area
#
#         worker_crop = frame[
#             max(0, y1):min(height, y2),
#             max(0, x1):min(width, x2)
#         ]
#
#
#         ppe_results = ppe_model(
#             worker_crop,
#             verbose=False
#         )
#
#
#         detected_ppe = set()
#
#
#         for ppe_result in ppe_results:
#
#             if ppe_result.boxes is None:
#                 continue
#
#
#             for ppe_box in ppe_result.boxes:
#
#                 ppe_confidence = float(
#                     ppe_box.conf[0]
#                 )
#
#                 if ppe_confidence < PPE_CONFIDENCE:
#                     continue
#
#
#                 class_id = int(
#                     ppe_box.cls[0]
#                 )
#
#
#                 class_name = (
#                     ppe_model.names[class_id]
#                 )
#
#
#                 detected_ppe.add(
#                     class_name
#                 )
#
#
#         # ----------------------------------------------------
#         # PPE VIOLATIONS
#         # ----------------------------------------------------
#
#         violations = []
#
#
#         if "no_helmet" in detected_ppe:
#             violations.append(
#                 "NO HELMET"
#             )
#
#
#         if "no_goggle" in detected_ppe:
#             violations.append(
#                 "NO GOGGLES"
#             )
#
#
#         if "no_gloves" in detected_ppe:
#             violations.append(
#                 "NO GLOVES"
#             )
#
#
#         if "no_boots" in detected_ppe:
#             violations.append(
#                 "NO BOOTS"
#             )
#
#
#         if fall_detected:
#
#             violations.append(
#                 "FALL DETECTED"
#             )
#
#
#         # ----------------------------------------------------
#         # DETERMINE STATUS
#         # ----------------------------------------------------
#
#         if violations:
#
#             status = "UNSAFE"
#
#         else:
#
#             status = "SAFE"
#
#
#         # ----------------------------------------------------
#         # DRAW WORKER BOX
#         # ----------------------------------------------------
#
#         if status == "UNSAFE":
#
#             box_color = (
#                 0,
#                 0,
#                 255
#             )
#
#         else:
#
#             box_color = (
#                 0,
#                 255,
#                 0
#             )
#
#
#         cv2.rectangle(
#             frame,
#             (x1, y1),
#             (x2, y2),
#             box_color,
#             2
#         )
#
#
#         # ----------------------------------------------------
#         # WORKER LABEL
#         # ----------------------------------------------------
#
#         label = (
#             f"Worker {track_id} - {status}"
#         )
#
#
#         cv2.putText(
#             frame,
#             label,
#             (
#                 x1,
#                 max(y1 - 10, 20)
#             ),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.6,
#             box_color,
#             2
#         )
#
#
#         # ----------------------------------------------------
#         # DISPLAY VIOLATIONS
#         # ----------------------------------------------------
#
#         text_y = y2 + 25
#
#
#         for violation in violations:
#
#             cv2.putText(
#                 frame,
#                 f"🚨 {violation}",
#                 (
#                     x1,
#                     min(text_y, height - 10)
#                 ),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.55,
#                 (0, 0, 255),
#                 2
#             )
#
#             text_y += 22
#
#
#         # ----------------------------------------------------
#         # SAVE VIOLATION SNAPSHOT
#         # ----------------------------------------------------
#
#         if violations:
#
#             snapshot_count += 1
#
#             snapshot_path = os.path.join(
#                 SNAPSHOT_DIR,
#                 f"CAM-01_worker_{track_id}_frame_{frame_number}.jpg"
#             )
#
#
#             # Save only occasionally
#             # to avoid thousands of images
#
#             if snapshot_count % 10 == 0:
#
#                 cv2.imwrite(
#                     snapshot_path,
#                     frame
#                 )
#
#
#     # ========================================================
#     # CAMERA INFORMATION
#     # ========================================================
#
#     cv2.putText(
#         frame,
#         "CAM-01",
#         (20, 35),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.9,
#         (255, 255, 255),
#         2
#     )
#
#
#     cv2.putText(
#         frame,
#         f"Frame: {frame_number}/{total_frames}",
#         (20, 70),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.6,
#         (255, 255, 255),
#         2
#     )
#
#
#     # ========================================================
#     # SAVE FRAME
#     # ========================================================
#
#     out.write(frame)
#
#
#     # ========================================================
#     # PROGRESS
#     # ========================================================
#
#     if frame_number % 50 == 0:
#
#         percentage = (
#             frame_number
#             / total_frames
#             * 100
#         )
#
#         print(
#             f"Progress: {percentage:.1f}%"
#         )
#
#
# # ============================================================
# # RELEASE
# # ============================================================
#
# cap.release()
# out.release()
#
#
# # ============================================================
# # FINAL RESULT
# # ============================================================
#
# print("\n==============================================")
# print("🎉 CAM-01 PIPELINE COMPLETED")
# print("==============================================")
#
# print(
#     f"Frames processed: {frame_number}"
# )
#
# print(
#     f"Output video: {OUTPUT_VIDEO}"
# )
#
# print(
#     f"Violation snapshots: {SNAPSHOT_DIR}"
# )
#
# print("\n✅ AI PIPELINE TEST COMPLETE")


      #codeeeeee to be safe
import os
import cv2
from ultralytics import YOLO
from api_client import send_safety_event


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

VIDEOS_DIR = os.path.join(
    PROJECT_ROOT,
    "videos"
)

PPE_MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "ppe_best.pt"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "snapshots",
    "pipeline"
)

SNAPSHOT_DIR = os.path.join(
    OUTPUT_DIR,
    "violations"
)


# ============================================================
# CAMERAS
# ============================================================

CAMERAS = [
    "CAM-01",
    "CAM-02",
    "CAM-03",
    "CAM-04",
    "CAM-05"
]


# ============================================================
# SETTINGS
# ============================================================

PERSON_CONFIDENCE = 0.5
PPE_CONFIDENCE = 0.4

FALL_ASPECT_RATIO = 1.2
FALL_CONFIRMATION_FRAMES = 8

SNAPSHOT_INTERVAL = 10

# Prevent the same worker/violation from
# creating an event on every frame.
EVENT_COOLDOWN_FRAMES = 100


# ============================================================
# CREATE DIRECTORIES
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

os.makedirs(
    SNAPSHOT_DIR,
    exist_ok=True
)


# ============================================================
# LOAD MODELS
# ============================================================

print("\n" + "=" * 60)
print("       CONSTRUCTION SAFETY AI PIPELINE")
print("=" * 60)

print("\n⏳ Loading person detection/tracking model...")

person_model = YOLO(
    "yolov8n.pt"
)

print("✅ Person model loaded")


print("\n⏳ Loading PPE model...")

ppe_model = YOLO(
    PPE_MODEL_PATH
)

print("✅ PPE model loaded")

print("\nPPE classes:")
print(ppe_model.names)


# ============================================================
# PROCESS ONE CAMERA
# ============================================================

def process_camera(camera_id):

    print("\n" + "=" * 60)
    print(f"🚧 PROCESSING {camera_id}")
    print("=" * 60)

    # --------------------------------------------------------
    # PATHS
    # --------------------------------------------------------

    video_path = os.path.join(
        VIDEOS_DIR,
        f"{camera_id}.mp4"
    )

    output_video = os.path.join(
        OUTPUT_DIR,
        f"{camera_id}_safety_pipeline.mp4"
    )

    # --------------------------------------------------------
    # CHECK VIDEO
    # --------------------------------------------------------

    if not os.path.exists(video_path):

        print(
            f"❌ Video not found: {video_path}"
        )

        return

    # --------------------------------------------------------
    # OPEN VIDEO
    # --------------------------------------------------------

    cap = cv2.VideoCapture(
        video_path
    )

    if not cap.isOpened():

        print(
            f"❌ Could not open: {video_path}"
        )

        return

    # --------------------------------------------------------
    # VIDEO INFORMATION
    # --------------------------------------------------------

    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps <= 0:
        fps = 25

    total_frames = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )

    print(
        f"Input     : {video_path}"
    )

    print(
        f"Resolution: {width} x {height}"
    )

    print(
        f"FPS       : {fps:.2f}"
    )

    print(
        f"Frames    : {total_frames}"
    )

    print(
        f"Output    : {output_video}"
    )

    # --------------------------------------------------------
    # VIDEO WRITER
    # --------------------------------------------------------

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    out = cv2.VideoWriter(
        output_video,
        fourcc,
        fps,
        (width, height)
    )

    # --------------------------------------------------------
    # TRACKING DATA
    # --------------------------------------------------------

    fall_counters = {}

    fall_alerted = set()

    frame_number = 0

    violation_count = 0

    snapshot_count = 0

    # --------------------------------------------------------
    # EVENT COOLDOWN DATA
    # --------------------------------------------------------

    last_event_frame = {}

    # ========================================================
    # PROCESS FRAMES
    # ========================================================

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1

        # ====================================================
        # PERSON DETECTION + TRACKING
        # ====================================================

        tracking_results = person_model.track(
            frame,
            persist=True,
            classes=[0],
            tracker="bytetrack.yaml",
            verbose=False
        )

        workers = []

        for result in tracking_results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                confidence = float(
                    box.conf[0]
                )

                if confidence < PERSON_CONFIDENCE:
                    continue

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                if box.id is not None:

                    track_id = int(
                        box.id[0]
                    )

                else:

                    track_id = -1

                workers.append(
                    (
                        track_id,
                        x1,
                        y1,
                        x2,
                        y2
                    )
                )

        # ====================================================
        # PROCESS EACH WORKER
        # ====================================================

        for (
            track_id,
            x1,
            y1,
            x2,
            y2
        ) in workers:

            # =================================================
            # FALL DETECTION
            # =================================================

            box_width = x2 - x1
            box_height = y2 - y1

            if box_height > 0:

                aspect_ratio = (
                    box_width /
                    box_height
                )

            else:

                aspect_ratio = 0

            possible_fall = (
                aspect_ratio >=
                FALL_ASPECT_RATIO
            )

            if track_id != -1:

                if track_id not in fall_counters:

                    fall_counters[
                        track_id
                    ] = 0

                if possible_fall:

                    fall_counters[
                        track_id
                    ] += 1

                else:

                    fall_counters[
                        track_id
                    ] = 0

            fall_detected = False

            if (
                track_id != -1
                and
                fall_counters.get(
                    track_id,
                    0
                ) >= FALL_CONFIRMATION_FRAMES
            ):

                fall_detected = True

                fall_alerted.add(
                    track_id
                )

            # =================================================
            # PPE DETECTION
            # =================================================

            worker_crop = frame[
                max(0, y1):min(height, y2),
                max(0, x1):min(width, x2)
            ]

            detected_ppe = set()

            if worker_crop.size > 0:

                ppe_results = ppe_model(
                    worker_crop,
                    verbose=False
                )

                for ppe_result in ppe_results:

                    if ppe_result.boxes is None:
                        continue

                    for ppe_box in ppe_result.boxes:

                        ppe_confidence = float(
                            ppe_box.conf[0]
                        )

                        if ppe_confidence < PPE_CONFIDENCE:
                            continue

                        class_id = int(
                            ppe_box.cls[0]
                        )

                        class_name = ppe_model.names[
                            class_id
                        ]

                        detected_ppe.add(
                            class_name
                        )

            # =================================================
            # PPE VIOLATIONS
            # =================================================

            violations = []

            if "no_helmet" in detected_ppe:

                violations.append(
                    "NO HELMET"
                )

            if "no_goggle" in detected_ppe:

                violations.append(
                    "NO GOGGLES"
                )

            if "no_gloves" in detected_ppe:

                violations.append(
                    "NO GLOVES"
                )

            if "no_boots" in detected_ppe:

                violations.append(
                    "NO BOOTS"
                )

            if fall_detected:

                violations.append(
                    "FALL DETECTED"
                )

            # =================================================
            # STATUS
            # =================================================

            if violations:

                status = "UNSAFE"

                box_color = (
                    0,
                    0,
                    255
                )

            else:

                status = "SAFE"

                box_color = (
                    0,
                    255,
                    0
                )

            # =================================================
            # DRAW WORKER BOX
            # =================================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                box_color,
                2
            )

            # =================================================
            # WORKER LABEL
            # =================================================

            worker_label = (
                f"Worker {track_id} - {status}"
            )

            cv2.putText(
                frame,
                worker_label,
                (
                    x1,
                    max(
                        y1 - 10,
                        20
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                box_color,
                2
            )

            # =================================================
            # DISPLAY VIOLATIONS
            # =================================================

            text_y = y2 + 25

            for violation in violations:

                cv2.putText(
                    frame,
                    violation,
                    (
                        x1,
                        min(
                            text_y,
                            height - 10
                        )
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 0, 255),
                    2
                )

                text_y += 22

            # =================================================
            # SEND EVENTS TO BACKEND
            # =================================================

            if violations:

                violation_count += len(
                    violations
                )

                # ------------------------------------------------
                # Create snapshot for this worker
                # ------------------------------------------------

                snapshot_path = None

                if (
                    frame_number %
                    SNAPSHOT_INTERVAL == 0
                ):

                    snapshot_count += 1

                    snapshot_path = os.path.join(
                        SNAPSHOT_DIR,
                        (
                            f"{camera_id}_"
                            f"worker_{track_id}_"
                            f"frame_{frame_number}_"
                            f"{snapshot_count}.jpg"
                        )
                    )

                    cv2.imwrite(
                        snapshot_path,
                        frame
                    )

                    print(
                        f"📸 Snapshot saved: "
                        f"{snapshot_path}"
                    )

                # ------------------------------------------------
                # Send every violation separately
                # ------------------------------------------------

                for violation in violations:

                    event_type = violation.replace(
                        " ",
                        "_"
                    )

                    event_key = (
                        f"{camera_id}_"
                        f"{track_id}_"
                        f"{event_type}"
                    )

                    last_frame = (
                        last_event_frame.get(
                            event_key,
                            -EVENT_COOLDOWN_FRAMES
                        )
                    )

                    # ------------------------------------------------
                    # Check cooldown
                    # ------------------------------------------------

                    if (
                        frame_number -
                        last_frame
                        < EVENT_COOLDOWN_FRAMES
                    ):

                        continue

                    # ------------------------------------------------
                    # Severity
                    # ------------------------------------------------

                    if violation == "FALL DETECTED":

                        severity = "CRITICAL"

                    else:

                        severity = "HIGH"

                    # ------------------------------------------------
                    # Convert snapshot path
                    # ------------------------------------------------

                    backend_snapshot_path = None

                    if snapshot_path is not None:

                        backend_snapshot_path = (
                            os.path.relpath(
                                snapshot_path,
                                PROJECT_ROOT
                            )
                        )

                    # ------------------------------------------------
                    # SEND TO NODE.JS
                    # ------------------------------------------------

                    print(
                        f"🚨 Sending event: "
                        f"{camera_id} | "
                        f"Worker {track_id} | "
                        f"{event_type}"
                    )

                    send_safety_event(
                        camera_id=camera_id,
                        worker_id=track_id,
                        event_type=event_type,
                        severity=severity,
                        snapshot_path=(
                            backend_snapshot_path
                        )
                    )

                    # ------------------------------------------------
                    # Update cooldown
                    # ------------------------------------------------

                    last_event_frame[
                        event_key
                    ] = frame_number

        # ====================================================
        # CAMERA INFORMATION
        # ====================================================

        cv2.putText(
            frame,
            f"Camera: {camera_id}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            (
                f"Frame: "
                f"{frame_number}/"
                f"{total_frames}"
            ),
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # ====================================================
        # SAVE FRAME
        # ====================================================

        out.write(
            frame
        )

        # ====================================================
        # PROGRESS
        # ====================================================

        if frame_number % 50 == 0:

            if total_frames > 0:

                percentage = (
                    frame_number /
                    total_frames *
                    100
                )

            else:

                percentage = 0

            print(
                f"{camera_id} Progress: "
                f"{percentage:.1f}%"
            )

    # ========================================================
    # RELEASE
    # ========================================================

    cap.release()

    out.release()

    # ========================================================
    # CAMERA RESULT
    # ========================================================

    print("\n----------------------------------------")

    print(
        f"✅ {camera_id} COMPLETED"
    )

    print(
        f"Frames processed: "
        f"{frame_number}"
    )

    print(
        f"Unsafe detections: "
        f"{violation_count}"
    )

    print(
        f"Snapshots created: "
        f"{snapshot_count}"
    )

    print(
        f"Output: "
        f"{output_video}"
    )

    print("----------------------------------------")


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 60)
    print("🚧 STARTING ALL 5 CAMERA PIPELINE")
    print("=" * 60)

    for camera_id in CAMERAS:

        process_camera(
            camera_id
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("\n" + "=" * 60)
    print("🎉 ALL 5 CAMERAS PROCESSED!")
    print("=" * 60)

    print("\nGenerated pipeline videos:")

    for camera_id in CAMERAS:

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{camera_id}_safety_pipeline.mp4"
        )

        if os.path.exists(
            output_file
        ):

            print(
                f"✓ {camera_id}_safety_pipeline.mp4"
            )

        else:

            print(
                f"❌ {camera_id} output missing"
            )

    print("\nPipeline output folder:")
    print(OUTPUT_DIR)

    print("\nViolation snapshots:")
    print(SNAPSHOT_DIR)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()