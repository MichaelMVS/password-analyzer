const passwordInput = document.getElementById('password-input');
const toggleBtn = document.getElementById('toggle-visibility');
const analyzeBtn = document.getElementById('analyze-btn');
const resultsSection = document.getElementById('results-section');

const vulnDescriptions = {
    'too_short': 'Password is too short for adequate security (minimum 8 characters)',
    'suboptimal_length': 'Password length could be improved for better security (aim for 16+ characters)',
    'common_password': 'This password appears in common breach databases',
    'keyboard_pattern': 'Contains sequential keyboard patterns (reduced entropy)',
    'excessive_repetition': 'Excessive character repetition (weak randomness)',
    'sequential_characters': 'Contains sequential character patterns (ABC, 123)',
    'insufficient_character_variety': 'Lacks character class diversity',
    'low_entropy': 'Insufficient entropy for strong security',
    'dictionary_words': 'Contains common dictionary words'
};

const strengthDescriptions = {
    'Very Strong': 'Excellent entropy and resistance to brute-force attacks',
    'Strong': 'Good entropy with strong resistance to modern attack vectors',
    'Moderate': 'Acceptable entropy but vulnerable to sophisticated attacks',
    'Weak': 'Low entropy; vulnerable to dictionary and brute-force attacks',
    'Very Weak': 'Critical entropy deficiency; easily compromised'
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

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        displayResults(data);
    } catch (error) {
        console.error('Full error:', error);
        alert('Error analyzing password: ' + error.message);
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
    updateAttackScenarios(data.time_to_crack, data.attack_scenarios);
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
    document.getElementById('metric-length').textContent = data.password_length + ' chars';
    document.getElementById('metric-entropy').textContent = data.effective_entropy + ' bits';
    
    const crackTime = data.time_to_crack.offline_attack || 'N/A';
    document.getElementById('metric-crack-time').textContent = crackTime;
}

function updateVulnerabilities(vulns) {
    const container = document.getElementById('vuln-list');
    container.innerHTML = '';
    
    if (vulns.length === 0) {
        const item = document.createElement('div');
        item.className = 'vuln-item';
        item.innerHTML = '<i class="fas fa-check-circle"></i> No critical vulnerabilities detected!';
        item.style.borderLeftColor = 'var(--success)';
        item.style.background = 'rgba(16, 185, 129, 0.1)';
        item.style.color = '#a7f3d0';
        container.appendChild(item);
        return;
    }
    
    vulns.forEach(vuln => {
        const item = document.createElement('div');
        item.className = 'vuln-item';
        const description = vulnDescriptions[vuln] || vuln;
        item.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${description}`;
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

function updateAttackScenarios(cracktimes, scenarios) {
    const container = document.getElementById('attack-scenarios');
    
    if (!container) {
        return;
    }
    
    container.innerHTML = '';
    
    const attackLabels = {
        'online_attack': '<i class="fas fa-globe"></i> Online Attack (Rate Limited)',
        'offline_attack': '<i class="fas fa-server"></i> Offline Attack (Brute Force)',
        'gpu_attack': '<i class="fas fa-microchip"></i> GPU Attack',
        'specialized_attack': '<i class="fas fa-rocket"></i> Specialized Hardware'
    };
    
    for (const [key, time] of Object.entries(cracktimes)) {
        const item = document.createElement('div');
        item.className = 'scenario-item';
        const label = attackLabels[key] || key;
        item.innerHTML = `<div class="scenario-label">${label}</div><div class="scenario-time">${time}</div>`;
        container.appendChild(item);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    passwordInput.focus();
    updateToggleBtnIcon();
});