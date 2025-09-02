from database import *

class MissingPerson(db.Model):
    missingid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    last_location = db.Column(db.String(200), nullable=False)
    contactid = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(25600), nullable=False)

    def __init__(self, name, last_seen, contact_number, photo):
        self.name = name
        self.last_location = last_seen
        self.contactid = contact_number
        self.status = 'Missing'
        self.photo = photo

    @staticmethod
    def getMissingPerson(missingid):
        return MissingPerson.query.filter_by(missingid=missingid).first()
    

    def registerMissing(self):
        db.session.add(self)
        db.session.commit()
        return True

    def updateMissing(self, name=None, last_location=None, contactid=None, status=None):
        if name:
            self.name = name
        if last_location:
            self.last_location = last_location
        if contactid:
            self.contactid = contactid
        if status:
            self.status = status
        db.session.commit()

    def matchFound(self):
        self.status = 'Found'
        db.session.commit()

    
    @staticmethod
    def getMissingPersons():
        return MissingPerson.query.all()
    
    @staticmethod
    def getMissingPersonByParam(id=None,name=None, last_location=None):
        if id:
            return MissingPerson.query.filter_by(missingid=id).first()
        if name:
            return MissingPerson.query.filter_by(name=name).all()
        if last_location:
            return MissingPerson.query.filter_by(last_location=last_location).all()
        