from loguru import logger
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.appeal_operations.router import router as router_operations

app = FastAPI(
    title="Механик"
)
app.mount("/result_imgs", StaticFiles(directory="img"), name="img")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router_operations
)

@app.get("/", status_code = 200)
def hello_app():
    return {"Hello!"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)