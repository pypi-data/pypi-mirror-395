# BioThings Suite (MyGene, MyDisease, MyChem)

This server provides access to the BioThings suite of APIs, offering unified access to gene, disease, and chemical annotation data.

## Server Details

- **Name:** `biothings-api-server`
- **Path:** `/tools/biothings/mcp`
- **Base URL:** `http://localhost:8000/tools/biothings/mcp` (default)

## Tools

### 1. `mygene_get_gene`

Retrieves gene annotation data from MyGene.info.

- **Description:** Get gene information by ID or symbol.
- **Parameters:**
    - `gene_id_or_symbol` (string, required): The identifier or symbol of the gene.
        - **Supported IDs:**
            - **Entrez Gene ID:** (e.g., `1017`) - NCBI numeric identifier.
            - **Ensembl Gene ID:** (e.g., `ENSG00000123374`) - Standard Ensembl identifier.
            - **Gene Symbol:** (e.g., `CDK2`) - Official HGNC symbol.
            - **RefSeq ID:** (e.g., `NM_001798`) - NCBI Reference Sequence identifier.
            - **Uniprot ID:** (e.g., `P24941`) - UniProt Knowledgebase accession.
    - `fields` (array of strings, optional): Specific fields to return (e.g., `['symbol', 'name', 'taxid']`). If omitted, returns default fields.

### 2. `mydisease_get_disease`

Retrieves disease annotation data from MyDisease.info.

- **Description:** Get disease information by ID or name.
- **Parameters:**
    - `disease_id_or_name` (string, required): The identifier or name of the disease.
        - **Supported IDs:**
            - **MONDO ID:** (e.g., `MONDO:0004972`) - Monarch Disease Ontology identifier.
            - **DOID:** (e.g., `DOID:10652`) - Disease Ontology identifier.
            - **UMLS CUI:** (e.g., `C0002395`) - Unified Medical Language System Concept Unique Identifier.
            - **Disease Name:** (e.g., `Alzheimer's disease`) - Common text name (fuzzy matching may occur).
    - `fields` (array of strings, optional): Specific fields to return.

### 3. `mychem_get_drug`

Retrieves drug and chemical annotation data from MyChem.info.

- **Description:** Get drug/chemical information by ID or name.
- **Parameters:**
    - `drug_id_or_name` (string, required): The identifier or name of the drug/chemical.
        - **Supported IDs:**
            - **ChemBL ID:** (e.g., `CHEMBL1308`) - ChEMBL identifier.
            - **DrugBank ID:** (e.g., `DB00533`) - DrugBank identifier.
            - **PubChem CID:** (e.g., `1983`) - PubChem Compound Identifier.
            - **UNII:** (e.g., `7S5I7G3JQL`) - FDA Unique Ingredient Identifier.
            - **Drug Name:** (e.g., `imatinib`) - Common text name.
    - `fields` (array of strings, optional): Specific fields to return.
