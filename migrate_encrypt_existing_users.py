from models.user import User
from models.crypto_utils import encrypt_field
from database import db
from app import app

def migrate_encrypt_existing_users():
    fields_to_encrypt = [
        'username', 'name', 'nid', 'date_of_birth', 'email', 'address', 'contact', 'blood_type'
    ]
    import base64
    with app.app_context():
        users = User.query.all()
        for user in users:
            for field in fields_to_encrypt:
                value = getattr(user, field)
                try:
                    base64.b64decode(value.encode())
                except Exception:
                    encrypted = encrypt_field(value)
                    setattr(user, field, encrypted)
            db.session.commit()
        print('Migration complete: all user fields encrypted except password.')

if __name__ == '__main__':
    migrate_encrypt_existing_users()
