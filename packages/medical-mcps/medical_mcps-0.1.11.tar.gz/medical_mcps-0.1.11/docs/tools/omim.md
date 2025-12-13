# OMIM API Server

This server provides access to Online Mendelian Inheritance in Man (OMIM), a comprehensive compendium of human genes and genetic phenotypes.

## Server Details

- **Name:** `omim-api-server`
- **Path:** `/tools/omim/mcp`
- **Base URL:** `http://localhost:8000/tools/omim/mcp` (default)

## Tools

### 1. `omim_get_entry`

Retrieves detailed information about a specific OMIM entry.

- **Parameters:**
    - `mim_number` (string, required): The MIM number identifier (e.g., `104300`).
    - `api_key` (string, required): Your OMIM API Key.
    - `include` (string, optional): Fields to include (e.g., `text`, `allelicVariantList`, `geneMap`). Default: `text`.

### 2. `omim_search_entries`

Searches OMIM entries.

- **Parameters:**
    - `search` (string, required): Search query.
    - `api_key` (string, required): Your OMIM API Key.
    - `limit` (integer, optional): Maximum number of results (default: 20).
    - `start` (integer, optional): Starting index.

### 3. `omim_get_gene`

Retrieves gene information by symbol.

- **Parameters:**
    - `gene_symbol` (string, required): Gene symbol (e.g., `BRCA1`).
    - `api_key` (string, required): Your OMIM API Key.

### 4. `omim_search_genes`

Searches for genes in OMIM.

- **Parameters:**
    - `search` (string, required): Search query.
    - `api_key` (string, required): Your OMIM API Key.

### 5. `omim_get_phenotype`

Retrieves phenotype information by MIM number.

- **Parameters:**
    - `mim_number` (string, required): The MIM number.
    - `api_key` (string, required): Your OMIM API Key.

### 6. `omim_search_phenotypes`

Searches for phenotypes in OMIM.

- **Parameters:**
    - `search` (string, required): Search query (e.g., `diabetes`).
    - `api_key` (string, required): Your OMIM API Key.
