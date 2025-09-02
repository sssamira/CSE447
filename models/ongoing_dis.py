from database import db

class OngoingDisaster(db.Model):
    __tablename__ = 'ongoing_disasters'
    
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.String, db.ForeignKey('volunteers.volunteerid'))
    disaster_type = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    def __init__(self, volunteer_id, disaster_type, location):
        self.volunteer_id = volunteer_id
        self.disaster_type = disaster_type
        self.location = location

    @staticmethod
    def addOrUpdateDisaster(volunteer_id, disaster_type, location):
        disaster = OngoingDisaster.query.filter_by(volunteer_id=volunteer_id).first()
        if disaster:
            disaster.disaster_type = disaster_type
            disaster.location = location
        else:
            disaster = OngoingDisaster(volunteer_id, disaster_type, location)
            db.session.add(disaster)
        db.session.commit()
        return disaster
