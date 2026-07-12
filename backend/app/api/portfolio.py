from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO
import uuid
from threading import Thread

from app.services.prediction_service import prediction_service

from app.core.job_manager import (jobs, create_job, update_progress, finish_job,
                                  cancel_job, is_cancelled)

router = APIRouter()

def process_portfolio(job_id: str, df: pd.DataFrame):
    results = []
    total = len(df)

    for i, (_, row) in enumerate(df.iterrows()):
        # Stop if cancelled
        if is_cancelled(job_id):
            print(f"Job {job_id} cancelled.")
            return

        prediction = prediction_service.predict(row.to_dict())

        results.append(prediction)

        update_progress(
            job_id,
            int((i + 1) / total * 100)
        )

    finish_job(
        job_id,
        {
            "total_businesses": len(results),
            "predictions": results,
        },
    )


@router.post("/portfolio")
async def portfolio_prediction(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file.",
        )

    contents = await file.read()

    df = pd.read_csv(
        StringIO(contents.decode("utf-8"))
    )

    job_id = str(uuid.uuid4())
    create_job(job_id)

    Thread(
        target=process_portfolio,
        args=(job_id, df),
        daemon=True,
    ).start()

    return {
        "job_id": job_id
    }


@router.get("/portfolio/status/{job_id}")
def portfolio_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return jobs[job_id]


@router.post("/portfolio/cancel/{job_id}")
def portfolio_cancel(job_id: str):
    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    cancel_job(job_id)

    return {
        "message": "Cancellation requested"
    }