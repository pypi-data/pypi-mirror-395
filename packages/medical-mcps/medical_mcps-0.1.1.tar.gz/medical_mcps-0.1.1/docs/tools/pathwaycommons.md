# Pathway Commons API Server

This server provides access to Pathway Commons, a convenient point of access to biological pathway and network information.

## Server Details

- **Name:** `pathwaycommons-api-server`
- **Path:** `/tools/pathwaycommons/mcp`
- **Base URL:** `http://localhost:8000/tools/pathwaycommons/mcp` (default)

## Tools

### 1. `pathwaycommons_search`

Search for biological entities (pathways, proteins, etc.).

- **Parameters:**
    - `q` (string, required): Search query (e.g., `TP53`, `glycolysis`).
    - `type` (string, optional): Entity type filter. Default: `Pathway`.
        - **Values:** `Pathway`, `Protein`, `Gene`, `Interaction`, etc.
        - **Note:** Use `Protein` for searching by gene symbol; `Gene` often returns few results.
    - `datasource` (string, optional): Filter by data source (e.g., `reactome`, `kegg`).
    - `page` (integer, optional): Page number.

### 2. `pathwaycommons_get_pathway_by_uri`

Retrieves a pathway or entity by its URI.

- **Parameters:**
    - `uri` (string, required): The BioPAX element URI.
        - **Example:** `http://identifiers.org/reactome/R-HSA-1640170`
    - `format` (string, optional): Output format (`json`, `xml`, `biopax`). Default: `json`.

### 3. `pathwaycommons_top_pathways`

Retrieves "top-level" pathways (root processes).

- **Parameters:**
    - `gene` (string, optional): Filter by gene symbol (e.g., `BRCA1`).
    - `datasource` (string, optional): Filter by data source.
    - `limit` (integer, optional): Max results.

### 4. `pathwaycommons_graph`

Retrieves a network graph around a source entity.

- **Parameters:**
    - `source` (string, required): Source entity ID in CURIE format.
        - **Format:** `PREFIX:ID` (e.g., `HGNC:6008`, `UniProt:P01589`).
    - `target` (string, optional): Target entity ID (for path finding).
    - `kind` (string, optional): Graph type.
        - **Values:** `neighborhood`, `pathsbetween`, `pathsfromto`, `commonstream`.
    - `limit` (integer, optional): Path length.

### 5. `pathwaycommons_traverse`

Traverses the graph from a URI using path expressions.

- **Parameters:**
    - `uri` (string, required): Starting URI.
    - `path` (string, required): Path expression (e.g., `Pathway/pathwayComponent:Interaction/participant*/displayName`).
    - `format` (string, optional): Output format.
