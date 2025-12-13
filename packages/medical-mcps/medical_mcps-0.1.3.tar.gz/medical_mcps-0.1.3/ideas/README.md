# Drug Repurposing Workflow Ideas

This folder contains ideas and patterns for building drug repurposing workflows using biomedical APIs. These ideas were developed and tested in the `ms-deep-dive` project and are shared here for inspiration.

## Documents

### [`drug-repurposing-workflows.md`](./drug-repurposing-workflows.md)

Comprehensive guide to building drug repurposing workflows, including:
- File system as state machine pattern
- Multi-stage evaluation workflow
- Parallel agent coordination
- API integration patterns
- Disease-specific evaluation criteria

### [`pathway-based-discovery.md`](./pathway-based-discovery.md)

Ideas for using pathway analysis APIs (KEGG, Reactome, Pathway Commons) to identify drug repurposing opportunities:
- Pathway-based discovery concepts
- GWAS-pathway integration
- Multi-pathway analysis patterns
- API integration tips

## Key Concepts

### 1. File System as State Machine

Use the file system to track drug evaluation state, enabling:
- Parallel agent work without conflicts
- Resumable sessions
- Atomic operations for conflict prevention
- Full audit trail in YAML files

### 2. Conservative Triage Approach

When uncertain about drug relevance, triage rather than archive. Repurposing often succeeds through unexpected secondary effects.

### 3. Secondary Effects Matter

Review ALL drug activities, not just primary mechanisms. Multi-target drugs and off-target effects can reveal repurposing opportunities.

### 4. Pathway-Based Discovery

Analyze drugs by their targets' involvement in disease-relevant pathways, not just primary indications. GWAS-validated pathways are high-priority targets.

## Tools Used

These workflows leverage the biomedical APIs available in `medical-mcps`:

- **ChEMBL API** - Drug targets, mechanisms, bioactivity
- **ClinicalTrials.gov API** - Disease-related trials
- **KEGG API** - Pathway and disease data
- **Reactome API** - Pathway hierarchies and interactions
- **Pathway Commons API** - Integrated pathway data
- **UniProt API** - Protein information
- **GWAS Catalog API** - Genetic association data
- **OMIM API** - Genetic disease information

## Example Use Cases

### Multiple Sclerosis Drug Repurposing

The `ms-deep-dive` project demonstrates these workflows applied to Multiple Sclerosis:
- Evaluated 3,857 drugs from EveryCure drug list
- Identified high-priority candidates (IL-23 inhibitors, JAK inhibitors)
- Generated mechanistic hypotheses for each candidate
- Used pathway analysis to validate targets

### Adapting to Other Diseases

These workflows can be adapted to any disease by:
1. Building disease knowledge base (mechanisms, pathways, unmet needs)
2. Identifying disease-relevant pathways using KEGG/Reactome
3. Mapping GWAS risk genes to pathways
4. Defining evaluation criteria based on disease pathophysiology
5. Systematically evaluating drugs against pathways

## Contributing

If you develop new patterns or workflows, consider:
- Documenting them in this folder
- Sharing examples from your disease-specific projects
- Contributing improvements to the core workflow patterns

## References

- `ms-deep-dive/agents/tasks/2025-01-12_00-00-00-drug-repurposing-workflows-requirements.md` - Detailed workflow documentation
- `ms-deep-dive/AGENTS.md` - Agent definitions and workflow documentation
- `ms-deep-dive/knowledge/10-drug-repurposing-opportunities.md` - Example drug repurposing analysis

---

**Note:** These ideas are meant to inspire and guide, not prescribe. Adapt them to your specific needs and constraints.

