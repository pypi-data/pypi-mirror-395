'''Diego Garay-Ruiz, 2024
Python interface to the REST API in ioChem-BD's Create module. The CollectionHandler class
allows to fetch information from collections, including the calcIds of the corresponding calculations,
and then fetch the files on these calculations or query them.'''

from collections import OrderedDict
from getpass import getpass
import re
import requests
from urllib.parse import quote_plus
import json

def prompt_token(rest_url,username,verify=True):
    """
    Request a login token from ioChem-BD REST API, passing username and interactively
    prompting for the password.
    Parameters:
    -----------
    rest_url : str
            The base URL for the ioChem-BD REST API.
    username: str
        The mail address to login to ioChem-BD
    verify : bool, optional
        Whether to verify SSL certificates for HTTPS requests. Default is True.

    Returns:
    --------
    token : str
        The authentication token used for API authorization.
    """
    print("Logging in as %s: enter password" % username)
    login_url = rest_url + "/login"
    full_url = login_url# % (quote_plus(username),quote_plus(getpass()))
    resp = requests.post(url=full_url,verify=verify,auth=(username,getpass()))
    token = resp.text
    return token

class ioChemHandler:
    def __init__(self,rest_url,project_id,token,service="create",verify=True):
        """
        Initialize a CollectionHandler instance.

        This constructor sets up the basic configuration for interacting with the ioChem-BD API,
        including the root URL, project ID, authentication token, and SSL verification setting.

        Parameters:
        -----------
        rest_url : str
            The base URL for the ioChem-BD REST API.
        project_id : str
            The unique identifier for the project or collection in ioChem-BD.
        token : str
            The authentication token used for API authorization.
        service : str
            Requested ioChem-BD service: Find, Browse or Create. 
            Two first are public, do not require token. 
        verify : bool, optional
            Whether to verify SSL certificates for HTTPS requests. Default is True.

        Returns:
        --------
        None
            This method initializes instance attributes but does not return any value.
        """
        self.rootURL = rest_url
        self.passedId = project_id
        self.collectionId = project_id
        self.idField = "id"
        self.service = service.lower()
        self.bitstreamMapping = {}      # only required for Find and Browse
        self.fileDictionary = {}
        self.numItems = 0
        if self.service == "create":
            self.headers = self.iochem_header_generator(token)
        else:
            # No POST requests are possible here
            self.headers = {"GET":{"Accept":"application/json"}}
        self.verify = verify

        # Setting up query URLs and other parameters
        if self.service == "create":
            self.itemQuery = "%s/project/descendant?type=calculation&depth=all&searchType=id&id=%s" % (self.rootURL,self.collectionId)
            self.mapKey = "id"

        # Find and Browse are based on collection handles, and need a mapping to the ID field
        elif self.service in ["find","browse"]:
            id_types = {"find":"uuid","browse":"id"}
            self.idField = id_types[self.service]
            query_id = "%s/handle/%s" % (self.rootURL,self.passedId)
            req_id = requests.get(query_id,headers=self.headers["GET"],verify=self.verify)
            
            self.numItems = req_id.json()["numberItems"]

            current_id = req_id.json()[self.idField]
            self.collectionId = current_id
            
            self.itemQuery = "%s/collections/%s/items" % (self.rootURL,self.collectionId)
            self.mapKey = "handle"
        else:
              print("No valid service requested. Exiting.")
              return None

    def iochem_header_generator(self,token):
        """
        Generate headers for different HTTP methods used in ioChem-BD Create API requests.

        This method creates headers for GET, POST, and GETB (GET Binary) requests
        using the provided authentication token.

        Parameters:
        -----------
        self : object
            The instance of the class containing this method.
        token : str
            The authentication token used for API authorization.

        Returns:
        --------
        header_dict : dict
            A dictionary containing headers for different HTTP methods:
            - 'GET': Headers for GET requests
            - 'POST': Headers for POST requests
            - 'GETB': Headers for GET Binary requests

        Each header includes the necessary content type, accept type, and authorization
        information required for ioChem-BD API communication.
        """
        headers_get = {'Accept':'application/json','Authorization': 'Bearer ' + token}
        headers_post = {'Content-Type':'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
        headers_getb = {'Accept':'application/octet-stream','Authorization':'Bearer ' + token}
        header_dict = {"GET":headers_get, "POST":headers_post, "GETB":headers_getb}
        return header_dict
    

class CollectionHandler(ioChemHandler):
    #### Fixed to support all services
    def get_items(self,query_limit=None):
        """
        Retrieve the list of items (calculations) in a given collection.

        This method fetches all calculation items from the specified collection using the ioChem-BD API.
        It constructs a query URL based on the collection ID and sends a GET request to retrieve the items.
        The response is then processed to extract a list of calculation items.

        Parameters:
        -----------
        self : object
            The instance of the class containing this method.
        query_limit : integer
            If not None, use paging to target the results.
        
        Returns:
        --------
        item_list : list
            A list of dictionaries, where each dictionary represents a calculation item
            in the collection. The structure of these dictionaries depends on the API response.
        """

        # Only support paging for Browse and Find
        if self.service in ["find","browse"] and query_limit:
            max_items = self.numItems
            offset_range = list(range(0,max_items,query_limit))
            queries_items = [self.itemQuery + "?limit=%d&offset=%d" % (query_limit,offset)
                               for offset in offset_range]
        else:
            queries_items = [self.itemQuery]

        # Get all calculations in the collection
        item_list = []
        for query in queries_items:
            req_items = [requests.get(query,headers=self.headers["GET"],verify=self.verify)]
            req_items_json = [item.json() for item in req_items if item]
            item_list += [item for entry in req_items_json for item in entry if item]

        # Add an additional property to manage file input/output
        for item in item_list:
            item["isTarget"] = True 

        self.itemList = item_list
        self.workingItemList = item_list
        print("Built item list with %d entries" % len(self.itemList))
        return item_list

    def get_item_dict(self,query_items=None):
        """
        Create a mapping between item IDs and names for the collection.

        This method retrieves information about items in the collection and creates
        an ordered dictionary mapping item IDs to their corresponding names.

        Parameters:
        -----------
        self : object
            The instance of the class containing this method.
        query_limit : integer
            If not None, use paging to target the results.

        Returns:
        --------
        None
            This method doesn't return a value directly. Instead, it sets the
            'itemHierarchy' attribute of the class instance to the created dictionary.
        """
        info_items = self.get_items(query_items)
        items_dict = OrderedDict((entry[self.mapKey],(entry["name"],entry[self.idField]))
                                 for entry in info_items)
        self.itemHierarchy = items_dict
        return None 
    
    def filter_names(self,names_to_filter,mode="exclude"):
        """
        Controls the isTarget property of all items in the collection depending on the strings in the list names_to_filter.
        If mode = "exclude", the entries that contain the target string will be set to False, and NOT downloaded
        If mode = "include", ONLY the entries containing the target string will be set to True, and thus downloaded
        """
        for item in self.workingItemList:
            bool_value = any([name in item["name"] for name in names_to_filter])
            if mode == "exclude":
                item["isTarget"] = not bool_value 
            else: 
                item["isTarget"] = bool_value 
        self.filter_item_list()
        return None

    def filter_item_list(self):
        """
        Modifies the workingItemList in the CollectionHandler by skipping all entries with isTarget = False
        """
        self.workingItemList = [item for item in self.itemList if item["isTarget"]]
        return None

    def get_bitstreams_by_id(self,id_item,all_files=False):
        """
        For Find and Browse modules, get the bitstreams of a single element for file retrievak
        Additional filter to match Create API behavior: get only the input and output files
        """
        query_bitstreams = "%s/items/%s/bitstreams" % (self.rootURL,id_item)
        req_bitstreams = requests.get(query_bitstreams,headers=self.headers["GET"],verify=self.verify)
        bitstream_dump = req_bitstreams.json()
        bitstream_elements = [(elem["name"],elem[self.idField],elem["format"]) for elem in bitstream_dump]
        if not all_files:
            io_mask = [(elem[0] == "output.cml" or "input" in elem[2].lower()) for elem in bitstream_elements]
            bitstream_elements[:] = [elem for elem,mask in zip(bitstream_elements,io_mask) if mask]

        return bitstream_elements

    def get_bitstreams(self,all_files=False):
        """
        For Find and Browse modules, get a mapping between the items and their bitstream elements for file retrieval.
        """
        bitstream_mapping = {}
        for item in self.workingItemList:
            bitstream_elements = self.get_bitstreams_by_id(item[self.idField],all_files=all_files)
            # For each item, map the handle to the item name and its bitstream ID 
            bitstream_mapping[item["handle"]] += bitstream_elements
        self.bitstreamMapping = bitstream_mapping
        return None

    def query_target_file_id(self,id_item,target_file):
        """Gets the URLs to query a given file for a given item"""
        if self.service == "create":
            base_url = "%s/calculation/files/bitstream?" % self.rootURL
            target_url = base_url + "id=%s&fileId=%s" % (id_item,target_file)

        elif self.service in ["find","browse"]:
            # must retrieve bitstreams for all items
            if self.bitstreamMapping:
                current_mapping = self.bitstreamMapping[id_item]
            else:
                current_mapping = self.get_bitstreams_by_id(id_item)
            current_mapping = {item[0]:item[1:] for item in current_mapping}
            target_url = "%s/bitstreams/%s/retrieve" % (self.rootURL,current_mapping[target_file][0])
        return target_url

    def get_files(self,outdir="cmlfiles",save_file=True,idx_to_print=20,skip_inputs=False):
        """
        Retrieve CML (Chemical Markup Language) files and input files for all items in the collection.

        This function iterates through the list of items in the collection, fetches the
        corresponding CML file for each item, and either saves it to disk or stores it
        in memory, depending on the 'save_file' parameter.

        Parameters:
        -----------
        outdir : str, optional
            The directory where CML files will be saved if save_file is True.
            Default is "cmlfiles".
        save_file : bool, optional
            If True, save the CML files to disk. If False, store them in memory.
            Default is True.

        idx_to_print : integer,optional
            Number of processed entries after which a message will be printed to check the status.
            Default is 20.
        Returns:
        --------
        tracking_list : list
            A list of lists, where each inner list contains:
            [output_filename, item_name, item_id]
        out_buffer : list
            A list of CML file contents (as strings) if save_file is False.
            An empty list if save_file is True.
        """
        out_buffer = []
        tracking_list = []
        if not self.fileDictionary:
            self.get_all_file_info()

        ct = 0
        print("Starting download:")
        for item in self.workingItemList:
            id_item = item[self.idField]
            key_item = item[self.mapKey]
            files = self.fileDictionary[id_item]

            if skip_inputs:
                files = [fn for fn in files if fn == "output.cml"]  # redundant, but may enable more flexibility later if desired

            if ct % idx_to_print == 0:
                print("%d calculations downloaded" % ct)

            for fn in files:
                name_item = item["name"]
                if fn == "output.cml":
                    out_fname = "%s/calc_%s.cml" % (outdir,str(key_item).replace("/","_"))
                else:
                    out_fname = "%s/%s" % (outdir,fn) 
                current_query = self.query_target_file_id(id_item,fn) 
                
                req = requests.get(current_query,headers=self.headers["GET"],verify=self.verify)
                if save_file:
                    with open(out_fname,"w") as fout:
                        fout.write(req.text)
                    tracking_list.append([name_item,key_item,out_fname,fn])
                else:
                    out_buffer.append([req.text])
                    tracking_list.append([name_item,key_item,None,fn])

            ct += 1
        return tracking_list,out_buffer

    def get_file_info(self,id_item):
        """
        Retrieve file information for a specific item in the collection.

        This function queries the ioChem-BD API to get information about files associated
        with a given item (calculation) ID. It processes the response to extract a list
        of filenames -> the input and the output.

        Parameters:
        -----------
        id_item : str
            The unique identifier of the item (calculation) for which to retrieve file information.

        Returns:
        --------
        tuple
            A tuple containing two elements:
            1. id_item (str): The input item ID.
            2. files_list (list): A list of filenames associated with the item.
        """

        # Two parallel operation modes, for Create and Find/Browse 

        if self.service == "create":
            file_info_query = "%s/calculation/files?searchType=id&id=%s&type=files" % (self.rootURL,id_item)
            req = requests.get(file_info_query,headers=self.headers["GET"],verify=self.verify)
            files_string = req.text
            # this is a string that we should transform to a valid list, removing all leading quotes and initial and final brackers
            files_list = [item.strip("\"") for item in files_string.split(",")]
            files_list[0] = re.sub("^\[","",files_list[0]).strip("\"")
            files_list[-1] = re.sub(']$',"",files_list[-1]).strip("\"")
        elif self.service in ["find","browse"]:
            if self.bitstreamMapping:
                files_list = [item[0] for item in self.bitstreamMapping[id_item]]
            else:
                files_list = [item[0] for item in self.get_bitstreams_by_id(id_item)]
        file_data = (id_item,files_list)
        return file_data

    def get_all_file_info(self):
        """
        Retrieve file information for all items in the collection.

        This method fetches file information for each item in the collection's item list.
        If the item list hasn't been populated yet, it calls the get_items() method to
        retrieve the items first.

        Returns:
        --------
        This method does not return a value, but instead sets the fileDictionary attribute 
        to a dictionary where keys are item IDs and values are lists of file names associated with each item.
        """
        if not self.itemList:
            self.get_items()

        all_files_data = []
        for item in self.workingItemList:
            all_files_data.append(self.get_file_info(item[self.idField]))
        self.fileDictionary = dict(all_files_data)
        return None
    
    def save_tracking(tracking_info,output_file="tracking_info.csv"):
        tracking_list_str = "\n".join([",".join(entry) for entry in tracking_info]) + "\n"
        with open(output_file,"w") as fout:
            fout.write(tracking_list_str)
        return None
    
### Management of reports and reaction networks
class ReportHandler(ioChemHandler):
    def __init__(self,rest_url,report_id,token,verify=True):
        """
        Initialize a ReportHandler instance.

        This constructor sets up the basic configuration for interacting with the ioChem-BD API,
        including the root URL, project ID, authentication token, and SSL verification setting.

        Parameters:
        -----------
        rest_url : str
            The base URL for the ioChem-BD REST API.
        report_id : str
            The unique identifier for the project or collection in ioChem-BD.
        token : str
            The authentication token used for API authorization.
        verify : bool, optional
            Whether to verify SSL certificates for HTTPS requests. Default is True.

        Returns:
        --------
        None
            This method initializes instance attributes but does not return any value.
        """
        self.rootURL = rest_url
        self.reportId = report_id
        self.idField = "id"
        self.headers = self.iochem_header_generator(token)
        self.verify = verify

        self.property_dict = {}

    # Report-specific functions, using ReportHandler attributes to simplify the syntax of requests
    def get_report_properties(self):
        '''GET request for the properties associated with a report'''
        url = self.rootURL + "/report?id=%d" % self.rid
        print("GET",url)
        response = requests.get(url, headers=self.headers["GET"], verify=self.verify)
        return response

    def create_report(self,report_info,auto_rid=True):
        '''POST request to instantiate a new report in ioChem-BD, with automatic assignment of a reportId'''
        url = self.rootURL
        # Extract information to prepare the request
        full_url = url + "/report"
        response = requests.post(full_url,headers=self.headers["POST"],verify=self.verify,data=json.dumps(report_info))
        if (auto_rid):
            resp_json = response.json()
            self.rid = resp_json
        return response

    def assign_calcs_to_report(self, calc_id_list):
        # now this is a PUT request
        '''POST request to assign a given calculation to a report in ioChem-BD, with the reportId in the self.rid
        property of the ReportHandler.
        calcData: JSON-organized string with dict-type data for a calculation, containing.
        - calcId. Integer identifying the calculation in the database.
        - calcOrder. Integer, order of the calculation in the list of calculations
        - title. String, name of the calculation.
        - reportId. Integer, id of the report to which the calculation is assigned.'''
        url = self.rootURL + "/report/calculations"
        calc_id_str = ",".join([str(cid) for cid in calc_id_list])
        response = requests.put(url, headers=self.headers["POST"], verify=self.verify,
                                data=json.dumps({"id":self.rid,"listCalculations":calc_id_str}))
        print(json.dumps({"id":self.rid,"listCalculations":calc_id_str}))
        print(url)
        return response

    def get_type_id(self):
        url = self.rootURL + "/report-type"
        req = requests.get(url, headers=self.headers["GET"], verify=self.verify)
        sel_item = [item for item in req.json() if item["name"] == "Reaction Graph"][0]
        return sel_item["id"]
