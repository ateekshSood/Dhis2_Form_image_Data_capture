from fastapi import FastAPI , HTTPException , Header , Depends
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os 
from dotenv import load_dotenv
import secrets
import time

app = FastAPI()

SESSION_TTL_SECONDS = 3600

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
            
    
        
@app.delete("/logout/{session_id}")
def logout(session_id : str):

    removed = cookiesDict.pop(session_id , None)

    if removed is None:
        return {"detail":"session not found"}
        
    return {"detail" : "session deleted"} 