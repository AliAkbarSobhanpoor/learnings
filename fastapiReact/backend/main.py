import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app:FastAPI = FastAPI()

class Fruit(BaseModel):
        name : str 
        
class Fruits(BaseModel):
    fruits: list[Fruit]
    

origins: list = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"fruits": []}

@app.get("/fruits", response_model=Fruits)
async def get_fruits() -> Fruits:
    return Fruits(fruits=memory_db["fruits"])


@app.post('/fruits', response_model=Fruit)
async def set_fruits(fruit: Fruit) -> Fruit:
    memory_db["fruits"].append(fruit)
    return fruit


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)