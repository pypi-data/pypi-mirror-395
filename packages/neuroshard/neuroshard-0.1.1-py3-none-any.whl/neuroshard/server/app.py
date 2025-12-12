import os
from fastapi import FastAPI, HTTPException, Request, Response
import uvicorn

app = FastAPI()

# Simple storage for the server (can be replaced with S3 later)
STORAGE_DIR = "server_storage"
OBJECTS_DIR = os.path.join(STORAGE_DIR, "objects")
MANIFESTS_DIR = os.path.join(STORAGE_DIR, "manifests")

os.makedirs(OBJECTS_DIR, exist_ok=True)
os.makedirs(MANIFESTS_DIR, exist_ok=True)

def get_object_path(obj_hash: str):
    return os.path.join(OBJECTS_DIR, obj_hash[:2], obj_hash)

@app.head("/blocks/{obj_hash}")
async def has_block(obj_hash: str):
    path = get_object_path(obj_hash)
    if os.path.exists(path):
        return Response(status_code=200)
    raise HTTPException(status_code=404, detail="Block not found")

@app.put("/blocks/{obj_hash}")
async def upload_block(obj_hash: str, request: Request):
    path = get_object_path(obj_hash)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    data = await request.body()
    with open(path, "wb") as f:
        f.write(data)
    return {"status": "ok"}

@app.get("/blocks/{obj_hash}")
async def download_block(obj_hash: str):
    path = get_object_path(obj_hash)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Block not found")
    with open(path, "rb") as f:
        return Response(content=f.read(), media_type="application/octet-stream")

@app.put("/manifests/{manifest_hash}")
async def upload_manifest(manifest_hash: str, request: Request):
    path = os.path.join(MANIFESTS_DIR, manifest_hash)
    data = await request.body()
    with open(path, "wb") as f:
        f.write(data)
    return {"status": "ok"}

@app.get("/manifests/{manifest_hash}")
async def download_manifest(manifest_hash: str):
    path = os.path.join(MANIFESTS_DIR, manifest_hash)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Manifest not found")
    with open(path, "rb") as f:
        return Response(content=f.read(), media_type="application/json")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
