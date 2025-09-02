from database import *


class Rcamp(db.Model):
    __tablename__ = 'Reliefcamp'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    v_capacity = db.Column(db.Integer, nullable=False)
    v_occupied = db.Column(db.Integer, nullable=False)
    v_id = db.Column(db.Integer, db.ForeignKey('volunteers.volunteerid'), nullable=False)

    def __init__(self, id, name, location, v_capacity, v_occupied, v_id):
        self.id = id
        self.name = name
        self.location = location
        self.v_capacity = v_capacity
        self.v_occupied = v_occupied
        self.v_id = v_id
        

    @staticmethod
    def addcamp(id, name, location, v_capacity, v_occupied):
        new_camp = Rcamp(id, name, location, v_capacity, v_occupied)
        db.session.add(new_camp)
        db.session.commit()
        return new_camp

    @staticmethod
    def get_camp(id):
        camp = Rcamp.query.filter_by(id=id).first()
        return camp
        

    def track_resources(self):
        pass

    def update_camp(self, v_cap, v_occ):
        self.v_capacity = v_cap
        self.v_occupied = v_occ
        db.session.commit()


    @staticmethod
    def get_all_camps():
        camps = Rcamp.query.all()
        return camps