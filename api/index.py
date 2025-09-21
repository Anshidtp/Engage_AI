# from app.main import app
# from mangum import Mangum
# handler = Mangum(app, lifespan="off")

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI on Vercel!"}

# Export the handler Vercel looks for
handler = Mangum(app)
