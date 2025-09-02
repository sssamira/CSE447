from database import *
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, type, location, status):
        self.type = type
        self.location = location
        self.status = status

    @staticmethod
    def getInfo(id):
        incident = Incident.query.get(id)
        return incident

    @staticmethod
    def updateInfo(id, new_status):
        incident = Incident.query.get(id)
        if incident:
            incident.status = new_status
            db.session.commit()
            return f"Incident {id} updated to status: {new_status}"
        else:
            return f"Failed to update incident {id}"

    def getIncidentDetails(self):
        return {
            'id': self.id,
            'type': self.type,
            'location': self.location,
            'status': self.status
        }
