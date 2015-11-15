from rdflib import Graph, URIRef, RDF, Namespace, Literal
from rdflib.namespace import DC, XSD
from datetime import datetime

def assign(rhs, namespace="", textdict = {}, uridict={}, provgraph=None):
	# record activity starting time
	stime = datetime.utcnow()

	# execute the normal assignment
	ret = rhs

	# record activity ending time
	etime = datetime.utcnow()

	# namespaces
	pub = Namespace("http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/")
	prov = Namespace("http://www.w3.org/ns/prov#")
	example = Namespace(namespace)

	# activity id, used data object id, and return value id
	aid = URIRef(uridict['fun'])
	if 0 in uridict:
		rhsid = URIRef(uridict[0])
	else:
		rhsid = URIRef(uridict['rhs'])
	returnid = URIRef(uridict['return'])

	if 0 in textdict:
		rhstext = textdict[0]
	else:
		rhstext = textdict['rhs']

	# add triples to the provenance graph
	provgraph.add((aid, RDF.type, prov.Activity))
	provgraph.add((aid, DC.description, Literal("Assign expression "+rhstext+" to variable "+textdict['return'])))
	provgraph.add((aid, pub.language, Literal("Python")))
	provgraph.add((aid, prov.startedAtTime, Literal(stime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, prov.endedAtTime, Literal(etime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, prov.used, rhsid))
	provgraph.add((rhsid, RDF.type, pub.InMemoryData))
	provgraph.add((rhsid, DC.description, Literal("Expression "+rhstext)))
	provgraph.add((aid, prov.generated, returnid))
	provgraph.add((returnid, RDF.type, prov.Entity))
	provgraph.add((returnid, DC.description, Literal("Data or result held by variable "+textdict['return'])))
	return ret

def delete(obj, key, namespace="", textdict={}, uridict={}, provgraph=None):
	# record activity starting time
	stime = datetime.utcnow()
	
	# execute the normal deletion
	del obj[key]

	# record activity ending time
	etime = datetime.utcnow()

	# namespaces
	pub = Namespace("http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/")
	prov = Namespace("http://www.w3.org/ns/prov#")
	example = Namespace(namespace)

	# activity id, used data object id, and return value id
	aid = URIRef(uridict['fun'])
	if 0 in uridict:
		objid = URIRef(uridict[0])
	else:
		objid = URIRef(uridict['obj'])
	returnid = URIRef(uridict['return'])

	if 0 in textdict:
		objtext = textdict[0]
	else:
		objtext = textdict['obj']

	if 1 in textdict:
		keytext = textdict[1]
	else:
		keytext = textdict['key']

	# add triples to the provenance graph
	provgraph.add((aid, RDF.type, pub.Transformation))
	provgraph.add((aid, DC.description, Literal("Delete "+objtext+"["+keytext+"]")))
	provgraph.add((aid, pub.language, Literal("Python")))
	provgraph.add((aid, prov.startedAtTime, Literal(stime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, prov.endedAtTime, Literal(etime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, pub.transformed, objid))
	provgraph.add((objid, RDF.type, pub.InMemoryData))
	provgraph.add((objid, DC.description, Literal("Variable "+objtext)))
	provgraph.add((aid, prov.generated, returnid))
	provgraph.add((returnid, RDF.type, pub.InMemoryData))
	provgraph.add((returnid, DC.description, Literal("Data held by variable "+textdict['return'])))
	return obj

