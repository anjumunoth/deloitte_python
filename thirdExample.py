from fastapi import FastAPI
import httpx
import asyncio

app = FastAPI()

@app.get("/users/")
async def get_users():
    async with httpx.AsyncClient(timeout=5) as client:
        # parallel calls to microservices
        user_req = client.get(f"https://jsonplaceholder.typicode.com/users")
        
        resp_user = await asyncio.gather(user_req)
     
    return {
        "users": resp_user[0].json()
        
    }


