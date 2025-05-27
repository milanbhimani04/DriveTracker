from base import db


class AreaVO(db.Model):
    __tablename__ = 'area_table'
    area_id = db.Column('area_id', db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    area_name = db.Column('area_name', db.String(255), nullable=False)
    area_description = db.Column('area_description', db.Text, nullable=False)

    def as_dict(self):
        return {
            'area_id': self.area_id,
            'area_name': self.area_name,
            'area_description': self.area_description

        }


db.create_all()
