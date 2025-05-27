from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.camera_vo import CameraVO
from base.com.vo.crossroad_vo import CrossRoadVO


class VideoVO(db.Model):
    __tablename__ = 'video_table'
    video_id = db.Column('video_id', db.Integer, primary_key=True, autoincrement=True, nullable=False)
    video_name = db.Column('video_name', db.String(255), nullable=False)
    video_path = db.Column('video_path', db.String(255), nullable=False)

    video_area_id = db.Column('video_area_id', db.Integer, db.ForeignKey(AreaVO.area_id, ondelete='CASCADE', onupdate='CASCADE'),
                              nullable=False)
    video_crossroad_id = db.Column('video_crossroad_id', db.Integer, db.ForeignKey(CrossRoadVO.crossroad_id,
                                                                                   ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    video_camera_id = db.Column('video_camera_id', db.Integer, db.ForeignKey(CameraVO.camera_id,
                                                                             ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    def as_dict(self):
        return {
            'video_id': self.video_id,
            'video_name': self.video_name,
            'video_path': self.video_path,
            'video_area_id': self.video_area_id,
            'video_crossroad_id': self.video_crossroad_id,
            'video_camera_id': self.video_camera_id

        }


db.create_all()
