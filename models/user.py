from database import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.crypto_utils import encrypt_field, decrypt_field

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(400), unique=True, nullable=False)
    name = db.Column(db.String(400), nullable=False)
    nid = db.Column(db.String(400), nullable=False)
    date_of_birth = db.Column(db.String(400), nullable=False)
    email = db.Column(db.String(400), unique=True, nullable=False)
    address = db.Column(db.String(400), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    contact = db.Column(db.String(400), nullable=False)
    blood_type = db.Column(db.String(400), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    blood_donation = db.Column(db.String(6))

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def authenticate(username, password):
        for user in User.query.all():
            if decrypt_field(user.username) == username:
                if user.verify_password(password):
                    return (True, user)
                else:
                    return (False, None)
        return (False, None)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def registerUser(username, email, name, nid, date_of_birth, address, password, contact, blood_type):
        encrypted_username = encrypt_field(username)
        encrypted_email = encrypt_field(email)
        encrypted_nid = encrypt_field(nid)
        if User.query.filter_by(username=encrypted_username).first():
            return (False, "Username already registered!")
        if User.query.filter_by(email=encrypted_email).first():
            return (False, "Email already registered!")
        if User.query.filter_by(nid=encrypted_nid).first():
            return (False, "NID already registered!")

        try:
            if isinstance(date_of_birth, str):
                datetime.strptime(date_of_birth, '%Y-%m-%d')
            else:
                date_of_birth = date_of_birth.strftime('%Y-%m-%d')
        except ValueError:
            return (False, "Invalid date format. Use YYYY-MM-DD")

        password = generate_password_hash(password)
        encrypted_name = encrypt_field(name)
        encrypted_address = encrypt_field(address)
        encrypted_contact = encrypt_field(contact)
        encrypted_dob = encrypt_field(date_of_birth)
        encrypted_blood_type = encrypt_field(blood_type)

        user = User(
            username=encrypted_username,
            email=encrypted_email,
            name=encrypted_name,
            nid=encrypted_nid,
            date_of_birth=encrypted_dob,
            address=encrypted_address,
            password=password,
            contact=encrypted_contact,
            blood_type=encrypted_blood_type
        )
        db.session.add(user)
        db.session.commit()
        return (True, "User registered!")

    def getInfo(self):
        return {
            'username': decrypt_field(self.username),
            'name': decrypt_field(self.name),
            'nid': decrypt_field(self.nid),
            'date_of_birth': decrypt_field(self.date_of_birth),
            'email': decrypt_field(self.email),
            'address': decrypt_field(self.address),
            'contact': decrypt_field(self.contact), 
            'blood_type': decrypt_field(self.blood_type),  
            'blood_donation': self.blood_donation
        }

    @staticmethod
    def getUser(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def donate_blood(id):
        user = User.getUser(id)
        if user.blood_donation == "False":
            user.blood_donation = "True"
        else:
            user.blood_donation = "False"
        db.session.commit()
        info = user.getInfo()
        return info

    @staticmethod
    def getAlluser():
        all_users = User.query.all()
        filtered = [user for user in all_users if user.blood_donation == "True"]
        sorted_users = sorted(
            filtered,
            key=lambda u: (decrypt_field(u.address), decrypt_field(u.blood_type))
        )
        return [user.getInfo() for user in sorted_users]

    @staticmethod
    def filter_bloodbank(blood_type, address):
        return User.query.filter(User.blood_donation=="True", User.blood_type==blood_type, User.address.like(f"%{address}%")).all()

    @staticmethod
    def get_user_by_email(email):
        encrypted_email = encrypt_field(email)
        return User.query.filter_by(email=encrypted_email).first()