from flask import render_template, request, redirect, url_for, jsonify

from base import app
from base.com.dao.area_dao import AreaDAO
from base.com.dao.camera_dao import CameraDAO
from base.com.dao.crossroad_dao import CrossRoadDAO
from base.com.vo.camera_vo import CameraVO
from base.com.vo.crossroad_vo import CrossRoadVO
from base.com.controller.login_controller import login_required



@app.route('/admin/load_camera')
@login_required('admin')
def admin_load_camera():
    area_dao = AreaDAO()
    data = area_dao.view_area()
    return render_template('admin/addCamera.html', area_vo_list=data)


@app.route('/admin/load_ajax_crossroad')
@login_required('admin')
def admin_load_ajax_crossroad():
    area_id = int(request.args.get('area_id'))
    print("area_id ???", area_id)
    response_message = []

    crossroad_dao_obj = CrossRoadDAO()
    data = crossroad_dao_obj.ajax_crossroad_list()

    for crossroad in data:
        if crossroad.crossroad_area_id == area_id:
            response_list = [
                {"crossroad_id": crossroad.crossroad_id,
                 "crossroad_name": crossroad.crossroad_name}]

            print(response_list, "response_list")
            response_message.extend(response_list)

    return jsonify(response_message)


@app.route('/admin/insert_camera', methods=['GET', 'POST'])
@login_required('admin')
def admin_insert_camera():
    area_id = request.form.get('area_id')
    crossroad_id = request.form.get('crossroad_id')
    print("area_id?????", area_id)
    print("crossroad_id??????", crossroad_id)
    camera_name = request.form.get('camera_name')
    RTSP_link = request.form.get('RTSP_link')
    status = request.form.get('status')
    print("status>>>>>>>>>>>>>", status)

    camera_vo = CameraVO()
    camera_vo.camera_area_id = area_id
    camera_vo.camera_crossroad_id = crossroad_id
    camera_vo.camera_name = camera_name
    camera_vo.RTSP_link = RTSP_link
    camera_vo.camera_status = status
    camera_dao = CameraDAO()
    camera_dao.insert_camera(camera_vo)

    return redirect(url_for('admin_view_camera'))


@app.route('/admin/view_camera')
@login_required('admin')
def admin_view_camera():
    camera_dao = CameraDAO()
    camera_dao_list = camera_dao.view_camera()
    area_dao = AreaDAO()
    data = area_dao.view_area()
    crossroad_dao = CrossRoadDAO()
    crossroad_vo_list = crossroad_dao.view_crossroad_name()
    return render_template('admin/viewCamera.html', camera_dao_list=camera_dao_list, area_vo_list=data, crossroad_vo_list=crossroad_vo_list)


@app.route("/admin/delete_camera")
@login_required('admin')
def admin_delete_camera():
    camera_dao = CameraDAO()
    camera_vo = CameraVO()
    camera_id = request.args.get('camera_id')
    camera_vo.camera_id = camera_id
    camera_vo_list = camera_dao.delete_camera(camera_id)
    return redirect(url_for('admin_view_camera'))


@app.route('/admin/edit_camera', methods=['GET', 'POST'])
@login_required('admin')
def admin_edit_camera():
    camera_id = request.args.get('camera_id')
    camera_vo = CameraVO()
    camera_dao = CameraDAO()
    camera_vo.camera_id = camera_id
    camera_vo_list = camera_dao.edit_camera(camera_vo)
    camera_vo_dict = camera_vo_list[0].as_dict()
    camera_area_id = camera_vo_dict.get('camera_area_id')
    crossroad_vo = CrossRoadVO()
    crossroad_dao = CrossRoadDAO()
    area_dao = AreaDAO()
    crossroad_vo.crossroad_area_id = camera_area_id
    area_vo_list = area_dao.view_area()
    crossroad_vo_list = crossroad_dao.ajax_crossroad_list(crossroad_vo)
    return render_template('admin/editCamera.html',
                           area_vo_list=area_vo_list,
                           camera_vo_list=camera_vo_list,
                           crossroad_vo_list=crossroad_vo_list)


@app.route('/admin/update_camera', methods=['GET', 'POST'])
@login_required('admin')
def admin_update_camera():
    camera_id = request.form.get('camera_id')
    area_id = request.form.get('area_id')
    crossroad_id = request.form.get('crossroad_id')
    camera_name = request.form.get('camera_name')
    RTSP_link = request.form.get('RTSP_link')
    status = request.form.get('status')
    camera_vo = CameraVO()
    camera_vo.camera_id = camera_id
    camera_vo.camera_area_id = area_id
    camera_vo.camera_crossroad_id = crossroad_id
    camera_vo.camera_name = camera_name
    camera_vo.camera_RTSP_link = RTSP_link
    camera_vo.camera_status = status
    camera_dao = CameraDAO()
    camera_dao.update_camera(camera_vo)
    return redirect(url_for('admin_view_camera'))


@app.route('/admin/get_camera_details')
@login_required('admin')
def get_camera_details():
    camera_dao = CameraDAO()
    camera_id = request.args.get('camera_id')

    camera = camera_dao.edit_camera(camera_id)

    camera_dict = {
        "camera_id": camera.camera_id,
        "camera_name": camera.camera_name,
        "RTSP_link": camera.RTSP_link,
        "camera_area_id": camera.camera_area_id,
        "camera_crossroad_id": camera.camera_crossroad_id,
        "camera_status": camera.camera_status
    }
    print("data=============", camera_dict)

    return jsonify({"success": True, "data": camera_dict})
