from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from .similarity import SimilarityEngine
from ..lexer.implementations import GenericLexer
from .normalization import Normalizer

router = APIRouter()

class BatchCompareRequest(BaseModel):
    language: str
    files: List[Dict[str, str]] # [{'name': 'file1', 'code': '...'}, ...]

@router.post("/api/batch/compare")
def batch_compare(req: BatchCompareRequest):
    if len(req.files) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 files")
        
    lexer = GenericLexer(req.language)
    processed = []
    for f in req.files:
        res = lexer.analyze(f['code'])
        norm = Normalizer.normalize(res.tokens)
        processed.append({"name": f['name'], "norm": norm, "count": res.total_tokens})
        
    matrix = {}
    for i in range(len(processed)):
        matrix[processed[i]['name']] = {}
        for j in range(len(processed)):
            if i == j:
                matrix[processed[i]['name']][processed[j]['name']] = 100.0
            else:
                sim = SimilarityEngine.compare(processed[i]['norm'], processed[j]['norm'])
                matrix[processed[i]['name']][processed[j]['name']] = sim['similarity']
                
    return {"matrix": matrix}
