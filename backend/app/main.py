from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .lexer.implementations import GenericLexer
from .services.normalization import Normalizer
from .services.similarity import SimilarityEngine

app = FastAPI(title="Lexicode API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    language: str
    code: str

class CompareRequest(BaseModel):
    language: str
    code_a: str
    code_b: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Lexicode API is healthy"}

@app.post("/api/analyze")
def analyze_code(req: AnalyzeRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Empty code")
    
    lexer = GenericLexer(req.language)
    res = lexer.analyze(req.code)
    
    normalized = Normalizer.normalize(res.tokens)
    
    return {
        "tokens": [t.dict() for t in res.tokens],
        "total_tokens": res.total_tokens,
        "normalized_tokens": normalized,
        "errors": [e.dict() for e in res.errors] if hasattr(res, 'errors') and res.errors else []
    }

@app.post("/api/compare")
def compare_code(req: CompareRequest):
    if not req.code_a or not req.code_b:
        raise HTTPException(status_code=400, detail="Empty code")
        
    lexer = GenericLexer(req.language)
    res_a = lexer.analyze(req.code_a)
    res_b = lexer.analyze(req.code_b)
    
    norm_a = Normalizer.normalize(res_a.tokens)
    norm_b = Normalizer.normalize(res_b.tokens)
    
    sim = SimilarityEngine.compare(norm_a, norm_b)
    return sim
