import re
import json
import requests
import pandas as pd
from tqdm import tqdm
from io import StringIO
from functools import reduce
from collections import defaultdict
from typing import List, Optional

# Function to Extract All Sessions Data
# --------------------------------------------------------------------------------------------------------------------------------
def get_all_sessions(client, CONGRESS_ID: str) -> pd.DataFrame:
    """Fetch and return all sessions for a given congress as a DataFrame."""
    if not client:
        raise RuntimeError("No login session found. Please call adminlogin(env_path).")
        
    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}/sessions/download"

    try:
        response = requests.get(url, headers=client, timeout=30)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), dtype={"tweets": str}, on_bad_lines='warn')

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch sessions: {e}") from e
    except pd.errors.ParserError as e:
        raise RuntimeError(f"Error parsing sessions CSV: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while fetching sessions: {e}") from e


# Function to Extract Session Keywords Data
# --------------------------------------------------------------------------------------------------------------------------------
def get_skg(client, CONGRESS_ID: str) -> pd.DataFrame:
    """Fetch and return session keywords grouped data for a given congress."""
    if not client:
        raise RuntimeError("No login session found. Please call adminlogin(env_path).")
        
    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}/sessions/keywords/download?download_type=grouped"
    try:
        response = requests.get(url, headers=client, timeout=30)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), on_bad_lines='warn')

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch session keywords: {e}") from e
    except pd.errors.ParserError as e:
        raise RuntimeError(f"Error parsing session keywords CSV: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while fetching session keywords: {e}") from e


# Function to Extract Sessions - Full Abstracts Data
# --------------------------------------------------------------------------------------------------------------------------------
def get_fullabstracts(client, CONGRESS_ID: str) -> pd.DataFrame:
    """Fetch and return session full abstracts data for a given congress."""
    if not client:
        raise RuntimeError("No login session found. Please call adminlogin(env_path).")
        
    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}/sessions/full_abstracts"

    try:
        response = requests.get(url, headers=client, timeout=30)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), on_bad_lines='warn')

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch session full abstracts: {e}") from e
    except pd.errors.ParserError as e:
        raise RuntimeError(f"Error parsing session full abstracts CSV: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while fetching session full abstracts: {e}") from e


# Function to Extract Session Keywords Data
# --------------------------------------------------------------------------------------------------------------------------------
def get_summary(client, CONGRESS_ID: str) -> pd.DataFrame:
    """Fetch and return session summary data for a given congress."""
    if not client:
        raise RuntimeError("No login session found. Please call adminlogin(env_path).")
        
    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}/sessions/v1_summary?status=1"
    
    try:
        response = requests.get(url, headers=client, timeout=30)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), on_bad_lines='warn')

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch session summary: {e}") from e
    except pd.errors.ParserError as e:
        raise RuntimeError(f"Error parsing session summary CSV: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while fetching session summary: {e}") from e


# Function to Extract Session - Tweets Data
# --------------------------------------------------------------------------------------------------------------------------------
def get_tweets(client, CONGRESS_ID: str) -> pd.DataFrame:
    """Fetch and return session tweets data for a given congress."""
    if not client:
        raise RuntimeError("No login session found. Please call adminlogin(env_path).")
    
    # Fetching Tweets Data from Ferma API
    # ---------------------------------------------------------------------------------
        
    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}/tweets/download"

    try:
        response = requests.get(url, headers=client, timeout=30)
        response.raise_for_status()
        tweets_df = pd.read_csv(StringIO(response.text), on_bad_lines='warn')

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch tweets: {e}") from e
    except pd.errors.ParserError as e:
        raise RuntimeError(f"Error parsing tweets CSV: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error fetching tweets: {e}") from e
    

    # Parsing Buzz Scores from SessionBuzzScores Column
    # ---------------------------------------------------------------------------------

    try:
        # Define the parse_buzz_scores function
        def parse_buzz_scores(x):
            if pd.isna(x) or not isinstance(x, str):
                print(f"Invalid data: {x}")
                return []
            try:
                return json.loads(x.replace("'", '"'))
            except (json.JSONDecodeError, AttributeError):
                print(f"Failed to parse JSON: {x}")
                return []
        
        tweets_df['session_buzz_scores'] = tweets_df['session_buzz_scores'].apply(parse_buzz_scores)
        tweets_df = tweets_df.explode('session_buzz_scores').reset_index(drop=True)

        # Extract buzz_score and session_id safely
        tweets_df['buzz_score'] = tweets_df['session_buzz_scores'].apply(lambda x: x.get('buzz_score') if isinstance(x, dict) else None)
        tweets_df['session_id'] = tweets_df['session_buzz_scores'].apply(lambda x: x.get('session_id') if isinstance(x, dict) else None)

        tweets_df = tweets_df.drop(columns=['session_buzz_scores', 'session_ids'], errors='ignore')
        tweets_df = tweets_df.sort_values(by='session_id').reset_index(drop=True)
        tweets_df['tweet_id'] = tweets_df['tweet_url'].str.extract(r'/status/(\d+)', expand=False)
    except Exception as e:
        raise RuntimeError(f"Error processing tweet buzz scores: {e}") from e

    
    # Fetching All Sessions Data and Merging with Tweets Data
    # ---------------------------------------------------------------------------------

    try:
        sessions_metadata_df = get_all_sessions(client, CONGRESS_ID)
        tweets_df = tweets_df.merge(
            sessions_metadata_df[['session_id', 'internal_id', 'abstract_id', 'session_title', 'abstract_title']],
            on='session_id',
            how='left')

    except Exception as e:
        raise RuntimeError(f"Error merging session metadata: {e}") from e
            
    # Reordering and Renaming Columns
    tweets_df = tweets_df[['internal_id', 'session_id', 'abstract_id', 'session_title', 'abstract_title', 'tweet_id', 'tweet_url',
                            'text', 'created_at', 'retweet_count', 'reply_count', 'like_count', 'view_count', 'user_name',
                            'user_description', 'followers_count', 'following_count', 'location', 'buzz_score']]

    tweets_df = tweets_df.rename(columns={'internal_id': 'Internal ID', 'session_id': 'Session ID', 'abstract_id': 'Abstract ID',
                    'session_title': 'Session Title', 'abstract_title': 'Abstract Title', 'tweet_id': 'Tweet ID',
                    'tweet_url': 'Tweet URL', 'text': 'Tweet Text', 'created_at': 'Date of Posting', 'retweet_count': 'Retweet Count',
                    'reply_count': 'Reply Count', 'like_count': 'Like Count', 'view_count': 'View Count', 'user_name': 'User Name',
                    'user_description': 'User Description', 'followers_count': 'Followers Count', 'following_count': 'Following Count',
                    'location': 'Location', 'buzz_score': 'Buzz Score'})

    
    # Fetching Priority Data and Merging with Tweets Data
    # ---------------------------------------------------------------------------------

    try:
        priority_df = get_priority(client, CONGRESS_ID)
        
        columns_to_remove = {
            'internal_id', 'abstract_id', 'session_title', 'session_type', 'abstract_title', 'authors', 'institution',
            'classification', 'location', 'start_date', 'end_date', 'Filename', 'Combined Priority', 'Teams'
        }

        priority_df = priority_df[[col for col in priority_df.columns if col not in columns_to_remove and 'Combined' not in col]]
        tweets_df = tweets_df.merge(priority_df, how='left', left_on='Session ID', right_on='session_id')
        tweets_df = tweets_df.drop(columns=['session_id'], errors='ignore')

    except Exception as e:
        raise RuntimeError(f"Error merging priority data with tweets: {e}") from e
    
    return tweets_df


# Function to Extract All Client's Priority Data
# --------------------------------------------------------------------------------------------------------------------------------
def get_priority(
    client,
    CONGRESS_ID: str,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None
    ) -> pd.DataFrame:
    """
    Extract and combine priority data from all client planners for a given congress.
    
    Args:
        client: Authenticated session headers
        CONGRESS_ID: Congress identifier
        include: List of tenant names to include (case-insensitive). If provided, only these will be processed.
        exclude: List of tenant names to exclude (case-insensitive). 'ZoomRx' and 'congress-insights' are always excluded.
    
    Returns:
        DataFrame with session metadata and priority rankings from all planners
    """
    if not client:
        raise RuntimeError("No login session found. Please call adminlogin(env_path).")
    
    # 1 Extracting All Sessions Data for additional columns
    # ----------------------------------------------------------------
    sessions_metadata_df = get_all_sessions(client, CONGRESS_ID)
    
    
    # 2 Extracting the list of planners
    # ----------------------------------------------------------------
    url = f"https://admin-portal.ferma.ai/congresses/{CONGRESS_ID}?include=planners"
    
    try:
        response = requests.get(url, headers=client, timeout=30)
        response.raise_for_status()
        planners = response.json().get('data', {}).get('planners', [])
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch planners: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error parsing planners response: {e}") from e
        
    # Handling No Priority Planners Found or only ZoomRx
    if not planners or (len(planners) == 1 and planners[0].get('tenantName', '').lower() == 'zoomrx'):
        print("! No Priority Planners Found or only ZoomRx Found. Returning -> Sessions Metadata.")
        session_columns_needed = ['internal_id', 'session_id', 'abstract_id', 'session_title', 'session_type',
        'abstract_title', 'authors', 'institution', 'classification', 'location', 'start_date', 'end_date']
            
        sessions_metadata_df = sessions_metadata_df[session_columns_needed].drop_duplicates()
        sessions_metadata_df['start_date'] = pd.to_datetime(sessions_metadata_df['start_date'], errors='coerce')
        sessions_metadata_df['end_date']   = pd.to_datetime(sessions_metadata_df['end_date'], errors='coerce')
        
        FILENAME_PATTERN = re.compile(r'[^A-Za-z0-9 ]+')
        sessions_metadata_df['Filename'] = sessions_metadata_df.apply(
                lambda row: f"{row['session_id']}_{FILENAME_PATTERN.sub('', str(row['abstract_title'])).strip()[:30].replace(' ', '')}",
                axis=1
            )
        return sessions_metadata_df[session_columns_needed + ['Filename']]
        
    planner_df = pd.json_normalize(planners)
    planner_df['link'] = planner_df['id'].apply(lambda pid: f'https://admin-portal.ferma.ai/planners/{pid}/download?download_type=all')
    
    
    #3 Processing Include/Exclude Lists
    # ------------------------------------------------------------------------------------------------------------
    include_normalized = [item.strip().lower() for item in include] if include else None
    
    # Always exclude 'zoomrx'
    if exclude is None:
        exclude = ['ZoomRx', 'congress-insights']
    else:
        normalized = [e.strip().lower() for e in exclude]
        if 'zoomrx' not in normalized:
            exclude.append('ZoomRx')
        if 'congress-insights' not in normalized:
            exclude.append('congress-insights')
            
    exclude_normalized = [item.strip().lower() for item in exclude] if exclude else None

    # 4 Defning the priority mapping and Inverse mapping
    # ------------------------------------------------------------------------------------------------------------
    PRIORITY_MAP = {"Very High": 1, "High": 2, "Internal": 3, "Medium": 4, "Low": 5, "Not Relevant": 6}
    REVERSE_PRIORITY_MAP = {v: k for k, v in PRIORITY_MAP.items()}
    
    
    # 5. Download and parse each planner file, applying include/exclude filters
    # ------------------------------------------------------------------------------------------------------------
    planner_priority_dfs = []

    for _, row in tqdm(planner_df.iterrows(), total=len(planner_df), desc="Processing Planners"):
        tenant_name = row['tenantName']
        tenant_normalized = tenant_name.strip().lower()

        # Filtering logic (comparison only)
        if include_normalized and tenant_normalized not in include_normalized:
            continue
        if exclude_normalized and tenant_normalized in exclude_normalized:
            continue

        priority_column_name = f"{tenant_name} - {row['teamName']}"
        try:
            planner_file_response = requests.get(row['link'], headers=client, timeout=30)
            planner_file_response.raise_for_status()
            priority_df = pd.read_csv(
                StringIO(planner_file_response.text),
                usecols=['internal_id', 'abstract_title', 'priority_name'],
                on_bad_lines='warn'
            )
            priority_df = priority_df.rename(columns={'priority_name': priority_column_name})
            planner_priority_dfs.append(priority_df)
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Skipping planner '{priority_column_name}' - download error: {e}")
        except pd.errors.ParserError as e:
            print(f"⚠️  Skipping planner '{priority_column_name}' - CSV parsing error: {e}")
        except Exception as e:
            print(f"⚠️  Skipping planner '{priority_column_name}' - unexpected error: {e}")

    if not planner_priority_dfs:
        raise RuntimeError("No planner data was successfully downloaded or parsed.")

    # 6. Merge all planners' priority data into one dataframe by internal_id and abstract_title
    # ------------------------------------------------------------------------------------------------------------
    combined_priority_df = reduce(
        lambda left, right: pd.merge(left, right, on=['internal_id', 'abstract_title'], how='outer'),
        planner_priority_dfs
    )

    # 7. Compute combined priority by mapping to numeric values and selecting the minimum
    # ------------------------------------------------------------------------------------------------------------
    priority_columns = [col for col in combined_priority_df.columns if col not in ['internal_id', 'abstract_title']]
    for column in priority_columns:
        combined_priority_df[column + '_num'] = combined_priority_df[column].map(PRIORITY_MAP)

    numeric_priority_columns = [col + '_num' for col in priority_columns]
    combined_priority_df['combined_priority_num'] = combined_priority_df[numeric_priority_columns].min(axis=1)
    combined_priority_df['Combined Priority'] = combined_priority_df['combined_priority_num'].map(REVERSE_PRIORITY_MAP)
    
    # 7b. Compute client-level combined priorities
    # ------------------------------------------------------------------------------------------------------------

    tenant_to_columns = defaultdict(list)
    for col in priority_columns:
        tenant = col.split(" - ")[0].strip()
        tenant_to_columns[tenant].append(col)

    for tenant, cols in tenant_to_columns.items():
        numeric_cols = [col + '_num' for col in cols]
        combined_col_name = f"{tenant} - Combined Priority"
        combined_priority_df[f"{tenant}_combined_priority_num"] = combined_priority_df[numeric_cols].min(axis=1)
        combined_priority_df[combined_col_name] = combined_priority_df[f"{tenant}_combined_priority_num"].map(REVERSE_PRIORITY_MAP)
    
    # 8. Determine which teams agree on the selected combined priority
    # ------------------------------------------------------------------------------------------------------------
    def compute_team_match(row):
        matched_columns = [
            col for col, num_col in zip(priority_columns, numeric_priority_columns)
            if row[num_col] == row['combined_priority_num']
        ]
        return "All Teams" if len(matched_columns) == len(priority_columns) else ', '.join(matched_columns)

    combined_priority_df['Teams'] = combined_priority_df.apply(compute_team_match, axis=1)
    combined_priority_df.drop(
        columns=numeric_priority_columns + ['combined_priority_num'] +
        [f"{tenant}_combined_priority_num" for tenant in tenant_to_columns], inplace=True
        )

    # 9. Merge session-level metadata to enrich the final output
    # ------------------------------------------------------------------------------------------------------------
    session_columns_needed = [
        'internal_id', 'session_id', 'abstract_id', 'session_title', 'session_type', 'authors', 'institution',
        'classification', 'location', 'start_date', 'end_date'
    ]
    sessions_metadata_df = sessions_metadata_df[session_columns_needed].drop_duplicates()
    sessions_metadata_df['start_date'] = pd.to_datetime(sessions_metadata_df['start_date'])
    sessions_metadata_df['end_date'] = pd.to_datetime(sessions_metadata_df['end_date'])
    final_df = pd.merge(combined_priority_df, sessions_metadata_df, on='internal_id', how='left')
    
    FILENAME_PATTERN = re.compile(r'[^A-Za-z0-9 ]+')
    final_df['Filename'] = final_df.apply(lambda row: f"{row['session_id']}_{FILENAME_PATTERN.sub('', str(row['abstract_title'])).strip()[:30].replace(' ', '')}", axis=1)

    # 10. Set final column order for clean output
    # ------------------------------------------------------------------------------------------------------------
    fixed_columns = [
        'internal_id', 'session_id', 'abstract_id', 'session_title', 'session_type', 'abstract_title', 'authors', 'institution',
        'classification', 'location', 'start_date', 'end_date', 'Filename', 'Combined Priority', 'Teams'
    ]

    # Organize by client: first their combined priority, then their team columns
    client_priority_columns = []
    for tenant in sorted(tenant_to_columns):  # Optional: sort for consistent order
        client_combined = f"{tenant} - Combined Priority"
        team_columns = tenant_to_columns[tenant]
        client_priority_columns.extend([client_combined] + team_columns)

    # Remaining columns not already accounted for
    already_included = set(fixed_columns + client_priority_columns)
    remaining_columns = [col for col in final_df.columns if col not in already_included]

    # Final column ordering
    ordered_columns = fixed_columns + client_priority_columns + remaining_columns

    return final_df[ordered_columns]