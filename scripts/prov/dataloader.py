import pandas as pd
from rdflib import Graph, URIRef, RDF, Namespace, Literal
from rdflib.namespace import DC, XSD
from datetime import datetime

def read_csv(csvinput, delimiter=',', skipinitialspace=True, captureprovenance=True, namespace="", textdict = {}, uridict={}, provgraph=None):
	# record activity starting time
	stime = datetime.utcnow()

	# execute normal operation
	ret = pd.read_csv(csvinput, delimiter = delimiter, skipinitialspace=skipinitialspace)

	# record activity ending time
	etime = datetime.utcnow()

	# namespaces
	example = Namespace(namespace)
	pub = Namespace("http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/")
	prov = Namespace("http://www.w3.org/ns/prov#")

	# activity id, used data object id, library id, and return value id
	aid = URIRef(uridict['fun'])

	if 0 in uridict:
		csvinputid = URIRef(uridict[0])
	else:
		csvinputid = URIRef(uridict['csvinput'])
	
	if 'pandas' in uridict:
		libid = URIRef(uridict['pandas'])
	else:
		libid = example.pandas
		s = str(example.pandas)
		uridict['pandas'] = s
	
	returnid = URIRef(uridict['return'])

	# add triples to the provenance graph
	provgraph.add((aid, RDF.type, pub.Loading))
	provgraph.add((aid, DC.description, Literal("Read CSV data in file "+csvinput+" to variable "+textdict['return'])))
	provgraph.add((aid, pub.language, Literal("Python")))
	provgraph.add((aid, prov.startedAtTime, Literal(stime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, prov.endedAtTime, Literal(etime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, pub.loaded, csvinputid))
	provgraph.add((csvinputid, RDF.type, pub.OnDiskData))
	provgraph.add((csvinputid, DC.description, Literal("Data stored in file "+csvinput)))
	provgraph.add((aid, prov.used, libid))
	provgraph.add((libid, RDF.type, pub.Library))
	provgraph.add((libid, DC.description, Literal("The pandas Python library")))
	provgraph.add((aid, prov.generated, returnid))
	provgraph.add((returnid, RDF.type, pub.InMemoryData))
	provgraph.add((returnid, DC.description, Literal("Data held by variable "+textdict['return'])))
	return ret


