from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TOTAL_PATIENTS = 140
USER_BUDGET = {"budget": 10.0}

class QueryRequest(BaseModel):
    condition: str
    epsilon: float

@app.get("/")
def home():
    return {"status": "DP Engine Running"}

@app.get("/budget")
def get_budget():
    return {"remaining_budget": round(USER_BUDGET["budget"], 2)}

@app.post("/query")
def run_query(req: QueryRequest):
    if USER_BUDGET["budget"] < req.epsilon:
        raise HTTPException(status_code=403, detail="Privacy Budget Exhausted! Query Denied.")

    noise = np.random.laplace(0, 1.0 / req.epsilon)
    noisy_count = max(0, int(round(TOTAL_PATIENTS + noise)))

    USER_BUDGET["budget"] -= req.epsilon

    return {
        "status": "success",
        "result_count": noisy_count,
        "remaining_budget": round(USER_BUDGET["budget"], 2)
    }

@app.post("/reset")
def reset_budget():
    USER_BUDGET["budget"] = 10.0
    return {"status": "Budget reset to 10.0"}
