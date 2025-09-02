from models.volunteer import Volunteer
from models.crypto_utils import encrypt_field
from database import db

def migrate_volunteer_encryption():
    volunteers = Volunteer.query.all()
    for v in volunteers:
        try:
            _ = encrypt_field(v.role)
            test = v.role
            try:
                decrypted = v.role
                decrypted = v.role if decrypted == encrypt_field(decrypted) else decrypted
            except Exception:
                decrypted = v.role
            v.role = encrypt_field(decrypted)
        except Exception:
            v.role = encrypt_field(v.role)
        try:
            _ = encrypt_field(v.availability)
            test = v.availability
            try:
                decrypted = v.availability
                decrypted = v.availability if decrypted == encrypt_field(decrypted) else decrypted
            except Exception:
                decrypted = v.availability
            v.availability = encrypt_field(decrypted)
        except Exception:
            v.availability = encrypt_field(v.availability)
        try:
            _ = encrypt_field(str(v.userId))
            test = v.userId
            try:
                decrypted = v.userId
                decrypted = v.userId if decrypted == encrypt_field(decrypted) else decrypted
            except Exception:
                decrypted = v.userId
            v.userId = encrypt_field(str(decrypted))
        except Exception:
            v.userId = encrypt_field(str(v.userId))
        db.session.commit()
    print("Volunteer table migration to encryption complete.")

if __name__ == "__main__":
    migrate_volunteer_encryption()
