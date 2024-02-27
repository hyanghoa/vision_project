from typing import Union

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/inference")
async def inference(file: UploadFile):
    return {"filename": file.filename}
