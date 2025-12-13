# Node Normalization API Server

This server provides access to the Node Normalization service, which standardizes identifiers (CURIEs) across various biological databases and maps them to BioLink Model types.

## Server Details

- **Name:** `nodenorm-api-server`
- **Path:** `/tools/nodenorm/mcp`
- **Base URL:** `http://localhost:8000/tools/nodenorm/mcp` (default)

## Tools

### 1. `nodenorm_get_normalized_nodes`

Normalizes one or more CURIEs to their preferred identifiers and types.

- **Parameters:**
    - `curies` (string, required): Comma-separated list of CURIEs to normalize.
        - **Format:** `PREFIX:ID` (e.g., `NCBIGene:7157`, `MONDO:0004972`, `DRUGBANK:DB00001`).
    - `conflate` (boolean, optional): Whether to apply gene/protein conflation (default: `True`).
    - `drug_chemical_conflate` (boolean, optional): Whether to apply drug/chemical conflation (default: `False`).
    - `description` (boolean, optional): Include descriptions in output (default: `False`).
    - `individual_types` (boolean, optional): Include types for each equivalent identifier (default: `False`).
    - `include_taxa` (boolean, optional): Include taxon info (default: `True`).

### 2. `nodenorm_get_semantic_types`

Returns the list of BioLink semantic types that the service can normalize.

- **Parameters:** None.

### 3. `nodenorm_get_curie_prefixes`

Returns the list of supported CURIE prefixes and their usage counts.

- **Parameters:** None.

### 4. `nodenorm_get_allowed_conflations`

Returns the types of conflations (e.g., Gene/Protein) available.

- **Parameters:** None.
