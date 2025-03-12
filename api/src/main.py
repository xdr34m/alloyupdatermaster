from fastapi import FastAPI, Header, HTTPException,UploadFile,File,Form
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from starlette.middleware.gzip import GZipMiddleware
from jinja2 import Template
import os,logging,sys,hashlib,signal,uvicorn,io,redis, time
from utils import *

redis_host=os.getenv("REDIS_HOST")
redis_port=os.getenv("REDIS_PORT")
data_path=os.getenv("DATA_PATH")
#r = aioredis.Connection(host=redis_host, port=redis_port, db=0)
FileBasePath="../files"
DirectoriesBasePath="../dirs"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Starting up...")

# Sync Redis connection (with redis-py)
def create_redis_connection():
    try:
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        return redis_client
    except redis.ConnectionError:
        logging.error("Connection failed. Retrying in 3 seconds...")
        time.sleep(3)
        return create_redis_connection()  # Retry connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to handle Redis connection."""
    app.state.redis = await create_redis_connection()
    print("✅ Redis connection established")
    
    yield  # Application runs here
    
    await app.state.redis.close()
    print("❌ Redis connection closed")

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get('/ready')  # Healthcheck
async def receive_healthcheck():
    return "ready"

@app.get('/test')
async def test():
    return get_all_files_in_matching_dirs(data_path,"testfolder")
    return "ready"

@app.get('/tools/update_redis')
async def update_redis():
    """Set a key-value pair in Redis."""


@app.get("/download-file/")
async def download_file(name: str = "User", age: int = 25):
    # Render template with Jinja2
    template = Template(TEMPLATE_STRING)
    rendered_content = template.render(name=name, age=age)

    # Create an in-memory file
    file_stream = io.BytesIO(rendered_content.encode("utf-8"))

    # Serve the file as an attachment
    return StreamingResponse(file_stream, media_type="text/plain", headers={
        "Content-Disposition": "attachment; filename=output.txt"
    })

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)