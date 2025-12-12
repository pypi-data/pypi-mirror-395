from pathlib import Path
from rdflib.namespace import DefinedNamespace
from rdflib import URIRef
from .ontology_reader import OntologyReader


# Absoluten Pfad zum aktuellen Skript-Verzeichnis bestimmen
current_dir = Path(__file__).parent

# TTL-Datei im gleichen Verzeichnis finden
ontology_file = current_dir / "mmut.ttl"
ontology = OntologyReader(str(ontology_file))


class MMUT(DefinedNamespace):

    _NS = ontology.get_namespace()

    MicroModel: URIRef = ontology.get_class('#MicroModel')
    RDFMicroModel: URIRef = ontology.get_class('#RDFMicroModel')
    BinaryMicroModel: URIRef = ontology.get_class('#BinaryMicroModel')
    SysMLMicroModel: URIRef = ontology.get_class('#SysMLMicroModel')

    Transformation: URIRef = ontology.get_class('#Transformation')
    PythonScriptTransformation: URIRef = ontology.get_class('#PythonScriptTransformation')

    TaskDefinition: URIRef = ontology.get_class('#TaskDefinition')
    ContainerProperties: URIRef = ontology.get_class('#ContainerProperties')
    Environment: URIRef = ontology.get_class('#Environment')
    KeyValuePair: URIRef = ontology.get_class('#KeyValuePair')

    isInputModelOf: URIRef = ontology.get_object_property('#isInputModelOf')
    hasOutputModel: URIRef = ontology.get_object_property('#hasOutputModel')
    hasLooseCoupling: URIRef = ontology.get_object_property('#hasLooseCoupling')
    extendsModel: URIRef = ontology.get_object_property('#extendsModel')
    hasTaskDefinition: URIRef = ontology.get_object_property('#hasTaskDefinition')
    hasContainerProperties: URIRef = ontology.get_object_property('#hasContainerProperties')
    hasCommandSequence: URIRef = ontology.get_object_property('#hasCommandSequence')
    hasEnvironment: URIRef = ontology.get_object_property('#hasEnvironment')
    hasKeyValuePair: URIRef = ontology.get_object_property('#hasKeyValuePair')
    
    key: URIRef = ontology.get_datatype_property('#key')
    value: URIRef = ontology.get_datatype_property('#value')
    image: URIRef = ontology.get_datatype_property('#image')
