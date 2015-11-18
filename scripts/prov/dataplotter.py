import pandas as pd
from rdflib import Graph, URIRef, RDF, Namespace, Literal
from rdflib.namespace import DC, XSD
from datetime import datetime
import matplotlib.pyplot as plt

def plot(dataframe, kind, figsize, **kwargs): # namespace="", textdict = {}, uridict={}, provgraph=None
	if 'namespace' not in kwargs:
		plt.style.use('ggplot')
		return dataframe.plot(kind=kind, figsize=figsize).get_figure()
		
	# record activity starting time
	stime = datetime.utcnow()

	# execute normal operation
	plt.style.use('ggplot')
	ret = dataframe.plot(kind=kind, figsize=figsize).get_figure()

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
	
	if 'pandas' in uridict:
		pdid = URIRef(uridict['pandas'])
	else:
		pdid = example.pandas
		uridict['pandas'] = str(pdid)
	
	if 'matplotlib.pyplot' in uridict:
		pltid = URIRef(uridict['matplotlib.pyplot'])
	else:
		pltid = example['matplotlib.pyplot']
		uridict['matplotlib.pyplot'] = str(pltid)

	returnid = URIRef(uridict['return'])
	
	# add triples to the provenance graph
	provgraph.add((aid, RDF.type, pub.Visualization))
	provgraph.add((aid, DC.description, Literal("Visualize data in "+dftext+" with the matplotlib.pyplot library")))
	provgraph.add((aid, pub.language, Literal("Python")))
	provgraph.add((aid, prov.startedAtTime, Literal(stime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, prov.endedAtTime, Literal(etime.strftime("%Y-%m-%dT%H:%M:%SZ"), datatype=XSD.dateTime)))
	provgraph.add((aid, pub.visualized, dfid))
	provgraph.add((dfid, RDF.type, pub.InMemoryData))
	provgraph.add((dfid, DC.description, Literal("Data held by variable or expression "+dftext)))
	provgraph.add((aid, prov.used, pdid))
	provgraph.add((pdid, RDF.type, pub.Library))
	provgraph.add((pdid, DC.description, Literal("The pandas Python library")))
	provgraph.add((aid, prov.used, pltid))
	provgraph.add((pltid, RDF.type, pub.Library))
	provgraph.add((pltid, DC.description, Literal("The matplotlib.pyplot Python library")))
	provgraph.add((aid, prov.generated, returnid))
	provgraph.add((returnid, RDF.type, pub.PublishedResult))
	provgraph.add((returnid, DC.description, Literal("Figure held by variable "+textdict['return'])))
	return ret

