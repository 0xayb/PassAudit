from pathlib import Path
from typing import Set, List
from utils.crypto import hash_password


def load_password_dictionaries(file_paths: List[str]) -> Set[str]:
    password_hashes: Set[str] = set()
    
    for file_path in file_paths:
        path = Path(file_path)
        
        if not path.exists():
            print(f"Warning: Dictionary file not found: {file_path}")
            continue
        
        try:
            lines_processed = 0
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    pwd = line.strip()
                    if pwd and not pwd.startswith('#'):
                        # Hash immediately to avoid keeping plaintext in memory
                        hashed = hash_password(pwd)
                        password_hashes.add(hashed)
                        lines_processed += 1
            
            print(f"  Loaded {lines_processed:,} passwords from {path.name}")
                        
        except UnicodeDecodeError as e:
            print(f"Warning: Encoding error in {file_path}: {e}")
            continue
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue
    
    return password_hashes


def load_custom_wordlist(file_path: str) -> List[str]:
    words = []
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Wordlist file not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word and not word.startswith('#'):
                words.append(word)
    
    return words


def create_sample_dictionary(output_path: str, passwords: List[str]) -> None:
    path = Path(output_path)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# Sample password dictionary\n")
        f.write("# One password per line\n")
        for pwd in passwords:
            f.write(f"{pwd}\n")
    
    print(f"Created sample dictionary at {output_path} with {len(passwords)} passwords")


def merge_dictionaries(input_paths: List[str], output_path: str) -> int:
    unique_passwords = set()
    
    for file_path in input_paths:
        path = Path(file_path)
        if not path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                pwd = line.strip()
                if pwd and not pwd.startswith('#'):
                    unique_passwords.add(pwd)
    
    # Write merged dictionary
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Merged password dictionary\n")
        for pwd in sorted(unique_passwords):
            f.write(f"{pwd}\n")
    
    return len(unique_passwords)