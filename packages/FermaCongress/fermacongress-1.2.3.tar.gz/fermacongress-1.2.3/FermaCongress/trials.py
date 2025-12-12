import re
import requests
import pandas as pd
from tqdm import tqdm
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================================================================================
# Step 0: General Configuration
# =========================================================================================

NCT_HEADERS = {
    "accept": "application/json",
    "user-agent": "ClinicalPhaseExtractor/1.0"
}

CTIS_PAYLOAD = {"pagination":{"page":1,"size":20},
        "sort":{"property":"decisionDate","direction":"DESC"},
        "searchCriteria":{"containAll":None,"containAny":None,"containNot":None,"title":None,"number":None,"status":None,
        "medicalCondition":None,"sponsor":None,"endPoint":None,"productName":None,"productRole":None,"populationType":None,
        "orphanDesignation":None,"msc":None,"ageGroupCode":None,"therapeuticAreaCode":None,"trialPhaseCode":None,
        "sponsorTypeCode":None,"gender":None,"eeaStartDateFrom":None,"eeaStartDateTo":None,"eeaEndDateFrom":None,"eeaEndDateTo":None,
        "protocolCode":None,"rareDisease":None,"pip":None,"haveOrphanDesignation":None,"hasStudyResults":None,
        "hasClinicalStudyReport":None,"isLowIntervention":None,"hasSeriousBreach":None,"hasUnexpectedEvent":None,
        "hasUrgentSafetyMeasure":None,"isTransitioned":None,"eudraCtCode":None,"trialRegion":None,"vulnerablePopulation":None,
        "mscStatus":None}}

CTIS_HEADERS = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
            "cache-control": "no-cache",
            "content-length": "905",
            "content-type": "application/json",
            "cookie": "accepted_cookie=true",
            "origin": "https://euclinicaltrials.eu",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://euclinicaltrials.eu/ctis-public/search?lang=en",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133")',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
        }


# =========================================================================================
# Step 1: Function to Extract NCT - Trial IDs
# =========================================================================================

def extract_nct(trial_id: str) -> Tuple[str, str, str, str, str]:
    """
    Extract trial information from ClinicalTrials.gov.
    
    Args:
        trial_id: NCT trial identifier (e.g., 'NCT12345678')
        delimiter: String to join multiple collaborators
        
    Returns:
        Tuple of (study_id, phase, enrollment_count, lead_sponsor, collaborators)
    """
    url = f"https://clinicaltrials.gov/api/v2/studies/{trial_id}"
    try:
        response = requests.get(url, headers=NCT_HEADERS, timeout=30)
        if response.status_code == 200:
            data = response.json()
            protocol = data.get('protocolSection', {})
            
            # Get Acronym or Study ID
            identification = protocol.get('identificationModule', {})
            study_id = identification.get('acronym') or identification.get('orgStudyIdInfo', {}).get('id', 'Unknown ID')
            
            # Extract Phase Information
            phases = protocol.get('designModule', {}).get('phases', [])
            phase = "" if phases == ['NA'] else "/".join(phases) if phases else ""
            
            # Extract Enrollment Count
            enrollment = protocol.get('designModule', {}).get('enrollmentInfo', {})
            enrollment_count = enrollment.get('count', '')
            
            # Extract Sponsors & Collaborators
            sponsors_data = protocol.get('sponsorCollaboratorsModule', {})
            lead_sponsor = sponsors_data.get('leadSponsor', {}).get('name', 'Unknown Sponsor')
            collaborators = sponsors_data.get('collaborators', [])
            collaborator_names = ", ".join([collab.get('name', 'Unknown Collaborator') for collab in collaborators]) if collaborators else ""
            
            return (study_id, phase, enrollment_count, lead_sponsor, collaborator_names)
        
        else:
            print(f"⚠️  Error fetching trial {trial_id}: Response Code: {response.status_code}")
            return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
        
    except requests.exceptions.Timeout:
        print(f"⚠️  Timeout while fetching trial {trial_id}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Network error for trial {trial_id}: {e}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
    except Exception as e:
        print(f"⚠️  Unexpected error for trial {trial_id}: {e}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")


# =========================================================================================
# Step 2: Function to Extract CTIs - Trial IDs
# =========================================================================================

def extract_ctis(trial_id: str) -> Tuple[str, str, str, str, str]:
    """
    Extract trial information from EU CTIS.
    
    Args:
        trial_id: CTIS trial identifier (format: YYYY-XXXXXX-XX-XX)
        
    Returns:
        Tuple of (acronym, phase, enrollment_count, lead_sponsor, collaborators)
    """

    url = "https://euclinicaltrials.eu/ctis-public-api/search"

    # Creating a copy to avoid mutation of global payload
    ctis_payload = CTIS_PAYLOAD.copy()
    ctis_payload['searchCriteria']['number'] = trial_id
    
    try:
        response = requests.post(url, headers=CTIS_HEADERS, json=ctis_payload, timeout=30)
        if response.status_code != 200:
            print(f"⚠️  Error fetching trial {trial_id}: Response Code: {response.status_code}")
            return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
        
        response_data = response.json()

        if 'data' not in response_data or len(response_data['data']) == 0:
            print(f"⚠️  No data found for trial {trial_id}")
            return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
        
        for trial in response_data['data']:
            if trial.get('ctNumber') == trial_id:
                acronym = trial.get('shortTitle', '')
                phase = trial.get('trialPhase', '')
                enrollment_count = str(trial.get('totalNumberEnrolled', ''))
                lead_sponsor = trial.get('sponsor', '')
                return (acronym, phase, enrollment_count, lead_sponsor, '')
                
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
        
    except requests.exceptions.Timeout:
        print(f"⚠️  Timeout while fetching CTIS trial {trial_id}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Network error for CTIS trial {trial_id}: {e}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
    except (KeyError, ValueError) as e:
        print(f"⚠️  Data parsing error for CTIS trial {trial_id}: {e}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
    except Exception as e:
        print(f"⚠️  Unexpected error for CTIS trial {trial_id}: {e}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")


# =========================================================================================
# Step 3: Function to Extract Eudract - Trial IDs
# =========================================================================================

def extract_eudract(trial_id: str) -> Tuple[str, str, str, str, str]:
    """
    Extract trial information from EudraCT.
    
    Args:
        trial_id: EudraCT trial identifier (format: YYYY-XXXXXX-XX)
        
    Returns:
        Tuple of (acronym, phase, enrollment_count, lead_sponsor, collaborators)
    """
    
    url = f"https://www.clinicaltrialsregister.eu/ctr-search/rest/download/full?query={trial_id}&mode=current_page"

    try:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"⚠️  Error fetching EudraCT trial {trial_id}: Response Code: {response.status_code}")
            return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")

        file_content = response.text
        
        # Extract Acronym
        acronym_match = re.search(r"A\.\d+(\.\d+)?\s*Name or abbreviated title of the trial where available:\s*(.+)", file_content)
        if acronym_match:
            acronym = acronym_match.group(2).strip()
        else:
            acronym = ''
        
        # Extract Phase
        if re.search(r"Therapeutic exploratory \(Phase II\): Yes", file_content):
            phase = "Phase 2"
        elif re.search(r"Human pharmacology \(Phase I\): Yes", file_content):
            phase = "Phase 1"
        elif re.search(r"Therapeutic confirmatory \(Phase III\): Yes", file_content):
            phase = "Phase 3"
        elif re.search(r"Therapeutic use \(Phase IV\): Yes", file_content):
            phase = "Phase 4"
        else:
            phase = ""
    
        # Extract Lead Sponsor
        sponsor_match = re.search(r"B\.1\.1 Name of Sponsor:\s*(.+)", file_content)
        if sponsor_match:
            lead_sponsor = sponsor_match.group(1).strip()
        else:
            lead_sponsor = ''
            
        return (acronym, phase, '', lead_sponsor, '')
    
    except requests.exceptions.Timeout:
        print(f"⚠️  Timeout while fetching EudraCT trial {trial_id}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Network error for EudraCT trial {trial_id}: {e}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
    except Exception as e:
        print(f"⚠️  Unexpected error for EudraCT trial {trial_id}: {e}")
        return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")


# =========================================================================================
# Step 4: Main - Driver Function
# =========================================================================================

def extracttrials(df: pd.DataFrame, column: str, delimiter: str = ";;") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extract clinical trial information from multiple registries.
    
    This function takes a DataFrame with a column containing trial IDs (separated by a delimiter) and 
    extracts detailed information from ClinicalTrials.gov, CTIS, or EudraCT.
    
    Args:
        df: Input DataFrame containing trial IDs
        column: Name of column containing trial IDs
        delimiter: Character(s) separating multiple trial IDs in a cell
        
    Returns:
        Tuple of (df_standard, df_long):
        - df_standard: Wide format with aggregated trial info per row
        - df_long: Long format with one row per trial ID
    """
    
    # Input Validation
    # ---------------------------------------------------------------------------------
    
    if df is None or df.empty:
        raise ValueError("DataFrame is empty or None.")
    
    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' not found in DataFrame. "
            f"Available columns: {list(df.columns)}"
        )
    
    if not delimiter or not isinstance(delimiter, str):
        raise ValueError("Delimiter must be a non-empty string.")

    # Processing Trial IDs
    # ---------------------------------------------------------------------------------
    
    CONFIG = {
        "regex_patterns": {
            "nct": r"^NCT",
            "ctis": r"\b\d{4}-\d{6}-\d{2}-\d{2}\b",
            "eudract": r"\b\d{4}-\d{6}-\d{2}\b"
        }
    }

    # Extraction Routing
    # ---------------------------------------------------------------------------------
    
    def route_extraction(trial_id: str) -> Tuple[str, str, str, str, str]:
        """Route trial ID to appropriate extraction function."""
        if not trial_id or str(trial_id).strip().lower() in ["", "nan", "none"]:
            return ("", "", "", "", "")
            
        trial_id = str(trial_id).strip()
        
        try:
            if re.match(CONFIG["regex_patterns"]["nct"], trial_id, re.IGNORECASE):
                return extract_nct(trial_id)

            elif re.match(CONFIG["regex_patterns"]["ctis"], trial_id):
                return extract_ctis(trial_id)

            elif re.match(CONFIG["regex_patterns"]["eudract"], trial_id):
                return extract_eudract(trial_id)

            else:
                return ("", "", "", "", "")

        except Exception as e:
            print(f"⚠️  Error routing trial {trial_id}: {e}")
            return ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")

    
    # Data Preparation
    # ---------------------------------------------------------------------------------
    try:
        df = df.copy()
        df['INTERNAL_ID_FLAG'] = range(len(df))
        
        # Create long format reference DataFrame
        df_long_ref = df.assign(**{column: df[column].astype(str).str.split(delimiter)}).explode(column, ignore_index=True)
        df_long_ref[column] = df_long_ref[column].str.strip()
        df_long_ref[column] = df_long_ref[column].replace(['nan', 'None', None], '')
        
        # Get unique trial IDs
        unique_trial_ids = df_long_ref[column].dropna().unique()
        unique_trial_ids = [tid for tid in unique_trial_ids if tid]
    
    except Exception as e:
        raise RuntimeError(f"Error during data preparation: {e}") from e

    
    # Extraction
    # ---------------------------------------------------------------------------------
    try:
        trial_map = {}
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_to_tid = {executor.submit(route_extraction, tid): tid for tid in unique_trial_ids}
            
            for future in tqdm(as_completed(future_to_tid), total=len(unique_trial_ids), desc="Extracting Trial Info"):
                tid = future_to_tid[future]
                try:
                    trial_map[tid] = future.result()
                except Exception as e:
                    print(f"⚠️  Failed to extract {tid}: {e}")
                    trial_map[tid] = ("ERROR", "ERROR", "ERROR", "ERROR", "ERROR")

    except Exception as e:
        raise RuntimeError(f"Error during trial extraction: {e}") from e

    
    # Data Aggregation
    # ---------------------------------------------------------------------------------
    
    try:
        # Map results back to long reference DataFrame
        df_long_ref[['Study ID','Phase','Enrollment','Lead Sponsor','Collaborators']] = \
            df_long_ref[column].apply(lambda x: pd.Series(trial_map.get(x, ("","","","",""))))
    
    
        # Generate standard (wide) format by INTERNAL_ID_FLAG
        group_cols = ['Study ID','Phase','Enrollment','Lead Sponsor','Collaborators']
        df_standard = df_long_ref.groupby('INTERNAL_ID_FLAG')[group_cols].agg(
            lambda x: ", ".join([str(i) for i in x if i not in [None, ""]])
        ).reset_index()

        df_standard = df.merge(df_standard, left_on='INTERNAL_ID_FLAG', right_on='INTERNAL_ID_FLAG', how='left')

        df_standard = df_standard.drop(columns=['INTERNAL_ID_FLAG'])
        df_long = df_long_ref.drop(columns=['INTERNAL_ID_FLAG'])

        return df_standard, df_long

    except KeyError as e:
        raise RuntimeError(f"Column error during aggregation: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error during data aggregation: {e}") from e