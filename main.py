from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import PasswordAnalyzer
import os

app = FastAPI(title="Password Security Analyzer", version="1.0.0")

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
    if not request.password:
        return JSONResponse(
            status_code=400,
            content={"error": "Password cannot be empty"}
        )
    
    result = analyzer.analyze(request.password)
    return JSONResponse(content=result)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
