import hashlib
import math
import string


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def calculate_entropy(password: str) -> float:
    if not password:
        return 0.0
    
    charset_size = 0
    
    # Check which character classes are present
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    has_space = any(c.isspace() for c in password)
    has_extended = any(ord(c) > 127 for c in password)
    
    # Add to charset size based on character classes present
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_special:
        charset_size += len(string.punctuation)
    if has_space:
        charset_size += 1
    if has_extended:
        charset_size += 100
    
    if charset_size == 0:
        return 0.0
    
    # Calculate entropy
    entropy = len(password) * math.log2(charset_size)
    
    return entropy


def calculate_password_strength_score(entropy: float, is_common: bool) -> int:
    if is_common:
        return 0  # Any breached password is automatically weak
    
    if entropy < 28:
        return 0  # Very weak
    elif entropy < 36:
        return 1  # Weak
    elif entropy < 60:
        return 2  # Fair
    elif entropy < 128:
        return 3  # Strong
    else:
        return 4  # Very strong


def hash_file_sha256(file_path: str, chunk_size: int = 8192) -> str:
    sha256_hash = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()