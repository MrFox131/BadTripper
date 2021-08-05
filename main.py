from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def get_url(url: str):
    return JSONResponse(
        status_code=200,
        content={
            "hello": url
        }
    )
