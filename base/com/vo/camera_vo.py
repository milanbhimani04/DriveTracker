from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.crossroad_vo import CrossRoadVO

class CameraVO(db.Model):
    __tablename__ = 'camera_table'
    camera_id = db.Column('camera_id',db.Integer, primary_key=True,
                          autoincrement=True, nullable=False)
    camera_name = db.Column('camera_name',db.String(50),
                            nullable=False)
    RTSP_link = db.Column('RTSP_link',db.String(50), unique=True,
                          nullable=False)
    camera_status = db.Column('camera_status',db.String(50),nullable=False)
    camera_area_id = db.Column('camera_area_id', db.Integer,
                                        db.ForeignKey(AreaVO.area_id,
                                                      ondelete='CASCADE',
                                                      onupdate='CASCADE'),
                                        nullable=False)
    camera_crossroad_id = db.Column('camera_crossroad_id', db.Integer,
                                        db.ForeignKey(CrossRoadVO.crossroad_id,
                                                      ondelete='CASCADE',
                                                      onupdate='CASCADE'),
                                        nullable=False)

    def as_dict(self):
        return{
            'camera_id':self.camera_id,
            'camera_name':self.camera_name,
            'RTSP_link':self.RTSP_link,
            'camera_status':self.camera_status,
            'camera_area_id':self.camera_area_id,
            'camera_crossroad_id':self.camera_crossroad_id
        }

db.create_all()

