import re
import math
from collections import defaultdict
from typing import Dict, List
import requests

COMMON_PASSWORDS = {
    'password', '123456', 'qwerty', 'abc123', 'letmein', 'trustno1',
    'dragon', 'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
    'bailey', 'passw0rd', '123456789', 'shadow', '123123', '666666',
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
        self.results = {
            'password_length': len(password),
            'strength_score': 0,
            'strength_label': '',
            'entropy': self.calculate_entropy(password),
            'character_types': self.analyze_character_types(password),
            'patterns': self.detect_patterns(password),
            'vulnerabilities': self.find_vulnerabilities(password),
            'time_to_crack': self.estimate_crack_time(password),
            'recommendations': self.get_recommendations(password)
        }
        self.results['strength_score'] = self.calculate_strength_score()
        self.results['strength_label'] = self.get_strength_label()
        return self.results

    def analyze_character_types(self, password: str) -> Dict[str, bool]:
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

    def calculate_entropy(self, password: str) -> float:
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
        
        entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
        return round(entropy, 2)

    def detect_patterns(self, password: str) -> Dict[str, bool]:
        lower_pass = password.lower()
        
        return {
            'sequential_chars': bool(self.find_sequential(password)),
            'repeated_chars': bool(re.search(r'(.)\1{2,}', password)),
            'keyboard_pattern': any(pattern in lower_pass for pattern in KEYBOARD_PATTERNS),
            'date_pattern': bool(re.search(r'(19|20)\d{2}|(\d{1,2}[/-]){2}\d{2,4}', password)),
            'email_pattern': bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', password)),
            'username_pattern': bool(re.search(r'^[a-z0-9]{3,}$', lower_pass))
        }

    def find_sequential(self, password: str) -> List[str]:
        sequential = []
        for i in range(len(password) - 2):
            if ord(password[i+1]) == ord(password[i]) + 1 and ord(password[i+2]) == ord(password[i+1]) + 1:
                sequential.append(password[i:i+3])
        return sequential

    def find_vulnerabilities(self, password: str) -> List[str]:
        vulns = []
        
        if len(password) < 8:
            vulns.append('too_short')
        
        if password.lower() in COMMON_PASSWORDS:
            vulns.append('common_password')
        
        if self.results['patterns']['keyboard_pattern']:
            vulns.append('keyboard_pattern')
        
        if re.search(r'(.)\1{3,}', password):
            vulns.append('excessive_repetition')
        
        if self.results['patterns']['sequential_chars']:
            vulns.append('sequential_characters')
        
        if len(self.results['character_types']) == 1:
            vulns.append('insufficient_character_variety')
        
        return vulns

    def estimate_crack_time(self, password: str) -> Dict[str, str]:
        if self.results['entropy'] == 0:
            return {'estimated_hours': '< 1 second', 'guess_per_second': '∞'}
        
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            charset_size += 32
        
        total_combinations = charset_size ** len(password)
        avg_attempts = total_combinations / 2
        guesses_per_second = 1e12
        
        seconds = avg_attempts / guesses_per_second
        
        if seconds < 1:
            return {'time': 'Less than 1 second', 'guesses_per_second': '1 trillion'}
        elif seconds < 60:
            return {'time': f'{seconds:.0f} seconds', 'guesses_per_second': '1 trillion'}
        elif seconds < 3600:
            minutes = seconds / 60
            return {'time': f'{minutes:.1f} minutes', 'guesses_per_second': '1 trillion'}
        elif seconds < 86400:
            hours = seconds / 3600
            return {'time': f'{hours:.1f} hours', 'guesses_per_second': '1 trillion'}
        else:
            days = seconds / 86400
            if days > 365:
                years = days / 365
                return {'time': f'{years:.1f} years', 'guesses_per_second': '1 trillion'}
            return {'time': f'{days:.1f} days', 'guesses_per_second': '1 trillion'}

    def calculate_strength_score(self) -> int:
        score = 0
        
        length = self.results['password_length']
        if length >= 12:
            score += 25
        elif length >= 10:
            score += 20
        elif length >= 8:
            score += 15
        elif length >= 6:
            score += 5
        
        char_types = self.results['character_types']
        if char_types['has_uppercase']:
            score += 15
        if char_types['has_lowercase']:
            score += 15
        if char_types['has_digits']:
            score += 15
        if char_types['has_special']:
            score += 15
        
        entropy = self.results['entropy']
        if entropy >= 70:
            score += 20
        elif entropy >= 50:
            score += 15
        elif entropy >= 40:
            score += 10
        
        vulns = self.results['vulnerabilities']
        score -= len(vulns) * 10
        
        return min(100, max(0, score))

    def get_strength_label(self) -> str:
        score = self.results['strength_score']
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

    def get_recommendations(self, password: str) -> List[str]:
        recs = []
        
        if len(password) < 12:
            recs.append('Increase password length to at least 12 characters')
        
        if not self.results['character_types']['has_uppercase']:
            recs.append('Add uppercase letters')
        
        if not self.results['character_types']['has_lowercase']:
            recs.append('Add lowercase letters')
        
        if not self.results['character_types']['has_digits']:
            recs.append('Add numbers')
        
        if not self.results['character_types']['has_special']:
            recs.append('Add special characters (!@#$%^&*)')
        
        if self.results['patterns']['keyboard_pattern']:
            recs.append('Avoid keyboard patterns (qwerty, asdfgh, etc.)')
        
        if self.results['patterns']['sequential_chars']:
            recs.append('Avoid sequential characters (abc, 123, etc.)')
        
        if self.results['patterns']['date_pattern']:
            recs.append('Avoid using dates in your password')
        
        if not recs:
            recs.append('Your password is excellent! Keep it secure.')
        
        return recs
