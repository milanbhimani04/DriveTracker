from base import db

from base.com.vo.detection_vo import DetectionVO


class DetectionDAO():
    def insert_detect(self, detection_vo):
        db.session.add(detection_vo)
        db.session.commit()

    def view_detection(self):
        detection_vo_list = DetectionVO.query.all()
        return detection_vo_list

    def detection_info(self, video_vo):
        video_id = video_vo.video_id
        print("Fetching detections for video_id:", video_id)
        detection_records = DetectionVO.query.filter_by(detection_video_id=video_id).all()
        print(detection_records, "<<< detection records found")
        return [record.as_dict() for record in detection_records] if detection_records else []

    def get_total_vehicle_counts(self):
        result = db.session.query(
            db.func.coalesce(db.func.sum(DetectionVO.car_count), 0) +
            db.func.coalesce(db.func.sum(DetectionVO.bus_count), 0) +
            db.func.coalesce(db.func.sum(DetectionVO.motorcycle_count), 0) +
            db.func.coalesce(db.func.sum(DetectionVO.truck_count), 0) +
            db.func.coalesce(db.func.sum(DetectionVO.bicycle_count), 0)
        ).scalar()

        return result
