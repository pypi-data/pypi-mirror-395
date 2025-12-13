# ClinicalTrials.gov API Server

This server provides access to ClinicalTrials.gov (version 2 API), the largest registry of clinical trials.

## Server Details

- **Name:** `ctg-api-server`
- **Path:** `/tools/ctg/mcp`
- **Base URL:** `http://localhost:8000/tools/ctg/mcp` (default)

## Tools

### 1. `ctg_search_studies`

General search for clinical trials with optional filters.

- **Parameters:**
    - `condition` (string, optional): Condition or disease query (e.g., `multiple sclerosis`).
    - `intervention` (string, optional): Intervention or treatment query (e.g., `ocrelizumab`).
    - `status` (string, optional): Comma-separated list of recruitment statuses (e.g., `RECRUITING,COMPLETED`).
        - **Common Statuses:** `RECRUITING`, `NOT_YET_RECRUITING`, `COMPLETED`, `TERMINATED`, `SUSPENDED`, `WITHDRAWN`.
    - `page_size` (integer, optional): Number of results per page (default: 10).
    - **Note:** At least one of `condition` or `intervention` should be provided for a meaningful search.

### 2. `ctg_get_study`

Retrieves detailed information about a single clinical trial by its NCT ID.

- **Parameters:**
    - `nct_id` (string, required): The ClinicalTrials.gov identifier.
        - **Format:** `NCT` followed by 8 digits (e.g., `NCT00841061`).
        - **Source:** Can be found via search tools or from other databases like ChEMBL.

### 3. `ctg_search_by_condition`

Convenience tool to search trials specifically by condition/disease.

- **Parameters:**
    - `condition_query` (string, required): Condition or disease name.
    - `status` (string, optional): Comma-separated list of statuses.
    - `page_size` (integer, optional): Number of results per page (default: 10).

### 4. `ctg_search_by_intervention`

Convenience tool to search trials specifically by intervention/treatment.

- **Parameters:**
    - `intervention_query` (string, required): Intervention or treatment name.
    - `status` (string, optional): Comma-separated list of statuses.
    - `page_size` (integer, optional): Number of results per page (default: 10).

### 5. `ctg_get_study_metadata`

Retrieves metadata about the ClinicalTrials.gov data model, including available fields and their descriptions.

- **Parameters:** None.
