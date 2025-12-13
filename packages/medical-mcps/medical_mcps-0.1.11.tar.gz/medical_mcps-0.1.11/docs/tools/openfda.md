# OpenFDA API Server

This server provides access to OpenFDA, an interface to public FDA datasets including adverse events, drug labels, and recalls.

## Server Details

- **Name:** `openfda-api-server`
- **Path:** `/tools/openfda/mcp`
- **Base URL:** `http://localhost:8000/tools/openfda/mcp` (default)

## Tools

### 1. `openfda_search_adverse_events`

Search FDA Adverse Event Reporting System (FAERS) data.

- **Parameters:**
    - `drug` (string, optional): Drug name (e.g., `ocrelizumab`).
    - `reaction` (string, optional): Adverse reaction term (e.g., `nausea`).
    - `serious` (boolean, optional): Filter for serious events.
    - `limit` (integer, optional): Max results (default: 25).
    - `page` (integer, optional): Page number.
    - `api_key` (string, optional): OpenFDA API key.

### 2. `openfda_get_adverse_event`

Retrieves a specific adverse event report.

- **Parameters:**
    - `report_id` (string, required): The Safety Report ID.
    - `api_key` (string, optional): OpenFDA API key.

### 3. `openfda_search_drug_labels`

Search FDA drug product labels (Structured Product Labeling).

- **Parameters:**
    - `drug_name` (string, optional): Drug name.
    - `indication` (string, optional): Indication or usage.
    - `section` (string, optional): Specific label section to search.
    - `limit` (integer, optional): Max results (default: 25).
    - `page` (integer, optional): Page number.
    - `api_key` (string, optional): OpenFDA API key.

### 4. `openfda_get_drug_label`

Retrieves a full drug label.

- **Parameters:**
    - `set_id` (string, required): The Label Set ID (SPL Set ID).
    - `sections` (array of strings, optional): Specific sections to retrieve.
    - `api_key` (string, optional): OpenFDA API key.

### 5. `openfda_search_device_events`

Search Manufacturer and User Facility Device Experience (MAUDE) data.

- **Parameters:**
    - `device` (string, optional): Device name.
    - `manufacturer` (string, optional): Manufacturer name.
    - `problem` (string, optional): Device problem.
    - `limit` (integer, optional): Max results (default: 25).
    - `page` (integer, optional): Page number.
    - `api_key` (string, optional): OpenFDA API key.
