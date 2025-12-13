# UniProt API Server

This server provides access to UniProt, the world's leading high-quality, comprehensive and freely accessible resource of protein sequence and functional information.

## Server Details

- **Name:** `uniprot-api-server`
- **Path:** `/tools/uniprot/mcp`
- **Base URL:** `http://localhost:8000/tools/uniprot/mcp` (default)

## Tools

### 1. `uniprot_get_protein`

Retrieves detailed information about a protein.

- **Parameters:**
    - `accession` (string, required): UniProt accession (e.g., `P00520`).
    - `format` (string, optional): Output format (`json`, `fasta`, `xml`). Default: `json`.
    - `fields` (array of strings, optional): Specific fields to return.

### 2. `uniprot_search_proteins`

Searches for proteins in UniProtKB.

- **Parameters:**
    - `query` (string, required): Search query (e.g., `gene:BRCA1`).
    - `format` (string, optional): Output format.
    - `limit` (integer, optional): Max results.
    - `offset` (integer, optional): Pagination offset.

### 3. `uniprot_get_protein_sequence`

Retrieves the protein sequence in FASTA format.

- **Parameters:**
    - `accession` (string, required): UniProt accession.

### 4. `uniprot_get_disease_associations`

Retrieves disease associations for a protein.

- **Parameters:**
    - `accession` (string, required): UniProt accession.

### 5. `uniprot_map_ids`

Maps identifiers between databases.

- **Parameters:**
    - `from_db` (string, required): Source database (e.g., `Gene_Name`).
    - `to_db` (string, required): Target database (e.g., `UniProtKB`).
    - `ids` (string, required): Comma-separated list of identifiers.
    - **Note:** This is an async job that polls for results.
