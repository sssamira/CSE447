from database import *
from sqlalchemy.sql import func
from models.donation import Donation

class Allocation(db.Model):
    __tablename__ = "fundallocations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    details = db.Column(db.String(500))
    amount = db.Column(db.Integer, nullable=False)

    def __init__(self, details, amount):
        self.details = details
        self.amount = amount

    @staticmethod
    def add_allocation(details, amount, date):
        if Allocation.available_fund() < amount:
            return False
        new_allocation = Allocation(details=details, amount=amount, date=date)
        db.session.add(new_allocation)
        db.session.commit()
        return True
    

    
    @staticmethod
    def total_allocation():
        return Allocation.query.with_entities(func.sum(Allocation.amount)).scalar()
    

    @staticmethod
    def available_fund():
        return Donation.total_donation() - Allocation.total_allocation()