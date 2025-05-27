import os

from charset_normalizer import detect
from flask import render_template, request, redirect, url_for, jsonify
from flask_executor import Executor
from werkzeug.utils import secure_filename

from base import app

executor = Executor(app)

from base.com.dao.area_dao import AreaDAO
from base.com.dao.camera_dao import CameraDAO
from base.com.dao.crossroad_dao import CrossRoadDAO
from base.com.dao.detection_dao import DetectionDAO
from base.com.dao.video_dao import VideoDAO
from base.com.vo.detection_vo import DetectionVO
from base.com.vo.video_vo import VideoVO
from base.service_d import detect
from base.com.controller.login_controller import login_required


VIDEO_FOLDER = 'base/static/adminResources/videos/input/'
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER

OUTPUT_VIDEO_FOLDER = 'base/static/adminResources/videos/output/'
app.config['OUTPUT_VIDEO_FOLDER'] = OUTPUT_VIDEO_FOLDER

AVI_VIDEO_FOLDER = 'base/static/adminResources/videos/avi/'
app.config['AVI_VIDEO_FOLDER'] = AVI_VIDEO_FOLDER

video_filename = None
video_name1 = None


@app.route('/admin/load_ajax_camera')
@login_required('admin')
def admin_load_ajax_camera():
    try:
        crossroad_id = int(request.args.get('crossroad_id'))
        print("s---", crossroad_id)
        response_message = []

        crossroad_dao_obj = CrossRoadDAO()
        data = crossroad_dao_obj.ajax_camera_list()

        for camera in data:
            if camera.camera_crossroad_id == crossroad_id:
                response_list = [
                    {"camera_id": camera.camera_id,
                     "camera_name": camera.camera_name}]

                print(response_list, "response_list??????????")
                response_message.extend(response_list)

        return jsonify(response_message)
    except:
        return render_template('')


@app.route("/admin/insert_video", methods=['GET', 'POST'])
@login_required('admin')
def insert_video():
    area_id = request.form.get('area_id')
    crossroad_id = request.form.get('crossroad_id')
    camera_id = request.form.get('camera_id')

    video_file = request.files.get('video_name')
    print("video_file????????????????", video_file)
    print("area_id", area_id)
    print("crossroad_id", crossroad_id)
    global video_name1
    video_name = secure_filename(video_file.filename)
    video_name1,ex = video_name.rsplit('.',1)
    video_path = os.path.join(app.config['VIDEO_FOLDER'])
    video_file.save(os.path.join(video_path, video_name))
    global video_filename
    video_filename = os.path.join(video_path, video_name)
    print("video_filename", video_filename)

    video_dao = VideoDAO()
    video_vo = VideoVO()

    video_vo.video_area_id = area_id
    video_vo.video_crossroad_id = crossroad_id
    video_vo.video_camera_id = camera_id
    video_vo.video_name = video_name
    video_vo.video_path = video_path.replace("base", "..")

    video_dao.insert_video(video_vo)
    video_id = video_vo.video_id
    # t = threading.Thread(target=video, args=(video_id,))
    # t.start()
    executor.submit(video, video_id)
    # video()
    return redirect(url_for('admin_view_video'))


def video(video_id):
    with app.app_context():
        print("video_id", video_id)

        ai = detect.ai(video_filename, video_name1)
        avi = detect.avi_to_mp4()
        print("aiiiiiiiiiiiiiiiiiiii", ai)
        bicycle = ai[0]['bicycle']
        car = ai[0]['car']
        motorcycle = ai[0]['motorcycle']
        bus = ai[0]['bus']
        truck = ai[0]['truck']
        output = ai[1]
        outputavi_video_path, outputavi_video_name = os.path.split(output)
        # print(output_video_path)
        print("aviiiiiiiiii", avi)
        output_folder_path, output_video_name = os.path.split(avi)
        # print("output folder path ",output_folder_path,output_video_name)
        detection_dao = DetectionDAO()
        detection_vo = DetectionVO()
        detection_vo.car_count = car
        detection_vo.truck_count = truck
        detection_vo.bus_count = bus
        detection_vo.bicycle_count = bicycle
        detection_vo.motorcycle_count = motorcycle
        detection_vo.output_video_path = output_folder_path
        detection_vo.output_video_name = output_video_name
        detection_vo.avi_video_path = outputavi_video_path
        detection_vo.avi_video_name = outputavi_video_name
        detection_vo.detection_video_id = video_id
        # app.app_context().push()
        detection_dao.insert_detect(detection_vo)
        print("done")

    # detection_dao.insert_detect(detection_vo)

    # detect.avi_to_mp4()


@app.route("/admin/view_video")
@login_required('admin')
def admin_view_video():
    # video_id = request.args.get('video_id')
    # print('///////////////', video_id)
    video_dao = VideoDAO()
    video_vo_list = video_dao.view_video()
    # print('//////QQQQQQQQQQQQ/////////', video_vo_list)
    # video_vo_info = video_dao.video_info(video_id)
    area_dao = AreaDAO()
    crossroad_dao = CrossRoadDAO()
    camera_dao = CameraDAO()
    area_data = area_dao.view_area()
    crossroad_data = crossroad_dao.view_crossroad()
    camera_data = camera_dao.view_camera()
    return render_template('admin/viewVideo.html',
                           video_vo_list=video_vo_list,
                           area_data=area_data,
                           crossroad_data=crossroad_data,
                           camera_data=camera_data)
    # video_vo_info=video_vo_info)


@app.route("/admin/video_info")
@login_required('admin')
def admin_info_video():
    video_id = request.args.get('video_id')
    # detection_id = request.args.get('detection_id')

    print("video_id received:", video_id)

    video_dao = VideoDAO()
    video_vo = VideoVO(video_id=video_id)

    info_data = video_dao.video_info(video_vo)

    if not info_data:
        return jsonify({"error": "Video not found"}), 404

    area_dao = AreaDAO()
    area_name = area_dao.get_area_name(info_data.get("video_area_id"))

    crossroad_dao = CrossRoadDAO()
    crossroad_name = crossroad_dao.get_crossroad_name(info_data.get("video_crossroad_id"))

    camera_dao = CameraDAO()
    camera_name = camera_dao.get_camera_name(info_data.get("video_camera_id"))

    video_filename = info_data["video_name"]
    video_path = f"/static/adminResources/videos/input/{video_filename}"
    file_type = os.path.splitext(video_filename)[1][1:]

    info_data["video_path"] = video_path
    info_data["area_name"] = area_name
    info_data["crossroad_name"] = crossroad_name
    info_data["camera_name"] = camera_name
    info_data["file_type"] = file_type
    info_data["video_name"] = video_filename

    detection_dao = DetectionDAO()
    detection_list = detection_dao.detection_info(video_vo)
    info_data["detections"] = detection_list  # Attach the list of detections to your response
    if detection_list:
        # Get the first detection (assuming one detection per video)
        detection = detection_list[0]
    info_data.update({
        "car_count": detection.get("car_count"),
        "bus_count": detection.get("bus_count"),
        "motorcycle_count": detection.get("motorcycle_count"),
        "truck_count": detection.get("truck_count"),
        "bicycle_count": detection.get("bicycle_count"),
        "output_video_path": f"/static/adminResources/videos/output/{detection.get('output_video_name')}",
        "avi_video_path": f"/static/adminResources/videos/output/{detection.get('avi_video_name')}",
        "input_video_path":f"/static/adminResources/videos/input/{detection.get('video_name')}"
    })


    print("Updated info_data:", info_data)
    print("video_area_id received:", info_data.get("video_area_id"))

    return jsonify(info_data)


# @app.route('/admin/delete_video', methods=['GET', 'POST'])
# def admin_delete_video():
#     video_dao = VideoDAO()
#     video_id = request.args.get('video_id')
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",video_id)
#     video_vo_list = video_dao.video_delete(video_id)
#     print("dknceddc", video_vo_list)
#     video_name = video_vo_list.video_name
#     print("product_image_name", video_name)
#     file_path = os.path.join(app.config['VIDEO_FOLDER'], video_name)
#     if os.path.exists(file_path):
#         os.remove(file_path)
#     else:
#         print("path not exist")
#     return redirect(url_for('admin_view_video'))

@app.route('/admin/delete_video', methods=['GET', 'POST'])
@login_required('admin')
def admin_delete_video():
    video_dao = VideoDAO()
    video_id = request.args.get('video_id')
    video_vo_list = video_dao.delete_video(video_id)
    print("video_vo_;lisr>>>>>>>>>>>>>>>>>>", video_vo_list)
    video_name = video_vo_list.video_name
    file_path = os.path.join(app.config['VIDEO_FOLDER'], video_name)
    output_file_path = os.path.join(app.config['OUTPUT_VIDEO_FOLDER'], video_name)
    avi_file_path = os.path.join(app.config['AVI_VIDEO_FOLDER'], video_name)

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("path not exist")
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    else:
        print("path not exist output")
    if os.path.exists(avi_file_path):
        os.remove(avi_file_path)
    else:
        print("avi path not exist")

    return redirect(url_for('admin_view_video'))


@app.route('/admin/get_crossroads_with_filter')
@login_required('admin')
def get_crossroads_with_filter():
    cossroad_dao = CrossRoadDAO()
    area_id = request.args.get('area_id')
    crossroads = cossroad_dao.get_crossroads_with_filter(area_id)
    return jsonify([{"crossroad_id": c.crossroad_id, "crossroad_name": c.crossroad_name} for c in crossroads])


@app.route('/admin/get_cameras_with_filter')
@login_required('admin')
def get_cameras_with_filter():
    camera_dao = CameraDAO()
    crossroad_id = request.args.get('crossroad_id')
    cameras = camera_dao.get_cameras_with_filter(crossroad_id)
    return jsonify([{"camera_id": c.camera_id, "camera_name": c.camera_name} for c in cameras])


@app.route('/admin/view_detection', methods=['GET', 'POST'])
@login_required('admin')
def admin_view_detection():
    detection_dao = DetectionDAO()
    detection_vo_list = detection_dao.view_detection()
    return render_template('admin/viewArea.html', detection_vo_list=detection_vo_list)

# import os
# import time
#
# from flask import render_template, request, redirect, url_for, jsonify
# from werkzeug.utils import secure_filename
#
# from base import app
# from base.com.dao.area_dao import AreaDAO
# from base.com.dao.camera_dao import CameraDAO
# from base.com.dao.crossroad_dao import CrossRoadDAO
# from base.com.dao.video_dao import VideoDAO
# from base.com.vo.video_vo import VideoVO
# from base.service_d.detect import ai
#
# VIDEO_FOLDER = 'base/static/adminResources/videos/'
# OUTPUT_FOLDER = 'base/static/adminResources/output/'
# app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
# app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
#
# if not os.path.exists(OUTPUT_FOLDER):
#     os.makedirs(OUTPUT_FOLDER)
#
#
# @app.route('/admin/load_video')
# def admin_load_video():
#     area_dao = AreaDAO()
#     crossroad_dao = CrossRoadDAO()
#     camera_dao = CameraDAO()
#     area_data = area_dao.view_area()
#     crossroad_data = crossroad_dao.view_crossroad()
#     camera_data = camera_dao.view_camera()
#     return render_template("admin/addVideo.html", area_data=area_data,
#                            crossroad_data=crossroad_data, camera_data=camera_data)
#
#
# @app.route('/admin/load_ajax_camera')
# def admin_load_ajax_camera():
#     crossroad_id = int(request.args.get('crossroad_id'))
#     response_message = []
#
#     crossroad_dao_obj = CrossRoadDAO()
#     data = crossroad_dao_obj.ajax_camera_list()
#
#     for camera in data:
#         if camera.camera_crossroad_id == crossroad_id:
#             response_list = [
#                 {"camera_id": camera.camera_id,
#                  "camera_name": camera.camera_name}]
#             response_message.extend(response_list)
#
#     return jsonify(response_message)
#
#
# @app.route("/admin/insert_video", methods=['GET', 'POST'])
# def insert_video():
#     area_id = request.form.get('area_id')
#     crossroad_id = request.form.get('crossroad_id')
#     camera_id = request.form.get('camera_id')
#     video_file = request.files.get('video_name')
#
#     video_name = secure_filename(video_file.filename)
#     video_path = os.path.join(app.config['VIDEO_FOLDER'])
#     video_file.save(video_path,video_name)
#
#     video_dao = VideoDAO()
#     video_vo = VideoVO()
#
#     video_vo.video_area_id = area_id
#     video_vo.video_crossroad_id = crossroad_id
#     video_vo.video_camera_id = camera_id
#     video_vo.video_name = video_name
#     video_vo.video_path = video_path.replace("base", "..")
#     video_dao.insert_video(video_vo)
#
#     timestamp = int(time.time())
#     processed_video_name = f"processed_video_{timestamp}.mp4"
#     processed_video_path = os.path.join(app.config['OUTPUT_FOLDER'], processed_video_name)
#
#     vehicle_count = ai(video_path, processed_video_path)
#     print("Processed Vehicle Count:", vehicle_count)
#
#     return redirect(url_for('admin_view_video'))
#
#
# @app.route("/admin/view_video")
# def admin_view_video():
#     video_dao = VideoDAO()
#     video_vo_list = video_dao.view_video()
#     area_dao = AreaDAO()
#     crossroad_dao = CrossRoadDAO()
#     camera_dao = CameraDAO()
#     area_data = area_dao.view_area()
#     crossroad_data = crossroad_dao.view_crossroad()
#     camera_data = camera_dao.view_camera()
#     return render_template('admin/viewVideo.html',
#                            video_vo_list=video_vo_list,
#                            area_data=area_data,
#                            crossroad_data=crossroad_data,
#                            camera_data=camera_data)
#
#
# @app.route("/admin/video_info")
# def admin_info_video():
#     video_id = request.args.get('video_id')
#     video_dao = VideoDAO()
#     video_vo = VideoVO(video_id=video_id)
#     info_data = video_dao.video_info(video_vo)
#
#     if not info_data:
#         return jsonify({"error": "Video not found"}), 404
#
#     area_dao = AreaDAO()
#     area_name = area_dao.get_area_name(info_data.get("video_area_id"))
#     crossroad_dao = CrossRoadDAO()
#     crossroad_name = crossroad_dao.get_crossroad_name(info_data.get("video_crossroad_id"))
#     camera_dao = CameraDAO()
#     camera_name = camera_dao.get_camera_name(info_data.get("video_camera_id"))
#
#     video_filename = info_data["video_name"]
#     video_path = f"/static/adminResources/videos/{video_filename}"
#     file_type = os.path.splitext(video_filename)[1][1:]
#
#     info_data.update({
#         "video_path": video_path,
#         "area_name": area_name,
#         "crossroad_name": crossroad_name,
#         "camera_name": camera_name,
#         "file_type": file_type,
#         "video_name": video_filename
#     })
#
#     return jsonify(info_data)
#
#
# @app.route('/admin/delete_video', methods=['GET', 'POST'])
# def admin_delete_video():
#     video_dao = VideoDAO()
#     video_id = request.args.get('video_id')
#     video_dao.delete_video(video_id)
#     return redirect(url_for('admin_view_video'))
#
#
# @app.route('/admin/get_crossroads_with_filter')
# def get_crossroads_with_filter():
#     crossroad_dao = CrossRoadDAO()
#     area_id = request.args.get('area_id')
#     crossroads = crossroad_dao.get_crossroads_with_filter(area_id)
#     return jsonify([{"crossroad_id": c.crossroad_id, "crossroad_name": c.crossroad_name} for c in crossroads])
#
#
# @app.route('/admin/get_cameras_with_filter')
# def get_cameras_with_filter():
#     camera_dao = CameraDAO()
#     crossroad_id = request.args.get('crossroad_id')
#     cameras = camera_dao.get_cameras_with_filter(crossroad_id)
#     return jsonify([{"camera_id": c.camera_id, "camera_name": c.camera_name} for c in cameras])

# import os
# import time
#
# from flask import render_template, request, redirect, url_for, jsonify
# from werkzeug.utils import secure_filename
#
# from base import app
# from base.com.dao.area_dao import AreaDAO
# from base.com.dao.camera_dao import CameraDAO
# from base.com.dao.crossroad_dao import CrossRoadDAO
# from base.com.dao.video_dao import VideoDAO
# from base.com.vo.video_vo import VideoVO
# from base.service_d.detect import ai
#
# VIDEO_FOLDER = 'base/static/adminResources/videos/'
# app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
#
# OUTPUT_FOLDER = 'base/static/adminResources/output/'
# app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
# app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
#
# if not os.path.exists(OUTPUT_FOLDER):
#     os.makedirs(OUTPUT_FOLDER)
#
#
# @app.route('/admin/load_video')
# def admin_load_video():
#     area_dao = AreaDAO()
#     crossroad_dao = CrossRoadDAO()
#     camera_dao = CameraDAO()
#     area_data = area_dao.view_area()
#     crossroad_data = crossroad_dao.view_crossroad()
#     camera_data = camera_dao.view_camera()
#     return render_template("admin/addVideo.html", area_data=area_data,
#                            crossroad_data=crossroad_data, camera_data=camera_data)
#
#
# @app.route('/admin/load_ajax_camera')
# def admin_load_ajax_camera():
#     crossroad_id = int(request.args.get('crossroad_id'))
#     print("s---", crossroad_id)
#     response_message = []
#
#     crossroad_dao_obj = CrossRoadDAO()
#     data = crossroad_dao_obj.ajax_camera_list()
#
#     for camera in data:
#         if camera.camera_crossroad_id == crossroad_id:
#             response_list = [
#                 {"camera_id": camera.camera_id,
#                  "camera_name": camera.camera_name}]
#
#             print(response_list, "response_list??????????")
#             response_message.extend(response_list)
#
#     return jsonify(response_message)
#
#
# @app.route("/admin/insert_video", methods=['GET', 'POST'])
# def insert_video():
#     area_id = request.form.get('area_id')
#     crossroad_id = request.form.get('crossroad_id')
#     camera_id = request.form.get('camera_id')
#
#     video_file = request.files.get('video_name')
#     print("video_file????????????????", video_file)
#     print("area_id", area_id)
#     print("crossroad_id", crossroad_id)
#
#     video_name = secure_filename(video_file.filename)
#     video_path = os.path.join(app.config['VIDEO_FOLDER'])
#     video_file.save(os.path.join(video_path, video_name))
#
#     video_dao = VideoDAO()
#     video_vo = VideoVO()
#
#     video_vo.video_area_id = area_id
#     video_vo.video_crossroad_id = crossroad_id
#     video_vo.video_camera_id = camera_id
#     video_vo.video_name = video_name
#     video_vo.video_path = video_path.replace("base", "..")
#     video_dao.insert_video(video_vo)
#
#     timestamp = int(time.time())
#     processed_video_name = f"processed_video_{timestamp}.mp4"
#     processed_video_path = os.path.join(app.config['OUTPUT_FOLDER'], processed_video_name)
#
#     vehicle_count = ai(video_path, processed_video_path)
#     print("Processed Vehicle Count:", vehicle_count)
#
#     return redirect(url_for('admin_view_video'))
#
#
# @app.route("/admin/view_video")
# def admin_view_video():
#     # video_id = request.args.get('video_id')
#     # print('///////////////', video_id)
#     video_dao = VideoDAO()
#     video_vo_list = video_dao.view_video()
#     # print('//////QQQQQQQQQQQQ/////////', video_vo_list)
#     # video_vo_info = video_dao.video_info(video_id)
#     area_dao = AreaDAO()
#     crossroad_dao = CrossRoadDAO()
#     camera_dao = CameraDAO()
#     area_data = area_dao.view_area()
#     crossroad_data = crossroad_dao.view_crossroad()
#     camera_data = camera_dao.view_camera()
#     return render_template('admin/viewVideo.html',
#                            video_vo_list=video_vo_list,
#                            area_data=area_data,
#                            crossroad_data=crossroad_data,
#                            camera_data=camera_data)
#     # video_vo_info=video_vo_info)
#
#
# @app.route("/admin/video_info")
# def admin_info_video():
#     video_id = request.args.get('video_id')
#     print("video_id received:", video_id)
#
#     video_dao = VideoDAO()
#     video_vo = VideoVO(video_id=video_id)
#
#     info_data = video_dao.video_info(video_vo)
#
#     if not info_data:
#         return jsonify({"error": "Video not found"}), 404
#
#     area_dao = AreaDAO()
#     area_name = area_dao.get_area_name(info_data.get("video_area_id"))
#
#     crossroad_dao = CrossRoadDAO()
#     crossroad_name = crossroad_dao.get_crossroad_name(info_data.get("video_crossroad_id"))
#
#     camera_dao = CameraDAO()
#     camera_name = camera_dao.get_camera_name(info_data.get("video_camera_id"))
#
#     video_filename = info_data["video_name"]
#     video_path = f"/static/adminResources/videos/{video_filename}"
#     file_type = os.path.splitext(video_filename)[1][1:]
#
#     info_data["video_path"] = video_path
#     info_data["area_name"] = area_name
#     info_data["crossroad_name"] = crossroad_name
#     info_data["camera_name"] = camera_name
#     info_data["file_type"] = file_type
#     info_data["video_name"] = video_filename
#
#     print("Updated info_data:", info_data)
#     print("video_area_id received:", info_data.get("video_area_id"))
#
#     return jsonify(info_data)
#
#
# @app.route('/admin/delete_video', methods=['GET', 'POST'])
# def admin_delete_video():
#     video_dao = VideoDAO()
#     video_id = request.args.get('video_id')
#     video_dao.delete_video(video_id)
#     return redirect(url_for('admin_view_video'))
#
#
# @app.route('/admin/get_crossroads_with_filter')
# def get_crossroads_with_filter():
#     cossroad_dao = CrossRoadDAO()
#     area_id = request.args.get('area_id')
#     crossroads = cossroad_dao.get_crossroads_with_filter(area_id)
#     return jsonify([{"crossroad_id": c.crossroad_id, "crossroad_name": c.crossroad_name} for c in crossroads])
#
#
# @app.route('/admin/get_cameras_with_filter')
# def get_cameras_with_filter():
#     camera_dao = CameraDAO()
#     crossroad_id = request.args.get('crossroad_id')
#     cameras = camera_dao.get_cameras_with_filter(crossroad_id)
#     return jsonify([{"camera_id": c.camera_id, "camera_name": c.camera_name} for c in cameras])
