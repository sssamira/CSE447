from database import db

class Resource(db.Model):
    __tablename__ = 'resources'
    
    resID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campID = db.Column(db.Integer, db.ForeignKey('Reliefcamp.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __init__(self, campID, type, quantity, location):
        self.campID = campID
        self.type = type
        self.quantity = quantity
        self.location = location

    @staticmethod
    def addResource(campID, type, quantity, location):
        new_resource = Resource(campID=campID, type=type, quantity=quantity, location=location)
        db.session.add(new_resource)
        try:
            db.session.commit()
            print("Resource added successfully")
        except Exception as e:
            db.session.rollback()
            print("Failed to add resource")
            print(e)

    @staticmethod
    def updateResource(resID, quantity):
        resource = Resource.query.filter_by(resID=resID).first()
        if resource:
            resource.quantity = quantity
            try:
                db.session.commit()
                print(f"Resource {resID} updated successfully")
            except Exception as e:
                db.session.rollback()
                print(f"Failed to update resource {resID}")
                print(e)
        else:
            print(f"Resource {resID} not found")

    @staticmethod
    def viewResource(resID):
        return Resource.query.filter_by(resID=resID).first()

    @staticmethod
    def trackResource(campID):
        return Resource.query.filter_by(campID=campID).all()

    @staticmethod
    def requestResource(type, location):
        return Resource.query.filter_by(type=type, location=location).first()


