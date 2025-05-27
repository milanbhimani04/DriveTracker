from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.camera_vo import CameraVO
from base.com.vo.crossroad_vo import CrossRoadVO
from base.com.vo.video_vo import VideoVO


class VideoDAO:
    def insert_video(self, video_vo=VideoVO):
        db.session.add(video_vo)
        db.session.commit()

    def view_video(self):
        video_vo_list = db.session.query(AreaVO, CrossRoadVO, CameraVO, VideoVO).filter(AreaVO.area_id == VideoVO.video_area_id).filter(CrossRoadVO.crossroad_id == VideoVO.video_crossroad_id).filter(
            CameraVO.camera_id == VideoVO.video_camera_id).all()
        return video_vo_list

    # def view_video_ajax(self):
    #     videos = db.session.query(VideoVO).all()  # or appropriate query
    #     return videos  # Return an empty list if no videos are found

    def video_info(self, video_vo=VideoVO):
        print("........dao")
        video_record = VideoVO.query.filter_by(video_id=video_vo.video_id).one_or_none()
        if video_record:
            return video_record.as_dict()  # Convert to dictionary
        return None

    def delete_video(self, video_id):
        video_vo_list = VideoVO.query.get(video_id)
        print(video_vo_list)
        db.session.delete(video_vo_list)
        db.session.commit()
        return video_vo_list

    def count_file(self):
        video_count = VideoVO.query.count()
        return video_count
