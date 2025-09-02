from models.volunteer import Volunteer
from models.crypto_utils import decrypt_field
from database import db
from app import app


def migrate_decrypt_volunteers():
    with app.app_context():
        volunteers = Volunteer.query.all()
        count = 0
        for v in volunteers:
            try:
                decrypted_role = decrypt_field(v.role)
                decrypted_availability = decrypt_field(v.availability) if v.availability is not None else None
                decrypted_userId = decrypt_field(v.userId) if v.userId is not None else None

                v.role = decrypted_role
                v.availability = decrypted_availability
                v.userId = decrypted_userId

                db.session.add(v)
                db.session.commit()
                count += 1
            except Exception as e:
                db.session.rollback()
                print(f"Failed to process volunteer id={getattr(v, 'volunteerid', None)}: {e}")
        print(f"Decryption migration completed. Rows processed: {count}")


if __name__ == '__main__':
    migrate_decrypt_volunteers()
