from base import db, app
from base.com.vo.video_vo import VideoVO


class DetectionVO(db.Model):
    __tablename__ = 'detection_table'
    detection_id = db.Column('detection_id', db.Integer, primary_key=True,
                             autoincrement=True, nullable=False)

    car_count = db.Column('car_count', db.Integer)
    bus_count = db.Column('bus_count', db.Integer)
    motorcycle_count = db.Column('motorcycle_count',     db.Integer)
    truck_count = db.Column('truck_count', db.Integer)
    bicycle_count = db.Column('bicycle_count', db.Integer)
    output_video_path = db.Column('output_video_path', db.String(255))
    output_video_name = db.Column('output_video_name', db.String(255))
    avi_video_path = db.Column('avi_video_path', db.String(255))
    avi_video_name = db.Column('avi_video_name', db.String(255))
    detection_video_id = db.Column('detection_video_id', db.Integer, db.ForeignKey(VideoVO.video_id,
                                                                             ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    def as_dict(self):
        return {
            'detection_id': self.detection_id,
            'car_count': self.car_count,
            'bus_count': self.bus_count,
            'motorcycle_count': self.motorcycle_count,
            'truck_count': self.truck_count,
            'bicycle_count': self.bicycle_count,
            'output_video_path': self.output_video_path,
            'output_video_name': self.output_video_name,
            'avi_video_path': self.avi_video_path,
            'avi_video_name': self.avi_video_name,
            'detection_video_id': self.detection_video_id

        }


with app.app_context():
    db.create_all()
