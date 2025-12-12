# FermaCongress

**FermaCongress** is a Python package for automating congress-level data extraction, management, and analysis at ZoomRx - Ferma Congress.

## 📦 Installation

```bash
pip install FermaCongress
pip install --upgrade FermaCongress
```

## 🔑 Setup

Create a `.env` file with your Ferma credentials:

```env
FERMA_USERNAME=your_username
FERMA_PASSWORD=your_password
```

---

## 📚 Modules Overview

| Module | Purpose | Authentication |
|--------|---------|----------------|
| `auth` | Login to Admin/Support portals | N/A |
| `extractferma` | Extract congress data | Admin Portal |
| `postferma` | Post tweets, trigger buzz scores | Admin Portal |
| `planner` | Generate planning files | Admin Portal |
| `annotate` | AI keyword annotation | Support Portal |
| `trials` | Extract clinical trial data | None (Public APIs) |
| `formatexcel` | Professional Excel formatting | None |

---

# 🔐 auth - Authentication
A lightweight utility that handles login for both the Ferma Admin and Support portals, returning ready-to-use headers or sessions.

```python
from FermaCongress.auth import adminlogin, supportlogin

# Admin Portal Authentication
adminclient = adminlogin(".env")

# Support Portal Authentication
supportclient = supportlogin(".env")

# With Encoded credentials for Admin Portal
adminclient = adminlogin(".env", format="ENCODED")
```

---

# 📥 extractferma - Data Extraction

Extract various types of congress data from the Admin Portal.

```python
from FermaCongress.auth import adminlogin
from FermaCongress.extractferma import (
    get_all_sessions,    # Session metadata
    get_skg,             # Session keywords
    get_fullabstracts,   # Full abstract texts
    get_summary,         # AI-generated summaries
    get_tweets,          # Tweet data with buzz scores
    get_priority         # Priority data from all planners
)

adminclient = adminlogin(".env")
CONGRESS_ID = "221"

# Extract data
sessions = get_all_sessions(adminclient, CONGRESS_ID)
keywords = get_skg(adminclient, CONGRESS_ID)
tweets = get_tweets(adminclient, CONGRESS_ID)
abstracts = get_fullabstracts(adminclient, CONGRESS_ID)
summaries = get_summary(adminclient, CONGRESS_ID)

# Get priorities with filtering
priority = get_priority(adminclient, CONGRESS_ID, include=["ClientA"], exclude=["ClientB"])
```

> **Note:** `include` and `exclude` accept Tenant Names only (not Team Names).

---

# 🔄 postferma - Post Data

Upload tweets and trigger buzz score calculations.

```python
from FermaCongress.auth import adminlogin
from FermaCongress.postferma import addtweets, modifytweets, populatebuzz

adminclient = adminlogin(".env")
CONGRESS_ID = "221"

# Add new tweets
addtweets(adminclient, tweets_add_df, CONGRESS_ID)

# Modify existing tweets
modifytweets(adminclient, tweets_modify_df, CONGRESS_ID)

# Recalculate buzz scores
populatebuzz(adminclient, CONGRESS_ID)
```

---

# 🗂️ planner - Generate Planner Files

Create enriched planning files with session data, keywords, and priorities.

```python
from FermaCongress.auth import adminlogin
from FermaCongress.planner import baseplanner

adminclient = adminlogin(".env")

# With priorities
planner_df = baseplanner(adminclient, "221", PLANNER_ID="4")

# Without priorities
planner_df = baseplanner(adminclient, "221")
```

**Returns:** DataFrame with session details, keywords, drugs, priorities, dates, locations

---

# 🧠 annotate - Knowledge Base Annotation

Annotate data using Ferma's AI knowledge base.

**Input Requirements:**
- DataFrame must contain an `id` column

```python
from FermaCongress.auth import supportlogin
from FermaCongress.annotate import annotate
import pandas as pd

supportclient = supportlogin(".env")

# Prepare input data
input_df = pd.read_excel("input.xlsx") / pd.read_csv("input.csv")

# Annotate
result = annotate(
    client=supportclient,
    input_df=input_df,
    needles=[1, 1],        # [kb_status, nct_status]: 1=enabled, 0=disabled
    long_table=True        # True=long format, False=pivot format
)
```

**Parameters:**
- `needles`: `[kb_status, nct_status]` - Enable/disable knowledge base and NCT annotation
- `long_table`: Output format (long or pivot)
- `custom_needles_df`: Optional custom keywords DataFrame

---

# 🏥 trials - Clinical Trials

Extract trial data from ClinicalTrials.gov, EU CTIS, and EudraCT.

```python
from FermaCongress.trials import extracttrials

df_wide, df_long = extracttrials(df, column='nct_ids', delimiter=';;')
```

**Supported Formats:**
- NCT: `NCT12345678`
- EU CTIS: `2022-500000-11-00`
- EudraCT: `2022-500000-11`

**Returns:** Study ID, Phase, Enrollment, Lead Sponsor, Collaborators

---

# ⚙️ formatexcel - Excel Formatting

Apply Ferma-branded styling to Excel files.

```python
from FermaCongress.formatexcel import format

# From DataFrame
format(dataframe=df, output_path="output.xlsx")

# From Excel file
format(input_path="raw.xlsx", output_path="formatted.xlsx", input_sheet="Sheet1")

# From CSV file
format(input_path="data.csv", output_path="output.xlsx", output_sheet="Sheet1")
```

---