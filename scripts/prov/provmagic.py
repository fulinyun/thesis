from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic
from IPython.core.interactiveshell import InteractiveShell
from IPython.core import magic_arguments
import re
from rdflib import Namespace, Literal
from rdflib.namespace import DC
from datetime import datetime
import urllib

@magics_class
class ProvMagics(Magics):

	@magic_arguments.magic_arguments()
	@magic_arguments.argument(
		'-v', '--verbose', action='store_true', default=False,
		help='Whether to print the rewritten code by %%prov or %%initprov.'
	)
	
	@cell_magic
	def prov(self, line, cell):
		args = magic_arguments.parse_argstring(self.prov, line)
		rewritten_cell = ""
		lines = cell.splitlines()
		for line in lines:
			rewritten_cell += rewrite(line, line, args.verbose)+"\n"
			if args.verbose:
				print("Actual code executed:\n"+rewritten_cell)
			get_ipython().run_cell(rewritten_cell)
			rewritten_cell = ""

		if rewritten_cell.strip() != "":
			if args.verbose:
				print("Actual code executed:\n"+rewritten_cell)
			get_ipython().run_cell(rewritten_cell)

	@cell_magic
	def initprov(self, line, cell):
		args = magic_arguments.parse_argstring(self.prov, line)
		rcode = """from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import DC, NamespaceManager
import operators
if '__NAMESPACE__' not in globals():
    __NAMESPACE__ = 'http://example.org/'
__URIDICT__ = {}
__TEXTDICT__ = {}
__PROV__ = Graph()
pub = Namespace("http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/")
prov = Namespace("http://www.w3.org/ns/prov#")
example = Namespace(__NAMESPACE__)
namespace_manager = NamespaceManager(Graph())
namespace_manager.bind('pub', pub, override=False)
namespace_manager.bind('prov', prov, override=False)
namespace_manager.bind('dc', DC, override=False)
namespace_manager.bind('', example, override=False)
__PROV__.namespace_manager = namespace_manager
"""
		if args.verbose:
			print("Actual code executed:\n"+rcode)
		get_ipython().run_cell(rcode)
		self.prov(line, cell)

def rewrite(origline, line, verbose=True):
	funtuple = matchfun(line)
	if not funtuple:
		proctuple = matchproc(line)
		if not proctuple:
			assigntuple = matchassign(line)
			if not assigntuple:
				deltuple = matchdel(line)
				if not deltuple:
					return line
				else:
					(obj, key) = deltuple
					line1 = obj+"=operators.delete("+obj+","+key+")"
					if verbose:
						print("First rewritten to:\n"+line1)
					return rewrite(line, line1, verbose)
			else:
				(lhs, rhs) = assigntuple
				line1 = lhs+"=operators.assign("+rhs+")"
				if verbose:
					print("First rewritten to:\n"+line1)
				return rewrite(line, line1, verbose)
		else:
			(fun, allargs) = proctuple
			rcode = "__TEXTDICT__ = {}\n"
			argsl = parseargs(allargs)
			for i in range(len(argsl)):
				if '=' in argsl[i]:
					[pname, text] = re.split("=", argsl[i])
					pname = pname.strip()
					text = text.strip()
					rcode += "__TEXTDICT__['"+pname+"'] = \""+text+"\"\n"
					rcode += "__URIDICT__['"+pname+"'] = __NAMESPACE__+'"+freshurl(pname)+"_a'\n"
				else:
					text = argsl[i].strip()
					rcode += "__TEXTDICT__["+str(i)+"] = \""+text+"\"\n"
					rcode += "__URIDICT__["+str(i)+"] = __NAMESPACE__+'"+freshurl(text)+"_a'\n"
			rcode += "__TEXTDICT__['fun'] = \""+fun+"\"\n"
			rcode += "__URIDICT__['fun'] = __NAMESPACE__+'"+freshurl(fun)+"'\n"
			rcode += "__PROV__.add((URIRef(__URIDICT__['fun']), pub.code, Literal(\""+origline.replace('"', '\\"')+"\")))\n"
			rcode += fun+"("+allargs+", namespace=__NAMESPACE__, textdict=__TEXTDICT__, uridict=__URIDICT__, provgraph=__PROV__)"
			return rcode
	else:
		(ret, fun, allargs) = funtuple
		rcode = "__TEXTDICT__ = {}\n"
		argsl = parseargs(allargs)
		for i in range(len(argsl)):
			if '=' in argsl[i]:
				[pname, text] = re.split("=", argsl[i])
				pname = pname.strip()
				text = text.strip()
				rcode += "__TEXTDICT__['"+pname+"'] = \""+text+"\"\n"
				rcode += "__URIDICT__['"+pname+"'] = __NAMESPACE__+'"+freshurl(pname)+"_a'\n"
			else:
				text = argsl[i].strip()
				rcode += "__TEXTDICT__["+str(i)+"] = \""+text+"\"\n"
				rcode += "__URIDICT__["+str(i)+"] = __NAMESPACE__+'"+freshurl(text)+"_a'\n"
		rcode += "__TEXTDICT__['fun'] = \""+fun+"\"\n"
		rcode += "__URIDICT__['fun'] = __NAMESPACE__+'"+freshurl(fun)+"'\n"
		rcode += "__TEXTDICT__['return'] = \""+ret+"\"\n"
		rcode += "__URIDICT__['return'] = __NAMESPACE__+'"+freshurl(ret)+"'\n"
		rcode += "__PROV__.add((URIRef(__URIDICT__['fun']), pub.code, Literal(\""+origline.replace('"', '\\"')+"\")))\n"
		funcall = fun+"("+allargs+", namespace=__NAMESPACE__, textdict=__TEXTDICT__, uridict=__URIDICT__, provgraph=__PROV__)"
		rcode += "__RETURN__ = None\n"
		rcode += "__RETURN__ = "+funcall
		rcode += "\n" + ret + " = __RETURN__"
		return rcode

def matchfun(line):
	line = stripcomment(line).strip()
	result = re.match(r"(.*?)=\s*(\S+?)\s*\((.*)\)", line)
	if not result:
		return None
	ret = result.group(1).strip()
	fun = result.group(2)
	allargs = result.group(3).strip()
	return (ret, fun, allargs)
	
def matchproc(line):
	line = stripcomment(line).strip()
	result = re.match(r"(\S+)\s*\((.*)\)", line)
	if not result:
		return None
	fun = result.group(1)
	allargs = result.group(2).strip()
	return (fun, allargs)

def matchassign(line):
	line = stripcomment(line).strip()
	result = re.match(r"(.*?)=(.*)", line)
	if not result:
		return None
	lhs = result.group(1).strip()
	rhs = result.group(2).strip()
	return (lhs, rhs)

def stripcomment(line):
	ret = ""
	instring = False
	quotation = '"'
	escape = False
	for c in line:
		if c == '#' and not instring:
			return ret
		ret += c
		if escape:
			escape = False
		elif c == '\\':
			escape = True
		elif c == '"' and not instring:
			instring = True
			quotation = c
		elif c == '"' and instring and quotation == '"':
			instring = False
		elif c == "'" and not instring:
			instring = True
			quotation  = c
		elif c == "'" and instring and quotation == "'":
			instring = False
	return ret

def matchdel(line):
	line = stripcomment(line).strip()
	result = re.match(r"del\s*(\S+)\s*\[(.*)\]", line)
	if not result:
		return None
	obj = result.group(1)
	key = result.group(2).strip()
	return (obj, key)

def parseargs(allargs):
	ret = []
	instring = False
	quotation = '"'
	escape = False
	left1 = 0
	left2 = 0
	left3 = 0
	currentarg = ""
	for c in allargs:
		if c == ',' and left1 == 0 and left2 == 0 and left3 == 0 and not instring:
			ret.append(currentarg)
			currentarg = ""
		else:
			currentarg += c
			if escape:
				escape = False
			elif c == '\\':
				escape = True
			elif c == '"' and not instring:
				instring = True
				quotation = '"'
			elif c == '"' and instring and quotation == '"':
				instring = False
			elif c == "'" and not instring:
				instring = True
				quotation = "'"
			elif c == "'" and instring and quotation == "'":
				instring = False
			elif c == '(' and not instring:
				left1 += 1
			elif c == ')' and not instring:
				left1 -= 1
			elif c == '[' and not instring:
				left2 += 1
			elif c == ']' and not instring:
				left2 -= 1
			elif c == '{' and not instring:
				left3 += 1
			elif c == '}' and not instring:
				left3 -= 1
	ret.append(currentarg)
	return ret

def timestr():
	return datetime.utcnow().strftime("_%A_%d_%B_%Y_%I_%M_%S_%p")

def freshurl(name):
	return urllib.quote_plus(name+timestr())

ip = get_ipython()
ip.register_magics(ProvMagics)

