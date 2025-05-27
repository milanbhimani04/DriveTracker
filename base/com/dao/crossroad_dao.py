from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.camera_vo import CameraVO
from base.com.vo.crossroad_vo import CrossRoadVO


class CrossRoadDAO:
    def insert_crossroad(self, crossroad_vo):
        db.session.add(crossroad_vo)
        db.session.commit()

    def view_crossroad(self):
        crossroad_vo_list = db.session.query(CrossRoadVO, AreaVO).join(AreaVO,
                                                                       CrossRoadVO.crossroad_area_id == AreaVO.area_id).all()
        return crossroad_vo_list

    # def view_crossroad(self, area_vo=AreaVO()):
    #     crossroad_data = db.session.query(AreaVO, CrossRoadVO).join(
    #         AreaVO,
    #         CrossRoadVO.crossroad_area_id == AreaVO.category_id).all()
    #     return crossroad_data

    def delete_crossroad(self, crossroad_id):
        crossroad_vo_list = CrossRoadVO.query.get(crossroad_id)
        db.session.delete(crossroad_vo_list)
        db.session.commit()

    def edit_crossroad(self, crossroad_vo):
        print("🔍 Searching for crossroad with ID:",crossroad_vo)
        crossroad_vo_list = CrossRoadVO.query.filter_by(crossroad_id=crossroad_vo).one_or_none()
        print("✅ Query Result:", crossroad_vo_list)
        return crossroad_vo_list

    def update_crossroad(self, crossroad_vo):
        db.session.merge(crossroad_vo)
        db.session.commit()

    def ajax_crossroad_list(self, crossroad_vo=CrossRoadVO):
        crossroad_vo_list = CrossRoadVO.query.filter_by(
            crossroad_area_id=crossroad_vo.crossroad_area_id).all()
        return crossroad_vo_list

    def ajax_camera_list(self,camera_vo=CameraVO):
        camera_vo_list = CameraVO.query.filter_by(
            camera_crossroad_id=camera_vo.camera_crossroad_id).all()
        return camera_vo_list

    def get_crossroad_name(self, crossroad_id):
        crossroad_name_list = CrossRoadVO.query.filter_by(crossroad_id=crossroad_id).one_or_none()
        return crossroad_name_list.crossroad_name

    def get_crossroads_with_filter(self, area_id):
        crossroads = CrossRoadVO.query.filter_by(crossroad_area_id=area_id).all()
        return crossroads

    def view_crossroad_name(self):
        crossroad_vo_list = CrossRoadVO.query.all()
        return crossroad_vo_list
