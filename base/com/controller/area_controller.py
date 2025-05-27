from flask import render_template, request, redirect, url_for, jsonify

from base import app
from base.com.dao.area_dao import AreaDAO
from base.com.vo.area_vo import AreaVO
from base.com.controller.login_controller import login_required

#
# @app.route('/admin/')
# def admin_load_area():
#     return render_template('admin/index.html')


@app.route('/admin/insert_area', methods=['GET', 'POST'])
@login_required('admin')
def admin_insert_area():
    area_dao = AreaDAO()
    area_vo = AreaVO()
    area_vo.area_name = request.form.get('area_name')
    area_vo.area_description = request.form.get('area_description')

    area_dao.insert_area(area_vo)
    return redirect(url_for('admin_view_area'))


@app.route('/admin/view_area', methods=['GET', 'POST'])
@login_required('admin')
def admin_view_area():
    area_dao = AreaDAO()
    area_vo_list = area_dao.view_area()
    return render_template('admin/viewArea.html', area_vo_list=area_vo_list)


# @app.route('/admin/delete_area', methods=['POST'])
# def admin_delete_area():
#     area_dao = AreaDAO()
#     area_vo = AreaVO()
#
#     data = request.get_json()
#     area_vo.area_id = data.get('area_id')
#
#     area_dao.delete_area(area_vo)
#
#     return jsonify({"message": "Area deleted successfully"}), 200


@app.route('/admin/delete_area', methods=['GET', 'POST'])
@login_required('admin')

def admin_delete_area():
    # try:
    area_dao = AreaDAO()
    area_vo = AreaVO()
    area_vo.area_id = request.args.get('area_id')
    area_vo_list = area_dao.delete_area(area_vo)
    return redirect(url_for('admin_view_area'))


#     return jsonify({'status': 'success'})
# except Exception:
#     return jsonify({'status': 'failed'})


@app.route('/admin/edit_area', methods=['GET', 'POST'])
@login_required('admin')
def admin_edit_area():
    area_dao = AreaDAO()
    area_vo = AreaVO()
    area_vo.area_id = request.args.get('area_id')
    area_vo_list = area_dao.edit_area(area_vo)
    return render_template('admin/editArea.html', area_vo_list=area_vo_list)


@app.route('/admin/update_area', methods=['GET', 'POST'])
@login_required('admin')
def admin_update_area():
    area_dao = AreaDAO()
    area_vo = AreaVO()
    area_vo.area_id = request.form.get('area_id')
    area_vo.area_name = request.form.get('area_name')
    area_vo.area_description = request.form.get('area_description')
    print("area id ====", area_vo.area_id)
    area_dao.update_area(area_vo)
    return redirect(url_for('admin_view_area'))


@app.route('/admin/get_area_info', methods=['GET'])
@login_required('admin')
def get_area_info():
    area_id = request.args.get('area_id')
    print("Received area_id:", area_id)

    area_dao = AreaDAO()
    area = area_dao.edit_area(area_id)

    response = {
        "area_id": area.area_id,
        "area_name": area.area_name,
        "area_description": area.area_description
    }
    print("Response Data:", response)
    return jsonify(response)
