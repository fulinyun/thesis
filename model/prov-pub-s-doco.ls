@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix dcterms: <http://www.purl.org/dc/terms/>.

@prefix pub:
<http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/>.
@prefix doco: <http://purl.org/spar/doco/>.

<http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/prov-p
ub-s-doco.ttl> a owl:Ontology;
    dcterms:modified "2015-11-16"^^xsd:date;
    rdfs:label "Bridge from PROV-PUB-O/S to DoCO, the
Document Components Ontology";
    dcterms:creator "Linyun Fu <ful2@rpi.edu>";
    rdfs:comment """
    This bridging ontology contains exclusively assertions
of PROV-PUB-O/S classes being subclasses of classes in
DoCO, the Document Components Ontology.
    
    PROV-PUB-O/S is a lightweight ontology designed to
describe the locations of published results such as
figures, tables, lists and textually described results
within the structural elements of a research publication.
To leave the decision for dependencies to the users ---
meaning that we do not hard code dependencies to other
ontologies which force the users to accept them, we just
provide suggestions in the documentation of PROV-PUB-O/S
and let the users decide whether to accept the suggested
dependencies.
    """.
    
pub:Chapter rdfs:subClassOf doco:Chapter.

pub:Section rdfs:subClassOf doco:Section.
