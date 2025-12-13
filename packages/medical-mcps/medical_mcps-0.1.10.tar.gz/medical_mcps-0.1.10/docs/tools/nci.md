# NCI Clinical Trials API Server

This server provides access to the National Cancer Institute (NCI) Clinical Trials Search API, focusing on cancer clinical trials.

**Status:** Tests for this server are currently disabled due to configuration stability issues. The server itself is functional if a valid API Key is provided.

## Server Details

- **Name:** `nci-api-server`
- **Path:** `/tools/nci/mcp`
- **Base URL:** `http://localhost:8000/tools/nci/mcp` (default)

## Tools

### 1. `nci_search_trials`

Search NCI clinical trials database.

- **Parameters:**
    - `conditions` (array of strings, optional): List of disease names.
    - `interventions` (array of strings, optional): List of treatment names.
    - `phase` (string, optional): Trial phase (e.g., `PHASE1`).
    - `status` (string, optional): Recruitment status.
    - `limit` (integer, optional): Max results (default: 20).
    - `offset` (integer, optional): Pagination offset.
    - `api_key` (string, optional): NCI API Key.

### 2. `nci_get_trial`

Retrieves details for a specific trial.

- **Parameters:**
    - `trial_id` (string, required): The NCI trial identifier.
    - `api_key` (string, optional): NCI API Key.
