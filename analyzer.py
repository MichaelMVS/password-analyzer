import re
import math
from typing import Dict, List

COMMON_PASSWORDS = {
    'password', '123456', 'qwerty', 'abc123', 'letmein', 'trustno1',
    'dragon', 'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
    'bailey', 'passw0rd', '123456789', 'shadow', '123123', '777777',
    'qazwsx', 'michael', 'football', 'welcome', 'jesus', 'ninja',
    'mustang', 'password123', 'admin', 'letmein', 'monkey', 'dragon'
}

KEYBOARD_PATTERNS = [
    'qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', 'qwertyuiop', 'asdfghjkl',
    'zxcvbnm', 'qweasd', '1234567890', 'abcdef'
]

class PasswordAnalyzer:
    def __init__(self):
        self.results = {}

    def analyze(self, password: str) -> Dict:
        try:
            password = str(password).strip()
            
            if not password:
                return {
                    'password_length': 0,
                    'strength_score': 0,
                    'strength_label': 'Very Weak',
                    'entropy': 0.0,
                    'character_types': {
                        'has_uppercase': False, 'has_lowercase': False,
                        'has_digits': False, 'has_special': False,
                        'uppercase_count': 0, 'lowercase_count': 0,
                        'digit_count': 0, 'special_count': 0
                    },
                    'patterns': {
                        'sequential_chars': False, 'repeated_chars': False,
                        'keyboard_pattern': False, 'date_pattern': False,
                        'email_pattern': False, 'username_pattern': False
                    },
                    'vulnerabilities': ['too_short'],
                    'time_to_crack': {'time': 'Less than 1 second', 'guesses_per_second': '1 trillion'},
                    'recommendations': ['Password cannot be empty']
                }
            
            character_types = self._analyze_character_types(password)
            patterns = self._detect_patterns(password)
            entropy = self._calculate_entropy(password)
            vulnerabilities = self._find_vulnerabilities(password, character_types, patterns)
            crack_time = self._estimate_crack_time(password, entropy)
            strength_score = self._calculate_strength_score(password, character_types, entropy, vulnerabilities)
            strength_label = self._get_strength_label(strength_score)
            recommendations = self._get_recommendations(password, character_types, patterns)
            
            self.results = {
                'password_length': len(password),
                'strength_score': int(strength_score),
                'strength_label': str(strength_label),
                'entropy': float(entropy),
                'character_types': character_types,
                'patterns': patterns,
                'vulnerabilities': vulnerabilities,
                'time_to_crack': crack_time,
                'recommendations': recommendations
            }
            
            return self.results
        
        except Exception as e:
            print(f"Error in analyze: {str(e)}")
            raise

    def _analyze_character_types(self, password: str) -> Dict:
        return {
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_digits': bool(re.search(r'\d', password)),
            'has_special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password)),
            'uppercase_count': len(re.findall(r'[A-Z]', password)),
            'lowercase_count': len(re.findall(r'[a-z]', password)),
            'digit_count': len(re.findall(r'\d', password)),
            'special_count': len(re.findall(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password))
        }

    def _calculate_entropy(self, password: str) -> float:
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            charset_size += 32

        if charset_size == 0:
            return 0.0
        
        try:
            entropy = len(password) * math.log2(charset_size)
            return round(float(entropy), 2)
        except:
            return 0.0

    def _detect_patterns(self, password: str) -> Dict:
        lower_pass = password.lower()
        sequential = self._find_sequential(password)
        
        return {
            'sequential_chars': bool(sequential),
            'repeated_chars': bool(re.search(r'(.)\1{2,}', password)),
            'keyboard_pattern': any(pattern in lower_pass for pattern in KEYBOARD_PATTERNS),
            'date_pattern': bool(re.search(r'(19|20)\d{2}|(\d{1,2}[/-]){2}\d{2,4}', password)),
            'email_pattern': bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', password)),
            'username_pattern': bool(re.search(r'^[a-z0-9]{3,}$', lower_pass))
        }

    def _find_sequential(self, password: str) -> List[str]:
        sequential = []
        try:
            for i in range(len(password) - 2):
                if ord(password[i+1]) == ord(password[i]) + 1 and ord(password[i+2]) == ord(password[i+1]) + 1:
                    sequential.append(password[i:i+3])
        except:
            pass
        return sequential

    def _find_vulnerabilities(self, password: str, character_types: Dict, patterns: Dict) -> List[str]:
        vulns = []
        
        if len(password) < 8:
            vulns.append('too_short')
        
        if password.lower() in COMMON_PASSWORDS:
            vulns.append('common_password')
        
        if patterns.get('keyboard_pattern', False):
            vulns.append('keyboard_pattern')
        
        if re.search(r'(.)\1{3,}', password):
            vulns.append('excessive_repetition')
        
        if patterns.get('sequential_chars', False):
            vulns.append('sequential_characters')
        
        char_variety = sum([
            character_types.get('has_uppercase', False),
            character_types.get('has_lowercase', False),
            character_types.get('has_digits', False),
            character_types.get('has_special', False)
        ])
        if char_variety <= 1:
            vulns.append('insufficient_character_variety')
        
        return vulns

    def _estimate_crack_time(self, password: str, entropy: float) -> Dict:
        try:
            if entropy == 0 or len(password) == 0:
                return {'time': 'Less than 1 second', 'guesses_per_second': '1 trillion'}
            
            charset_size = 0
            if re.search(r'[a-z]', password):
                charset_size += 26
            if re.search(r'[A-Z]', password):
                charset_size += 26
            if re.search(r'\d', password):
                charset_size += 10
            if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
                charset_size += 32
            
            if charset_size == 0:
                return {'time': 'Less than 1 second', 'guesses_per_second': '1 trillion'}
            
            total_combinations = charset_size ** len(password)
            avg_attempts = total_combinations / 2.0
            guesses_per_second = 1e12
            
            seconds = float(avg_attempts) / float(guesses_per_second)
            
            if seconds < 1:
                return {'time': 'Less than 1 second', 'guesses_per_second': '1 trillion'}
            elif seconds < 60:
                return {'time': f'{int(seconds)} seconds', 'guesses_per_second': '1 trillion'}
            elif seconds < 3600:
                minutes = seconds / 60.0
                return {'time': f'{minutes:.1f} minutes', 'guesses_per_second': '1 trillion'}
            elif seconds < 86400:
                hours = seconds / 3600.0
                return {'time': f'{hours:.1f} hours', 'guesses_per_second': '1 trillion'}
            else:
                days = seconds / 86400.0
                if days > 365:
                    years = days / 365.0
                    return {'time': f'{years:.1f} years', 'guesses_per_second': '1 trillion'}
                return {'time': f'{days:.1f} days', 'guesses_per_second': '1 trillion'}
        except Exception as e:
            print(f"Error in estimate_crack_time: {e}")
            return {'time': 'Unable to calculate', 'guesses_per_second': '1 trillion'}

    def _calculate_strength_score(self, password: str, character_types: Dict, entropy: float, vulnerabilities: List) -> int:
        try:
            score = 0
            
            length = len(password)
            if length >= 12:
                score += 25
            elif length >= 10:
                score += 20
            elif length >= 8:
                score += 15
            elif length >= 6:
                score += 5
            
            if character_types.get('has_uppercase', False):
                score += 15
            if character_types.get('has_lowercase', False):
                score += 15
            if character_types.get('has_digits', False):
                score += 15
            if character_types.get('has_special', False):
                score += 15
            
            if entropy >= 70:
                score += 20
            elif entropy >= 50:
                score += 15
            elif entropy >= 40:
                score += 10
            
            score -= len(vulnerabilities) * 10
            
            return int(max(0, min(100, score)))
        except Exception as e:
            print(f"Error in calculate_strength_score: {e}")
            return 0

    def _get_strength_label(self, score: int) -> str:
        if score >= 80:
            return 'Very Strong'
        elif score >= 60:
            return 'Strong'
        elif score >= 40:
            return 'Moderate'
        elif score >= 20:
            return 'Weak'
        else:
            return 'Very Weak'

    def _get_recommendations(self, password: str, character_types: Dict, patterns: Dict) -> List[str]:
        recs = []
        
        if len(password) < 12:
            recs.append('Increase password length to at least 12 characters')
        
        if not character_types.get('has_uppercase', False):
            recs.append('Add uppercase letters')
        
        if not character_types.get('has_lowercase', False):
            recs.append('Add lowercase letters')
        
        if not character_types.get('has_digits', False):
            recs.append('Add numbers')
        
        if not character_types.get('has_special', False):
            recs.append('Add special characters (!@#$%^&*)')
        
        if patterns.get('keyboard_pattern', False):
            recs.append('Avoid keyboard patterns (qwerty, asdfgh, etc.)')
        
        if patterns.get('sequential_chars', False):
            recs.append('Avoid sequential characters (abc, 123, etc.)')
        
        if patterns.get('date_pattern', False):
            recs.append('Avoid using dates in your password')
        
        if not recs:
            recs.append('Your password is excellent! Keep it secure.')
        
        return recs
