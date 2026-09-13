import requests
import os

# ============================================================
# BACKEND URL
# ============================================================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:5001/api/safety-events"
)


# ============================================================
# SEND SAFETY EVENT TO BACKEND
# ============================================================

def send_safety_event(
    camera_id,
    worker_id,
    event_type,
    severity,
    snapshot_path=None
):

    data = {
        "cameraId": camera_id,
        "workerId": str(worker_id),
        "eventType": event_type,
        "severity": severity,
        "snapshotPath": snapshot_path,
        "status": "OPEN"
    }

    try:

        response = requests.post(
            BACKEND_URL,
            json=data,
            timeout=5
        )

        if response.status_code in [200, 201]:

            print(
                f"✅ Event sent successfully: "
                f"{event_type}"
            )

            return True

        else:

            print(
                f"❌ Backend error: "
                f"{response.status_code}"
            )

            print(response.text)

            return False

    except requests.exceptions.RequestException as e:

        print(
            f"❌ Could not connect to backend: {e}"
        )

        return False


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    send_safety_event(
        camera_id="CAM-01",
        worker_id="1",
        event_type="NO_HELMET",
        severity="HIGH",
        snapshot_path="snapshots/violations/test.jpg"
    )