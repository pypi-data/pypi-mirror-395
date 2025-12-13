# MyVariant.info API Server

This server provides access to MyVariant.info, a high-performance variant query service providing comprehensive variant annotation data.

## Server Details

- **Name:** `myvariant-api-server`
- **Path:** `/tools/myvariant/mcp`
- **Base URL:** `http://localhost:8000/tools/myvariant/mcp` (default)

## Tools

### 1. `myvariant_get_variant`

Retrieves detailed annotation for a specific genetic variant.

- **Parameters:**
    - `variant_id` (string, required): The variant identifier.
        - **Supported Formats:**
            - **HGVS ID:** (e.g., `chr7:g.140453136A>T`) - Human Genome Variation Society nomenclature.
            - **dbSNP rsID:** (e.g., `rs56116432`).
            - **ClinVar ID:** (e.g., `RCV000000012`).
            - **COSMIC ID:** (e.g., `COSM1122`).
    - `include_external` (boolean, optional): Whether to include external links (default: `False`).

### 2. `myvariant_search_variants`

Search for variants based on various criteria.

- **Parameters:**
    - `gene` (string, optional): Gene symbol or ID (e.g., `CDK2`, `1017`).
    - `rsid` (string, optional): dbSNP rsID (e.g., `rs56116432`).
    - `hgvsp` (string, optional): Protein change in HGVS format.
    - `hgvsc` (string, optional): Coding sequence change in HGVS format.
    - `significance` (string, optional): Clinical significance (e.g., `pathogenic`, `benign`).
    - `min_frequency` (number, optional): Minimum allele frequency.
    - `max_frequency` (number, optional): Maximum allele frequency.
    - `cadd_min` (number, optional): Minimum CADD score (deleteriousness).
    - `limit` (integer, optional): Maximum results (default: 50).
    - `offset` (integer, optional): Pagination offset.
    - **Note:** Provide at least one filter parameter for a meaningful search.
