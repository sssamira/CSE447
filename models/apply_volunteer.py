from database import *
from models import User, Volunteer

class ApplyVolunteer(db.Model):
    __tablename__ = 'apply_volunteer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100))


    def __init__(self, email):
        self.email = email

    @staticmethod
    def get_all_applicant():
        result = ApplyVolunteer.query.all()
        return result
    

    def delete_applicant(self, email):
        ApplyVolunteer.query.filter_by(email=email).delete()
        db.session.commit()

    @staticmethod
    def accept_application(id):
        applicant = ApplyVolunteer.query.get(id)
        user = User.query.filter_by(email=applicant.email).first()
        if user:
            user.role = 'volunteer'
            new_volunteer = Volunteer(role="volunteer", availability="True", userId=user.id)
            db.session.add(new_volunteer)
            ApplyVolunteer.query.filter_by(id=id).delete()
            db.session.commit()
            return "Application accepted", 'success'
        else:
            return "User not found", 'danger'