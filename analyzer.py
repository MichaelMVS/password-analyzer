import re
import math
from typing import Dict, List, Tuple

COMMON_PASSWORDS = {
    'password', '123456', 'qwerty', 'abc123', 'letmein', 'trustno1',
    'dragon', 'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
    'bailey', 'passw0rd', '123456789', 'shadow', '123123', '777777',
    'qazwsx', 'michael', 'football', 'welcome', 'jesus', 'ninja',
    'mustang', 'password123', 'admin', 'letmein', 'monkey', 'dragon',
    '111111', 'welcome', '1234567', 'login', 'princess', 'starwars'
}

KEYBOARD_PATTERNS = {
    'qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', 'qwertyuiop', 'asdfghjkl',
    'zxcvbnm', 'qweasd', '1234567890', 'abcdef', 'qwertyu', 'asdfghjk',
    'zxcvbn', 'dvorak', 'colemak'
}

COMMON_SUBSTITUTIONS = {
    'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7', 'l': '1'
}

class PasswordAnalyzer:
    def __init__(self):
        self.results = {}
        self.attack_speeds = {
            'online': 100,
            'offline': 1e9,
            'gpu': 1e10,
            'specialized': 1e12
        }

    def analyze(self, password: str) -> Dict:
        try:
            password = str(password).strip()
            
            if not password:
                return self._empty_password_result()
            
            character_types = self._analyze_character_types(password)
            patterns = self._detect_patterns(password)
            entropy_data = self._calculate_advanced_entropy(password, character_types)
            vulnerabilities = self._find_vulnerabilities(password, character_types, patterns, entropy_data)
            crack_times = self._estimate_crack_times(password, entropy_data)
            strength_score = self._calculate_nist_strength_score(password, character_types, entropy_data, vulnerabilities)
            strength_label = self._get_strength_label(strength_score)
            recommendations = self._get_recommendations(password, character_types, patterns)
            
            self.results = {
                'password_length': len(password),
                'strength_score': int(strength_score),
                'strength_label': str(strength_label),
                'entropy': float(entropy_data['shannon_entropy']),
                'effective_entropy': float(entropy_data['effective_entropy']),
                'character_types': character_types,
                'patterns': patterns,
                'vulnerabilities': vulnerabilities,
                'time_to_crack': crack_times,
                'recommendations': recommendations,
                'attack_scenarios': self._generate_attack_scenarios(entropy_data)
            }
            
            return self.results
        
        except Exception as e:
            print(f"Error in analyze: {str(e)}")
            raise

    def _empty_password_result(self) -> Dict:
        return {
            'password_length': 0,
            'strength_score': 0,
            'strength_label': 'Very Weak',
            'entropy': 0.0,
            'effective_entropy': 0.0,
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
            'time_to_crack': {'offline_attack': '< 1 second'},
            'recommendations': ['Password cannot be empty'],
            'attack_scenarios': {}
        }

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

    def _calculate_advanced_entropy(self, password: str, char_types: Dict) -> Dict:
        try:
            charset_size = self._calculate_charset_size(password)
            shannon_entropy = len(password) * math.log2(charset_size) if charset_size > 1 else 0
            
            patterns_penalty = self._calculate_pattern_entropy_penalty(password)
            dictionary_penalty = self._calculate_dictionary_penalty(password)
            
            effective_entropy = max(0, shannon_entropy - patterns_penalty - dictionary_penalty)
            
            return {
                'shannon_entropy': round(float(shannon_entropy), 2),
                'effective_entropy': round(float(effective_entropy), 2),
                'charset_size': charset_size,
                'pattern_penalty': patterns_penalty,
                'dictionary_penalty': dictionary_penalty
            }
        except:
            return {
                'shannon_entropy': 0.0,
                'effective_entropy': 0.0,
                'charset_size': 0,
                'pattern_penalty': 0.0,
                'dictionary_penalty': 0.0
            }

    def _calculate_charset_size(self, password: str) -> int:
        size = 0
        if re.search(r'[a-z]', password):
            size += 26
        if re.search(r'[A-Z]', password):
            size += 26
        if re.search(r'\d', password):
            size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            size += 32
        return size

    def _calculate_pattern_entropy_penalty(self, password: str) -> float:
        penalty = 0.0
        
        if re.search(r'(.)\1{2,}', password):
            penalty += 5.0
        if re.search(r'(.)\1{4,}', password):
            penalty += 10.0
            
        sequential_count = len(self._find_sequential(password))
        penalty += sequential_count * 3.0
        
        if self._is_keyboard_pattern(password):
            penalty += 8.0
        
        if self._is_date_pattern(password):
            penalty += 6.0
        
        return penalty

    def _calculate_dictionary_penalty(self, password: str) -> float:
        penalty = 0.0
        lower = password.lower()
        
        if lower in COMMON_PASSWORDS:
            return 50.0
        
        for common_pass in COMMON_PASSWORDS:
            if common_pass in lower:
                penalty += 10.0
                break
        
        common_words = ['password', 'admin', 'user', 'test', 'demo', 'login', 'welcome']
        for word in common_words:
            if word in lower:
                penalty += 5.0
        
        return penalty

    def _is_keyboard_pattern(self, password: str) -> bool:
        lower = password.lower()
        for pattern in KEYBOARD_PATTERNS:
            if pattern in lower:
                if len(pattern) >= 3:
                    return True
        return False

    def _is_date_pattern(self, password: str) -> bool:
        return bool(re.search(r'(19|20)\d{2}|(\d{1,2}[/-]){2}\d{2,4}', password))

    def _detect_patterns(self, password: str) -> Dict:
        lower_pass = password.lower()
        sequential = self._find_sequential(password)
        
        return {
            'sequential_chars': bool(sequential),
            'repeated_chars': bool(re.search(r'(.)\1{2,}', password)),
            'keyboard_pattern': self._is_keyboard_pattern(password),
            'date_pattern': self._is_date_pattern(password),
            'email_pattern': bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', password)),
            'username_pattern': bool(re.search(r'^[a-z0-9]{3,}$', lower_pass)),
            'l33t_speak': self._has_leet_speak(password),
            'dictionary_words': self._contains_dictionary_words(password)
        }

    def _has_leet_speak(self, password: str) -> bool:
        return bool(re.search(r'[@3!1$0]', password))

    def _contains_dictionary_words(self, password: str) -> bool:
        lower = password.lower()
        common_words = ['password', 'admin', 'user', 'test', 'welcome', 'dragon']
        for word in common_words:
            if word in lower:
                return True
        return False

    def _find_sequential(self, password: str) -> List[str]:
        sequential = []
        try:
            for i in range(len(password) - 2):
                if ord(password[i+1]) == ord(password[i]) + 1 and ord(password[i+2]) == ord(password[i+1]) + 1:
                    sequential.append(password[i:i+3])
        except:
            pass
        return sequential

    def _find_vulnerabilities(self, password: str, char_types: Dict, patterns: Dict, entropy: Dict) -> List[str]:
        vulns = []
        
        if len(password) < 8:
            vulns.append('too_short')
        if len(password) < 12:
            vulns.append('suboptimal_length')
        
        if password.lower() in COMMON_PASSWORDS:
            vulns.append('common_password')
        
        if patterns.get('keyboard_pattern', False):
            vulns.append('keyboard_pattern')
        
        if re.search(r'(.)\1{3,}', password):
            vulns.append('excessive_repetition')
        
        if patterns.get('sequential_chars', False):
            vulns.append('sequential_characters')
        
        char_variety = sum([
            char_types.get('has_uppercase', False),
            char_types.get('has_lowercase', False),
            char_types.get('has_digits', False),
            char_types.get('has_special', False)
        ])
        if char_variety <= 1:
            vulns.append('insufficient_character_variety')
        
        if entropy.get('effective_entropy', 0) < 30:
            vulns.append('low_entropy')
        
        if patterns.get('dictionary_words', False):
            vulns.append('dictionary_words')
        
        return vulns

    def _estimate_crack_times(self, password: str, entropy: Dict) -> Dict:
        try:
            eff_entropy = entropy.get('effective_entropy', 0)
            
            if eff_entropy == 0 or len(password) == 0:
                return {'offline_attack': 'Less than 1 second', 'online_attack': 'Less than 1 millisecond'}
            
            total_combinations = 2 ** eff_entropy
            avg_attempts = total_combinations / 2.0
            
            crack_times = {}
            for scenario, speed in self.attack_speeds.items():
                seconds = avg_attempts / speed
                crack_times[f'{scenario}_attack'] = self._format_time(seconds)
            
            return crack_times
        except Exception as e:
            print(f"Error in estimate_crack_times: {e}")
            return {'offline_attack': 'Unable to calculate'}

    def _format_time(self, seconds: float) -> str:
        if seconds < 0.001:
            return 'Less than 1ms'
        elif seconds < 1:
            return f'{seconds*1000:.0f}ms'
        elif seconds < 60:
            return f'{int(seconds)}s'
        elif seconds < 3600:
            return f'{seconds/60:.1f}m'
        elif seconds < 86400:
            return f'{seconds/3600:.1f}h'
        elif seconds < 31536000:
            return f'{seconds/86400:.1f}d'
        else:
            years = seconds / 31536000
            return f'{years:.1f}y'

    def _generate_attack_scenarios(self, entropy: Dict) -> Dict:
        eff_entropy = entropy.get('effective_entropy', 0)
        
        scenarios = {
            'dictionary_attack': 'Resistance: ' + self._format_time((2**min(eff_entropy, 20)) / 1e9),
            'brute_force_cpu': 'Resistance: ' + self._format_time((2**eff_entropy) / 1e9),
            'brute_force_gpu': 'Resistance: ' + self._format_time((2**eff_entropy) / 1e10),
            'specialized_hardware': 'Resistance: ' + self._format_time((2**eff_entropy) / 1e12)
        }
        return scenarios

    def _calculate_nist_strength_score(self, password: str, char_types: Dict, entropy: Dict, vulns: List) -> int:
        try:
            score = 0
            eff_entropy = entropy.get('effective_entropy', 0)
            
            if eff_entropy >= 60:
                score += 40
            elif eff_entropy >= 50:
                score += 30
            elif eff_entropy >= 40:
                score += 20
            elif eff_entropy >= 30:
                score += 10
            
            length = len(password)
            if length >= 16:
                score += 30
            elif length >= 12:
                score += 25
            elif length >= 10:
                score += 15
            elif length >= 8:
                score += 10
            
            char_variety = sum([
                char_types.get('has_uppercase', False),
                char_types.get('has_lowercase', False),
                char_types.get('has_digits', False),
                char_types.get('has_special', False)
            ])
            
            if char_variety == 4:
                score += 20
            elif char_variety == 3:
                score += 10
            
            score -= len(vulns) * 8
            
            return int(max(0, min(100, score)))
        except Exception as e:
            print(f"Error in calculate_nist_strength_score: {e}")
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

    def _get_recommendations(self, password: str, char_types: Dict, patterns: Dict) -> List[str]:
        recs = []
        
        if len(password) < 16:
            recs.append('Increase length to 16+ characters for maximum security')
        elif len(password) < 12:
            recs.append('Increase length to at least 12 characters')
        
        if not char_types.get('has_uppercase', False):
            recs.append('Include uppercase letters (A-Z)')
        
        if not char_types.get('has_lowercase', False):
            recs.append('Include lowercase letters (a-z)')
        
        if not char_types.get('has_digits', False):
            recs.append('Include numbers (0-9)')
        
        if not char_types.get('has_special', False):
            recs.append('Include special characters (!@#$%^&*)')
        
        if patterns.get('keyboard_pattern', False):
            recs.append('Avoid keyboard walks (qwerty, asdfgh)')
        
        if patterns.get('sequential_chars', False):
            recs.append('Avoid sequential patterns (abc, 123)')
        
        if patterns.get('date_pattern', False):
            recs.append('Avoid dates and year patterns')
        
        if patterns.get('dictionary_words', False):
            recs.append('Avoid common dictionary words')
        
        if patterns.get('repeated_chars', False):
            recs.append('Minimize repeated characters')
        
        if not recs:
            recs.append('Password follows security best practices!')
        
        return recs
