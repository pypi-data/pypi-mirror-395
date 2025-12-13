# Reactome API Server

This server provides access to Reactome, a curated database of biological pathways and reactions.

## Server Details

- **Name:** `reactome-api-server`
- **Path:** `/tools/reactome/mcp`
- **Base URL:** `http://localhost:8000/tools/reactome/mcp` (default)

## Tools

### 1. `reactome_get_pathway`

Retrieves detailed information about a pathway.

- **Parameters:**
    - `pathway_id` (string, required): The Reactome stable identifier.
        - **Format:** `R-ORG-NUMBER` (e.g., `R-HSA-1640170` for Human).
        - **Note:** Do not use KEGG IDs.

### 2. `reactome_query_pathways`

Searches for pathways by keyword, gene symbol, or protein name.

- **Parameters:**
    - `query` (string, required): Search term (e.g., `apoptosis`, `TAGAP`).
    - `species` (string, optional): Species filter (e.g., `Homo sapiens`, `Mus musculus`). Default: `Homo sapiens`.

### 3. `reactome_get_pathway_participants`

Retrieves all participants (genes, proteins, small molecules) in a pathway.

- **Parameters:**
    - `pathway_id` (string, required): The Reactome stable identifier.

### 4. `reactome_get_disease_pathways`

Finds pathways associated with a specific disease.

- **Parameters:**
    - `disease_name` (string, required): Disease name (e.g., `multiple sclerosis`).
