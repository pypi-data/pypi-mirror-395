# KEGG API Server

This server provides access to the Kyoto Encyclopedia of Genes and Genomes (KEGG) database, a major resource for understanding high-level functions and utilities of the biological system.

## Server Details

- **Name:** `kegg-api-server`
- **Path:** `/tools/kegg/mcp`
- **Base URL:** `http://localhost:8000/tools/kegg/mcp` (default)

## Tools

### 1. `kegg_list_pathways`

Lists KEGG pathways.

- **Parameters:**
    - `organism` (string, optional): KEGG organism code (e.g., `hsa` for human). If omitted, lists reference pathways (`map`).

### 2. `kegg_find_pathways`

Finds pathways matching a keyword.

- **Parameters:**
    - `query` (string, required): Search term (e.g., `cancer`, `apoptosis`).

### 3. `kegg_get_pathway_info`

Retrieves detailed information about a specific pathway.

- **Parameters:**
    - `pathway_id` (string, required): The KEGG pathway identifier.
        - **Format:** `[organism_code][5_digits]` (e.g., `hsa04010`).

### 4. `kegg_find_genes`

Finds genes matching a keyword.

- **Parameters:**
    - `query` (string, required): Search term (e.g., `p53`, `kinase`).
    - `organism` (string, optional): KEGG organism code (e.g., `hsa`).

### 5. `kegg_get_gene`

Retrieves detailed information about a specific gene.

- **Parameters:**
    - `gene_id` (string, required): The KEGG gene identifier.
        - **Format:** `[organism_code]:[gene_id]` (e.g., `hsa:7157`).

### 6. `kegg_find_diseases`

Finds diseases matching a keyword.

- **Parameters:**
    - `query` (string, required): Search term (e.g., `cancer`).

### 7. `kegg_get_disease`

Retrieves detailed information about a specific disease entry.

- **Parameters:**
    - `disease_id` (string, required): The KEGG disease identifier.
        - **Format:** `H` followed by 5 digits (e.g., `H00001`).

### 8. `kegg_link_pathway_genes`

Retrieves a list of genes associated with a specific pathway.

- **Parameters:**
    - `pathway_id` (string, required): The KEGG pathway identifier (e.g., `hsa04010`).
