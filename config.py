LABEL = 'hpscreg'

WhichResource = {
    # ordo catalog fdp
    'ordo-catalog-fdp': 'resources/rd-resources/ordo-catalog-fdp/ordo-catalog-fdp.ttl',
    'rare-disease-resources': 'resources/rd-resources/ordo-catalog-fdp/rare disease resources.ttl',
    'digestive-tumor-registry': 'resources/rd-resources/ordo-catalog-fdp/Digestive Tumor Registry of Finistère.ttl',
    'nasopharyngeal': 'resources/rd-resources/ordo-catalog-fdp/A multicenter registry '
                      'for nasopharyngeal cancer in children.ttl',
    'default': 'resources/rd-resources/ordo-catalog-fdp/ordo-catalog-fdp-default.ttl',
    'head-and-neck-tumor': 'resources/rd-resources/ordo-catalog-fdp/Head and neck tumor registry Austria.ttl',
    'histiocytic-disorders': 'resources/rd-resources/ordo-catalog-fdp/Non-Interventional, web-based Registry for Histiocytic Disorders.ttl',
    'wolfram-syndrome': 'resources/rd-resources/ordo-catalog-fdp/Registry for Wolfram syndrome and so on contributing to EURO-WABB.ttl',
    'granulomatous-disease': 'resources/rd-resources/ordo-catalog-fdp/The National Chronic Granulomatous Disease Registry.ttl',

    # hpscreg
    'hpscreg': 'resources/rd-resources/hpscreg/hpscreg.ttl',

    # nextprot
    'nextprot-terminology': 'resources/rd-resources/nextprot/nextprot_terminology.ttl',
    'nextprot-schema': 'resources/rd-resources/nextprot/schema.ttl',

    # uniprot
    'P04156': 'resources/rd-resources/uniprot/P04156.rdf',

    # fhir
    'fhir': 'resources/fhir/fhir.ttl',

    # others
    'addison': 'resources/addison_dataset.ttl',

    # 'SIO': 'http://semanticscience.org/ontology/sio.owl',
    'SIO': 'resources/sio-release.owl',

    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',

    'grddl': 'http://www.w3.org/2003/g/data-view#',

    'rim': 'resources/fhir/rim.ttl',

    'dct': 'http://purl.org/dc/elements/1.1/',

    'foaf': 'resources/foaf.rdf',

    'test': 'resources/test.ttl',

    'wikipathway': 'https://wikipathways-data.wmcloud.org/20220410/rdf/wikipathways-20220410-rdf-void.ttl'

}


WhichReport = {
    # ordo catalog fdp
    "ordo-catalog-fdp": "report/rd-resources/ordo-catalog-fdp.pickle",
    'digestive-tumor-registry': 'report/rd-resources/digestive-tumor-registry.pickle',
    "rare-disease-resources": "report/rd-resources/rare-disease-resources.pickle",
    "nasopharyngeal": 'report/rd-resources/nasopharyngeal.pickle',
    'head-and-neck-tumor': 'report/rd-resources/head-and-neck-tumor.pickle',
    'histiocytic-disorders': 'report/rd-resources/histiocytic-disorders.pickle',
    'wolfram-syndrome': 'report/rd-resources/wolfram-syndrome.pickle',
    'granulomatous-disease': 'report/rd-resources/granulomatous-disease.pickle',

    # nextprot
    'nextprot-schema': 'report/rd-resources/nextprot-schema.pickle',
    'nextprot-terminology': 'report/rd-resources/nextprot-terminology.pickle',

    # uniprot
    'P04156': 'report/rd-resources/P04156.pickle',

    # hpscreg
    "hpscreg": 'report/rd-resources/hpscreg.pickle',

    # fhir
    'fhir': 'report/rd-resources/fhir.pickle',

    # others
    'addison': 'report/addison_dataset.pickle',

    'SIO': 'report/SIO_000332.pickle',

    'rdf': 'report/rdf.pickle',

    'grddl': 'report/grddl.pickle',

    'rim': 'report/rim.pickle',

    'dct': 'report/dct.pickle',

    'foaf': 'report/foaf.pickle',

    'test': 'report/test.pickle'


}
