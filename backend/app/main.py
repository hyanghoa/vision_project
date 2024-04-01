from typing import Union

import aiohttp
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.post("/inference")
async def inference(file: UploadFile):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector()
    ) as session:

        url = "http://backend_model:8080/predictions/yolov8_cls"
        files = {"data": file.file.read()}

        async with session.post(url, data=files) as response:
            return {"response": await response.text()}  