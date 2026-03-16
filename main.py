import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routes import router

app = FastAPI()

@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def root():
    # Simple dark‑theme landing page with endpoint list
    endpoints = [
        {"method": "GET", "path": "/health", "desc": "Health check"},
        {"method": "POST", "path": "/plan", "desc": "Generate batch plan from idea"},
        {"method": "POST", "path": "/insights", "desc": "Get AI insights for a batch"},
        {"method": "GET", "path": "/batches", "desc": "List saved batches"},
        {"method": "GET", "path": "/batches/{batch_id}", "desc": "Get batch details"},
        {"method": "POST", "path": "/batches/{batch_id}/export", "desc": "Export checklist"},
    ]
    rows = "".join(
        f"<tr><td style='padding:4px 8px;'>{e['method']}</td><td style='padding:4px 8px;'>{e['path']}</td><td style='padding:4px 8px;'>{e['desc']}</td></tr>"
        for e in endpoints
    )
    html = f"""
    <html><head><title>Creator Batch Studio API</title></head>
    <body style='background:#111;color:#eee;font-family:Arial,sans-serif;padding:2rem;'>
        <h1 style='color:#4fd1c5;'>Creator Batch Studio</h1>
        <p>Batch‑plan, shoot, and publish short‑form videos in seconds.</p>
        <h2>Available Endpoints</h2>
        <table style='border-collapse:collapse;width:100%;max-width:800px;'>
            <thead><tr style='background:#222;'><th>Method</th><th>Path</th><th>Description</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
        <p style='margin-top:2rem;'>
            <a href='/docs' style='color:#4fd1c5;margin-right:1rem;'>OpenAPI Docs</a>
            <a href='/redoc' style='color:#4fd1c5;'>ReDoc</a>
        </p>
        <footer style='margin-top:3rem;font-size:0.9rem;color:#777;'>
            Tech Stack: FastAPI 0.115 • PostgreSQL • DigitalOcean Serverless Inference • Open‑source backend
        </footer>
    </body></html>
    """
    return html
