from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO

from app.services.prediction_service import prediction_service

router = APIRouter()


@router.post("/portfolio")
async def portfolio_prediction(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file."
        )

    contents = await file.read()

    df = pd.read_csv(
        StringIO(contents.decode("utf-8"))
    )

    results = []

    for _, row in df.iterrows():

        prediction = prediction_service.predict(
            row.to_dict()
        )

        results.append(prediction)

    return {
        "total_businesses": len(results),
        "predictions": results
    }