from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from app import app

def migrate_hash_passwords():
    with app.app_context():
        users = User.query.all()
        for user in users:
            password = user.password
            if not (password.startswith('pbkdf2:sha256:') or password.startswith('sha256$')):
                user.password = generate_password_hash(password)
        db.session.commit()
    print('Migration complete: all user passwords hashed.')

if __name__ == '__main__':
    migrate_hash_passwords()
