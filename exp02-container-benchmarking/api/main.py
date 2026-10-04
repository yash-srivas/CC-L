from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI(
    title="Container vs VM Performance Benchmarking API",
    description="Lightweight endpoints for profiling CPU, memory, and HTTP response latencies.",
    version="1.0.0"
)

@app.get("/health")
def health() -> Dict[str, Any]:
    """Non-blocking diagnostic health probe."""
    return {"status": "healthy", "service": "performance-benchmark-api"}

@app.get("/compute")
def compute() -> Dict[str, Any]:
    """CPU-bound calculation: iterative sum-of-squares."""
    total = sum(i * i for i in range(1_000_000))
    return {"status": "success", "result": total}

@app.get("/memory")
def memory() -> Dict[str, Any]:
    """Memory-bound allocation: dynamic 1,000,000 integer array creation."""
    payload = [i for i in range(1_000_000)]
    return {"status": "success", "elements": len(payload)}
