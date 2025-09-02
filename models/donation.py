from database import *
from sqlalchemy.sql import func

class Donation(db.Model):
    __tablename__ = "donations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donorID = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Integer, nullable=False)
    medium = db.Column(db.String(10), nullable=False)
    tid = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(10), nullable=False)


    def __init__(self, method, donorID, amount, date, tid):
        self.medium = method
        self.donorID = donorID
        self.amount = amount
        self.date = date
        self.tid = tid

    @staticmethod
    def add_donation(method, donorID, amount, date, tid):
        new_donation = Donation(method=method,donorID=donorID, amount=amount, date=date, tid=tid)
        db.session.add(new_donation)
        db.session.commit()


    @staticmethod
    def total_donation():
        return Donation.query.with_entities(func.sum(Donation.amount)).scalar()