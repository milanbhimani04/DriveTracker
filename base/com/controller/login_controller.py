from datetime import timedelta, datetime
from datetime import timedelta, datetime
from functools import wraps

import bcrypt
import httpagentparser
import jwt
from flask import render_template, redirect, request, url_for, make_response, \
    flash

from base import app
from base.com.dao.area_dao import AreaDAO
from base.com.dao.camera_dao import CameraDAO
from base.com.dao.detection_dao import DetectionDAO
from base.com.dao.device_info_dao import DeviceInfoDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.video_dao import VideoDAO
from base.com.vo.device_info_vo import DeviceInfoVO
from base.com.vo.login_vo import LoginVO


def get_client_identity():
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    agent = request.environ.get('HTTP_USER_AGENT')
    browser = httpagentparser.detect(agent)
    if not browser:
        browser = agent.split('/')[0]
    else:
        browser = browser['browser']['name']
    return "{}:{}".format(ip_addr, browser)


def insert_client_identity(login_id):
    login_vo = LoginVO()
    login_vo.login_id = login_id

    device_info_dao = DeviceInfoDAO()
    device_info_vo = DeviceInfoVO()

    device_list = device_info_dao.search_device(login_vo)

    for device in device_list:
        if bcrypt.checkpw(get_client_identity().encode("utf-8"),
                          device.device_identity.encode("utf-8")):
            device_info_vo = device
            break

    hashed_client_identity = bcrypt.hashpw(
        get_client_identity().encode("utf-8"),
        bcrypt.gensalt(rounds=12))
    device_info_vo.device_identity = hashed_client_identity
    device_info_vo.device_login_id = login_id

    device_info_dao.insert_device_info(device_info_vo)


def refresh_token(fn):
    try:
        refreshtoken = request.cookies.get('refreshtoken')

        if refreshtoken is not None:
            data = jwt.decode(refreshtoken, app.config['SECRET_KEY'], 'HS256')

            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = data['public_id']

            login_vo_list = login_dao.login_validate(login_vo)

            device_info_dao = DeviceInfoDAO()

            device_list = device_info_dao.search_device(login_vo_list[0])

            for device in device_list:
                print('In Token Refresh')
                if bcrypt.checkpw(get_client_identity().encode("utf-8"),
                                  device.device_identity.encode("utf-8")):
                    print('Device Matched')
                    response = make_response(fn())
                    response.set_cookie('accesstoken',
                                        value=jwt.encode({
                                            'public_id': login_vo_list[
                                                0].login_username,
                                            'role': login_vo_list[
                                                0].login_role,
                                            'exp': datetime.utcnow() + timedelta(
                                                seconds=30)
                                        }, app.config['SECRET_KEY'],
                                            'HS256'),
                                        max_age=timedelta(seconds=30))
                    refresh = jwt.encode({
                        'public_id': login_vo_list[0].login_username,
                        'exp': datetime.utcnow() + timedelta(hours=1)
                    }, app.config['SECRET_KEY'], 'HS256')

                    print('Token Refreshed Successfully')
                    response.set_cookie('refreshtoken',
                                        value=refresh,
                                        max_age=timedelta(hours=1))
                    return response
            else:
                error_message = 'We Encounterd Malicious Activity Please Re-Login'
                flash(error_message)
                return admin_logout_session(login_vo.login_username)
        else:
            error_message = 'Unauthorized Access'
            flash(error_message)
            return admin_logout_session()
    except Exception as ex:
        print('Exception in Refreshing Token', ex)
        error_message = 'Session expired'
        flash(error_message)
        return admin_logout_session()


def login_required(role):
    def inner(fn):
        @wraps(fn)
        def decorator():
            try:
                accesstoken = request.cookies.get('accesstoken')

                if accesstoken is None:
                    return refresh_token(fn)
                else:
                    data = jwt.decode(accesstoken, app.config['SECRET_KEY'],
                                      'HS256')
                    login_vo = LoginVO()
                    login_dao = LoginDAO()

                    login_vo.login_username = data['public_id']

                    login_vo_list = login_dao.login_validate(login_vo)
                    if login_vo_list is not None:
                        login_list = [i.as_dict() for i in login_vo_list]

                        if login_list[0]['login_status'] == 1 and data[
                            'role'] == role:
                            return fn()
                        else:
                            return redirect('/')
                    else:
                        error_message = 'Unauthorized Access'
                        flash(error_message)
                        return redirect('/')
            except Exception as ex:
                print(ex)
                return refresh_token(fn)

        return decorator

    return inner


@app.route('/')
def index():
    return render_template('admin/indexUser.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('admin/login.html')


@app.route('/admin/')
@login_required('admin')
def admin_load():
    area_dao = AreaDAO()
    video_dao = VideoDAO()
    camera_dao = CameraDAO()
    detection_dao = DetectionDAO()

    count_area = area_dao.area_count()
    count_file = video_dao.count_file()
    count_camera = camera_dao.count_camera()
    count_all_vehicles = detection_dao.get_total_vehicle_counts()
    print(count_area, "-------------------------------------------------------------")

    return render_template('admin/index.html', count_area=count_area, count_file=count_file, count_camera=count_camera, count_all_vehicles=count_all_vehicles)


@app.route("/insert_login", methods=['POST'])
def insert_login():
    try:
        login_username = request.form.get('login_username')
        login_password = request.form.get('login_password').encode("utf-8")

        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = login_username

        login_vo_list = login_dao.login_validate(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        len_login_list = len(login_list)

        if len_login_list == 0:
            error_message = 'username is incorrect !'
            flash(error_message)
            return redirect('/')
        elif not login_list[0]['login_status']:
            error_message = 'You have been temporarily blocked by website admin !'
            flash(error_message)
            return redirect('/')
        else:
            login_username = login_list[0]['login_username']
            login_role = login_list[0]['login_role']
            hashed_login_password = login_list[0]['login_password'].encode(
                "utf-8")
            if bcrypt.checkpw(login_password, hashed_login_password):
                insert_client_identity(login_list[0]['login_id'])

                if login_role == 'admin':
                    response = make_response(
                        redirect(url_for('admin_load')))
                    response.set_cookie('accesstoken',
                                        value=jwt.encode({
                                            'public_id': login_username,
                                            'role': login_role,
                                            'exp': datetime.utcnow() + timedelta(
                                                seconds=30)
                                        }, app.config['SECRET_KEY'], 'HS256'),
                                        max_age=timedelta(seconds=30))
                    refresh = jwt.encode({
                        'public_id': login_username,
                        'exp': datetime.utcnow() + timedelta(hours=1)
                    }, app.config['SECRET_KEY'], 'HS256')

                    response.set_cookie('refreshtoken',
                                        value=refresh,
                                        max_age=timedelta(hours=1))
                    return response

                else:
                    return admin_logout_session()
            else:
                error_message = 'password is incorrect !'
                flash(error_message)
                return redirect('/')
    except Exception as ex:
        print("admin_validate_login route exception occured>>>>>>>>>>", ex)
        return redirect(url_for('admin_logout_session'))


@app.route("/admin/logout_session", methods=['GET'])
def admin_logout_session(*user_name):
    try:
        if len(user_name) != 0 and user_name[0] is not None:
            login_vo = LoginVO()
            login_dao = LoginDAO()
            device_info_dao = DeviceInfoDAO()

            login_vo.login_username = user_name[0]

            login_vo_list = login_dao.login_validate(login_vo)

            login_id = login_vo_list[0].login_id
            device_info_dao.delete_all_device(login_id)

            response = make_response(redirect('/login'))
            response.set_cookie('accesstoken', max_age=0)
            response.set_cookie('refreshtoken', max_age=0)
            return response
        elif request.cookies.get('refreshtoken') is not None:
            refreshtoken = request.cookies.get('refreshtoken')

            data = jwt.decode(refreshtoken, app.config['SECRET_KEY'], 'HS256')

            login_vo = LoginVO()
            login_dao = LoginDAO()
            device_info_dao = DeviceInfoDAO()
            device_info_vo = DeviceInfoVO()

            login_vo.login_username = data['public_id']

            login_vo_list = login_dao.login_validate(login_vo)
            login_vo = login_vo_list[0]

            device_list = device_info_dao.search_device(login_vo)

            if len(device_list) != 0:
                for device in device_list:
                    if bcrypt.checkpw(get_client_identity().encode("utf-8"),
                                      device.device_identity.encode("utf-8")):
                        device_info_vo = device
                        break

                device_info_dao.delete_device(device_info_vo)

            response = make_response(redirect('/login'))
            response.set_cookie('accesstoken', max_age=0)
            response.set_cookie('refreshtoken', max_age=0)
            return response
        else:
            response = make_response(redirect('/login'))
            response.set_cookie('accesstoken', max_age=0)
            response.set_cookie('refreshtoken', max_age=0)

            return response

    except Exception as ex:
        print("admin_logout_session route exception occured>>>>>>>>>>", ex)
