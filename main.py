from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import PasswordAnalyzer
import traceback
import json

app = FastAPI(title="Password Entropy Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = PasswordAnalyzer()

class PasswordRequest(BaseModel):
    password: str

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/analyze")
async def analyze_password(request: PasswordRequest):
    try:
        if not request.password:
            return JSONResponse(
                status_code=400,
                content={"error": "Password cannot be empty"}
            )
        
        result = analyzer.analyze(request.password)
        
        if result is None:
            return JSONResponse(
                status_code=500,
                content={"error": "Analysis returned no result"}
            )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error in analyze_password: {str(e)}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )

@app.get("/")
async def root():
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Could not load page: {str(e)}"}
        )

try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
