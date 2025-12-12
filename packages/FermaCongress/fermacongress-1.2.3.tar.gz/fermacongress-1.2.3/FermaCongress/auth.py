import os
import base64
import requests
from datetime import datetime
from dotenv import dotenv_values
from typing import Dict, Optional, Literal

# ---------------------------------------------------------------------
# Admin Portal Login
# ---------------------------------------------------------------------

ADMIN_LOGIN_CACHE: Dict[tuple, Dict[str, str]] = {}

def adminlogin(env_path: str, format: Optional[Literal["ENCODED"]] = None) -> Dict[str, str]:
    """
    Authenticate with Ferma Admin Portal and return authorization headers.
    
    Args:
        env_path: Path to .env file containing credentials
        format: If "ENCODED", credentials are base64-decoded
        
    Returns:
        Dictionary with Authorization header
    """
    if not os.path.isfile(env_path):
        raise FileNotFoundError(f".env file not found at: {env_path}")
    
    creds = dotenv_values(env_path)

    # Extract and decode credentials
    if format == "ENCODED":
        username_raw = creds.get("FERMA_USERNAME", "")
        password_raw = creds.get("FERMA_PASSWORD", "")
        
        if not username_raw or not password_raw:
            raise ValueError("Missing FERMA_USERNAME or FERMA_PASSWORD in env file")
        
        try:
            username = base64.b64decode(username_raw).decode("utf-8")
            password = base64.b64decode(password_raw).decode("utf-8")

        except Exception as e:
            raise ValueError(f"Failed to decode credentials: {e}")
    else:
        username = creds.get("FERMA_USERNAME")
        password = creds.get("FERMA_PASSWORD")

        if not username or not password:
            raise ValueError("Missing FERMA_USERNAME or FERMA_PASSWORD in env file")

    cache_key = (username, password)
    if cache_key in ADMIN_LOGIN_CACHE:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}]: (Cache) Ferma Admin Portal Login successful")
        return ADMIN_LOGIN_CACHE[cache_key]

    try:
        resp = requests.post(
            "https://admin-portal.ferma.ai/users/login",
            json={"username": username, "password": password, "persist": 1},
            timeout=10
        )
    except requests.RequestException as e:
        raise RuntimeError(f"Admin login failed: network error: {e}")

    if resp.status_code == 401:
        try:
            msg = resp.json().get("message") or resp.json().get("error")
        except ValueError:
            msg = resp.text or "Unauthorized"
        raise RuntimeError(f"Admin login failed (401 Unauthorized): {msg}")

    if resp.status_code != 200:
        raise RuntimeError(f"Admin login failed: HTTP {resp.status_code}: {resp.text}")

    try:
        data = resp.json()
    except ValueError:
        raise RuntimeError("Admin login failed: response not valid JSON")

    token = data.get("accessToken")
    if not token:
        msg = data.get("message") or data.get("error") or resp.text
        raise RuntimeError(f"Admin login failed: {msg}")

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0"
    }

    ADMIN_LOGIN_CACHE[cache_key] = headers
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}]: Ferma Admin Portal Login successful")
    return headers


# ---------------------------------------------------------------------
# Support Portal Login
# ---------------------------------------------------------------------

session = None

def supportlogin(env_path: str) -> requests.Session:
    """
    Authenticate with Ferma support portal and return session.
    
    Args:
        env_path: Path to .env file containing credentials
        
    Returns:
        requests.Session: Authenticated session object
    """
    global session
    
    if not os.path.isfile(env_path):
        raise FileNotFoundError(f".env file not found at: {env_path}")
    
    # Load Credentials
    creds = dotenv_values(env_path)
    username = creds.get("FERMA_USERNAME")
    password = creds.get("FERMA_PASSWORD")
    
    # Validate Credentials
    if not username or not password:
        raise ValueError("Missing FERMA_USERNAME or FERMA_PASSWORD in env file")

    # Initialize Session
    session = requests.Session()

    # Set headers on sessions
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://support.ferma.ai/main/login"
    })

    try:
        session.get("https://support.ferma.ai/main/login", timeout=30)

        login_data = {"username": username, "password": password}
    
        resp = session.post("https://support.ferma.ai/main/validate", data=login_data, timeout=30)
    
        # Check response
        resp.raise_for_status()  # Raises HTTPError for 4xx/5xx status codes
        
        # Verify successful login
        if "Invalid credentials" in resp.text or "Error" in resp.text:
            raise Exception(f"[{datetime.now():%Y-%m-%d %H:%M:%S}]: Login failed - Invalid credentials")
        
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}]: Ferma Support Portal Login successful")
        return session
        
    except requests.exceptions.Timeout:
        raise Exception(f"[{datetime.now():%Y-%m-%d %H:%M:%S}]: Login failed - Request timeout")
    except requests.exceptions.RequestException as e:
        raise Exception(f"[{datetime.now():%Y-%m-%d %H:%M:%S}]: Login failed - {str(e)}")