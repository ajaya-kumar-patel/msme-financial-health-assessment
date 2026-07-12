import requests

# FastAPI Backend URL
BASE_URL = "https://msme-healthai-api.onrender.com"

# Prediction Endpoint
PREDICT_URL = f"{BASE_URL}/predict"


def predict(customer_data: dict):
    """
    Send customer data to FastAPI and return prediction results.

    Parameters
    ----------
    customer_data : dict
        MSME customer information.

    Returns
    -------
    dict
        Prediction response from the backend.
    """

    try:
        response = requests.post(
            PREDICT_URL,
            json=customer_data,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": (
                "Unable to connect to the backend. "
                "Please make sure the FastAPI server is running."
            )
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "Request timed out."
        }

    except requests.exceptions.HTTPError:
        return {
            "success": False,
            "message": response.text
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }