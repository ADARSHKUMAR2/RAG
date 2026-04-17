from fastapi import FastAPI, Query, HTTPException
from client.rq_client import queue
from queues.worker import process_query

app = FastAPI()

@app.get('/')
def root():
    return {"status": 'Server is up and running'}

@app.post('/chat')
def chat(query: str = Query(..., description="The chat query of user")):
    # Put the job in the queue
    job = queue.enqueue(process_query, query)
    return {"status": "queued", "job_id": job.id}

@app.get('/job_status')
def get_result(job_id: str = Query(..., description="Job Id")):
    job = queue.fetch_job(job_id=job_id)
    
    # 1. Check if the job even exists
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    # 2. Check the status and safely get the result (No parentheses!)
    if job.is_finished:
        return {"status": "completed", "result": job.result}
    elif job.is_failed:
        return {"status": "failed", "error": "The AI worker crashed."}
    else:
        return {"status": job.get_status(), "message": "Still processing..."}