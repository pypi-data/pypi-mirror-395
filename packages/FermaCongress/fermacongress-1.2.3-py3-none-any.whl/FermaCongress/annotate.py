import json
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from io import StringIO, BytesIO
from typing import Optional, List, Dict, Any

IST_OFFSET = timedelta(hours=5, minutes=30)

def format_timestamp(dt_str: Optional[str] = None, utc_time: bool = True) -> str:
    if dt_str is None:
        now_utc = datetime.utcnow()
        now_ist = now_utc + IST_OFFSET
        return now_ist.strftime('%Y-%m-%d %H:%M:%S')
    
    if utc_time:
        try:
            utc_dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
            ist_dt = utc_dt + IST_OFFSET
            return ist_dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return dt_str
        except Exception:
            return dt_str
    return dt_str

def annotate(
    client,
    input_df: pd.DataFrame,
    custom_needles_df: Optional[pd.DataFrame] = None,
    needles: List[int] = None,
    entities: Optional[Dict[str, Any]] = None,
    long_table: bool = True,
    poll_interval: int = 30,
    max_wait: int = 1200
) -> pd.DataFrame:

    """
    Performing Annotation on the data by using Ferma AI Annotation API - Knowledge Base
    
    Args:
        client: Authenticated session client
        input_df: DataFrame containing input data with required 'id' column
        custom_needles_df: Optional DataFrame with custom needle configurations
        needles: List of two integers [kb_status, nct_status] where 1=enabled, 0=disabled
        entities: Optional dictionary of entity configurations
        long_table: If True, return long format; if False, return pivot format
        poll_interval: Seconds between progress checks (default: 30)
        max_wait: Maximum seconds to wait for completion (default: 1200)
    
    Returns:
        pd.DataFrame: Annotated results in requested format
    """

    # ============================================================================
    # SECTION 1: Input Validation
    # ============================================================================

    if client is None:
        raise Exception("Client not initialized. Call supportlogin() first & try again.")

    if not isinstance(input_df, pd.DataFrame):
        raise ValueError("`input_df` must be a pandas DataFrame")
    
    if input_df.empty:
        raise ValueError("`input_df` cannot be empty")
    
    if 'id' not in input_df.columns:
        raise ValueError("Input DataFrame must contain 'id' column")

    # Default Needles: [kb_status: 1, nct_status: 1]
    if needles is None:
        needles = [1, 1]

    if not isinstance(needles, list) or len(needles) != 2:
        raise ValueError("needles must be a list of two integers: [kb_status, nct_status]")
    
    if not all(isinstance(n, int) and n in [0, 1] for n in needles):
        raise ValueError("Each needle value must be 0 or 1")
    
    if poll_interval < 5:
        raise ValueError("poll_interval must be at least 5 seconds")
    
    if max_wait < poll_interval:
        raise ValueError("max_wait must be greater than poll_interval")


    # ============================================================================
    # SECTION 2: Prepare Request Headers
    # ============================================================================
  
    try:
        cookies_dict = client.cookies.get_dict()
        if not cookies_dict:
            raise ValueError("Client has no cookies. Authentication may have failed.")
        
        cookie_header = "; ".join(f"{k}={v}" for k, v in cookies_dict.items())
        download_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://support.ferma.ai/annotation/progress-tracker",
            "Cookie": cookie_header
        }
    except Exception as e:
        raise Exception(f"Failed to prepare request headers: {str(e)}")


    # ============================================================================
    # SECTION 3: Configure Needles
    # ============================================================================

    kb_status, nct_status = needles
    ordered_needles = []

    if kb_status == 1:
        ordered_needles.append("kb")
    if nct_status == 1:
        ordered_needles.append("nct")
    if custom_needles_df is not None:
        if not isinstance(custom_needles_df, pd.DataFrame):
            raise ValueError("custom_needles_df must be a pandas DataFrame")
        ordered_needles.append("custom")

    if not ordered_needles:
        raise ValueError("At least one needle type must be enabled")


    # ============================================================================
    # SECTION 4: Prepare CSV Files
    # ============================================================================

    csv_buffer = None
    custom_csv_buffer = None

    try:
        # Prepare input CSV
        csv_buffer = StringIO()
        input_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        files = {
            "input_csv": ("input.csv", csv_buffer, "text/csv")
        }

        # Prepare custom needles CSV if provided

        if custom_needles_df is not None:
            custom_csv_buffer = StringIO()
            custom_needles_df.to_csv(custom_csv_buffer, index=False)
            custom_csv_buffer.seek(0)
            files["custom_needles"] = ("custom_needles.csv", custom_csv_buffer, "text/csv")

    except Exception as e:
        # Clean up buffers
        if csv_buffer:
            csv_buffer.close()
        if custom_csv_buffer:
            custom_csv_buffer.close()
        raise Exception(f"Failed to prepare CSV files: {str(e)}")


    # ============================================================================
    # SECTION 5: Prepare and Submit Annotation Request
    # ============================================================================

    # Prepare form data
    form_data = {
        "ann_name": "Annt",
        "output_db": "annotations",
        "output_table_name": "Annt",
        "entities": json.dumps(entities) if entities else "",
        "needles": ordered_needles
    }

    try:
        resp = client.post(
            "https://support.ferma.ai/annotation/csv-input",
            data = form_data,
            files = files,
            timeout = 120)
        if resp.status_code != 200:
            raise Exception(
                f"Failed to initiate annotation. "
                f"Status code: {resp.status_code}, Response: {resp.text[:200]}"
            )
        
    except Exception as e:
        raise Exception(f"Annotation request failed: {str(e)}")

    finally:
        # Clean up CSV buffers after submission
        if csv_buffer:
            csv_buffer.close()
        if custom_csv_buffer:
            custom_csv_buffer.close()


    # ============================================================================
    # SECTION 6: Extract Transaction ID
    # ============================================================================
    
    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        trans_id_input = soup.find("input", {"name": "trans_id"})

        if not trans_id_input or "value" not in trans_id_input.attrs:
            raise Exception("Transaction ID not found in response")

        trans_id = trans_id_input["value"]

        print(f"\n{'-'*80}")
        print(f"[{format_timestamp()}]: Annotation Initiated, Transaction ID: {trans_id}")

    except Exception as e:
        raise Exception(f"Failed to extract transaction ID: {str(e)}")


    # ============================================================================
    # SECTION 7: Poll Progress Tracker
    # ============================================================================
   
    tracker_url = f"https://support.ferma.ai/annotation/progress-tracker?trans_id={trans_id}"
    waited = 0
    total = 0
    completed = 0
    failed = 0

    while waited < max_wait:
        try:
            progress_resp = client.get(tracker_url, timeout=30)
            if progress_resp.status_code != 200:
                time.sleep(poll_interval)
                waited += poll_interval
                continue

            soup = BeautifulSoup(progress_resp.text, "html.parser")

            # Helper function to extract values from progress table
            def get_value(field: str) -> Optional[str]:
                """Extract field value from HTML table."""
                cell = soup.find("td", string=field)
                if cell:
                    next_cell = cell.find_next_sibling("td")
                    if next_cell:
                        return next_cell.text.strip()
                return None

            # Extract progress metrics
            total = get_value("total")
            completed = get_value("completed")
            failed = get_value("failed")
            failure_details = get_value("failure_details")
            last_modified_at = get_value("last_modified_at")

            # Convert to integers with safe defaults
            total = int(total) if total and total.isdigit() else 0
            completed = int(completed) if completed and completed.isdigit() else 0
            failed = int(failed) if failed and failed.isdigit() else 0

            # Convert server time (UTC) to IST
            last_modified_ist = format_timestamp(last_modified_at, utc_time=True) if last_modified_at else 'N/A'

            print(f"• {waited:03d}s -> Completed: {completed}/{total} | Failed: {failed} | Last Modified: {last_modified_ist}")
            
            if failed > 0 and failure_details:
                print(f"⚠️ Failure Details: {failure_details}")

            if total > 0 and completed >= total:
                break

            # Check if all items failed
            if total > 0 and failed >= total:
                raise Exception(
                    f"All {total} items failed. Details: {failure_details or 'None provided'}"
                )

        except Exception as e:
            print("Error parsing progress:", e)

        time.sleep(poll_interval)
        waited += poll_interval
    
    if waited >= max_wait and completed < total:
        print(f"⚠️ Max wait limit reached ({max_wait}s). Annotation may still be processing.")
        print(f"   Status: {completed}/{total} completed | {failed} failed.")
        print(f"   You can increase the wait time by setting a higher 'max_wait' value (current: {max_wait}s).")


    # ============================================================================
    # SECTION 8: Download Results
    # ============================================================================
    
    download_format = "long_table_format" if long_table else "pivot_table_format"
    
    try:
        download_data = {"trans_id": (None, trans_id), "format_type": (None, download_format)}
        start_download = time.time()
        download_resp = client.post("https://support.ferma.ai/annotation/progress-tracker", files=download_data, headers=download_headers)
        end_download = time.time()
        download_time = end_download - start_download

        if download_resp.status_code != 200:
            raise Exception(
                f"Download failed with status code {download_resp.status_code}"
            )
    
        if download_resp.headers.get("Content-Type", "").startswith("text/csv"):
            print(f"[{format_timestamp()}]: Annotation Completed (Data retrieved in {download_time:.2f} secs)")
            print(f"{'-'*80}\n")
            return pd.read_csv(BytesIO(download_resp.content), encoding='utf-8-sig')
        else:
            raise Exception(f"[{format_timestamp()}]: Download failed or invalid format received")
    except Exception as e:
        raise Exception(f"Annotation download failed: {str(e)}")