# Drug Repurposing Workflow Ideas

This document captures ideas and approaches for building drug repurposing workflows using biomedical
APIs. These ideas were developed and tested in the `ms-deep-dive` project and are shared here for
inspiration.

## Core Workflow Pattern: File System as State Machine

### Concept

Use the file system as a distributed state tracking mechanism that enables:

- **Parallel agent work** - Multiple agents can work simultaneously without conflicts
- **Resumable sessions** - Work can be paused and resumed across sessions
- **Atomic operations** - File moves provide natural locking mechanisms
- **Full audit trail** - Each drug evaluation is preserved in YAML files

### Folder Structure

```
drugs/
├── queue/          # Unevaluated drugs (status: pending)
├── in_progress/    # Currently being evaluated (prevents parallel conflicts)
├── archive/        # Not promising for repurposing
├── triage/         # Needs deeper evaluation (~10-100x more effort than initial)
├── shortlist/      # Promising candidates (10-100x more effort than triage)
└── deep_dive/      # Top candidates (10-100x more effort than shortlist)
```

### State Flow

```
unknown (queue) → triage → shortlist → deep_dive
                      ↓         ↓          ↓
                   archive   archive    archive
```

Any stage can lead to `archive` if the drug is not promising.

## Key Principles

### 1. Conservative Triage Approach

**Principle:** When uncertain about relevance, triage rather than archive.

**Rationale:**

- Repurposing often succeeds through unexpected secondary effects or off-target mechanisms
- A drug's primary indication may not reflect its full therapeutic potential
- Only archive drugs that are clearly and definitively not relevant

**Example:** A drug approved for hypertension might have immunomodulatory side effects that could be
therapeutically relevant for autoimmune diseases.

### 2. Look for Secondary Effects

**Critical:** Review ALL activities from APIs, not just the primary mechanism.

**What to look for:**

- Multi-target drugs (drugs affecting multiple pathways simultaneously)
- Off-target effects that might be therapeutically relevant
- Side effect profiles that suggest additional mechanisms
- Pleiotropic effects (one drug affecting multiple biological processes)

**Example:** A JAK inhibitor's primary mechanism is blocking cytokine signaling, but it might also
affect neuroinflammation through secondary targets.

### 3. Hypothesis Generation

**Requirement:** For every triaged drug, generate a testable hypothesis.

**Hypothesis should:**

- Connect the drug's mechanism(s) to disease pathophysiology
- Consider both primary targets and secondary/off-target effects
- Be specific and mechanistic, not generic
- Reference disease knowledge base

**Example:** "JAK2 inhibition could reduce pro-inflammatory cytokine signaling (IL-6, IFN-γ,
IL-12/IL-23) that drives MS pathogenesis, potentially reducing neuroinflammation and disease
progression"

## Evaluation Stages

### Stage 1: Initial Triage (~10 seconds per drug)

**Process:**

1. Select random drug from `queue/`
2. Move file to `in_progress/` (atomic claim - prevents parallel conflicts)
3. Quick evaluation:
   - Search ChEMBL for drug info, targets, mechanism of action
   - Use `chembl_get_activities` to see ALL activities, not just primary mechanism
   - If ChEMBL has limited data, perform web search via Tavily
   - Assess disease relevance based on:
     - Targets disease-relevant pathways?
     - Secondary/off-target effects suggest relevance?
     - Already approved for target disease? → archive
     - Clearly not relevant? → archive
4. Update YAML with findings
5. Move file to appropriate folder (`archive/` or `triage/`)

**YAML Structure:**

```yaml
drug_id: "CHEMBL123"
name: "Drug Name"
status: "triage" # or "archive"
evaluated_at: "2025-01-12T10:05:00Z"
targets: ["target1", "target2"] # Include ALL relevant targets
secondary_targets: ["target3", "target4"] # Off-target effects
mechanism: "Brief mechanism description"
secondary_effects: "Notable off-target or pleiotropic effects"
ms_relevance: "High/Medium/Low - reasoning"
reasoning: "Why triage or archive. Note secondary effects or uncertainties."
hypothesis: "REQUIRED for triaged drugs: How this drug could work for the disease"
```

### Stage 2: Triage Evaluation (~10-100x more effort)

**For drugs in `triage/`:**

1. Move to `in_progress/`
2. Deep evaluation:
   - Literature search (PubMed) for disease-related research
   - Check ClinicalTrials.gov for disease trials
   - Analyze target overlap with disease pathways (Reactome, KEGG, Pathway Commons)
   - Evaluate safety profile and contraindications
   - Assess mechanism alignment with disease unmet needs
3. Decision: **Keep** → `shortlist/` or **Kill** → `archive/`
4. Update YAML with detailed findings

### Stage 3: Shortlist → Deep Dive

- **Shortlist**: Promising candidates requiring detailed pathway analysis
- **Deep Dive**: Top candidates for comprehensive evidence synthesis

Each stage involves 10-100x more effort than the previous.

## Parallel Agent Workflow

### Conflict Prevention

- Agents claim work by moving files to `in_progress/`
- Other agents check `in_progress/` and skip those drugs
- File moves are atomic operations (no locking needed)
- Stale locks: If file in `in_progress/` >1 hour old, consider reclaiming

### Resuming Work

- Check `queue/` for unevaluated drugs
- Check `triage/` for drugs needing deeper evaluation
- Files contain full evaluation history in YAML

## API Integration Patterns

### Multi-Source Data Gathering

**Pattern:** Use multiple APIs to build comprehensive drug profiles.

**Example Workflow:**

1. **ChEMBL API** - Primary source for drug targets and mechanisms

   - `chembl_search_molecules` - Find drug by name
   - `chembl_get_molecule` - Get drug details
   - `chembl_get_mechanism` - Get primary mechanism
   - `chembl_get_activities` - Get ALL activities (critical for secondary effects)

2. **Tavily Web Search** - Fallback when ChEMBL has limited data

   - Search for: "[drug name] mechanism of action"
   - Search for: "[drug name] targets"
   - Search for: "[drug name] side effects"

3. **ClinicalTrials.gov API** - Check for existing disease trials

   - `ctg_search_studies` - Search by condition

4. **Pathway APIs** - Analyze target overlap with disease pathways
   - Reactome, KEGG, Pathway Commons for pathway analysis
   - UniProt for protein information

### Handling API Limitations

**When ChEMBL returns no data:**

- Perform web search via Tavily
- Look for DrugBank, Wikipedia, or scientific literature summaries
- Extract mechanism, targets, and side effects from web results

**When APIs timeout or fail:**

- Implement retry logic
- Use alternative APIs when available
- Document limitations in evaluation notes

## Disease-Specific Evaluation Criteria

### Example: Multiple Sclerosis

**Key Mechanisms to Evaluate Against:**

**Immune Mechanisms:**

- T/B cell activation (CD20, CD40, CD28, CTLA-4, PD-1)
- Cytokine networks (IL-17, TNF-α, IFN-γ, IL-12/IL-23)
- B cell depletion/regulation

**Neuroinflammation:**

- Microglia activation
- BBB disruption/repair
- Astrocyte activation

**Neurodegeneration:**

- Mitochondrial dysfunction
- Excitotoxicity (glutamate)
- Oxidative stress
- Axonal protection

**Remyelination:**

- OPC differentiation
- Myelin repair pathways
- Oligodendrocyte survival

**Unmet Needs:**

- Progressive MS (PPMS/SPMS)
- Neuroprotection
- Remyelination promotion

### Adapting for Other Diseases

1. Build disease knowledge base (mechanisms, pathways, unmet needs)
2. Identify key pathways using KEGG, Reactome
3. Map GWAS-identified risk genes to pathways
4. Define evaluation criteria based on disease pathophysiology
5. Prioritize drugs targeting disease-relevant pathways

## Pathway-Based Drug Discovery Strategy

### Step 1: Target Identification

Based on pathway analysis, prioritize targets that:

1. Are in disease-relevant pathways
2. Have GWAS support (genetic validation)
3. Are druggable (enzymes, receptors, cytokines)
4. Have approved drugs available

### Step 2: Drug Selection

For each target, identify:

1. Approved drugs targeting the pathway
2. Drugs in clinical trials for other indications
3. Mechanism of action alignment with disease pathogenesis
4. Safety profile and contraindications

### Step 3: Prioritization Criteria

**High Priority:**

- Targets with GWAS support
- Drugs approved for similar diseases
- Strong mechanistic rationale
- Favorable safety profile

**Medium Priority:**

- Targets in validated disease pathways
- Drugs with acceptable safety profile
- Moderate mechanistic support

**Low Priority:**

- Targets with limited disease evidence
- Drugs with significant toxicity
- Contradictory evidence

## Implementation Example

### Pseudocode for Agent

```python
# Pseudocode for agent
for drug_file in random_50_drugs:
    # 1. Claim work
    move(drug_file, "queue/", "in_progress/")

    # 2. Read drug info
    drug = read_yaml(drug_file)

    # 3. Search ChEMBL
    chembl_results = chembl_search_molecules(drug["name"])
    if chembl_results:
        molecule = chembl_get_molecule(chembl_results[0]["molecule_chembl_id"])
        mechanism = chembl_get_mechanism(chembl_results[0]["molecule_chembl_id"])
        activities = chembl_get_activities(chembl_results[0]["molecule_chembl_id"])  # Get ALL activities
        targets = extract_targets(mechanism)
        secondary_targets = extract_secondary_targets(activities)  # Look for off-target effects
    else:
        # If ChEMBL has no data, do web search
        web_results = tavily_search(f"{drug['name']} mechanism of action targets")
        # Extract information from web search

    # 4. Assess disease relevance - be conservative
    if has_disease_relevant_targets(targets) or has_disease_relevant_secondary_effects(secondary_targets):
        drug["status"] = "triage"
        drug["targets"] = targets
        drug["secondary_targets"] = secondary_targets
        drug["mechanism"] = mechanism["mechanism_of_action_type"]
        drug["disease_relevance"] = assess_relevance(targets, secondary_targets)
        # REQUIRED: Generate hypothesis for how this drug could work
        drug["hypothesis"] = generate_hypothesis(targets, secondary_targets, mechanism, disease_knowledge)
    elif is_clearly_not_relevant(drug):  # Only archive if clearly not relevant
        drug["status"] = "archive"
        drug["reasoning"] = "Clear exclusion reason"
    else:
        # When in doubt, triage
        drug["status"] = "triage"
        drug["reasoning"] = "Uncertain relevance - requires deeper evaluation"
        drug["hypothesis"] = generate_hypothesis(targets, secondary_targets, mechanism, disease_knowledge)

    # 5. Update and move
    write_yaml(drug_file, drug)
    move(drug_file, "in_progress/", f"{drug['status']}/")
```

## Lessons Learned

### What Works Well

1. **File system state tracking** - Simple, reliable, enables parallel work
2. **YAML files** - Human-readable, preserves full evaluation history
3. **Multi-stage filtering** - Prevents premature elimination of promising candidates
4. **Conservative triage** - Captures unexpected repurposing opportunities
5. **Hypothesis generation** - Forces mechanistic thinking about drug-disease connections

### Challenges

1. **API rate limits** - Need to implement retry logic and caching
2. **Incomplete data** - Some drugs have limited ChEMBL data, require web search fallback
3. **Large datasets** - GWAS and UniProt results require focused analysis
4. **API errors** - Need robust error handling and alternative data sources

### Future Improvements

1. **Automated pathway analysis** - Use Reactome/KEGG APIs to automatically assess target-disease
   pathway overlap
2. **Literature mining** - Integrate PubMed API for automated literature review
3. **Confidence scoring** - Develop quantitative confidence scores based on evidence strength
4. **Batch processing** - Optimize API calls for batch evaluation
5. **Visualization** - Generate pathway diagrams showing drug-target-disease connections

## References

These ideas were developed in the `ms-deep-dive` project:

- `agents/tasks/2025-01-12_00-00-00-drug-repurposing-workflows-requirements.md` - Detailed workflow
  documentation
- `AGENTS.md` - Agent definitions and workflow documentation
- `knowledge/10-drug-repurposing-opportunities.md` - Example drug repurposing analysis

## Tools Used

- **ChEMBL API** - Drug targets, mechanisms, bioactivity
- **ClinicalTrials.gov API** - Disease-related trials
- **Tavily** - Web search (DrugBank, PubMed, general info)
- **PubMed MCP** - Literature search
- **Reactome/KEGG/Pathway Commons** - Pathway analysis
- **UniProt** - Protein information
- **GWAS Catalog** - Genetic association data

---

**Note:** These workflows are designed to be adaptable to any disease. The key is building a
comprehensive disease knowledge base first, then systematically evaluating drugs against
disease-relevant pathways and mechanisms.
