from ultralytics import YOLO

model = YOLO("../model/yolov8n.pt")
# image = ("E:\internship\projectworkspace\EyesOnTheCattle/base/static/adminResourses/input/WhatsApp_Video.mp4")
image = ("D:/CompanyProject/Internship_project_2024_2025/cattle_detection"
         "/projectworkspace/EyesOnTheCattle/base/static/adminResourses/input"
         "/2.mp4")
# classes_id = [15, 16, 17, 18, 19, 20, 21, 22]
classes_id = [1,2,3,5,7]

results = model.predict(image, show=True, stream=True, imgsz=512,
                        classes=classes_id)
for result in results:
    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        if (class_id == classes_id):
            cords = box.xyxy[0].tolist()
            cords = [round(x) for x in cords]
            conf = round(box.conf[0].item(), 2)
print(results)
