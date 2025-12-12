import hashlib
import os


def calculate_hash(file_path):
    """Calculate SHA-256 hash of the file."""
    hash = hashlib.blake2s()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash.update(byte_block)
    return hash.hexdigest()


def check_file(_file_path, _last_hash):
    if not os.path.exists(_file_path):
        return (15, "")

    current_hash = calculate_hash(_file_path)

    if _last_hash == current_hash:
        return (0, current_hash)
    else:
        return (23, current_hash)
