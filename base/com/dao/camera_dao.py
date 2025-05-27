from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.camera_vo import CameraVO
from base.com.vo.crossroad_vo import CrossRoadVO


class CameraDAO:
    def insert_camera(self, camera_vo=CameraVO):
        db.session.add(camera_vo)
        db.session.commit()

    def view_camera(self):
        camera_vo_list = db.session.query(AreaVO, CrossRoadVO,
                                          CameraVO) \
            .filter(
            AreaVO.area_id == CameraVO.camera_area_id) \
            .filter(
            CrossRoadVO.crossroad_id == CameraVO.camera_crossroad_id) \
            .all()
        return camera_vo_list

    def delete_camera(self, camera_id):
        camera_vo_list = CameraVO.query.get(camera_id)
        db.session.delete(camera_vo_list)
        db.session.commit()
        return camera_vo_list

    def edit_camera(self, camera_id):
        camera_vo_list = CameraVO.query.filter_by(camera_id=camera_id).first()
        return camera_vo_list

    def update_camera(self, camera_vo):
        db.session.merge(camera_vo)
        db.session.commit()

    def get_camera_name(self, camera_id):
        camera_name_list = CameraVO.query.filter_by(camera_id=camera_id).one_or_none()
        return camera_name_list.camera_name

    def get_cameras_with_filter(self, crossroad_id):
        cameras = CameraVO.query.filter_by(camera_crossroad_id=crossroad_id, camera_status='active').all()
        return cameras

    def count_camera(self):
        camera_count = CameraVO.query.count()
        return camera_count