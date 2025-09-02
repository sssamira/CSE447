from database import *
from models import Volunteer, User
class WorkAssigned(db.Model):
    __tablename__ = 'workAssigned'
    
    rcamp_id = db.Column(db.Integer, db.ForeignKey('Reliefcamp.id'))
    volnID = db.Column(db.Integer, db.ForeignKey('volunteers.volunteerid'), primary_key=True)
    
    def __init__(self, rcamp_id, volnID):
        self.rcamp_id = rcamp_id
        self.volnID = volnID

    @staticmethod
    def count_volunteers(rcamp_id):
        count = WorkAssigned.query.filter_by(rcamp_id = rcamp_id).count()
        return count
    

    @staticmethod
    def getCampID(volnID):
        wa = WorkAssigned.query.filter_by(volnID = volnID).first()
        if wa:
            return wa.rcamp_id
        else:
            return None
        
    @staticmethod
    def assign_volunteer(rcamp_id, volnID):
        try:
            voln = Volunteer.query.filter_by(volunteerid = volnID).first()
            uid = voln.userId
            user = User.query.filter_by(id = uid).first()
            wa = WorkAssigned(rcamp_id, volnID)
            db.session.add(wa)
            db.session.commit()
            return "Successfully assigned", 'success'
        except Exception as e:
            db.session.rollback()
            return str(e), 'danger'
