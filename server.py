from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    model_type: str  # "ollama" or "openai"

class ChatResponse(BaseModel):
    answer: str
    vector_similarity: float
    semantic_similarity: float
    scoreBleu: float
    scoreRouge: float
    model_type: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Received request: model_type={request.model_type}, prompt length={len(request.prompt)}")
        
        # Import functions here to catch import errors
        try:
            from ollama import ask_ollama
            from OpenAiApi import ask_openai
        except ImportError as e:
            logger.error(f"Import error: {e}")
            raise HTTPException(status_code=500, detail=f"Import error: {str(e)}")
        
        if request.model_type == "ollama":
            logger.info("Calling ask_ollama function")
            result = ask_ollama(request.prompt)
        elif request.model_type == "openai":
            logger.info("Calling ask_openai function")
            result = ask_openai(request.prompt)
        else:
            raise HTTPException(status_code=400, detail="Invalid model_type. Use 'ollama' or 'openai'")
        
        logger.info(f"Function returned result type: {type(result)}, length: {len(result) if hasattr(result, '__len__') else 'N/A'}")
        
        # Check if result is the expected tuple format
        if not isinstance(result, (tuple, list)) or len(result) != 5:
            logger.error(f"Expected tuple/list of 5 elements, got: {result}")
            raise HTTPException(status_code=500, detail=f"Invalid result format from model function. Expected 5 elements, got {len(result) if hasattr(result, '__len__') else 'non-iterable'}")
        
        # Unpack the result tuple
        answer, vector_similarity, semantic_similarity, scoreBleu, scoreRouge = result
        
        logger.info(f"Successfully unpacked result: answer length={len(str(answer))}")
        logger.info(f"ROUGE score type: {type(scoreRouge)}, value: {scoreRouge}")
        
        # Handle ROUGE score - extract a single value from the dictionary
        if isinstance(scoreRouge, dict):
            # Try to get rougeL F-measure, fallback to rouge1, then average
            if 'rougeL' in scoreRouge:
                rouge_value = scoreRouge['rougeL'].fmeasure if hasattr(scoreRouge['rougeL'], 'fmeasure') else scoreRouge['rougeL']
            elif 'rouge1' in scoreRouge:
                rouge_value = scoreRouge['rouge1'].fmeasure if hasattr(scoreRouge['rouge1'], 'fmeasure') else scoreRouge['rouge1']
            else:
                # Take the first available score
                first_key = list(scoreRouge.keys())[0]
                rouge_value = scoreRouge[first_key].fmeasure if hasattr(scoreRouge[first_key], 'fmeasure') else scoreRouge[first_key]
        else:
            rouge_value = scoreRouge
        
        logger.info(f"Extracted ROUGE value: {rouge_value}")
        
        return ChatResponse(
            answer=str(answer),
            vector_similarity=float(vector_similarity),
            semantic_similarity=float(semantic_similarity),
            scoreBleu=float(scoreBleu),
            scoreRouge=float(rouge_value),
            model_type=request.model_type
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Chat API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    """Health check endpoint to test if imports work"""
    try:
        from ollama import ask_ollama
        from OpenAiApi import ask_openai
        return {"status": "healthy", "imports": "ok"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)