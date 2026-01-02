import math
import secrets
import string
from pathlib import Path
from typing import List


class PasswordGenerator:
    
    def __init__(self):
        self.rng = secrets.SystemRandom()
        self.eff_words = self._load_eff_wordlist()
    
    def _load_eff_wordlist(self) -> List[str]:
        wordlist_path = Path(__file__).parent.parent / 'data' / 'eff_large_wordlist.txt'
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                words = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 2:
                            words.append(parts[1])
                return words
        except FileNotFoundError:
            # Fallback to a minimal wordlist if file not found
            print(f"Warning: EFF wordlist not found at {wordlist_path}")
            print("Using fallback wordlist. For full security, download the EFF wordlist.")
            return self._get_fallback_wordlist()
    
    def _get_fallback_wordlist(self) -> List[str]:
        return [
            "abacus", "abdomen", "able", "abstract", "academy", "acrobat",
            "active", "actor", "adapt", "admiral", "adventure", "advice",
            "afraid", "agency", "agent", "airport", "album", "alcohol",
            "alert", "algebra", "alien", "along", "alpha", "already",
            "also", "altitude", "aluminum", "always", "amazed", "amber",
            "ambition", "amount", "amused", "anchor", "ancient", "angel",
            "anger", "angle", "animal", "ankle", "announce", "answer"
        ]
    
    def generate_passphrase(
        self,
        entropy: int = 52,
        separator: str = "-",
        capitalize: bool = True,
        add_number: bool = True
    ) -> str:
        # Each word provides ~12.925 bits of entropy
        bits_per_word = math.log2(len(self.eff_words))
        words_needed = max(3, math.ceil(entropy / bits_per_word))
        
        # Select random words
        words = [self.rng.choice(self.eff_words) for _ in range(words_needed)]
        
        if capitalize:
            words = [w.capitalize() for w in words]
        
        passphrase = separator.join(words)
        
        # Add a random number for extra entropy (adds ~6.6 bits)
        if add_number:
            random_num = self.rng.randint(10, 99)
            passphrase += str(random_num)
        
        return passphrase
    
    def generate_mixed(self, length: int = 16) -> str:
        if length < 4:
            raise ValueError("Password length must be at least 4")
        
        charset = string.ascii_letters + string.digits + string.punctuation
        
        # Ensure at least one of each type for strength
        password = [
            self.rng.choice(string.ascii_lowercase),
            self.rng.choice(string.ascii_uppercase),
            self.rng.choice(string.digits),
            self.rng.choice(string.punctuation)
        ]
        
        # Fill the rest randomly
        password.extend(self.rng.choice(charset) for _ in range(length - 4))
        
        # Shuffle to avoid predictable pattern
        self.rng.shuffle(password)
        
        return ''.join(password)
    
    def generate_alphanumeric(self, length: int = 12) -> str:
        if length < 2:
            raise ValueError("Password length must be at least 2")
        
        charset = string.ascii_letters + string.digits
        
        # Ensure at least one letter and one digit
        password = [
            self.rng.choice(string.ascii_letters),
            self.rng.choice(string.digits)
        ]
        
        # Fill the rest
        password.extend(self.rng.choice(charset) for _ in range(length - 2))
        
        # Shuffle
        self.rng.shuffle(password)
        
        return ''.join(password)
    
    def generate_pin(self, length: int = 6) -> str:
        return ''.join(str(self.rng.randint(0, 9)) for _ in range(length))
    
    def generate_batch(
        self,
        count: int,
        style: str = "passphrase",
        **kwargs
    ) -> List[str]:
        generators = {
            'passphrase': self.generate_passphrase,
            'mixed': self.generate_mixed,
            'alphanumeric': self.generate_alphanumeric,
            'pin': self.generate_pin
        }
        
        if style not in generators:
            raise ValueError(f"Unknown style: {style}. Choose from: {list(generators.keys())}")
        
        return [generators[style](**kwargs) for _ in range(count)]
    
    def get_wordlist_info(self) -> dict:
        return {
            'size': len(self.eff_words),
            'bits_per_word': math.log2(len(self.eff_words)),
            'source': 'EFF Large Wordlist' if len(self.eff_words) > 1000 else 'Fallback'
        }