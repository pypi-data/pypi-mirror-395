import requests
import pandas as pd
from io import StringIO
from FermaCongress.extractferma import *

def baseplanner(client, CONGRESS_ID: str, PLANNER_ID: str = None) -> pd.DataFrame:

    # -------------------------------------------------------------------------------------------------
    # Step 0: Validating Client
    # -------------------------------------------------------------------------------------------------
    if client is None:
        raise ValueError("Something went wrong with Client, Please retry logging in.")

    # -------------------------------------------------------------------------------------------------
    # Step 1: Extracting Sessions and Entities
    # -------------------------------------------------------------------------------------------------
    try:
        sessions_data = get_all_sessions(client, CONGRESS_ID)
        keywords_data = get_skg(client, CONGRESS_ID)
    except Exception as e:
        raise ValueError(f"Error while Extracting Data: {str(e)}")

    # -------------------------------------------------------------------------------------------------
    # Step 2: Merging Sessions and Entities
    # -------------------------------------------------------------------------------------------------
    df = sessions_data[['internal_id', 'abstract_id', 'session_title', 'session_type', 'abstract_title', 'abstract_link',
        'authors', 'institution', 'location', 'start_date', 'end_date', 'classification', 'full_abstract_text']]

    df = df.merge(keywords_data[['internal_id', 'firms', 'diseases', 'primary_drugs', 'secondary_drugs', 'comparator_drugs',
        'nct', 'acronym', 'drug_classes', 'indications']], on='internal_id', how='left')
    
    # -------------------------------------------------------------------------------------------------
    # Step 3: Data Pre-Processing
    # -------------------------------------------------------------------------------------------------
    df['Date'] = df['start_date']
    df['firms'] = df['firms'].fillna('').astype(str).str.replace('<0>', '', regex=False).str.strip()
    
    # Replacing double semicolon with a comma and removing 'nan' and 'None'
    for col in ['firms', 'diseases', 'primary_drugs', 'secondary_drugs', 'comparator_drugs', 'nct', 'acronym', 'drug_classes', 'indications']:
        df[col] = df[col].fillna('').astype(str).str.replace(';;', ', ', regex=False).replace(['nan', 'None'], '')

    # Renaming the columns
    df = df.rename(columns={"internal_id": "Int ID", "abstract_id": "Abstract ID", "abstract_link": "Abstract Link", 
                    "session_type": "Session Type", "session_title": "Session Title", "abstract_title": "Abstract Title",
                    "full_abstract_text": "Full Abstract Text", "authors": "Authors", "institution": "Institution",
                    "location": "Location", "start_date": "Start Time", "end_date": "End Time", "firms": "Agencies",
                    "drug_classes": "Drug Class", "indications": "Indication", "primary_drugs": "Primary Drugs",
                    "secondary_drugs": "Secondary Drugs", "comparator_drugs": "Comparator Drugs", "nct": "NCT", "acronym": "Acronym"})


    # -------------------------------------------------------------------------------------------------
    # Step 4: Merging Planner Data
    # -------------------------------------------------------------------------------------------------
    if PLANNER_ID is not None:
        try:
            planner_resp = requests.get(f"https://admin-portal.ferma.ai/planners/{PLANNER_ID}/download?download_type=all", headers=client)
            if planner_resp.status_code == 200:
                planner_data = pd.read_csv(StringIO(planner_resp.text))
                df = df.merge(planner_data[['internal_id', 'priority_name']], left_on='Int ID', right_on='internal_id', how='left')
                df = df.rename(columns={"priority_name": "Priority"})
                columns = ['Int ID','Abstract ID', 'Abstract Link', 'Priority', 'Session Title', 'Session Type', 'Abstract Title', 'Full Abstract Text', 'Authors', 'Institution',
                        'Location', 'Date', 'Start Time', 'End Time', 'Agencies', 'Drug Class', 'Indication', 'Primary Drugs', 'Secondary Drugs', 'Comparator Drugs',
                        'NCT', 'Acronym', 'classification']
                
                return df[columns]

            else:
                raise Exception(f"Failed to fetch planner data: {planner_resp.status_code} - {planner_resp.text}")

        except Exception as e:
            raise Exception(f"Failed to fetch planner data: {str(e)}")
        
    elif PLANNER_ID is None:
        columns = ['Int ID','Abstract ID', 'Abstract Link','Session Title', 'Session Type', 'Abstract Title', 'Full Abstract Text', 'Authors', 'Institution',
                'Location', 'Date', 'Start Time', 'End Time', 'Agencies', 'Drug Class', 'Indication', 'Primary Drugs', 'Secondary Drugs', 'Comparator Drugs',
                'NCT', 'Acronym', 'classification']

        return df[columns]