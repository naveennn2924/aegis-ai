from fastapi import FastAPI
from orchestration.workflow import run_workflow

app = FastAPI(title="AegisAI")

@app.post("/process")
def process_message(message: str):
    task = {"message": message}
    return run_workflow(task)
