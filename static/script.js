const passwordInput = document.getElementById('password-input');
const toggleBtn = document.getElementById('toggle-visibility');
const copyBtn = document.getElementById('copy-btn');
const resultsSection = document.getElementById('results-section');

const vulnDescriptions = {
    'too_short': 'Password is shorter than 8 characters',
    'common_password': 'This is a commonly used password',
    'keyboard_pattern': 'Contains keyboard patterns (qwerty, asdfgh, etc.)',
    'excessive_repetition': 'Contains excessive repeated characters',
    'sequential_characters': 'Contains sequential characters (abc, 123, etc.)',
    'insufficient_character_variety': 'Uses only one type of character'
};

const patternDescriptions = {
    'sequential_chars': 'Sequential characters detected',
    'repeated_chars': 'Repeated characters detected',
    'keyboard_pattern': 'Keyboard pattern detected',
    'date_pattern': 'Date format detected',
    'email_pattern': 'Email format detected',
    'username_pattern': 'Username-like pattern detected'
};

const strengthDescriptions = {
    'Very Strong': 'Excellent password with high security',
    'Strong': 'Good password with solid security',
    'Moderate': 'Acceptable password, could be improved',
    'Weak': 'Poor security, needs improvement',
    'Very Weak': 'Insufficient security'
};

let debounceTimer;

toggleBtn.addEventListener('click', () => {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    toggleBtn.classList.toggle('active');
    updateToggleBtnIcon();
});

function updateToggleBtnIcon() {
    const icon = toggleBtn.querySelector('i');
    if (passwordInput.type === 'text') {
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

copyBtn.addEventListener('click', () => {
    const score = document.getElementById('strength-score').textContent;
    const label = document.getElementById('strength-label').textContent;
    const text = `Password Strength: ${label} (${score})`;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check"></i>';
        copyBtn.style.color = 'var(--success)';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.color = '';
        }, 2000);
    });
});

passwordInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    
    const password = e.target.value;
    
    if (!password) {
        resultsSection.style.display = 'none';
        copyBtn.style.display = 'none';
        return;
    }
    
    copyBtn.style.display = 'flex';
    
    debounceTimer = setTimeout(async () => {
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password })
            });

            if (!response.ok) throw new Error('Analysis failed');
            
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
        }
    }, 100);
});

function displayResults(data) {
    resultsSection.style.display = 'block';
    
    updateStrengthMeter(data.strength_score, data.strength_label);
    updateCharacterTypes(data.character_types);
    updateMetrics(data);
    updatePatterns(data.patterns);
    updateVulnerabilities(data.vulnerabilities);
    updateRecommendations(data.recommendations);
}

function updateStrengthMeter(score, label) {
    const fill = document.getElementById('meter-fill');
    const scoreEl = document.getElementById('strength-score');
    const labelEl = document.getElementById('strength-label');
    const descEl = document.getElementById('strength-desc');
    const circle = document.getElementById('strength-circle');
    
    fill.style.width = score + '%';
    scoreEl.textContent = score;
    labelEl.textContent = label;
    descEl.textContent = strengthDescriptions[label] || '';
    
    fill.classList.remove('weak', 'moderate', 'strong', 'very-strong');
    circle.classList.remove('weak', 'moderate', 'strong', 'very-strong');
    
    if (score >= 80) {
        fill.classList.add('very-strong');
        circle.classList.add('very-strong');
    } else if (score >= 60) {
        fill.classList.add('strong');
        circle.classList.add('strong');
    } else if (score >= 40) {
        fill.classList.add('moderate');
        circle.classList.add('moderate');
    } else {
        fill.classList.add('weak');
        circle.classList.add('weak');
    }
}

function updateCharacterTypes(charTypes) {
    const checks = [
        { id: 'check-uppercase', key: 'has_uppercase' },
        { id: 'check-lowercase', key: 'has_lowercase' },
        { id: 'check-digits', key: 'has_digits' },
        { id: 'check-special', key: 'has_special' }
    ];
    
    checks.forEach(({ id, key }) => {
        const el = document.getElementById(id);
        if (charTypes[key]) {
            el.classList.add('active');
        } else {
            el.classList.remove('active');
        }
    });
}

function updateMetrics(data) {
    document.getElementById('metric-length').textContent = data.password_length;
    document.getElementById('metric-entropy').textContent = data.entropy;
    
    const crackTime = data.time_to_crack.time || 'N/A';
    document.getElementById('metric-crack-time').textContent = crackTime;
}

function updatePatterns(patterns) {
    const container = document.getElementById('pattern-list');
    container.innerHTML = '';
    
    Object.entries(patterns).forEach(([key, value]) => {
        const item = document.createElement('div');
        item.className = 'pattern-item';
        if (value) item.classList.add('active');
        item.textContent = patternDescriptions[key] || key;
        container.appendChild(item);
    });
}

function updateVulnerabilities(vulns) {
    const container = document.getElementById('vuln-list');
    container.innerHTML = '';
    
    if (vulns.length === 0) {
        const item = document.createElement('div');
        item.className = 'vuln-item';
        item.innerHTML = '<i class="fas fa-shield"></i> No vulnerabilities detected! Your password looks secure.';
        item.style.borderLeftColor = 'var(--success)';
        item.style.background = 'rgba(16, 185, 129, 0.08)';
        item.style.color = '#a7f3d0';
        container.appendChild(item);
        return;
    }
    
    vulns.forEach(vuln => {
        const item = document.createElement('div');
        item.className = 'vuln-item';
        item.innerHTML = `<i class="fas fa-warning"></i> ${vulnDescriptions[vuln] || vuln}`;
        container.appendChild(item);
    });
}

function updateRecommendations(recs) {
    const container = document.getElementById('rec-list');
    container.innerHTML = '';
    
    recs.forEach(rec => {
        const item = document.createElement('div');
        item.className = 'rec-item';
        item.innerHTML = `<i class="fas fa-check-circle"></i> ${rec}`;
        container.appendChild(item);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    passwordInput.focus();
    updateToggleBtnIcon();
});