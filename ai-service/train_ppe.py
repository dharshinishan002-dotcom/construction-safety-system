# from ultralytics import YOLO
#
#
# # Load pretrained YOLO model
# model = YOLO("yolov8n.pt")
#
#
# # Train on Construction-PPE dataset
# model.train(
#     data="construction-ppe.yaml",
#     epochs=50,
#     imgsz=640,
#     batch=8,
#     name="construction_ppe"
# )

from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="construction-ppe.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    name="construction_ppe"
)