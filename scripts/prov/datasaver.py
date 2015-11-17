import pandas as pd
from rdflib import Graph, URIRef, RDF, Namespace, Literal
from rdflib.namespace import DC, XSD
from datetime import datetime
import urllib

def write_csv(dataframe, csvoutput, delimiter=',', index=True, **kwargs): # namespace="", textdict = {}, uridict={}, provgraph=None
	# record activity starting time
	stime = datetime.utcnow()

	# execute normal operation
	dataframe.to_csv(csvoutput, sep = delimiter, index = index)

	# record activity ending time
	etime = datetime.utcnow()

	# augmented provenance parameters
	namespace = kwargs['namespace']
	textdict = kwargs['textdict']
	uridict = kwargs['uridict']
	provgraph = kwargs['provgraph']

	# namespaces
	example = Namespace(namespace)
	pub = Namespace("http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/")
	prov = Namespace("http://www.w3.org/ns/prov#")

	# activity id, used data object id, library id, and return value id
	aid = URIRef(uridict['fun'])

	if 0 in uridict:
		dfid = URIRef(uridict[0])
	else:
		dfid = URIRef(uridict['dataframe'])
	
	if 0 in textdict:
		dftext = textdict[0]
	else:
		dftext = textdict['dataframe']
	
	# since csvoutput is gonna be a new on-disk data object, generate a fresh URI for it
	if 1 in textdict:
		csvoutputtext = textdict[1]
	else:
		csvoutputtext = textdict['csvoutput']

	csvoutputid = URIRef(namespace+freshurl(csvoutputtext))
		
	if 'pandas' in uridict:
		libid = URIRef(uridict['pandas'])
	else:
		libid = example.pandas
		uridict['pandas'] = str(libid)
	
	# add triples to the provenance graph
	provgraph.add((aid, RDF.type, pub.Saving))
	provgraph.add((aid, DC.description, Literal("Save data in "+dftext+" to file "+csvoutput)))
	provgraph.add((aid, pub.language, Literal("Python")))
	provgraph.add((aid, prov.startedAtTime, Literal(stime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, prov.endedAtTime, Literal(etime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, pub.saved, dfid))
	provgraph.add((dfid, RDF.type, pub.InMemoryData))
	provgraph.add((dfid, DC.description, Literal("Data held by variable or expression "+dftext)))
	provgraph.add((aid, prov.used, libid))
	provgraph.add((libid, RDF.type, pub.Library))
	provgraph.add((libid, DC.description, Literal("The pandas Python library")))
	provgraph.add((aid, prov.generated, csvoutputid))
	provgraph.add((csvoutputid, RDF.type, pub.OnDiskData))
	provgraph.add((csvoutputid, DC.description, Literal("Data stored in file "+csvoutput)))

def timestr():
	return datetime.utcnow().strftime("_%Y_%m_%dT%H_%M_%SZ")

def freshurl(name):
	return urllib.quote_plus(name+timestr())

