from database import *
from models.user import User
from models.crypto_utils import decrypt_field

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    
    volunteerid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.String(50))
    userId = db.Column(db.Integer, db.ForeignKey('users.id')) 
    
    def __init__(self, role, availability, userId):
        self.role = role
        self.availability = availability
        self.userId = userId

    def assignTask(self, task):
        pass

    @staticmethod
    def registerVolunteer(volunteerid, role, availability):
        volunteer = Volunteer(role, availability, volunteerid)
        db.session.add(volunteer)
        db.session.commit()
        return volunteer

    @staticmethod
    def getVolunteer(userId):
        return Volunteer.query.filter_by(userId=userId).first()

    def trackActivity(self):
        pass

    def getAvailability(self):
        return self.availability

    def setAvailability(self, new_availability):
        self.availability = new_availability
        db.session.commit()
    
    def getInfo(self):
        return self
    
    @staticmethod
    def getAllVolunteers():
        return Volunteer.query.all()



    def getVolunteerName(self):
        user = User.query.get(self.userId)
        return decrypt_field(user.name)