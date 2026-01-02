from typing import Dict, List
from zxcvbn import zxcvbn
from utils.crypto import hash_password, calculate_entropy
from core.checker import PasswordChecker


class PasswordAnalyzer:
    def __init__(self):
        self._analysis_count = 0
    
    def analyze(self, password: str, checker: PasswordChecker) -> Dict:
        self._analysis_count += 1
        
        # Use zxcvbn for strength analysis
        zxcvbn_result = zxcvbn(password)
        
        # Check if it's a common password
        is_common = checker.is_common_password(password)
        
        # Get hash
        pwd_hash = hash_password(password)
        
        # Calculate entropy
        entropy = calculate_entropy(password)
        
        # Generate feedback
        feedback = self._generate_feedback(
            password, 
            zxcvbn_result, 
            is_common,
            entropy
        )
        
        return {
            'password_length': len(password),
            'score': zxcvbn_result['score'],
            'is_common': is_common,
            'hash': pwd_hash,
            'feedback': feedback,
            'entropy': entropy,
            'crack_times': zxcvbn_result.get('crack_times_display', {}),
            'sequence_info': zxcvbn_result.get('sequence', []),
            'pattern_matches': self._extract_pattern_info(zxcvbn_result)
        }
    
    def _generate_feedback(
        self, 
        password: str, 
        zxcvbn_result: dict,
        is_common: bool,
        entropy: float
    ) -> List[str]:
        
        feedback = []
        
        # Add breach warning first if applicable
        if is_common:
            feedback.append("⚠️  This password has been exposed in data breaches")
        
        # Add zxcvbn warning
        if zxcvbn_result['feedback']['warning']:
            feedback.append(zxcvbn_result['feedback']['warning'])
        
        # Add zxcvbn suggestions
        feedback.extend(zxcvbn_result['feedback']['suggestions'])
        
        # Add length recommendations
        if len(password) < 12:
            feedback.append("Use at least 12 characters for better security")
        elif len(password) < 16:
            feedback.append("Consider using 16+ characters for optimal security")
        
        # Add entropy recommendations
        if entropy < 40:
            feedback.append("Password has low entropy - add more character variety")
        
        # Check for character variety
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        missing_types = []
        if not has_lower:
            missing_types.append("lowercase letters")
        if not has_upper:
            missing_types.append("uppercase letters")
        if not has_digit:
            missing_types.append("numbers")
        if not has_special:
            missing_types.append("special characters")
        
        if len(missing_types) > 0:
            feedback.append(f"Add {', '.join(missing_types)} for better security")
        
        return feedback
    
    def _extract_pattern_info(self, zxcvbn_result: dict) -> List[Dict]:
        patterns = []
        
        if 'sequence' in zxcvbn_result:
            for match in zxcvbn_result['sequence']:
                pattern_info = {
                    'pattern': match.get('pattern', 'unknown'),
                    'token': match.get('token', ''),
                }
                
                # Add pattern-specific information
                if match.get('pattern') == 'dictionary':
                    pattern_info['dictionary_name'] = match.get('dictionary_name', '')
                elif match.get('pattern') == 'date':
                    pattern_info['year'] = match.get('year', '')
                
                patterns.append(pattern_info)
        
        return patterns
    
    def get_stats(self) -> dict:
        return {
            'total_analyses': self._analysis_count
        }