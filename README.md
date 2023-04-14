# An Automated Tool for Assessing Resolvability, Parsability, and Consistency of RDF Resources    

This automated tool implements 6 metrics about resolvability, parsability, and consistency of RDF resources, 
as described in the research manuscript: 
**Automated Approach for Minimal Quality Assessment of RDF Resources for Reuse**.

## Dependencies
Run the following command to install dependencies with `pip` installed:
 
```
pip install -r requirements.txt
```

## Basic Usage
Two steps need to be performed to validate an RDF resource:
1. Edit `config.py`. 
    1. Decide the `ListOfLABEL`. This `ListOfLABEL` will be used to (a) locate the resource to be tested, (2) support 
    the naming the assessment report and the directory for storing it. 
    2. Add {`LABEL`: `Path of RDF resource`} to `WhichResource`. 
    You should set correct `Path of RDF resource` so as to successfully load the test RDF resource. 
    This `Path of RDF resource` can be a URI, e.g., `'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'`, 
    or a local path, e.g., `'rdf':'resources/foaf.rdf'`.
    
2. Run `$ python run_assessment.py`.
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

There are four folders:

* `resources`: to store RDF resources
* `metrics`: contain scripts that implement metrics
* `output`: to store assessment reports and data frames storing intermediate results
* `functions`: contain scripts that implement some basic functions 

The structure (and built-in functions) of assessment report is described in `functions/generate_report.py`. 