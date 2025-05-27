# from base import app
import math
import os
import sys

import cv2
import cvzone
import numpy as np
from ultralytics import YOLO

from base import app

OUTPUT_VIDEO_FOLDER = 'base/static/adminResources/videos/output'
app.config['OUTPUT_VIDEO_FOLDER'] = OUTPUT_VIDEO_FOLDER
AVI_VIDEO_FOLDER = 'base/static/adminResources/videos/avi'
app.config['AVI_VIDEO_FOLDER'] = AVI_VIDEO_FOLDER

# Set base directory and import Sort tracker
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, BASE_DIR)
from base.service_d.sort.sort import Sort


def ai(video_filename, video_name1):
    print("video_filename>>>>>>>>>>", video_filename)
    input_video_path = os.path.join(BASE_DIR, video_filename)

    avi_video_path = os.path.join(AVI_VIDEO_FOLDER, f"proced_{video_name1}")
    folder_path, video_filename1 = os.path.split(avi_video_path)
    print("folder path ???????????????????????????/", folder_path)
    print("video_filename1???????????????????????????", video_filename1)

    if not os.path.exists(OUTPUT_VIDEO_FOLDER):
        os.makedirs(OUTPUT_VIDEO_FOLDER)

    print("Input video path:", input_video_path)
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Error: Cannot open video file.")
        sys.exit(1)

    model = YOLO("model/yolov8n.pt")

    class_file = os.path.join(BASE_DIR, "base/service_d/model/classes.txt")
    with open(class_file, 'r') as f:
        classnames = f.read().splitlines()

    tracker = Sort(max_age=30, min_hits=3)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    avi_video_path = f'base/static/adminResources/videos/avi/avi_video_{video_name1}.avi'

    out = cv2.VideoWriter(avi_video_path, fourcc, fps, (frame_width, frame_height))

    counter = {cls: set() for cls in ["bicycle", "car", "motorcycle", "bus", "truck"]}
    seen_ids = {}
    id_lost_tracker = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video reached or error reading frame.")
            break

        detections = np.empty((0, 6))
        result = model(frame, stream=True)

        for info in result:
            boxes = info.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                classindex = box.cls[0]

                conf = math.ceil(conf * 100)
                classindex = int(classindex)
                objectdetect = classnames[classindex]

                if objectdetect in counter and conf > 60:
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    new_detections = np.array([x1, y1, x2, y2, conf, classindex])
                    detections = np.vstack((detections, new_detections))

        if detections.shape[0] > 0:
            track_result = tracker.update(detections[:, :5])
            current_ids = {cls: set() for cls in counter}

            for results, classindex in zip(track_result, detections[:, 5]):
                x1, y1, x2, y2, id = results
                x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
                obj_class = classnames[int(classindex)]

                if obj_class in counter:
                    current_ids[obj_class].add(id)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cvzone.putTextRect(frame, f'{id}', [x1 + 8, y1 - 12], thickness=2, scale=1.5)

                    if id not in counter[obj_class]:
                        if seen_ids.get(id, 0) > 3:
                            counter[obj_class].add(id)
                        seen_ids[id] = seen_ids.get(id, 0) + 1

        lost_ids = set(seen_ids.keys()) - {id for ids in current_ids.values() for id in ids}
        for lost_id in lost_ids:
            id_lost_tracker[lost_id] = id_lost_tracker.get(lost_id, 0) + 1
            if id_lost_tracker[lost_id] > 10:
                seen_ids.pop(lost_id, None)
                id_lost_tracker.pop(lost_id, None)

        for present_id in {id for ids in current_ids.values() for id in ids}:
            id_lost_tracker.pop(present_id, None)

        y_offset = 34
        for vehicle_type, ids in counter.items():
            cvzone.putTextRect(frame, f'{vehicle_type.capitalize()}s = {len(ids)}', [30, y_offset], thickness=3, scale=1.8, border=2)
            y_offset += 40

        cv2.imshow('Processed Video', frame)

        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vehicle_counts = {vehicle_type: len(ids) for vehicle_type, ids in counter.items()}
    # =================================================

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    if os.path.exists(avi_video_path):
        print(f" Processed video saved at: {avi_video_path}")
    else:
        print("Error: Processed video was not saved!")

    print("\nVehicle Counts:")
    for vehicle_type, count in vehicle_counts.items():
        print(f"{vehicle_type.capitalize()}s: {count}")
    # avi_to_mp4()
    return [vehicle_counts, avi_video_path]


from moviepy import VideoFileClip


def avi_to_mp4():
    print("helllooooooooooooooooooo")
    # Iterate through all files in the AVI folder
    for video_filename in os.listdir(AVI_VIDEO_FOLDER):
        if video_filename.endswith(".avi"):
            # Get the full path of the input and output files
            if True:
                input_path = os.path.join(AVI_VIDEO_FOLDER, video_filename)
                output_name = os.path.splitext(video_filename)[0] + ".mp4"
                output_path = os.path.join(OUTPUT_VIDEO_FOLDER, output_name)

                # Convert AVI to MP4
                clip = VideoFileClip(input_path)
                clip.write_videofile(output_path)
                print(f"Converted {video_filename} to {output_name}")

            return output_path

        # return output_name, output_path

# import cv2
# from ultralytics import YOLO
#
# model = YOLO("base/service_d/model/yolov8n.pt")
#
# def add_detection(source, name):
#     cap = cv2.VideoCapture(source)
#     frameRate = 1  # Frames per second to process
#     sec = round(0 + frameRate, 1)
#
#     # Valid class IDs based on your model's output
#     classes_id = [1, 2, 3, 5, 7]
#
#     hasFrames, image = cap.read()
#     if not hasFrames:
#         print("Error: Unable to read the video source.")
#         return
#
#     height, width, _ = image.shape
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI format
#     output_video_filename = f'base/static/adminResourses/avi_video/output_video_{name}.avi'
#     video = cv2.VideoWriter(output_video_filename, fourcc, frameRate,
#                             (width, height))
#
#     while True:
#         cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
#         hasFrames, image = cap.read()
#         if not hasFrames:
#             break  # Stop if no more frames
#
#         results_list = model.track(image, classes=classes_id, persist=True)
#         for results in results_list:
#             annotated_frame = results.plot()
#             video.write(annotated_frame)
#
#             # Dictionary to store counts for each class in the frame
#             class_counts = {model.names[class_id]: 0 for class_id in classes_id
#                             if class_id < len(model.names)}
#
#             # Loop through detected objects and count them
#             for box in results.boxes:
#                 class_id = int(box.cls)  # Get class ID
#
#                 if class_id in classes_id and class_id < len(model.names):
#                     class_name = model.names[class_id]
#                     class_counts[class_name] += 1
#                 else:
#                     print(
#                         f"Warning: Detected class ID {class_id} is out of range!")
#
#             # Print class counts for debugging
#             print(f"Counts for frame {sec}:")
#             for class_name, count in class_counts.items():
#                 print(f"{class_name}: {count}")
#
#         sec = round(sec + frameRate, 2)
#     cap.release()
#     video.release()
#     cv2.destroyAllWindows()
#     print(f"Processing complete. Video saved at {output_video_filename}")
#     return class_name,count
#
# import os
# from moviepy import VideoFileClip
#
# avi_folder = "base/static/adminResourses/avi_video/"
# output_folder = "base/static/adminResourses/output/"
#
#
# def avi_to_mp4():
#     # Iterate through all files in the AVI folder
#     for filename in os.listdir(avi_folder):
#         if filename.endswith(".avi"):
#             # Get the full path of the input and output files
#             input_path = os.path.join(avi_folder, filename)
#             output_name = os.path.splitext(filename)[0] + ".mp4"
#             output_path = os.path.join(output_folder, output_name)
#
#             # Convert AVI to MP4
#             clip = VideoFileClip(input_path)
#             clip.write_videofile(output_path)
#
#             print(f"Converted {filename} to {output_name}")
#
#
# ### Vehicle Count ###
#
#
# =================================================================================
# import math
# import os
# import sys
# import cv2
# import cvzone
# import numpy as np
# from ultralytics import YOLO
#
# # Set base directory and import Sort tracker
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
# sys.path.insert(0, BASE_DIR)
# from base.service_d.sort.sort import Sort
#
# def ai(video_path, processed_video_path):
#     if not os.path.exists(os.path.dirname(processed_video_path)):
#         os.makedirs(os.path.dirname(processed_video_path))
#
#     print("🔹 Input video path:", video_path)
#     cap = cv2.VideoCapture(video_path)
#
#     if not cap.isOpened():
#         print("❌ Error: Cannot open video file.")
#         sys.exit(1)
#
#     model = YOLO("model/yolov8n.pt")
#
#     class_file = os.path.join(BASE_DIR, "base/service_d/model/classes.txt")
#     with open(class_file, 'r') as f:
#         classnames = f.read().splitlines()
#
#     tracker = Sort(max_age=30, min_hits=3)
#
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     if fps == 0:
#         fps = 30  # Default FPS if video metadata is incorrect
#
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(processed_video_path, fourcc, fps, (frame_width, frame_height))
#
#     counter = {cls: set() for cls in ["bicycle", "car", "motorcycle", "bus", "truck"]}
#     seen_ids = {}
#     id_lost_tracker = {}
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             print("🔚 End of video reached or error reading frame.")
#             break
#
#         detections = np.empty((0, 6))
#         result = model(frame, stream=True)
#
#         for info in result:
#             boxes = info.boxes
#             for box in boxes:
#                 x1, y1, x2, y2 = box.xyxy[0].tolist()
#                 conf = box.conf[0].item()
#                 classindex = int(box.cls[0].item())
#
#                 conf = math.ceil(conf * 100)
#                 objectdetect = classnames[classindex]
#
#                 if objectdetect in counter and conf > 70:  # Increased threshold for better accuracy
#                     x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#                     new_detections = np.array([x1, y1, x2, y2, conf, classindex])
#                     detections = np.vstack((detections, new_detections))
#
#         if detections.shape[0] > 0:
#             track_result = tracker.update(detections[:, :5])
#             current_ids = {cls: set() for cls in counter}
#
#             for results, classindex in zip(track_result, detections[:, 5]):
#                 x1, y1, x2, y2, id = map(int, results)
#                 obj_class = classnames[int(classindex)]
#
#                 if obj_class in counter:
#                     current_ids[obj_class].add(id)
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
#                     cvzone.putTextRect(frame, f'ID: {id}', [x1 + 8, y1 - 12], thickness=2, scale=1.5)
#
#                     if id not in counter[obj_class]:
#                         if seen_ids.get(id, 0) > 3:
#                             counter[obj_class].add(id)
#                         seen_ids[id] = seen_ids.get(id, 0) + 1
#
#         lost_ids = set(seen_ids.keys()) - {id for ids in current_ids.values() for id in ids}
#         for lost_id in lost_ids:
#             id_lost_tracker[lost_id] = id_lost_tracker.get(lost_id, 0) + 1
#             if id_lost_tracker[lost_id] > 10:
#                 seen_ids.pop(lost_id, None)
#                 id_lost_tracker.pop(lost_id, None)
#
#         for present_id in {id for ids in current_ids.values() for id in ids}:
#             id_lost_tracker.pop(present_id, None)
#
#         y_offset = 34
#         for vehicle_type, ids in counter.items():
#             cvzone.putTextRect(frame, f'{vehicle_type.capitalize()}s = {len(ids)}', [30, y_offset], thickness=3, scale=1.8, border=2)
#             y_offset += 40
#
#         cv2.imshow('Processed Video', frame)
#         out.write(frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             print("🛑 Detection stopped manually by user.")
#             break
#
#     vehicle_counts = {vehicle_type: len(ids) for vehicle_type, ids in counter.items()}
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()
#
#     if os.path.exists(processed_video_path):
#         print(f"✅ Processed video saved at: {processed_video_path}")
#     else:
#         print("❌ Error: Processed video was not saved!")
#
#     print("\n📊 Vehicle Counts:")
#     for vehicle_type, count in vehicle_counts.items():
#         print(f"{vehicle_type.capitalize()}s: {count}")
#
#     return vehicle_counts
# =================================================================================

#
#
#
# ### cattle Count ###
#
#
# import sys
# import os
# import cv2
# import math
# import numpy as np
# from ultralytics import YOLO
# import cvzone
#
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(_file_), '../..'))
# sys.path.insert(0, BASE_DIR)
#
# from base.service_d.sort.sort import Sort
#
# video_path = os.path.join(BASE_DIR, "base/static/adminResources/input/4.mp4")
# cap = cv2.VideoCapture(video_path)
#
# model = YOLO("model/yolov8n.pt")
#
# class_file = "model/classes.txt"
# with open(class_file, 'r') as f:
#     classnames = f.read().splitlines()
#
# tracker = Sort(max_age=30, min_hits=3)
#
# ret, frame = cap.read()
# if not ret:
#     print("Error: Unable to read video file.")
#     sys.exit(1)
#
# counter = set()
# seen_ids = {}
# id_lost_tracker = {}
# specific_classes = [15, 16, 17, 18, 19]
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         cap = cv2.VideoCapture(video_path)
#         continue
#
#     detections = np.empty((0, 5))
#     result = model(frame, stream=True)
#
#     for info in result:
#         boxes = info.boxes
#         for box in boxes:
#             x1, y1, x2, y2 = box.xyxy[0]
#             conf = box.conf[0]
#             classindex = box.cls[0]
#
#             conf = math.ceil(conf * 100)
#             classindex = int(classindex)
#
#             if classindex in specific_classes and conf > 60:
#                 x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#                 new_detections = np.array([x1, y1, x2, y2, conf])
#                 detections = np.vstack((detections, new_detections))
#
#     track_result = tracker.update(detections)
#     current_ids = set()
#
#     for results in track_result:
#         x1, y1, x2, y2, id = results
#         x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
#
#         current_ids.add(id)
#
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
#         cvzone.putTextRect(frame, f'{id}', [x1 + 8, y1 - 12], thickness=2, scale=1.5)
#
#         if id not in counter:
#             if seen_ids.get(id, 0) > 3:
#                 counter.add(id)
#             seen_ids[id] = seen_ids.get(id, 0) + 1
#
#     lost_ids = set(seen_ids.keys()) - current_ids
#     for lost_id in lost_ids:
#         id_lost_tracker[lost_id] = id_lost_tracker.get(lost_id, 0) + 1
#         if id_lost_tracker[lost_id] > 10:
#             seen_ids.pop(lost_id, None)
#             id_lost_tracker.pop(lost_id, None)
#
#     for present_id in current_ids:
#         id_lost_tracker.pop(present_id, None)
#
#     cvzone.putTextRect(frame, f'Total Count = {len(counter)}', [290, 34], thickness=4, scale=2.3, border=2)
#
#     cv2.imshow('frame', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
