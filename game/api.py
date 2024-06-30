from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import settings

app = FastAPI()
origins = [
    "http://localhost:5000"
]

app.add_middleware(
                   CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.post("/p1")
def phase_one_endpoint_supplier():
    # print(p1_input)
    settings.ENDPOINT_RESPONSE = "hello"
    print("hello")
    return "hello"
