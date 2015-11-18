import pandas as pd
import numpy as np
from rdflib import Graph, URIRef, RDF, Namespace, Literal
from rdflib.namespace import DC, XSD
from datetime import datetime

def group_aggregate(dataframe, keys, aggregation=np.sum, **kwargs): # namespace="", textdict = {}, uridict={}, provgraph=None
	if 'namespace' not in kwargs:
		return dataframe.groupby(keys).aggregate(aggregation)

	# record activity starting time
	stime = datetime.utcnow()

	# execute normal operation
	ret = dataframe.groupby(keys).aggregate(aggregation)

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

	# id and text for activity, used data object, library, and return value
	aid = URIRef(uridict['fun'])

	if 0 in uridict:
		dfid = URIRef(uridict[0])
	else:
		dfid = URIRef(uridict['dataframe'])
	
	if 0 in textdict:
		dftext = textdict[0]
	else:
		dftext = textdict['dataframe']

	if 1 in textdict:
		keystext = textdict[1]
	else:
		keystext = textdict['keys']

	if 2 in textdict:
		aggtext = textdict[2]
	else:
		aggtext = textdict['aggregation']

	if 'pandas' in uridict:
		pdid = URIRef(uridict['pandas'])
	else:
		pdid = example.pandas
		uridict['pandas'] = str(pdid)

	if 'numpy' in uridict:
		npid = URIRef(uridict['numpy'])
	else:
		npid = example.numpy
		uridict['numpy'] = str(npid)

	returnid = URIRef(uridict['return'])
	returntext = textdict['return']

	# add triples to the provenance graph
	provgraph.add((aid, RDF.type, pub.Transformation))
	provgraph.add((aid, DC.description, Literal("Group data in data frame "+dftext+" by key(s) "+keystext+" and aggregate by function "+aggtext+" to get data in "+returntext)))
	provgraph.add((aid, pub.language, Literal("Python")))
	provgraph.add((aid, prov.startedAtTime, Literal(stime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, prov.endedAtTime, Literal(etime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, pub.transformed, dfid))
	provgraph.add((dfid, RDF.type, pub.InMemoryData))
	provgraph.add((dfid, DC.description, Literal("Data frame held by variable or expression "+dftext)))
	provgraph.add((aid, prov.used, pdid))
	provgraph.add((pdid, RDF.type, pub.Library))
	provgraph.add((pdid, DC.description, Literal("The pandas Python library")))
	provgraph.add((aid, prov.used, npid))
	provgraph.add((npid, RDF.type, pub.Library))
	provgraph.add((npid, DC.description, Literal("The numpy Python library")))
	provgraph.add((aid, prov.generated, returnid))
	provgraph.add((returnid, RDF.type, pub.InMemoryData))
	provgraph.add((returnid, DC.description, Literal("Data held by variable or expression "+returntext)))
	return ret

def average(li, **kwargs):
	if 'namespace' not in kwargs:
		return np.average(li)

	# record activity starting time
	stime = datetime.utcnow()

	# execute normal operation
	ret = np.average(li)

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

	# id and text for activity, used data object, library, and return value
	aid = URIRef(uridict['fun'])

	if 0 in uridict:
		listid = URIRef(uridict[0])
	else:
		listid = URIRef(uridict['li'])
	
	if 0 in textdict:
		listtext = textdict[0]
	else:
		listtext = textdict['li']

	if 'numpy' in uridict:
		npid = URIRef(uridict['numpy'])
	else:
		npid = example.numpy
		uridict['numpy'] = str(npid)

	returnid = URIRef(uridict['return'])
	returntext = textdict['return']

	# add triples to the provenance graph
	provgraph.add((aid, RDF.type, pub.Transformation))
	provgraph.add((aid, DC.description, Literal("Get the average of data in list "+listtext+" and save it at "+returntext)))
	provgraph.add((aid, pub.language, Literal("Python")))
	provgraph.add((aid, prov.startedAtTime, Literal(stime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, prov.endedAtTime, Literal(etime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, pub.transformed, listid))
	provgraph.add((listid, RDF.type, pub.InMemoryData))
	provgraph.add((listid, DC.description, Literal("Data held by variable or expression "+listtext)))
	provgraph.add((aid, prov.used, npid))
	provgraph.add((npid, RDF.type, pub.Library))
	provgraph.add((npid, DC.description, Literal("The numpy Python library")))
	provgraph.add((aid, prov.generated, returnid))
	provgraph.add((returnid, RDF.type, pub.InMemoryData))
	provgraph.add((returnid, DC.description, Literal("Data held by variable or expression "+returntext)))
	return ret

