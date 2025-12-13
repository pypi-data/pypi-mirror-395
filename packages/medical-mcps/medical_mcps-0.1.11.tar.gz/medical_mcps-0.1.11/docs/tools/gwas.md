# GWAS Catalog API Server

This server provides access to the NHGRI-EBI GWAS Catalog, a quality-controlled, manually curated, literature-derived collection of all published genome-wide association studies and summary statistics.

## Server Details

- **Name:** `gwas-api-server`
- **Path:** `/tools/gwas/mcp`
- **Base URL:** `http://localhost:8000/tools/gwas/mcp` (default)

## Tools

### 1. `gwas_search_associations`

Search for SNP-trait associations.

- **Parameters:**
    - `query` (string, optional): General search query.
    - `variant_id` (string, optional): Variant identifier (rsID, e.g., `rs3093017`).
    - `study_id` (string, optional): Study identifier (GCST ID, e.g., `GCST90132222`).
    - `trait` (string, optional): Trait name (e.g., `diabetes`).
    - `size` (integer, optional): Number of results per page (default: 20).
    - `page` (integer, optional): Page number (0-indexed).

### 2. `gwas_get_association`

Retrieves details for a specific association by its ID.

- **Parameters:**
    - `association_id` (string, required): The internal GWAS Catalog identifier for the association.

### 3. `gwas_get_variant`

Retrieves information about a Single Nucleotide Polymorphism (SNP).

- **Parameters:**
    - `variant_id` (string, required): The SNP rsID.
        - **Format:** `rs` followed by digits (e.g., `rs3093017`).

### 4. `gwas_search_variants`

Searches for SNPs/variants by rsID.

- **Parameters:**
    - `query` (string, optional): SNP rsID to search for (e.g., `rs3093017`).
    - `size` (integer, optional): Number of results per page (default: 20).
    - `page` (integer, optional): Page number (0-indexed).

### 5. `gwas_search_studies`

Searches for genome-wide association studies.

- **Parameters:**
    - `query` (string, optional): General search query.
    - `trait` (string, optional): Trait name (e.g., `multiple sclerosis`).
    - `size` (integer, optional): Number of results per page (default: 20).
    - `page` (integer, optional): Page number (0-indexed).

### 6. `gwas_get_study`

Retrieves details for a specific study.

- **Parameters:**
    - `study_id` (string, required): The GWAS Catalog Study ID.
        - **Format:** `GCST` followed by digits (e.g., `GCST90132222`).

### 7. `gwas_search_traits`

Searches for traits (EFO terms) in the catalog.

- **Parameters:**
    - `query` (string, optional): Trait name or keyword (e.g., `autoimmune`).
    - `size` (integer, optional): Number of results per page (default: 20).
    - `page` (integer, optional): Page number (0-indexed).

### 8. `gwas_get_trait`

Retrieves details for a specific trait (EFO term).

- **Parameters:**
    - `trait_id` (string, required): The EFO identifier for the trait.
        - **Format:** `EFO_` followed by digits (e.g., `EFO_0000400`).
