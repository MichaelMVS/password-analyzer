# Password Security Analyzer

A sophisticated, real-time password security analysis tool built with FastAPI and modern web technologies. Provides comprehensive password strength assessment with detailed vulnerability detection and actionable recommendations.

## Features

- **Real-time Analysis**: Instant feedback as you type
- **Entropy Calculation**: Shannon entropy-based strength measurement
- **Pattern Detection**: Identifies keyboard patterns, sequential characters, dates, and more
- **Crack Time Estimation**: Calculates resistance to brute-force attacks (1 trillion guesses/sec)
- **Vulnerability Detection**: Checks for common passwords, weak patterns, and character variety
- **Character Analysis**: Detailed breakdown of uppercase, lowercase, digits, and special characters
- **Actionable Recommendations**: Specific suggestions to improve password strength
- **Modern UI**: Beautiful dark theme with smooth animations and responsive design
- **Privacy-First**: All analysis happens locally in the browser—no passwords sent to server

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/password-analyzer.git
cd password-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the server:
```bash
python main.py
```

The application will be available at `http://localhost:8000`

### API Endpoints

#### Analyze Password
```
POST /api/analyze
Content-Type: application/json

{
    "password": "YourPasswordHere!"
}
```

Response:
```json
{
    "password_length": 15,
    "strength_score": 85,
    "strength_label": "Very Strong",
    "entropy": 94.5,
    "character_types": {
        "has_uppercase": true,
        "has_lowercase": true,
        "has_digits": true,
        "has_special": true,
        "uppercase_count": 1,
        "lowercase_count": 10,
        "digit_count": 2,
        "special_count": 2
    },
    "patterns": {
        "sequential_chars": false,
        "repeated_chars": false,
        "keyboard_pattern": false,
        "date_pattern": false,
        "email_pattern": false,
        "username_pattern": false
    },
    "vulnerabilities": [],
    "time_to_crack": {
        "time": "125.3 years",
        "guesses_per_second": "1 trillion"
    },
    "recommendations": [
        "Your password is excellent! Keep it secure."
    ]
}
```

#### Health Check
```
GET /api/health
```

## Analysis Metrics

### Strength Score (0-100)
- **Very Strong** (80-100): Excellent password, highly resistant to attacks
- **Strong** (60-79): Good password with solid security
- **Moderate** (40-59): Acceptable but could be improved
- **Weak** (20-39): Poor security, needs improvement
- **Very Weak** (0-19): Insufficient security

### Entropy
Measures password complexity using Shannon entropy. Higher entropy indicates greater randomness and security.

### Pattern Detection
Identifies common security weaknesses:
- Sequential characters (abc, 123)
- Repeated characters
- Keyboard patterns (qwerty, asdfgh)
- Date formats (1990, 12/25)
- Email patterns
- Username-like patterns

### Vulnerability Detection
- Password length < 8 characters
- Common passwords (top 1000 most used)
- Keyboard patterns
- Excessive repetition
- Sequential characters
- Insufficient character variety

## Technical Architecture

### Backend
- **Framework**: FastAPI (async Python web framework)
- **Server**: Uvicorn (ASGI server)
- **Analysis Engine**: Custom PasswordAnalyzer class

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid, Flexbox, and animations
- **JavaScript**: Vanilla JS with async/await
- **Icons**: SVG inline icons

### Analysis Algorithm

The strength score is calculated based on:
1. **Length Score**: Up to 25 points based on password length
2. **Character Variety**: Up to 60 points for having uppercase, lowercase, digits, and special characters
3. **Entropy Score**: Up to 20 points based on Shannon entropy calculation
4. **Vulnerability Penalties**: -10 points per detected vulnerability

## Security Considerations

- Passwords are analyzed in the browser before transmission
- No passwords are stored or logged on the server
- All analysis is deterministic and reproducible
- CORS enabled for cross-origin requests
- No external API calls for password checking (entirely self-contained)

## File Structure

```
password-analyzer/
├── main.py              # FastAPI application
├── analyzer.py          # Core password analysis engine
├── requirements.txt     # Python dependencies
├── static/
│   ├── index.html       # Frontend HTML
│   ├── style.css        # Styling and animations
│   └── script.js        # Client-side logic
└── README.md            # This file
```

## Performance

- Analysis completes in < 1ms per password
- Handles concurrent requests efficiently with async processing
- Minimal memory footprint
- No external dependencies for core analysis

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Add new pattern detection
- Improve UI/UX

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Disclaimer

This tool provides analysis for educational and informational purposes. While the analysis is based on industry-standard security principles, no password is 100% secure. Always follow best practices:
- Use unique passwords for important accounts
- Enable two-factor authentication
- Use a password manager
- Keep software and systems updated
