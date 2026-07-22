from fastapi import FastAPI , HTTPException , Header , Depends , File , UploadFile , Form
import filetype
import anyio
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import secrets
import time
import asyncio

from image_pipeline.image_processing import image_processing
from image_pipeline.tessearct_ocr import getOcrResult
from llm_pipeline.llm_text_to_fiels import llm_field_mapping

app = FastAPI()

SESSION_TTL_SECONDS = 3600
UPLOAD_DIR = "UPLOAD_DIR"

origins=[
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Credentials(BaseModel):
    username : str
    password : str

load_dotenv()
cookiesDict = {}
uploadsDict = {}

async def verify_session(authorization : Annotated[str | None, Header()] = None):

    if authorization is not None and authorization.startswith("Bearer "):

        session_id = authorization.split(" ")[1]
        if session_id not in cookiesDict:
            raise HTTPException(status_code = 401 , detail="you are not authorized")

        current_time = time.time()
        if current_time - cookiesDict[session_id][1] > SESSION_TTL_SECONDS:
            raise HTTPException(status_code = 401 , detail="your session has expired please log in again")

        return cookiesDict[session_id][0]

    raise HTTPException(status_code=401 , detail="you are not authorized")


@app.post("/Credentials/")
async def sendCredentials(credentials : Credentials):

    async with httpx.AsyncClient() as client:
        payload = (credentials.username , credentials.password)
        url = str(os.getenv("base_url")) +"/me"
        r = await client.get(url , auth=payload)

        if(r.status_code != 200):
            raise HTTPException(status_code = int(r.status_code) , detail="Something went wrong")


        cookie =  r.cookies
        session_id = secrets.token_urlsafe()
        current_time = time.time()

        cookiesDict[session_id] =(cookie , current_time)



        return session_id


@app.get("/datasets")
async def fetchDatasets(session_cookie : Annotated[httpx.Cookies , Depends(verify_session)]):

    async with httpx.AsyncClient() as client:

        url = str(os.getenv("base_url")) + "/dataSets"
        r = await client.get(url , cookies=session_cookie ,params={"fields": "id,name"})

        if r.status_code != 200:
            raise HTTPException(status_code = r.status_code , detail="Something went wrong in fetching datasets" )

    return r.json()["dataSets"]

@app.post("/upload")
async def uploadForm(file : UploadFile = File(...) , dataset : str = Form(...) , session_cookie : httpx.Cookies = Depends(verify_session) ):
    CHUNK_SIZE = 1024 * 10
    MAX_SIZE = 1024 * 1024 * 10

    contents = b""
    while True:
        chunk = await file.read(CHUNK_SIZE)
        if chunk == b"": #it returns empty byte obj when nothing is left to reaad can also use not chunk here
                        # but to remember it does that i used this
            break

        contents += chunk

        if len(contents) > MAX_SIZE:
            raise HTTPException(status_code = 413 , detail="File Size is too large to process")
            # 413 = payload too large



    detected = filetype.guess(contents)

    if detected is None:
        raise HTTPException(status_code = 415 , detail = "Unsupported media type ")
        # 415 = unsupporeted media type
        # 400 = bad requeset


    ALLOWED_EXTENSIONS = ["jpg" , "png" , "pdf"]

    if detected.extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code = 415 , detail = "Unsupported Extension")

    upload_id = secrets.token_urlsafe()
    filename = upload_id + "." + detected.extension

    os.makedirs(UPLOAD_DIR , exist_ok=True)

    filepath = f"{UPLOAD_DIR}/{filename}"

    async with await anyio.open_file(filepath , "wb") as f:
        await f.write(contents)

    uploadsDict[upload_id] = (filepath , dataset , session_cookie)

    return upload_id

async def datasetMetadata(session_cookie : httpx.Cookies , dataset_name : str):

    async with httpx.AsyncClient() as client:
        url = str(os.getenv("base_url")) + "/dataSets"
        query_params= {
            "filter":f"name:eq:{dataset_name}",
            "fields":"id,name,dataSetElements[dataElement[id,name,valueType]]"
        }

        r = await client.get(url , cookies = session_cookie , params=query_params)

        if r.status_code != 200:
            raise HTTPException(status_code = int(r.status_code) , detail = "Failed to fetch dataset metadata")

        return r.json()["dataSets"][0]["dataSetElements"]


@app.post("/field_mapping/{upload_id}")
async def fieldMapping(session_cookie : Annotated[httpx.Cookies , Depends(verify_session)] , upload_id : str):

    (file_path , dataset_name) = (uploadsDict[upload_id][0] , uploadsDict[upload_id][1])



    output_path =  await asyncio.to_thread(image_processing , file_path)
    text_content = await asyncio.to_thread(getOcrResult , output_path)
    field_list = await datasetMetadata(session_cookie , dataset_name)

    id_to_name = {}
    for entry in field_list:
        id_to_name[entry["dataElement"]["id"]] = entry["dataElement"]["name"]


    try:
        field_mapping = await llm_field_mapping(text_content , field_list)

        for mapping in field_mapping:
            mapping["name"] = id_to_name[mapping["dataElementId"]]

        return field_mapping


    except KeyError:
        raise HTTPException(status_code = 400  , detail = "llm failed to map fields correctly . Please Upload clear photo ")

    except Exception as e:
        raise HTTPException(status_code = int(e.args[0]) , detail = "Failed to connect to llm")







@app.delete("/logout/{session_id}")
def logout(session_id : str):

    removed = cookiesDict.pop(session_id , None)

    if removed is None:
        return {"detail":"session not found"}

    return {"detail" : "session deleted"}
