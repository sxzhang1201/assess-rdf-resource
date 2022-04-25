# An Automated Tool for Assessing Resolvability, Parsability, and Consistency of RDF Resources    

This automated tool implements 7 metrics about resolvability, parsability, and consistency of RDF resources, 
as described in the research manuscript: 
**Automated Approach for Minimal Quality Assessment of RDF Resources for Reuse**.

## Dependencies
Run the following command to install dependencies with `pip` installed:
 
```
pip install -r requirements.txt
```

## Getting Started
Two steps need to be performed to validate an RDF resource:
1. Edit `config.py`. 
    1. Decide the `LABEL`. This `LABEL` will be used to name the assessment report for this tested RDF resource. 
    2. Add {`LABEL`: `Path of RDF resource`} to `WhichResource`. 
    You should set correct `Path of RDF resource` so as to successfully load the test RDF resource. 
    3. Add {`LABEL`: `Path of Assessment Report`} to `WhichReport`. 
    You can specify where to store the assessment report by setting appropriate `Path of Assessment Report`.
     
    All keys (`LABEL`) and values (`Path of RDF resource`, `Path of Assessment Report`) should be string.
    
2. Run `run_assessment.py`.
    After evaluation, an assessment report can be generated in the specified `Path of Assessment Report`.

3. Run `visualise_report.py` (optional)
   
    
### To Play with It 
If you want to further customise this tool to your own 'playground', it might be necessary to have following information.

There are four folders:

* `resources`: containing RDF datasets
* `metrics`: containing scripts that implement metrics
* `report`: to store assessment reports 
* `functions`: containing scripts that implement some basic functions 

The structure (and built-in functions) of assessment report is described in `functions/assessment_report.py`. 

