from typing import Set
from utils.crypto import hash_password


class PasswordChecker:
    
    def __init__(self, common_password_hashes: Set[str]):
        self.common_password_hashes = common_password_hashes
        self._check_count = 0
    
    def is_common_password(self, password: str) -> bool:
        self._check_count += 1
        pwd_hash = hash_password(password)
        return pwd_hash in self.common_password_hashes
    
    def get_stats(self) -> dict:
        return {
            'total_checks': self._check_count,
            'database_size': len(self.common_password_hashes)
        }
    
    def __repr__(self) -> str:
        return f"PasswordChecker(database_size={len(self.common_password_hashes)})"