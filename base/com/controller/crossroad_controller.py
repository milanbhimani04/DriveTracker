from flask import render_template, request, redirect, url_for, jsonify

from base import app
from base.com.dao.area_dao import AreaDAO
from base.com.dao.crossroad_dao import CrossRoadDAO
from base.com.vo.area_vo import AreaVO
from base.com.vo.crossroad_vo import CrossRoadVO
from base.com.controller.login_controller import login_required



@app.route('/admin/load_crossroad', methods=['GET', 'POST'])
@login_required('admin')
def admin_load_crossroad():
    area_dao = AreaDAO()
    area_vo = AreaVO()
    area_vo_list = area_dao.view_area()
    print("////////////", area_vo_list)
    return render_template('admin/addCrossRoad.html',
                           area_vo_list=area_vo_list)


@app.route('/admin/insert_crossroad', methods=['GET', 'POST'])
@login_required('admin')
def admin_insert_crossroad():
    print("function call")
    crossroad_dao = CrossRoadDAO()
    crossroad_vo = CrossRoadVO()
    crossroad_vo.crossroad_name = request.form.get('crossroad_name')
    print("???", crossroad_vo.crossroad_name)
    crossroad_vo.crossroad_description = request.form.get(
        'crossroad_description')
    print("{{???}}", crossroad_vo.crossroad_description)
    crossroad_vo.crossroad_area_id = request.form.get('crossroad_area_id')
    print("???+++", crossroad_vo.crossroad_area_id)
    crossroad_dao.insert_crossroad(crossroad_vo)
    return redirect(url_for('admin_view_crossroad'))


@app.route('/admin/view_crossroad', methods=['GET', 'POST'])
@login_required('admin')
def admin_view_crossroad():
    crossroad_dao = CrossRoadDAO()
    area_dao = AreaDAO()
    crossroad_vo_list = crossroad_dao.view_crossroad()
    area_vo_list = area_dao.view_area()
    print("area vpo list", area_vo_list)
    print("crossroad vo list......", crossroad_vo_list)

    return render_template('admin/viewCrossRoad.html',
                           crossroad_vo_list=crossroad_vo_list, area_vo_list=area_vo_list)


@app.route('/admin/delete_crossroad', methods=['GET', 'POST'])
@login_required('admin')
def admin_delete_crossroad():
    crossroad_dao = CrossRoadDAO()

    crossroad_id = request.args.get('crossroad_id')
    crossroad_dao.delete_crossroad(crossroad_id)
    return redirect(url_for('admin_view_crossroad'))


@app.route('/admin/edit_crossroad', methods=['GET', 'POST'])
@login_required('admin')
def admin_edit_crossroad():
    crossroad_dao = CrossRoadDAO()
    area_dao = AreaDAO()
    area_vo = AreaVO()
    crossroad_vo = CrossRoadVO()
    crossroad_id = request.args.get('crossroad_id')
    print("crossroad_id $$$$$", crossroad_id)
    crossroad_vo.crossroad_id = crossroad_id
    crossroad_vo_list = crossroad_dao.edit_crossroad(crossroad_vo)
    area_vo_list = area_dao.view_area()
    print("crossroad_Vo_list????", crossroad_vo_list)
    print("area_vo_list{{{{{{", area_vo_list)
    return render_template('admin/editCrossroad.html',
                           crossroad_vo_list=crossroad_vo_list,
                           area_vo_list=area_vo_list)


@app.route('/admin/update_crossroad', methods=['GET', 'POST'])
@login_required('admin')
def admin_update_crossroad():
    crossroad_id = request.form.get('crossroad_id')
    crossroad_name = request.form.get('crossroad_name')
    crossroad_description = request.form.get('crossroad_description')
    crossroad_area_id = request.form.get('crossroad_area_id')

    crossroad_dao = CrossRoadDAO()
    crossroad_vo = CrossRoadVO()

    crossroad_vo.crossroad_id = crossroad_id
    crossroad_vo.crossroad_name = crossroad_name
    crossroad_vo.crossroad_description = crossroad_description
    crossroad_vo.crossroad_area_id = crossroad_area_id
    crossroad_dao.update_crossroad(crossroad_vo)
    return redirect(url_for('admin_view_crossroad'))

@app.route('/admin/get_crossroad_info', methods=['GET'])
@login_required('admin')
def get_crossroad_info():
    crossroad_id = request.args.get('crossroad_id')
    print(f" Received crossroad_id: {crossroad_id}")

    crossroad_dao = CrossRoadDAO()
    crossroad = crossroad_dao.edit_crossroad(crossroad_id)

    response = {
        "crossroad_id": crossroad.crossroad_id,
        "crossroad_area_id": crossroad.crossroad_area_id,
        "crossroad_name": crossroad.crossroad_name,
        "crossroad_description": crossroad.crossroad_description
    }

    return jsonify(response)
