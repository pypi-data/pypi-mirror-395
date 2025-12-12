from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .rag_service import run_query


app = FastAPI(title="RAG Example API", version="1.0.0")


class QueryRequest(BaseModel):
    query: str
    output_mode: str = Query("answer", enum=["answer", "full"])


@app.post("/rag/query")
async def rag_query(request: QueryRequest):
    try:
        result = await run_query(request.query, request.output_mode)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": traceback.format_exc()},
        )


@app.get("/healthz")
def health():
    return {"status": "ok"}
