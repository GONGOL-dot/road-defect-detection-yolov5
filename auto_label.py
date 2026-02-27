from ultralytics import YOLO
import os

# load pretrained model
model = YOLO("yolov8n.pt")

# image & label folders
img_dir = "dataset/images/train"
label_dir = "dataset/labels/train"

os.makedirs(label_dir, exist_ok=True)

# loop all images
for img in os.listdir(img_dir):

    if img.endswith((".jpg", ".png", ".jpeg")):

        img_path = os.path.join(img_dir, img)

        # predict
        results = model(img_path)

        # get boxes
        r = results[0]
        boxes = r.boxes.xywhn.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy()

        # save label txt
        label_path = os.path.join(label_dir, img.split(".")[0] + ".txt")

        with open(label_path, "w") as f:
            for box, cls in zip(boxes, classes):
                x, y, w, h = box
                f.write(f"{int(cls)} {x} {y} {w} {h}\n")

print("AUTO LABELING COMPLETED")