from database import *
from models import User, Volunteer
from models.crypto_utils import encrypt_field, decrypt_field

class ApplyVolunteer(db.Model):
    __tablename__ = 'apply_volunteer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(512))


    def __init__(self, email):
        self.email = encrypt_field(email)

    @staticmethod
    def get_all_applicant():
        result = ApplyVolunteer.query.all()
        # Decrypt email for each applicant
        for applicant in result:
            applicant.email = decrypt_field(applicant.email)
        return result
    

    def delete_applicant(self, email):
        encrypted_email = encrypt_field(email)
        ApplyVolunteer.query.filter_by(email=encrypted_email).delete()
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