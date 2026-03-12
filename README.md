# An Automated Tool for Assessing Resolvability, Parsability, and Consistency of RDF Resources    

This automated tool implements 6 metrics about resolvability, parsability, and consistency of RDF resources. 
The methodology and implementation are described in the following papers:

1. **Automated approach for quality assessment of RDF resources**  
   Zhang S, Benis N, Cornet R. *BMC Med Inform Decis Mak*. 2023.  
   [https://pubmed.ncbi.nlm.nih.gov/37165363/](https://pubmed.ncbi.nlm.nih.gov/37165363/)

2. **Assessing resolvability, parsability, and consistency of RDF resources: a use case in rare diseases**  
   Zhang S, Benis N, Cornet R. *J Biomed Semantics*. 2023.  
   [https://pubmed.ncbi.nlm.nih.gov/38053130/](https://pubmed.ncbi.nlm.nih.gov/38053130/)

## Dependencies
Run the following command to install dependencies with `pip` installed:
 
```
pip install -r requirements.txt
```

## Python Support
Require Python 3.7 or later.

## Basic Usage

**Quick start (default):** The config is pre-set to assess `hpscreg` (a local file included in the repo). Just run:

> **Note:** Step I (resolvability) and Step II (parsability) each make HTTP requests per URI. For hpscreg (~940 URIs) this can take 30+ min per step. For a quick test, set `MaxURIsForQuickTest = 20` in `config.py` to assess only 20 URIs (~2 min total).

```bash
python run_assessment.py
```

**Customize:** Edit `config.py`:
1. **ListOfLABEL** – which resources to assess. Options:
   - `QUICK_START` (default): `['hpscreg']` – single local file
   - `ListOfLabelsForConceptualPaper` – 8 ontologies from the paper
   - `ListOfLabelsForRareDiseaseResources` – 16 rare-disease resources
2. **WhichResource** – add `{label: path_or_uri}` for your own resources. Path can be:
   - A URI, e.g. `'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'`
   - A local path, e.g. `'my-ontology': 'resources/my-ontology.ttl'`

Then run `python run_assessment.py`.
    1. After running, a pickle file of storing the RDF graph for the target resource will be generated in the directory 
  `pickle/{LABEL}_graph.pickle'`. Once created, the tool will directly load the pickle, reducing the parsing time. 
  This is very useful for resources of large size.
    2. After evaluation, four CSV files will be generated that contains URIs with labels indicating resolvability, 
    parsability, and consistency in the directory `output/{LABEL}/`; 
    an assessment report will be generated in the directory `output/{LABEL}/report-{LABEL}.ttl` in the form of Turtle.

### Use case 
So far there has been two use cases:  
1. Evaluate 8 ontologies in RDF (see `test resources` file or `ListOfLabelsForConceptualPaper` in `config.py`) 
2. Evaluate 16 rare disease resources in RDF (see `ListOfLabelsForRareDiseaseResources` in `config.py`)

If only assess these resources, you can assign  `ListOfLabelsForConceptualPaper` or 
`ListOfLabelsForRareDiseaseResources` to `ListOfLABEL` .
    
### To Play With It 
If you want to further customise this tool to your own 'playground', it might be necessary to have following information.

There are five main folders:

* `resources`: to store RDF resources
* `metrics`: scripts that implement resolvability, parsability, classification, and consistency metrics
* `core`: constants, path utilities, and logging configuration
* `output`: assessment reports and CSV files with intermediate results
* `functions`: utilities for loading resources, generating reports, and inspection

The structure (and built-in functions) of assessment report is described in `functions/generate_report.py`.

### Quick Reference

| Purpose | Location |
|---------|-----------|
| **Entry point** | `run_assessment.py` – main workflow |
| **Configuration** | `config.py` – `ListOfLABEL`, `WhichResource`, `ChunkSize` |
| **Metrics** | `metrics/` – resolvability, parsability, classify, consistency, coverage |
| **Helpers** | `functions/` – load_resource, generate_report, create_directory, etc. |
| **Constants & paths** | `core/` – constants, paths, logging |
| **Analysis** | `quantitative_analysis.py` – aggregates results and computes statistics |

```
assess-rdf-resource/
├── run_assessment.py      # Start here
├── config.py              # Configure resources to assess
├── quantitative_analysis.py
├── core/                  # Constants, paths, logging
├── metrics/               # Resolvability, parsability, consistency, etc.
├── functions/             # Load, report, utilities
├── resources/             # RDF files to assess
├── output/                # Results (CSV, TTL reports)
└── pickle/                # Cached graphs
```

### Logging
The tool uses Python's `logging` module. By default, INFO-level messages are printed to stdout. To increase verbosity (e.g., for debugging), configure the `assess_rdf` logger:

```python
import logging
logging.getLogger("assess_rdf").setLevel(logging.DEBUG)
``` 

### Issues
If you have any questions or problems in using this tool, please create Issues.