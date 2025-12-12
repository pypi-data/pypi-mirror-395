from keeshond import logging_logger

log = logging_logger.getlogger(__name__, logging_logger.ERROR)

from keeshond.ktoga.keystore.database import Database
import bcrypt
import random
import base64
import hashlib

class Auth:
    def __init__(self, _database_path, _pepper=b"enter yout pepper value here"):
        self.db = Database(_database_path, "sqlite3")
        self.pepper = _pepper  # Fixed pepper value for all passwords

    def is_password_set(self):
        """Check if _password has been set"""
        return self.db.get_password_hash() is not None

    def set_password(self, _password):
        """Hash and store _password with pepper"""
        # Generate salt only once
        # Store hash in database
        # Bcrypt uses a modified Base64 encoding for the salt and hash portions, which does not include the '$' character
        self.db.store_password_hash(
            bcrypt.hashpw(base64.b64encode(hashlib.sha256((_password + self.pepper).encode('utf-8')).digest()),
                          bcrypt.gensalt(rounds=random.randint(4, 16))).decode('utf-8'))


    def verify_password(self, _password):
        """Verify provided _password against stored hash"""
        # Retrieve the stored data
        stored_hash = self.db.get_password_hash()
        if not stored_hash:
            return False

        try:
            return bcrypt.checkpw(base64.b64encode(hashlib.sha256((_password + self.pepper).encode('utf-8')).digest()),
                                  stored_hash)
        except ValueError as e:
            log.warning(f"Error verifying password: {e}")  # FUTURE translate text
            return False
