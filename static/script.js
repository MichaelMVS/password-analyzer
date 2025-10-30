const passwordInput = document.getElementById('password-input');
const toggleBtn = document.getElementById('toggle-visibility');
const analyzeBtn = document.getElementById('analyze-btn');
const resultsSection = document.getElementById('results-section');

const vulnDescriptions = {
    'too_short': 'Password is shorter than 8 characters',
    'common_password': 'This is a commonly used password',
    'keyboard_pattern': 'Contains keyboard patterns',
    'excessive_repetition': 'Has excessive repeated characters',
    'sequential_characters': 'Contains sequential characters',
    'insufficient_character_variety': 'Needs more character variety'
};

const strengthDescriptions = {
    'Very Strong': 'Excellent password with high security',
    'Strong': 'Good password with solid security',
    'Moderate': 'Acceptable but could be improved',
    'Weak': 'Poor security, needs improvement',
    'Very Weak': 'Very weak security'
};

toggleBtn.addEventListener('click', () => {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
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

analyzeBtn.addEventListener('click', async () => {
    const password = passwordInput.value;
    
    if (!password) {
        alert('Please enter a password to analyze');
        return;
    }
    
    analyzeBtn.disabled = true;
    analyzeBtn.style.opacity = '0.7';
    
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
        alert('Error analyzing password. Please try again.');
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = '1';
    }
});

passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        analyzeBtn.click();
    }
});

function displayResults(data) {
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    updateStrengthMeter(data.strength_score, data.strength_label);
    updateCharacterTypes(data.character_types);
    updateMetrics(data);
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

function updateVulnerabilities(vulns) {
    const container = document.getElementById('vuln-list');
    container.innerHTML = '';
    
    if (vulns.length === 0) {
        const item = document.createElement('div');
        item.className = 'vuln-item';
        item.innerHTML = '<i class="fas fa-check-circle"></i> No issues found! Your password looks good.';
        item.style.borderLeftColor = 'var(--success)';
        item.style.background = 'rgba(16, 185, 129, 0.1)';
        item.style.color = '#a7f3d0';
        container.appendChild(item);
        return;
    }
    
    vulns.forEach(vuln => {
        const item = document.createElement('div');
        item.className = 'vuln-item';
        item.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${vulnDescriptions[vuln] || vuln}`;
        container.appendChild(item);
    });
}

function updateRecommendations(recs) {
    const container = document.getElementById('rec-list');
    container.innerHTML = '';
    
    recs.forEach(rec => {
        const item = document.createElement('div');
        item.className = 'rec-item';
        item.innerHTML = `<i class="fas fa-check"></i> ${rec}`;
        container.appendChild(item);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    passwordInput.focus();
    updateToggleBtnIcon();
});