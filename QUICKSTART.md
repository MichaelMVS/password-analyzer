# Quick Start Guide

## Prerequisites
- Python 3.8+
- pip

## Installation & Setup (Windows)

```powershell
cd password-analyzer

pip install -r requirements.txt
```

## Running the Application

```powershell
python main.py
```

You'll see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

## Testing

In another terminal, run:
```powershell
python test_api.py
```

You should see analysis results for a test password.

## API Usage

### Analyze a Password
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d "{\"password\": \"YourPassword123!\"}"
```

### Response Format
```json
{
  "password_length": 15,
  "strength_score": 85,
  "strength_label": "Very Strong",
  "entropy": 94.5,
  "character_types": {...},
  "patterns": {...},
  "vulnerabilities": [],
  "time_to_crack": {...},
  "recommendations": [...]
}
```

## Features

✅ Real-time password analysis  
✅ Entropy calculation  
✅ Pattern detection  
✅ Vulnerability detection  
✅ Crack time estimation  
✅ Modern dark UI  
✅ Privacy-first (local analysis)  

## Troubleshooting

**Port 8000 already in use?**
```powershell
netstat -ano | findstr :8000
```

**Want to use a different port?**
Edit `main.py` line 34:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)
```

## File Structure
```
password-analyzer/
├── main.py                 # FastAPI server
├── analyzer.py             # Analysis engine
├── test_api.py             # API test script
├── requirements.txt        # Dependencies
├── static/
│   ├── index.html         # Frontend
│   ├── style.css          # Styling
│   └── script.js          # Client logic
├── README.md              # Documentation
└── QUICKSTART.md          # This file
```
