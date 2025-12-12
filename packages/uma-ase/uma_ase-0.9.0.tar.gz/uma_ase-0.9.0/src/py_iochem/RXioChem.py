'''Diego Garay-Ruiz, 2021
Management of reaction networks via ioChem-BD'''
from py_iochem.RESTAPIManager import ReportHandler,prompt_token
from collections import OrderedDict
import configparser
import json
import networkx as nx

### Classes

	### General functaions for managing the upload of reaction networks to ioChem-BD
def simple_prop_fetch(G,key,prop):
	# Function to fetch properties from edges or nodes
	if (isinstance(key,tuple)):
		return G.edges[key][prop]
	else:
		return G.nodes[key][prop]

def prepare_network_config(graph_file,config_file):
	'''From a simple CRN where nodes and edges have the corresponding formula field mapping
	stages to individual calculations, prepare required I/O files
	Input:
	- graph_file. String, JSON graph containing the CRN, where formulas consistent with output file names are defined.
	- config_file. String, INI-organized config file containing data about the CRN.
	Output:
	Generates bash_upload_config.dat and iochem_upload_summ.dat files

	'''

	config = configparser.ConfigParser()
	config.read(config_file)

	G = read_json_graph(graph_file,False,None)
	species_names = []
	for nd in G.nodes(data="formula"):
		species_names += nd[1].split("+")

	for ed in G.edges(data="formula"):
		if not ed[2]:
			continue
		species_names += ed[2].split("+")

	species_names = sorted(list(set(species_names)))

	calculation_path = config["Uploader"]["calculations_path"]
	upload_summary = [(spc,"%s/%s.in" % (calculation_path,spc),"%s/%s.out" % (calculation_path,spc)) for spc in species_names]
	with open("iochem_upload_summ.dat","w") as fout:
		out_block = "\n".join([";".join(line) for line in upload_summary]) + "\n"
		fout.write(out_block)

	bash_config_gen(config)
	return None

	
def bash_config_gen(config,outfile="bash_upload_config.dat"):
	'''Generates the text file with information for the ioChem-BD shell script.
	Input:
	- config. Instantiated ConfigParser() object with read configuration information.
	- outfile. String, name of the file to be written.
	Output:
	- None, writes to file.'''

	out_bash_block = ""
	# Prepare bash script config & dump to file
	remote_data = [config["Uploader"].get(par) for par in ["remote_folder","remote_description","shell_route","iochem_route"]]
	out_bash_block += "\n".join(remote_data)
	out_bash_block += "\n"
	with open(outfile,"w") as fout:
		fout.write(out_bash_block)
	return None

def calcid_reader(fn_calcids):
	'''Generates an OrderedDict mapping names to calculation IDs from the raw output of network_parser().
	Input:
	- fn_calcids. String, filename to be read.
	Output:
	- calcid_dict. OrderedDict mapping calc. names to its ID and to its corresponding order in the initial definition, as a cN string -> for simplicity, although it could be recovered from the dict'''
	with open(fn_calcids,"r") as fids:
		calcid_info = [entry.strip().split(";") for entry in fids.readlines() if entry]
		# assign to dict, including the cN locator
	calcid_dict = OrderedDict((name.strip(),[int(cid),"c%d" % (ii+1)])
							  for ii,(name,cid) in enumerate(calcid_info))
	return calcid_dict

def read_json_graph(graph_file,add_cid_formulas=False,cid_mapping_file=None):
	'''Read a JSON graph (as produced by auto_network_parsing) and possibly map
	formulas to cid-based formulas using a calcid mapping'''
	with open(graph_file,"r") as fgr:
		graph_data = json.load(fgr)
	G = nx.cytoscape_graph(graph_data)

	# Check whether cid_formula field is already present
	nodes_have_cf = ["cid_formula" in nd[1] for nd in G.nodes(data=True)]
	edges_have_cf = ["cid_formula" in ed[2] for ed in G.edges(data=True)]

	if all(nodes_have_cf) and all(edges_have_cf):
		add_cid_formulas = False

	if not add_cid_formulas:
		return G
	if add_cid_formulas and (not cid_mapping_file):
		print("A calcid mapping file is required")
		return None


	cid_mapping = calcid_reader(cid_mapping_file)
	for nd in G.nodes(data=True):
		formula_raw = nd[1].get("formula",None)
		if not formula_raw:
			elements = [nd[0]]
		else:
			elements = formula_raw.replace(" ","").split("+")
		cid_elems = [cid_mapping[el][0] for el in elements]
		cid_formula = "+".join([str(el) for el in cid_elems])
		nd[1]["cid_formula"] = cid_formula

	for ed in G.edges(data=True):
		formula = ed[2].get("formula",None)
		if not formula:
			ed[2]["cid_formula"] = None
		else:
			elements = formula.split("+")
			cid_elems = [cid_mapping[el][0] for el in elements]
			cid_formula = "+".join([str(el) for el in cid_elems])
			ed[2]["cid_formula"] = cid_formula

	return G

def report_definer(G,info={}):
	'''Prepare the required parameters and series/variables definitions for an ioChem report.
	Input:
	- config. ConfigParser object with configuration info
	- G. NetworkX Graph object, should contain cid_formula field to map nodes and edges to calcIds
	- calcid_dict. OrderedDict mapping calc. names to its ID and to its corresponding order in the initial definition, as a cN string
	- reference. String for the FORMULA to be used as energy reference, to look up in calcid_dict
	Output:
	- report. ReportHandler object with assigned properties (name, description, configuration...)'''

	# Go through the graph and retrieve all calcIds
	cid_list = []
	for nd in G.nodes(data=True):
		current_cids = nd[1]["cid_formula"].split("+")
		new_cids = [cid for cid in current_cids if cid not in cid_list]
		cid_list.extend(new_cids)

	for ed in G.edges(data=True):
		cid_string = ed[2].get("cid_formula",None)
		if not cid_string:
			continue
		current_cids = cid_string.split("+")
		new_cids = [int(cid) for cid in current_cids if int(cid) not in cid_list]
		cid_list.extend(new_cids)

	# Dump the graph
	graph_data = nx.cytoscape_data(G)
	graph_json = json.dumps(graph_data)
	graph_json_de = json.dumps(graph_json).replace(" ","")
	report_config = "<configuration><parameters><graph>"
	report_config += graph_json_de
	report_config += "</graph></parameters></configuration>"

	# Assign things to the report
	report_name = info["report_name"]
	report_desc = info["report_desc"]
	report_properties = {"name":report_name,"title":report_name,
							"description":report_desc,
							"configuration":report_config,
							"reportTypeId":4}

	return report_properties

def report_instantiation(file_config,G,file_calcids,
						 add_calcs=True,verify=True):
	'''Wrapper for report instantiation from input files (profiles, calcids & configuration).
	Input:
	- file_config. String, file to read config from.
	- G. NetworkX.Graph
	- file_calcids. String, file to read calcids from (as generated by the S2 shell script).
	- prune_profiles. Boolean, if True, prune the profiles to avoid repeated species.
	- add_calcs. Boolean, if True, directly create the report in ioChem and map the calculations.
	Output:
	- report. ReportHandler object with assigned properties (name, description, configuration...)'''
	calcids = calcid_reader(file_calcids)

	# Read the configuration to get login details
	config = configparser.ConfigParser()
	config.read(file_config)
	rest_url = config["Connection"]["restUrl"]
	#login_details = config["Uploader"]["iochem_"]
	token = prompt_token(rest_url,config["Connection"]["username"],verify=verify)

	report_info = report_definer(G,{"report_name":config["Network"]["name"],
											"report_desc":config["Network"]["description"]})

	report = ReportHandler(rest_url,None,token,verify)
	if (add_calcs):
		resp = report.create_report(report_info,auto_rid=True)
		calc_ids_list = [v[0] for v in calcids.values()]
		resp_calcs = report.assign_calcs_to_report(calc_ids_list)
	return report

# Handling of pre-loaded networks & profiles
def calc_matching(G,frag_matching,renaming_func=None):
	'''Maps nodes/edges in the input graph to the corresponding calculations. Checks frag_matching
	to find fragments, and all other species are assumed to be a single calculation named after its
	node or edge. A renaming function can be provided to transform names in the graph to names
	in the calculations (e.g. changing upper/lowercase or doing simple string substitutions.)
	Input:
	- G. NetworkX.Graph object as generated by RXReader.RX_builder()
	- frag_info. Dictionary mapping nodes and edges in the network to individual calculation names,
	as from product_fragment_matching().
	- renaming_func. Simple function for desired string transformation.
	Output:
	- full_frag_info. Dictionary, mapping every node/edge to a list of the corresponding chemical
	species according to frag_matching and to the renaming rule.
	'''
	full_frag_info = {}
	node_names = [nd[1] for nd in G.nodes(data="name")]
	edge_names = [ed[2] for ed in G.edges(data="name")]
	for entry in (node_names + edge_names):
		if (entry not in frag_matching.keys()):
			mapped_species = [entry]
		else:
			mapped_species = [entry] + [frag_matching[entry]]

		if (renaming_func):
			mapped_species[:] = [renaming_func(nm) for nm in mapped_species]
		full_frag_info[entry] = list(set(mapped_species))
	return full_frag_info


def report_reacgraph_definition(graph_content,report_name,report_desc):
	'''Generates the necessary string for a POST request to Create API
	from a JSON-based graph, passed as a dictionary.
	Input:
	- graph_content. Dictionary, containing a Cytoscape-compliant graph
	Output:
	- report_propdict. Dictionary, containing the formatted XML-based string for ioChem-BD compatibility ("configuration"),
	as well as name, title, description and reportTypeId for ioChem-BD.
	'''
	## remove non-compliant elements
	invalid_keys = [k for k in graph_content.keys() if k not in ["data","elements"]]
	if "data" not in graph_content.keys():
		graph_content["data"] = []
	for k in invalid_keys:
		del graph_content[k]

	# Clear things and define list of calculations
	all_cids = []
	allowed_fields = ["name","cid_formula","source","target","id"]
	for item in (graph_content["elements"]["nodes"] + graph_content["elements"]["edges"]):
		out_keys = [k for k in item["data"].keys() if k not in allowed_fields]
		for k in out_keys:
			item["data"].pop(k,None)

		all_cids += item["data"]["cid_formula"].split("+")

	graph_json = json.dumps(graph_content)
	report_config = "<configuration><parameters><graph>"
	report_config += graph_json
	report_config += "</graph></parameters></configuration>"

	# Assign things to the report
	report_propdict = {"reportType":None,"name":report_name,"title":report_name,
							"description":report_desc,
							"configuration":report_config,
							"calculationIds":",".join(all_cids)
							}
	return report_propdict

def auto_report_from_json(graph_file,calcid_file,config_file):
	'''Generation of a report in ioChem-BD via REST API from a Cytoscape-compliant graph in JSON format
	Input:
	- graph_file. String, name of the graph file containing the CRN. Nodes/edges must have a cid_formula field
	mapping them to the calculation IDs in ioChem-BD
	- calcid_file. String, name of the file mapping calculation names to their corresponding IDs.
	- config_file. String, INI-organized config file containing data about the report.
	- rest_url. String, REST API endpoint to be used.
	- user_name. String, mail address of the user in ioChem-BD.
	Output:
	- report. ReportHandler object containing all information.
	Generates a new report in ioChem-BD.
	'''
	### Read the JSON and prepare report info
	G = read_json_graph(graph_file,True,calcid_file)
	G_json = nx.cytoscape_data(G)

	### API interaction
	config = configparser.ConfigParser()
	config.read(config_file)

	rest_url = config["ioChem"]["rest_url"]
	user_name = config["ioChem"]["user_name"]

	token = prompt_token(rest_url,user_name,False)
	### Preparing the report: metadata and XML content
	report = ReportHandler(rest_url,None,token,False)
	typeId = report.get_type_id()

	# Prepare the POST
	graph_properties = report_reacgraph_definition(G_json,config["Report"]["report_name"],config["Report"]["report_desc"])
	graph_properties["reportType"] = str(typeId)

	# POST
	report.create_report(graph_properties)
	calc_id_list = graph_properties["calculationIds"].split(",")
	r2 = report.assign_calcs_to_report(calc_id_list)
	print("Created report with id %d" % report.rid)
	return report
