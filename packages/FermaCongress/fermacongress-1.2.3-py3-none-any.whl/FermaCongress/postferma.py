import requests
import pandas as pd
from io import BytesIO
from datetime import datetime

def addtweets(client, dataframe: pd.DataFrame, CONGRESS_ID: str) -> None:

    # Input Validation
    # ------------------------------------------------------------
    if not client:
        raise ValueError("No login session found. Please call adminlogin(env_path).")
    
    if dataframe is None or dataframe.empty:
        raise ValueError("DataFrame is empty or None. No tweets to add.")
    
    if not CONGRESS_ID or not isinstance(CONGRESS_ID, str):
        raise ValueError("Invalid CONGRESS_ID provided.")

    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}/tweets/add"

    # Data Preparation and Processing
    # ------------------------------------------------------------
    buffer = BytesIO()
    dataframe.to_csv(buffer, index=False)
    buffer.seek(0)
    files = {"file": (f"tweets_{CONGRESS_ID}.csv", buffer, "text/csv")}

    # API Request and Response Handling
    # ------------------------------------------------------------
    try:
        response = requests.post(url, headers=client, files=files, timeout=120)
        response.raise_for_status()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: Tweets were successfully added...")
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Request timeout while adding tweets to Congress ID: {CONGRESS_ID}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to add tweets to Congress ID: {CONGRESS_ID}: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while adding tweets: {e}") from e
    
    finally:
        buffer.close()


def modifytweets(client, dataframe: pd.DataFrame, CONGRESS_ID: str) -> None:

    # Input Validation
    # ------------------------------------------------------------
    if not client:
        raise ValueError("No login session found. Please call adminlogin(env_path).")
    
    if dataframe is None or dataframe.empty:
        raise ValueError("DataFrame is empty or None. No tweets to modify.")
    
    if not CONGRESS_ID or not isinstance(CONGRESS_ID, str):
        raise ValueError("Invalid CONGRESS_ID provided.")


    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}/tweets/modify"
    
    # Data Preparation and Processing
    # ------------------------------------------------------------
    buffer = BytesIO()
    dataframe.to_csv(buffer, index=False)
    buffer.seek(0)
    files = {"file": (f"tweets_{CONGRESS_ID}.csv", buffer, "text/csv")}

    # API Request and Response Handling
    # ------------------------------------------------------------
    try:
        response = requests.post(url, headers=client, files=files, timeout=120)
        response.raise_for_status()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: Tweets were successfully modified for Congress ID: {CONGRESS_ID}")
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Request timeout while modifying tweets for Congress ID: {CONGRESS_ID}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to modify tweets for Congress ID: {CONGRESS_ID}: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while modifying tweets: {e}") from e

    finally:
        buffer.close()

def populatebuzz(client, CONGRESS_ID: str) -> None:

    # Input Validation
    # ------------------------------------------------------------
    if not client:
        raise ValueError("No login session found. Please call adminlogin(env_path).")
    
    if not CONGRESS_ID or not isinstance(CONGRESS_ID, str):
        raise ValueError("Invalid CONGRESS_ID provided.")


    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}/sessions/buzz_score/populate"

    try:
        response = requests.post(url, headers=client, timeout=120)
        response.raise_for_status()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: Buzz Score has been successfully triggered for the Congress ID: {CONGRESS_ID}")
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Request timeout while triggering buzz score for Congress ID: {CONGRESS_ID}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to trigger buzz score for Congress ID: {CONGRESS_ID}: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while triggering buzz score: {e}") from e