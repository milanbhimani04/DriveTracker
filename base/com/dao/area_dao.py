from base import db
from base.com.vo.area_vo import AreaVO


class AreaDAO:
    def insert_area(self,area_vo):
        # area_vo = AreaVO()
        db.session.add(area_vo)
        db.session.commit()


    def view_area(self):
        area_vo_list = AreaVO.query.all()
        return area_vo_list


    def delete_area(self, area_vo):
        area_vo_list = AreaVO.query.get(area_vo.area_id)
        db.session.delete(area_vo_list)
        db.session.commit()

    def edit_area(self, area_id):
        area_edit_list = AreaVO.query.filter_by(area_id=area_id).one_or_none()
        print("Area Retrieved=========", area_edit_list)
        return area_edit_list

    def update_area(self, area_vo):
        db.session.merge(area_vo)
        db.session.commit()

    def get_area_name(self, area_id):
        area_name_list = AreaVO.query.filter_by(area_id=area_id).one_or_none()
        return area_name_list.area_name

    def area_count(self):
        area_count = AreaVO.query.count()
        print(area_count, "/////////////////////////////////////////////////")
        return area_count