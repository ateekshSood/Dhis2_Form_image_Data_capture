from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
import httpx
import os 
from dotenv import load_dotenv
import secrets
import time

app = FastAPI()

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
        
@app.delete("/logout/{session_id}")
def logout(session_id : str):

    removed = cookiesDict.pop(session_id , None)

    if removed is None:
        return {"detail":"session not found"}
        
    return {"detail" : "session deleted"} 