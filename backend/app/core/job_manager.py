from threading import Lock

jobs = {}
lock = Lock()


def create_job(job_id):
    with lock:
        jobs[job_id] = {
            "status": "running",
            "progress": 0,
            "result": None,
            "cancelled": False,
        }


def cancel_job(job_id):
    with lock:
        if job_id in jobs:
            jobs[job_id]["cancelled"] = True


def update_progress(job_id, progress):
    with lock:
        if job_id in jobs:
            jobs[job_id]["progress"] = progress


def finish_job(job_id, result):
    with lock:
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result


def is_cancelled(job_id):
    return jobs[job_id]["cancelled"]