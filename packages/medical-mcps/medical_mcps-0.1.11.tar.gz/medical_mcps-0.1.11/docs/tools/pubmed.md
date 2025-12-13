# PubMed/PubTator3 API Server

This server provides access to biomedical literature via PubMed and PubTator3, including advanced semantic search for genes, diseases, and chemicals.

## Server Details

- **Name:** `pubmed-api-server`
- **Path:** `/tools/pubmed/mcp`
- **Base URL:** `http://localhost:8000/tools/pubmed/mcp` (default)

## Tools

### 1. `pubmed_search_articles`

Search for articles using semantic annotations (PubTator3).

- **Parameters:**
    - `genes` (array of strings, optional): Gene names (e.g., `['BRAF']`).
    - `diseases` (array of strings, optional): Disease names (e.g., `['melanoma']`).
    - `chemicals` (array of strings, optional): Chemical/drug names (e.g., `['vemurafenib']`).
    - `variants` (array of strings, optional): Variant names (e.g., `['V600E']`).
    - `keywords` (array of strings, optional): Additional text keywords.
    - `limit` (integer, optional): Max results (default: 10).
    - `page` (integer, optional): Page number.

### 2. `pubmed_get_article`

Retrieves detailed information about a specific article.

- **Parameters:**
    - `pmid_or_doi` (string, required): The article identifier.
        - **PMID:** PubMed ID (numeric, e.g., `34397683`).
        - **DOI:** Digital Object Identifier (e.g., `10.1101/...`).
    - `full` (boolean, optional): Fetch full text if available (default: `False`).

### 3. `pubmed_search_preprints`

Search for preprints (bioRxiv/medRxiv) via Europe PMC.

- **Parameters:**
    - `query` (string, required): Search query.
    - `limit` (integer, optional): Max results (default: 10).
