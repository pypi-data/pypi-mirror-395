# Playbooks Architecture (Archived)

This document describes the conceptual architecture and structure of the playbooks system that was previously implemented in the medical MCPs project. This is intended as a reference for potential future reimplementation.

## Overview

The playbooks system provided a declarative, framework-based approach to drug repurposing and medical research. Instead of ad-hoc tool usage, playbooks encoded domain expertise and established scientific methodologies as executable workflows.

**Core Philosophy**: Start with what you know (drug, disease, target, pathway, or genetic variant) and systematically explore using established scientific frameworks.

## Playbook Concepts

### What is a Playbook?

A playbook is a structured, multi-step workflow that guides users through a specific drug discovery or repurposing methodology. Each playbook:

- Has a **starting point** (a single entity type: drug, disease, target, pathway, genetic variant, or phenotype)
- Follows a **first-principles scientific framework** (e.g., reverse pharmacology, network medicine, Mendelian randomization)
- Consists of **ordered steps** with recommended tools and validation criteria
- Produces **expected outputs** (candidate drugs, validated targets, mechanistic hypotheses, etc.)

### The 8 Playbook Types

The system implemented 8 distinct playbooks, each representing a different scientific approach:

#### 1. **Drug-Centric Discovery**
- **Starting Point**: A drug of interest
- **Framework**: Reverse Pharmacology
- **Concept**: If a drug works against one disease, what other diseases might it treat?
- **Key Approach**:
  - Query the drug's full activity profile (ChEMBL)
  - Identify off-target activities and secondary mechanisms
  - Find disease associations with these activities
  - Validate with literature and clinical trials
- **Example**: Start with a cardiovascular drug, discover potential oncology applications

#### 2. **Disease-Centric Discovery**
- **Starting Point**: A disease of interest
- **Framework**: Systems Biology / Network Medicine
- **Concept**: Map the disease landscape comprehensively, then identify intervention points
- **Key Approach**:
  - Identify disease-relevant pathways (Reactome, KEGG)
  - Find GWAS variants associated with the disease
  - Validate pathways against disease biology
  - Search for drugs that modulate disease pathways
  - Check clinical trial landscape
- **Example**: Start with multiple sclerosis, find all relevant immune pathways, identify drugs that modulate them

#### 3. **Target-Centric Discovery**
- **Starting Point**: A validated disease target
- **Framework**: Target-Based Drug Discovery
- **Concept**: Once you have a good target, find all compounds that hit it
- **Key Approach**:
  - Verify target validation (disease association, pathway relevance)
  - Find all ChEMBL compounds with activity against the target
  - Prioritize by binding affinity, selectivity, and mechanism
  - Check if any are already approved drugs (repositioning opportunity)
  - Review off-target effects
- **Example**: Start with CD20 as MS target, find all antibodies and small molecules, discover new modalities

#### 4. **Pathway-Centric Discovery**
- **Starting Point**: A disease-dysregulated pathway
- **Framework**: Network Pharmacology
- **Concept**: Understand pathway topology and identify the best intervention points
- **Key Approach**:
  - Map the complete pathway (Reactome, KEGG, Pathway Commons)
  - Identify hub proteins and critical nodes
  - Find drugs that modulate pathway components
  - Assess network effects and robustness
  - Check for compensatory pathways
- **Example**: Start with the T-cell activation pathway, identify multiple intervention points, find combination therapy opportunities

#### 5. **Genetic-Centric Discovery**
- **Starting Point**: A disease-associated genetic variant
- **Framework**: Mendelian Randomization / Functional Genomics
- **Concept**: Use genetic evidence to prioritize targets and drugs
- **Key Approach**:
  - Identify protective vs. risk variants
  - Map variants to genes and regulatory elements
  - Verify causal relationships (Mendelian randomization)
  - Find drugs that modulate these genetic targets
  - Validate with population data
- **Example**: Start with MS risk variant in IL7R, identify IL7R as validated target, find drugs hitting IL7R

#### 6. **Network-Centric Discovery**
- **Starting Point**: A disease network (multiple interconnected genes/pathways)
- **Framework**: Network Medicine
- **Concept**: Leverage system-level understanding of disease biology
- **Key Approach**:
  - Build disease-specific network (genes, proteins, pathways)
  - Analyze network topology (hubs, bottlenecks, modules)
  - Identify optimal network intervention points
  - Find drugs that disrupt critical network interactions
  - Simulate network effects
- **Example**: Build MS disease network from GWAS + pathways, find hub proteins with drug targets

#### 7. **Phenotypic-Centric Discovery**
- **Starting Point**: A desired clinical outcome or phenotype
- **Framework**: Phenotypic Drug Discovery (PDD)
- **Concept**: Work backwards from desired outcomes to biology to drugs
- **Key Approach**:
  - Define phenotype precisely (molecular, cellular, tissue-level)
  - Identify biological processes underlying the phenotype
  - Screen for compounds that shift the phenotype in screening assays
  - Characterize mechanisms of action
  - Predict efficacy
- **Example**: Start with "reduced neuroinflammation" phenotype, find drugs that achieve it

#### 8. **Individualized-Centric Discovery** (Patient-Led)
- **Starting Point**: Patient-specific symptoms/data
- **Framework**: Precision Medicine / Patient-Led Research
- **Concept**: Use patient data to find personalized therapeutic options
- **Key Approach**:
  - Analyze patient genotype, phenotype, medical history
  - Identify patient-specific pathways and targets
  - Find drugs matching patient-specific biology
  - Check for drug-drug interactions and contraindications
  - Prioritize by patient's specific needs
- **Note**: Requires actual patient data in specific format

## Playbook Architecture

### File Structure

```
medical_mcps/
├── agent_playbooks/
│   ├── __init__.py                    # Public API
│   ├── definitions.py                 # Type definitions and loader
│   ├── drug_centric.yaml              # Playbook YAML files
│   ├── disease_centric.yaml
│   ├── pathway_centric.yaml
│   ├── genetic_centric.yaml
│   ├── target_centric.yaml
│   ├── network_centric.yaml
│   ├── phenotypic_centric.yaml
│   └── individualized_centric.yaml
├── servers/
│   └── playbook_server.py             # MCP server implementation
└── med_mcp_server.py                  # Tool registration system
```

### YAML Specification

Each playbook was defined in YAML with this structure:

```yaml
playbook_id: drug_centric              # Unique identifier
name: Drug-Centric Discovery           # Display name
description: |                         # Human-readable description
  Discover new indications for an existing drug...
starting_point: drug                   # One of: drug, disease, target, pathway,
                                       # genetic_variant, disease_network, phenotype
first_principles_framework: |          # Academic/scientific framework
  Reverse Pharmacology framework states that...
steps:                                 # Ordered list of steps
  - step_id: step_1                    # Step identifier
    step_type: query                   # Type: query, analyze, filter, hypothesize, validate, synthesize
    description: Search for all ChEMBL activities...
    tool_suggestions:                  # Recommended MCP tools
      - chembl_search_molecules
      - chembl_get_activities
    criteria:                          # Optional filtering criteria
      affinity_threshold: 1000         # nM
    outputs:                           # What this step produces
      - compound_list
      - activity_data
expected_outputs:                      # Final deliverables
  - candidate_drugs
  - mechanism_of_action
  - clinical_evidence
convergence_criteria:                  # Success criteria (optional)
  min_candidates: 3
  evidence_types: ["in_vitro", "clinical"]
```

### Step Types

Each playbook step has a `step_type` that describes the operation:

- **query**: Retrieve information from databases/APIs
- **analyze**: Process and interpret results
- **filter**: Apply criteria to narrow results
- **hypothesize**: Generate mechanistic explanations
- **validate**: Check against evidence or criteria
- **synthesize**: Combine findings into conclusions

## Tool Integration

### MCP Tools Exposed

The playbooks system exposed 5 MCP tools:

1. **`playbook_list_all()`**
   - Returns all available playbooks with metadata
   - Used for discovery and selection

2. **`playbook_get_details(playbook_id: str)`**
   - Returns complete playbook definition with all steps
   - Used for comprehensive workflow understanding

3. **`playbook_get_steps(playbook_id: str)`**
   - Returns just the steps for a playbook
   - Used for step-by-step execution

4. **`playbook_execute_step(playbook_id, step_id, inputs, tool_results?)`**
   - Provides guidance for executing a specific step
   - Suggests which tools to use, what to look for, how to interpret results
   - Contextual hints based on playbook and step type
   - Used for guided execution with AI assistance

5. **`playbook_compare_strategies(starting_point?, disease?)`**
   - Compares multiple playbooks suitable for a starting point or disease
   - Helps users choose the best playbook(s) for their research question
   - Can suggest triangulation (running multiple playbooks)

### Tool Suggestions Pattern

Rather than hardcoding tool calls, each playbook step listed suggested tools. This allowed:

- Flexible, AI-driven execution (Claude could choose which specific tools to use)
- Adaptation based on intermediate results
- Integration with external resources not listed in suggestions
- User override if they knew a better approach

**Example tool suggestions across playbooks**:
- ChEMBL: Molecular data, activities, mechanisms, target interactions
- Reactome: Pathway analysis, disease pathways
- KEGG: Metabolic pathways, disease associations
- GWAS Catalog: Genetic variants, disease associations
- UniProt: Protein information, disease associations
- ClinicalTrials.gov: Trial landscape for validation
- PubMed: Literature validation
- OpenFDA: Drug safety and approvals
- Pathway Commons: Network analysis

## Conceptual Framework

### Scientific Methodologies Encoded

Each playbook encoded an established scientific methodology:

| Playbook | Methodology | Strength | Use Case |
|---|---|---|---|
| Drug-Centric | Reverse Pharmacology | Existing drug knowledge | Drug repositioning |
| Disease-Centric | Systems Biology | Comprehensive view | New indications |
| Target-Centric | Traditional Drug Discovery | Target validation | Hit identification |
| Pathway-Centric | Network Pharmacology | System understanding | Multi-target drugs |
| Genetic-Centric | Mendelian Randomization | Causal inference | Target prioritization |
| Network-Centric | Network Medicine | Disease networks | Combination therapy |
| Phenotypic-Centric | Phenotypic Screening | Functional outcomes | Hit discovery |
| Individualized-Centric | Precision Medicine | Patient-specific | Personalized therapy |

### Triangulation Strategy

The design encouraged running multiple playbooks for the same research question:

- **Drug-Centric + Disease-Centric**: Confirm from both sides
- **Target-Centric + Pathway-Centric**: Validate mechanism
- **Genetic-Centric + Disease-Centric**: Combine genetic and network evidence
- **Any + Genetic-Centric**: Add causal inference validation

Higher confidence when multiple playbooks converge on the same answer.

## Execution Flow

### Typical User Journey

1. **Select Playbook**: User chooses starting point (drug/disease/target/etc.)
   - Tool: `playbook_list_all()` or `playbook_compare_strategies()`

2. **Understand Workflow**: Review playbook steps and framework
   - Tool: `playbook_get_details()` or `playbook_get_steps()`

3. **Execute Step-by-Step**: For each step:
   - Tool: `playbook_execute_step()` gets execution guidance
   - Claude executes suggested tools (ChEMBL, Reactome, etc.)
   - Claude interprets results and moves to next step
   - Optional: Claude calls `playbook_execute_step()` again for next step

4. **Synthesize Results**: Use convergence criteria to validate findings

### AI Integration

Claude (or another AI) would:
- Parse playbook structure
- Call `playbook_execute_step()` for guidance on each step
- Execute suggested tools intelligently (adapting to results)
- Interpret intermediate outputs
- Apply convergence criteria
- Synthesize findings into actionable recommendations

The playbook provided structure; the AI provided intelligence.

## Design Principles

1. **Declarative Over Imperative**: YAML definitions instead of code
2. **Framework-First**: Encode scientific methodologies, not tool sequences
3. **Modular**: Each step independent with clear inputs/outputs
4. **Tool-Agnostic**: Suggest tools, don't hardcode execution
5. **Human-Readable**: YAML format for version control, review, modification
6. **Extensible**: Easy to add new playbooks (just add YAML file)
7. **Type-Safe**: Full TypedDict definitions for validation
8. **Graceful Degradation**: Error responses include context (available playbooks, steps)

## Data Flow

```
User Query
    ↓
Select Playbook (playbook_list_all / compare_strategies)
    ↓
Get Playbook Details (playbook_get_details / playbook_get_steps)
    ↓
For Each Step:
    ├→ Get Step Guidance (playbook_execute_step)
    ├→ Execute Suggested Tools (ChEMBL, Reactome, etc.)
    ├→ Interpret Results
    └→ Accumulate Evidence
    ↓
Synthesize Results
    ↓
Apply Convergence Criteria
    ↓
Generate Recommendations
```

## Error Handling

The playbooks system used graceful error handling:

- Invalid playbook ID: Return error + list of available playbooks
- Invalid step ID: Return error + list of available steps
- Invalid step type: Raise during YAML loading with clear message
- Missing required fields: Raise during loading with file location

This allowed for fast iteration and user correction.

## Configuration

The playbooks system had **no external configuration**:

- All playbooks defined statically in YAML files
- Auto-loaded at import time
- No environment variables needed
- No database required
- Version controlled along with code

## Testing Strategy

The system used declarative Tavern tests:

```yaml
test: List all playbooks
  POST /tools/playbooks/mcp
  Expect: drug_centric, disease_centric, etc. in response

test: Get drug-centric details
  POST /tools/playbooks/mcp with playbook_id=drug_centric
  Expect: Complete structure with all steps

test: Error on invalid playbook
  POST /tools/playbooks/mcp with invalid ID
  Expect: Error response + available_playbooks list
```

## Integration Points

The playbooks MCP server integrated with:

1. **HTTP Server**: Mounted at `/tools/playbooks/mcp`
2. **Unified MCP Server**: Tools also registered to unified endpoint
3. **Med MCP Server**: Used central `@medmcps_tool` decorator system
4. **All API Clients**: Suggested tools from ChEMBL, Reactome, GWAS, UniProt, etc.

## Future Reimplementation Considerations

If reimplementing this system, consider:

1. **Declarative Definition**: Keep YAML-based playbook definitions
2. **Step Execution Engine**: Consider explicit step execution tracking
3. **State Management**: Track intermediate results through playbook execution
4. **Result Caching**: Cache tool results to avoid redundant API calls
5. **Reasoning Chains**: Capture AI reasoning alongside playbook execution
6. **User Feedback Loop**: Collect feedback on playbook effectiveness
7. **Dynamic Playbooks**: Allow runtime playbook composition
8. **Performance**: Consider database backing for frequently-used playbooks
9. **Visualization**: Consider graphical representation of playbook workflows
10. **Validation**: Enhance convergence criteria and evidence validation

## Conclusion

The playbooks system represented a conceptual framework for systematically exploring drug discovery and repurposing using domain-specific methodologies. While the implementation has been removed, this architecture provides a solid foundation for future systems that combine structured scientific workflows with AI-driven tool execution.

The key insight: **Structure the methodology, let intelligence handle the execution.**
