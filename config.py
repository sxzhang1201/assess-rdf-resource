ListOfLABEL = ['geno']
ChunkSize = 50

WhichResource = {
    # 'ordo-catalog-fdp': 'resources/rd-resources/ordo-catalog-fdp/ordo catalog fdp.ttl',
    'ordo-catalog-fdp': 'https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/?format=ttl',

    # 'rare-disease-resources': 'resources/rd-resources/ordo-catalog-fdp/rare disease resources.ttl',
    'rare-disease-resources': 'https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/catalog/2a3f1a0e-ddbb-4a07-960e-fa92e1e9f4bc',

    # 'digestive-tumor-registry': 'resources/rd-resources/ordo-catalog-fdp/Digestive Tumor Registry of Finistère.ttl',
    'digestive-tumor-registry': 'https://w3id.org/ejp-rd/fairdatapoints/orphanet-catalog-fdp/patientRegistry/e2f9b235-39d5-4490-ba40-eda0a27d0199',

    # 'nasopharyngeal-cancer': 'resources/rd-resources/ordo-catalog-fdp/A multicenter registry for nasopharyngeal cancer in children.ttl',
    'nasopharyngeal-cancer': 'https://w3id.org/ejp-rd/fairdatapoints/orphanet-catalog-fdp/patientRegistry/b6a6bdad-6233-4b44-9b5a-5b26eb020eeb',

    # 'head-and-neck-tumor': 'resources/rd-resources/ordo-catalog-fdp/Head and neck tumor registry Austria.ttl',
    'head-and-neck-tumor': 'https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/patientRegistry/6759d7b2-73ee-4711-bffe-c0483ec0f214',

    'primary-immune-deficiency': 'https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/biobank/d7cdf993-e7f8-459f-9aad-3a5cf437bf20',

    'ejp-metadata-ontology': 'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema-ontology/main/ejprd_resource_metadata_ontology.owl',

    # hpscreg
    'hpscreg': 'resources/rd-resources/hpscreg/hpscreg.ttl',

    # 'hpscreg': 'https://hpscreg.eu/ontologies/hPSCreg_clo_without_imports_2022_07_26.owl',
    # nextprot
    'nextprot-terminology': 'resources/rd-resources/nextprot/nextprot_terminology.ttl',
    'nextprot-schema': 'resources/rd-resources/nextprot/schema.ttl',

    # uniprot
    'P04156': 'resources/rd-resources/uniprot/P04156.rdf',
    'uniprot-ontology': 'http://purl.uniprot.org/core/',

    # fhir
    'fhir': 'resources/health data models/fhir/fhir.ttl',

    # others
    'addison': 'resources/addison_dataset.ttl',

    # 'SIO': 'http://semanticscience.org/ontology/sio.owl',
    'sio': 'resources/sio-release.owl',

    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',

    'grddl': 'http://www.w3.org/2003/g/data-view#',

    'rim': 'resources/health data models/fhir/rim.ttl',

    'dct': 'http://purl.org/dc/elements/1.1/',

    'dcterm': 'http://purl.org/dc/terms/',

    'foaf': 'resources/foaf.rdf',

    'test': 'resources/test.ttl',

    'wikipathway': 'https://wikipathways-data.wmcloud.org/20220410/rdf/wikipathways-20220410-rdf-void.ttl',

    'ordo': "resources/ontologies/ORDO_en_3.3.owl",

    'issva': "resources/ontologies/issva-ontology.owl",

    'cdash-ct-schema': "resources/health data models/CDASH Terminology.OWL/ct-schema.owl",

    'meta-model-schema': "resources/health data models/CDASH Terminology.OWL/meta-model-schema.owl",

    "chebi-in-bfo": "resources/ontologies/chebi-in-bfo.owl",

    "fma": "resources/ontologies/fma.owl",

    'snomedct': "resources/ontologies/snomedct.owl",


    # 'wikipathway': 'https://vocabularies.wikipathways.org/wp',

    'sato': 'https://w3id.org/CAPABLE/ontologies/SATO',

    'loinc': 'http://loinc.org/owl',

    'atc': "resources/ontologies/ATC.ttl",

    'geno': "resources/ontologies/geno.owl",

    'hpo': "resources/ontologies/hp.owl",

    'ncit': "resources/ontologies/ncit.owl",

    'snomedct_ttl': "resources/ontologies/snomed-turtle.ttl",

    'cido': "resources/ontologies/cido.owl",

    'misfoaf': "resources/temporary/mis_foaf.rdf",

    'alaric-foaf': "resources/temporary/alaric-foaf.rdf"
}


ListOfLabelsForRareDiseaseResources = [
    'ordo-catalog-fdp',
    'rare-disease-resources',
    'head-and-neck-tumor',
    'primary-immune-deficiency',
    'ejp-metadata-ontology',
    'wikipathway',
    'hpscreg',
    'nextprot-schema',
    'nextprot-terminology',
    'uniprot-ontology',
    'ordo',
    'atc',
    'geno',
    'hpo',
    'ncit',
    'snomedct'
]

# Temporarily not in use
WhichRareDiseaseResource = {
    'ordo-catalog-fdp': 'https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/?format=ttl',
    'rare-disease-resources': 'https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/catalog/2a3f1a0e-ddbb-4a07-960e-fa92e1e9f4bc',
    'head-and-neck-tumor':'https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/patientRegistry/6759d7b2-73ee-4711-bffe-c0483ec0f214',
    'primary-immune-deficiency':'https://ejp-rd-dev1.vm.cesnet.cz/fdps/orphanet-catalog-fdp/biobank/d7cdf993-e7f8-459f-9aad-3a5cf437bf20',
    'ejp-metadata-ontology': 'https://raw.githubusercontent.com/ejp-rd-vp/resource-metadata-schema-ontology/main/ejprd_resource_metadata_ontology.owl',
    'wikipathway':'https://wikipathways-data.wmcloud.org/20220410/rdf/wikipathways-20220410-rdf-void.ttl',
    'hpscreg':'https://hpscreg.eu/ontologies/hPSCreg_clo_without_imports_2022_07_26.owl',
    'nextprot-schema': 'resources/rd-resources/nextprot/schema.ttl',
    'nextprot-terminology': 'resources/rd-resources/nextprot/nextprot_terminology.ttl',
    'uniprot-ontology':'http://purl.uniprot.org/core/',
    'ordo': "resources/ontologies/ORDO_en_3.3.owl",
    'atc': "resources/ontologies/ATC.ttl",
    'geno': "resources/ontologies/geno.owl",
    'hpo': "resources/ontologies/hp.owl",
    'ncit': "resources/ontologies/ncit.owl",
    'snomedct': "resources/ontologies/snomedct.owl"
}


# This is the list of labels (which indicate corresponding resources) to be tested in the conceptual paper
ListOfLabelsForConceptualPaper = [
    'dct',
    'sio',
    'foaf',
    'rim',
    'fhir',
    'grddl',
    'cdash',
    'ordo'
]


QUERY1 = """
    PREFIX  dcat: <http://www.w3.org/ns/dcat#>
    PREFIX  dqv:  <http://www.w3.org/ns/dqv#>
    PREFIX  fqm:  <http://purl.org/fqm#>
    
    SELECT DISTINCT ?rname  ?value
    WHERE {
        ?rname a dcat:Resource .
        ?rname dqv:hasQualityMeasurement ?resolvable_measure .
        ?resolvable_measure dqv:isMeasurementOf fqm:uriNonResolvableMetric .
        ?resolvable_measure dqv:value ?value .
        FILTER (?value > 0.1)
    }
    """

QUERY2 = """
    PREFIX  dcat: <http://www.w3.org/ns/dcat#>
    PREFIX  dqv:  <http://www.w3.org/ns/dqv#>
    PREFIX  fqm:  <http://purl.org/fqm#>
    PREFIX  dcterms:  <http://purl.org/dc/terms/>
    
    SELECT DISTINCT ?resource  ?undefined_uris
    WHERE {
        ?resource a dcat:Resource .
        ?resource dqv:hasQualityMeasurement ?measure .
        ?measure  dqv:isMeasurementOf fqm:uriUndefinedMetric .
        ?measure  dcterms:relation ?undefined_uris .
    }
    """

QUERY3 = """
    PREFIX  dcat: <http://www.w3.org/ns/dcat#>
    PREFIX  dqv:  <http://www.w3.org/ns/dqv#>
    PREFIX  fqm:  <http://purl.org/fqm#>    
    PREFIX  skos:  <http://www.w3.org/2004/02/skos/core#>
    
    SELECT DISTINCT ?measure ?metric ?definition
    WHERE {
        <https://wikipathways-data.wmcloud.org/20220410/rdf/wikipathways-20220410-rdf-void.ttl> 
        dqv:hasQualityMeasurement ?measure .
        ?measure  dqv:isMeasurementOf ?metric .     
        ?metric skos:definition  ?definition .
    }
    """