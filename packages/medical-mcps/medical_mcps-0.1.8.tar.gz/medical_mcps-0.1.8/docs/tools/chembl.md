# ChEMBL API Server

This server provides access to the ChEMBL database, a manually curated database of bioactive molecules with drug-like properties.

## Server Details

- **Name:** `chembl-api-server`
- **Path:** `/tools/chembl/mcp`
- **Base URL:** `http://localhost:8000/tools/chembl/mcp` (default)

## Tools

### 1. `chembl_get_molecule`

Retrieves detailed information about a molecule (drug or compound) by its ChEMBL ID.

- **Parameters:**
    - `molecule_chembl_id` (string, required): The ChEMBL identifier for the molecule.
        - **Format:** `CHEMBL` followed by digits (e.g., `CHEMBL2108041`).
        - **Source:** Can be found via `chembl_search_molecules` or from other databases like MyChem.

### 2. `chembl_search_molecules`

Searches for molecules by name or synonym.

- **Parameters:**
    - `query` (string, required): Search term (e.g., `ocrelizumab`, `aspirin`).
    - `limit` (integer, optional): Maximum number of results to return (default: 20).

### 3. `chembl_get_target`

Retrieves detailed information about a target (protein) by its ChEMBL ID.

- **Parameters:**
    - `target_chembl_id` (string, required): The ChEMBL identifier for the target.
        - **Format:** `CHEMBL` followed by digits (e.g., `CHEMBL2058`).
        - **Source:** Can be found via `chembl_search_targets`.

### 4. `chembl_search_targets`

Searches for targets (proteins/organisms) by name or synonym.

- **Parameters:**
    - `query` (string, required): Search term (e.g., `CD20`, `MS4A1`).
    - `limit` (integer, optional): Maximum number of results to return (default: 20).

### 5. `chembl_get_activities`

Retrieves bioactivity data (Ki, IC50, etc.) for a target or molecule.

- **Parameters:**
    - `target_chembl_id` (string, optional): Filter by ChEMBL target ID.
    - `molecule_chembl_id` (string, optional): Filter by ChEMBL molecule ID.
    - `limit` (integer, optional): Maximum number of results (default: 50).
    - **Note:** At least one of `target_chembl_id` or `molecule_chembl_id` should be provided.

### 6. `chembl_get_mechanism`

Retrieves the mechanism of action for a specific molecule.

- **Parameters:**
    - `molecule_chembl_id` (string, required): The ChEMBL identifier for the molecule.

### 7. `chembl_find_drugs_by_target`

Finds all drugs or compounds that target a specific protein.

- **Parameters:**
    - `target_chembl_id` (string, required): The ChEMBL identifier for the target.
    - `limit` (integer, optional): Maximum number of results (default: 50).

### 8. `chembl_find_drugs_by_indication`

Finds drugs indicated for a specific disease.

- **Parameters:**
    - `disease_query` (string, required): Disease name or MeSH heading (e.g., `Multiple Sclerosis`).
    - `limit` (integer, optional): Maximum number of results (default: 50).

### 9. `chembl_get_drug_indications`

Retrieves all approved indications for a specific drug.

- **Parameters:**
    - `molecule_chembl_id` (string, required): The ChEMBL identifier for the molecule.
