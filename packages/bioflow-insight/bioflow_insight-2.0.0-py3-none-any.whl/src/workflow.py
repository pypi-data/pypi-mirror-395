#Import dependencies
#Local
from .nextflow_file import Nextflow_File
from .ro_crate import RO_Crate
from .condition import Condition
from .DBfile import DBfile
from . import constant
from .outils import is_git_directory, format_with_tabs, replace_thing_by_call, replace_group1, group_together_ifs, extract_curly, remove_extra_jumps, get_channels_to_add_in_false_conditions, extract_conditions, remove_empty_conditions_place_anker, get_basic_blocks, hsl_to_rgb
from .outils_graph import get_flatten_dico, initia_link_dico_rec, get_number_cycles, generate_graph, enrich_json_with_positions
from .outils_annotate import get_tools_commands_from_user_for_process
from .bioflowinsighterror import BioFlowInsightError
from .graph import Graph
import warnings
from .bioflowinsightwarning import BioFlowInsightWarning
from .language_server import Language_Server

#Outside packages
import os
import re
import json
from pathlib import Path
import glob
import ctypes
import time
import numpy as np

def get_object(address):
    address = int(re.findall(r"\dx\w+", address)[0], base=16)
    return ctypes.cast(address, ctypes.py_object).value


color_index = 0
class Workflow:
    """
    This is the main workflow class, from this class, workflow analysis can be done.
    After analysis, workflow structure reconstruction can be done.

    Attributes:
        file: A string indicating the address to the workflow main or the directory containing the workflow
        duplicate: A boolean indicating if processes are to be duplicated in the structure
        display_info: A boolean indicating if the analysis information should be printed
        output_dir: A string indicating where the results will be saved
        name: A string indicating the name of the workflow
    """

    def __init__(self, file, duplicate=True, display_info=True, output_dir = './results',
                 name = None, engines = ['nls', 'bioflow']):
        
        
        #Getting the main nextflow file
        if(not os.path.isfile(file)):
            nextflow_files = glob.glob(f'{file}/*.nf')
            if(len(nextflow_files)==0):
                raise BioFlowInsightError("nnfid", None)
            txt = ""
            #Try to read the main.nf file -> if this cannot be found then the first nextflow file is used
            try:
                
                file = file+"/main.nf"
                with open(file, 'r') as f:
                    txt= f.read()
            except:
                None
                #raise BioFlowInsightError("No 'main.nf' file found at the root of the prohject")
            if(txt==""):
                if(len(nextflow_files)==1):
                    file = nextflow_files[0]
                    with open(file, 'r') as f:
                        txt= f.read()
                else:
                    #If there are multiple files and no main -> we just choose one at random
                    file = nextflow_files[0]
                    with open(file, 'r') as f:
                        txt= f.read()
                    #raise BioFlowInsightError("Multiple Nextflow files found at the root with no 'main.nf' file: I don't know which one to select")


        self.file = file
        self.duplicate = duplicate
        self.display_info = display_info
        self.output_dir = Path(output_dir)
        self.nextflow_files = []
        self.workflow_directory = '/'.join(file.split('/')[:-1])
        self.name = name
        self.graph = None
        self.conditions_2_ignore = []
        self.ternary_operation_dico = {}
        self.map_element_dico = {}
        self.language_server = None
        self.all_conditions_language_server = {}
        self.engines = ['nls', 'bioflow']

        OG_file = Nextflow_File(self.file, workflow = self, first_file = True)
        self.DSL = OG_file.find_DSL()
        self.create_empty_results()
        if(self.display_info):
            print(f"Workflow is written in {self.DSL}")
        self.cycle_in_workflow = False
        self.alias_2_tools = {}
        self.scripts_2_tools = {}
        self.abstraction = None
        
    def purge(self):
        self.language_server = None
        self.nextflow_files = []
        OG_file = Nextflow_File(self.file, workflow = self, first_file = True)

    def get_name(self):
        if(self.name!=None):
            return self.name
        else:
            return self.get_root_directory().split('/')[-2]

    def get_workflow_directory(self):
        return self.workflow_directory

    def create_empty_results(self):
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.output_dir / 'debug', exist_ok=True)
        os.makedirs(self.output_dir / 'graphs', exist_ok=True)

        with open(self.output_dir / "debug" / "operations.nf",'w') as file:
            pass
        with open(self.output_dir / "debug" / "calls.nf",'w') as file:
            pass
        with open(self.output_dir / "debug" / "operations_in_call.nf",'w') as file:
            pass

    def get_cycle_status(self):
        return self.cycle_in_workflow 
    
    def get_root_directory(self):
        first_file = self.get_first_file()
        return '/'.join(str(first_file.get_file_address()).split('/')[:-1])+"/"

    def get_conditions_2_ignore(self):
        return self.conditions_2_ignore

    def get_duplicate_status(self):
        return self.duplicate

    def get_output_dir(self):
        return Path(self.output_dir)

    def get_DSL(self):
        return self.DSL
    
    def get_display_info_bool(self):
        return self.display_info
    
    def set_DSL(self, DSL):
        self.DSL = DSL

    def add_2_rocrate(self, dico):
        self.get_workflow_main().add_2_rocrate(dico)

    def get_first_file(self):
        for file in self.nextflow_files:
            if(file.first_file):
                return file
            
    def get_workflow_main(self):
        return self.get_first_file().main

    def add_nextflow_file_2_workflow(self, nextflow_file):
        self.nextflow_files.append(nextflow_file)
        self.nextflow_files = list(set(self.nextflow_files))
    
    def get_nextflow_file(self, address):
        for file in self.nextflow_files:
            if(file.get_file_address()==Path(os.path.normpath(address))):
                return file
        return None
    
    def print_citation(self):
        if(self.display_info):
            citation = """\nTo cite BioFlow-Insight, please use the following publication:
George Marchment, Bryan Brancotte, Marie Schmit, Frédéric Lemoine, Sarah Cohen-Boulakia, BioFlow-Insight: facilitating reuse of Nextflow workflows with structure reconstruction and visualization, NAR Genomics and Bioinformatics, Volume 6, Issue 3, September 2024, lqae092, https://doi.org/10.1093/nargab/lqae092"""
            print(citation)

    def initialise(self):

        

        if("nls" in self.engines and "bioflow" in self.engines):
            try:
                self.initialise_with_language_server() 
            except Exception as e:
                print(e)
                self.purge()
                self.initialise_with_bioflow()
        elif("bioflow" not in self.engines):
            self.initialise_with_language_server()
        else:
            self.initialise_with_bioflow()
        
    def is_initialised_with_bioflow(self):
        return self.get_workflow_main()!=None

    def initialise_with_bioflow(self, conditions_2_ignore = [], extract_tools = False):
        """Method that initialises the analysis of the worflow

        Keyword arguments:
        
        """
        self.conditions_2_ignore = conditions_2_ignore
        #Right now i'm just gonna do everything in DSL2

        #At this point there should only be one nextflow file
        if(len(self.nextflow_files)==1):
            self.nextflow_files[0].initialise()
        else:
            raise Exception("This souldn't happen. There are multiple Nextflow files composing the workflow before the analysis has even started.")
        
        self.print_citation()

        if(self.graph==None):
            self.graph = Graph(self)

        if(extract_tools):
            for p in self.get_processes_called():
                tools = p.get_tools()
                self.alias_2_tools[p.get_alias()] = tools
                self.scripts_2_tools[p.get_script_code()] = tools
        with open(self.get_output_dir()/"engine.txt", "w") as outfile: 
            outfile.write("bioflow")
    
    def initialise_with_language_server(self):
        self.language_server = Language_Server()
        self.print_citation()
        if(len(self.nextflow_files)==1):
            self.nextflow_files[0].initialise(language_server = self.language_server)
        else:
            raise Exception("This souldn't happen. There are multiple Nextflow files composing the workflow before the analysis has even started.")
        self.graph = Graph(self)
        with open(self.get_output_dir()/"engine.txt", "w") as outfile: 
            outfile.write("NLS")

    
    def get_link_dico_processes(self):
        self.graph.initialise()
        return self.graph.link_dico_processes




    def get_structure(self):
        dico = {}
        dico['nodes'] = []
        dico['edges'] = []
        dico['subworkflows'] = {}

        if(self.language_server==None):
            if(self.get_DSL() == "DSL1"):
                main = self.get_workflow_main()
                if(main!=None):
                    return main.get_structure(dico)
            elif(self.get_DSL() == "DSL2"):
                main = self.get_workflow_main()
                if(main!=None):
                    return main.get_structure(dico)
                else:
                    return dico
                #return self.get_structure_DSL2(dico=dico, start = True)
            else:
                raise Exception(f"The workflow's DSL is '{self.DSL}' -> I don't know what this is!")
        else:
            structure = self.get_first_file().get_structure(dico,  element = "")
            return structure


    #################
    #    GRAPHS
    #################

    def generate_specification_graph(self, render_graphs = True):
        self.graph.initialise()
        self.graph.get_specification_graph(render_graphs = render_graphs)
        self.enrich_json_files_with_positions()

    def generate_process_dependency_graph(self, render_graphs = True):
        self.graph.initialise()
        self.graph.render_process_dependency_graph(render_graphs = render_graphs)
        self.enrich_json_files_with_positions()

    def get_process_dependency_graph_dico(self):
        self.graph.initialise()
        self.graph.render_process_dependency_graph(render_graphs = False)
        return self.graph.get_process_dependency_graph()

    


    #TODO -> update this
    def generate_all_graphs(self, render_graphs = True):
        self.generate_specification_graph(render_graphs = render_graphs)
        self.generate_process_dependency_graph(render_graphs = render_graphs)
        self.enrich_json_files_with_positions()


    #This function takes the json files and searches for the corrresponding dot pos files
    #And adds the information regarding the position of the nodes
    def enrich_json_files_with_positions(self):
        jsons = glob.glob(f'{self.get_output_dir()/"graphs"}/*.json', recursive=False)
        for file in jsons:
            enrich_json_with_positions(file)
    
    #Method that checks if a given graph sepcification is an isomorphism with the workflows
    def check_if_json_equal_to_full_structure(self, file):
        return self.graph.check_if_json_equal_to_full_structure(file)

    def get_abstraction(self):
        from .abstraction import Abstraction
        self.abstraction = Abstraction(workflow = self)
        return self.abstraction.get_condition_abtsraction()

    def get_number_of_nodes_without_clouds(self):
        return self.abstraction.get_number_of_nodes_without_clouds()
    
    def get_number_split_subworkflows(self):
        number_split_subworkflows = 0
        subworkflows = self.get_operations_and_processes_per_subworkflows()
        nb_subworkflows = len(subworkflows)
        created_groups = self.abstraction.get_tree().get_groups({})

        def get_smallest_set(a, b):
            if(len(a)<len(b)):
                return a
            return b

        for sub in subworkflows:
            group_subworkflow = set(subworkflows[sub])
            split_subworkflow = False
            for c in created_groups:
                cluster = set(created_groups[c])
                #If the intersection of the two groups aren't equal
                if(group_subworkflow.intersection(cluster)!=set()):
                    #Verify that one group isn't including in the other
                    if(group_subworkflow.intersection(cluster)!=get_smallest_set(group_subworkflow, cluster)):
                        split_subworkflow = True
                        break
            if(split_subworkflow):
                number_split_subworkflows+=1

        return number_split_subworkflows, nb_subworkflows

    
    def get_metro_map_json(self, render_dot=True):
        global color_index

        self.generate_process_dependency_graph(render_graphs=render_dot)
        self.enrich_json_files_with_positions()
        json_file = glob.glob(f'{self.get_output_dir()/"graphs"}/process_dependency_graph.json', recursive=False)[0]
        with open(json_file, 'r') as JSON:
            full_workflow = json.load(JSON)
        metro_map_dico = {"nodes":[], "edges":[], "subworkflows":{}}
        
        def fill_metro_map(dico_wf, metro_map, current_sub = [], depth_sub_max = 0, ids_2_homogene_ids = {}):
            global color_index
            ids_added = []
            for node in dico_wf["nodes"]:
                process = get_object(node['id'])
                node['id'] = ids_2_homogene_ids[str(node['id'])]
                node["position"]['x'] = str(1.6*int(node["position"]['x']))
                node["position"]['y'] = str(1.6*int(node["position"]['y'])) 
                node['code'] = process.get_code()
                node['file_ref'] = f"({process.get_file_address(short = True)})"
                for ele in ["artificial", "shape", "xlabel", "fillcolor"]:
                    
                    try:
                        node.pop(ele)
                    except:
                        None
                if(node["id"] not in ids_added):
                    ids_added.append(node["id"])
                    metro_map["nodes"].append(node)
            for edge in dico_wf["edges"]:
                edge['A'] = ids_2_homogene_ids[str(edge['A'])]
                edge['B'] = ids_2_homogene_ids[str(edge['B'])]
                for ele in ["label"]:
                    edge.pop(ele)
                metro_map["edges"].append(edge)
            for sub in dico_wf["subworkflows"]:
                def get_all_nodes_in_sub(dico, nodes):
                    for node in dico["nodes"]:
                        nodes.append(ids_2_homogene_ids[str(node['id'])])
                    for sub in dico["subworkflows"]:
                        nodes = get_all_nodes_in_sub(dico["subworkflows"][sub], nodes)
                    return nodes
                all_nodes = get_all_nodes_in_sub(dico_wf['subworkflows'][sub], [])
                #TODO Check this
                #name = "_".join(sub.split("_")[:-1])
                name = sub

                subworkflows_colors = ["#f4f4f4",
                               "#cee2ff",
                               "#fffcd6",
                               "#defee1",
                               "#f6E4F3",
                               "#FFEDDE",
                               "#E2DCEB",
                               "#E4FDFF",
                               "#FFEBEB"]

                h = [
                    58,#yellow
                    100, #green
                    241, #dark blue
                     0,#red
                     177, #light blue
                     37,#oragne
                     281#purple
                     ]
                s = 90
                l_min, l_max = 85, 99
                if(all_nodes!=[]):
                    norm = (l_max-l_min)
                    if(depth_sub_max==0):
                        l = l_min
                    else:
                        l = l_max - (len(current_sub)/ depth_sub_max)**3 * norm
                        l = max(l, 99 - len(current_sub)*4)
                    color = '#%02x%02x%02x' % hsl_to_rgb(h = h[color_index%len(h)], s = s, l = l)
                    metro_map["subworkflows"]['.'.join(current_sub+[sub])] = {"nodes":all_nodes, "label":name, "color":color}
                    color_index+=1
                fill_metro_map(dico_wf['subworkflows'][sub], metro_map, current_sub+[sub], depth_sub_max, ids_2_homogene_ids)
        color_index = 0


        def get_sub_max(dico_wf, depth_sub_max):
            temp = depth_sub_max
            for sub in dico_wf["subworkflows"]:
                depth = get_sub_max(dico_wf["subworkflows"][sub], depth_sub_max+1)
                if(depth>temp):
                    temp = depth
            return temp
        
        def get_ids_2_homogene_ids(dico_wf, ids_2_homogene_ids, current_sub):
            for node in dico_wf["nodes"]:
                process = get_object(node['id'])
                ids_2_homogene_ids[str(process)] = ".".join(current_sub)+"."+str(process.get_alias())
            for sub in dico_wf["subworkflows"]:
                get_ids_2_homogene_ids(dico_wf["subworkflows"][sub], ids_2_homogene_ids, current_sub+[str(sub)])
            return ids_2_homogene_ids
        
        ids_2_homogene_ids = get_ids_2_homogene_ids(full_workflow, {}, [])
        depth_sub_max = get_sub_max(full_workflow, -1)
        fill_metro_map(full_workflow, metro_map_dico, [], depth_sub_max, ids_2_homogene_ids)
        with open(f"{self.get_output_dir()}/graphs/metro_map.json", 'w') as output_file :
            json.dump(metro_map_dico, output_file, indent=4)
        return metro_map_dico


    ###########################
    #    Generate test data
    ###########################
    #These are the methods which generate the test data

    def generate_test_specification_graph(self):
        dico = self.graph.get_full_dico()
        with open(self.get_output_dir()/ 'test' /"specification_graph.json", "w") as outfile: 
            json.dump(dico, outfile, indent = 4)

    def generate_all_executors(self):
        executors = self.get_workflow_main().get_all_executors_in_workflow()
        dico= {}
        for e in executors:
            dico[str(e)] = e.get_code(get_OG = True)
        with open(self.get_output_dir()/ 'test' /"all_executors.json", "w") as outfile: 
            json.dump(dico, outfile, indent = 4)

    def generate_executors_per_subworkflows(self):
        subs = self.get_subworkflows_called()
        dico= {}
        for s in subs:
            dico[str(s)]= {}
            executors = s.get_all_executors_in_workflow()
            for e in executors:
                dico[str(s)][str(e)] = e.get_code(get_OG = True)
        with open(self.get_output_dir()/ 'test' /"executors_per_subworkflows.json", "w") as outfile: 
            json.dump(dico, outfile, indent = 4)


    def get_operations_and_processes_per_subworkflows(self):
        subs = self.get_subworkflows_called()
        dico= {}
        for s in subs:
            executors = s.get_all_executors_in_workflow()
            tab = []
            for e in executors:
                if(not e.get_artificial_status()):
                    tab += get_basic_blocks(e, {})
            dico[s] = tab
        return dico

    def generate_all_processes(self):
        processes = self.get_processes_called()
        dico= {}
        for p in processes:
            dico[str(p)] = p.get_code()
        with open(self.get_output_dir()/ 'test' /"all_processes.json", "w") as outfile: 
            json.dump(dico, outfile, indent = 4)

    def generate_all_subworkflows(self):
        subs = self.get_subworkflows_called()
        dico= {}
        for s in subs:
            dico[str(s)] = s.get_code()
        with open(self.get_output_dir()/ 'test' /"all_subworkflows.json", "w") as outfile: 
            json.dump(dico, outfile, indent = 4)
        
    def generate_all_test_data(self):
        self.generate_test_specification_graph()
        self.generate_all_executors()
        self.generate_all_processes()
        self.generate_all_subworkflows()
        self.generate_executors_per_subworkflows()

    
    #The generation of the Ro-Crate has been valid from 
    # - https://ro-crate.ldaca.edu.au/explorer, and
    # - https://github.com/crs4/rocrate-validator (with the workflow-ro-crate-1.0 profile) 
    def get_rocrate(self, display_info=False, personnal_acces_token = None,
                    datePublished=None, description=None,
                  license=None, authors = None,
                   publisher = None, keywords = None,
                   producer = None):
        
        self.rocrate = RO_Crate(self, display_info=display_info, personnal_acces_token = personnal_acces_token,
                 datePublished=datePublished, description=description,
                  license=license, authors = authors,
                   publisher = publisher, keywords = keywords,
                   producer = producer)
        self.rocrate.initialise()

    def get_DBfile(self):
        file = DBfile(self)
        file.initialise()


    #Returns a dico of number of executors per each condition 
    #For example : {condition1: [exe1, exe2, exe3], condition2: [exe3], condition:[exe1]}
    def get_most_influential_conditions(self):

        def uniform_conditions(dico):
            condition_in_commun = {}
            for cond in dico:
                try:
                    temp = condition_in_commun[cond.get_value()]
                except:
                    condition_in_commun[cond.get_value()] = []
                condition_in_commun[cond.get_value()].append(cond)
            new_dico = {}
            for cond in condition_in_commun:
                if(len(condition_in_commun[cond])>1):
                    new_cond = Condition(self, cond)
                    new_tab = []
                    for id in condition_in_commun[cond]:
                        new_tab += dico[id]
                    new_dico[new_cond] = new_tab
                else:
                    new_dico[condition_in_commun[cond][0]] = dico[condition_in_commun[cond][0]]
            return new_dico
                    

        if(self.get_workflow_main()):
            most_influential_conditions = self.get_workflow_main().get_most_influential_conditions()
            return uniform_conditions(most_influential_conditions)
        else:
            if(self.all_conditions_language_server=={}):
                #Case language server
                conditions = self.get_first_file().get_conditions({}, "")
                new_conditions = {}
                for cond in conditions:
                    c = Condition(self, str(cond))
                    new_conditions[c] = []
                    for ele in conditions[cond]:
                        if(ele.get_type()=="Operation" and ele.get_artificial_status()):
                            None
                        else:
                            new_conditions[c].append(ele)
                self.all_conditions_language_server = uniform_conditions(new_conditions)
                return self.all_conditions_language_server
            else:
                return self.all_conditions_language_server
        #if(self.get_duplicate_status()):
        #    most_influential_conditions = self.get_workflow_main().get_most_influential_conditions()
        #    ##If show values then we replace the the conditions ids with their values
        #    #if(show_values):
        #    #    most_influential_conditions_values = {}
        #    #    for condition in most_influential_conditions:
        #    #        try:
        #    #            t = most_influential_conditions_values[condition.get_value()]
        #    #        except:
        #    #            most_influential_conditions_values[condition.get_value()] = 0
        #    #        most_influential_conditions_values[condition.get_value()] += most_influential_conditions[condition]
        #    #    most_influential_conditions = most_influential_conditions_values
        #    #
        #    ##Sort the dico
        #    #most_influential_conditions = {k: v for k, v in sorted(most_influential_conditions.items(), key=lambda item: item[1], reverse=True)}
        #    return most_influential_conditions
        #else:
        #    BioFlowInsightError("Need to activate 'duplicate' mode to use this method.")

    def get_conditions_decomposed(self):
        decomposed_tab = []
        for full_condition in list(self.get_most_influential_conditions().keys()):
            for decomposed in full_condition.get_minimal_sum_of_products():
                decomposed_tab.append(" | ".join(decomposed))
            for decomposed in full_condition.get_minimal_product_of_sums():
                decomposed_tab.append(" & ".join(decomposed))
        return list(set(decomposed_tab))

    #When there are multiple emits turn them into one and the end of the call eg, instead of fastp_ch2 = fastp.out.fastp_ch2 -> have fastp_ch2 = fastp_ch
    def convert_to_DSL2(self):
        if(self.get_DSL()=="DSL2"):
            print("Workflow is already written in DSL2")
        else:
            #This tag is used as an identification to safely manipulate the string 
            tag = str(time.time())
            nextflow_file = self.get_first_file()

            code = nextflow_file.get_code()

            #Move the workflow.complete to end of the workflow if it's not already done
            for match in re.finditer(r"workflow\.onComplete\s*{", code):
                start = match.span(0)[0]
                end = extract_curly(code, match.span(0)[1])#This function is defined in the functions file
                workflow_on_complete = code[start:end]
                code = code.replace(workflow_on_complete, "")
                code+="\n"*2+workflow_on_complete

            start_code = r"#!/usr/bin/env nextflow"
            start_code_pattern = r"\#\!\s*\/usr\/bin\/env\s+nextflow"
            end_code = "workflow.onComplete"
            
            pos_start, pos_end= 0, len(code)
            if(code.find(end_code)!=-1):
                pos_end = code.find(end_code)
            code_to_replace = code[pos_start:pos_end]
            for match in re.finditer(start_code_pattern, code):
                pos_start = match.span(0)[1]+1
            #if(code.find(start_code)!=-1):
            #    pos_start = code.find(start_code)+len(start_code)
            body = code[pos_start:pos_end].strip()#.replace('\n', '\n\t')

            include_section = f"//INCLUDE_SECTION_{tag}"
            params_section = f"//PARAMS_SECTION_{tag}"
            function_section = f"//FUNCTION_SECTION_{tag}"
            process_section = f"//PROCESS_SECTION_{tag}"

            code = code.replace(code_to_replace, f"""{start_code}\n\n\n{include_section}\n\n\n{params_section}\n\n\n{function_section}\n\n\n{process_section}\n\n\nworkflow{{\n\n{body}\n}}\n\n""")

            ##I've out this in a comment cause since it's a DSL1 
            #params_list = []
            #for match in re.finditer(r"params.\w+ *\= *[^\n=]([^\n])*", code):
            #    params_list.append(match.group(0))
            #for params in params_list:
            #    code = code.replace(params, "")
            #params_code = "\n".join(params_list)
            #code = code.replace(params_section, params_code)

            #Moving Functions
            functions = []
            for f in nextflow_file.functions:
                function = f.get_code()
                functions.append(function)
            for r in functions:
                code = code.replace(r, "")
            code = code.replace(function_section, "\n\n".join(functions))

            #Moving Processes
            processes = []
            to_replace = []
            for p in nextflow_file.get_processes():
                new_process, call = p.convert_to_DSL2()
                processes.append(new_process)
                to_replace.append((p.get_code(get_OG = True), call))
            
            for r in to_replace:
                code = code.replace(r[0], r[1])
            code = code.replace(process_section, "\n\n".join(processes))

            #TODO -> update the operations -> also consider the operations in the params of the calls which need to be updated

            for o in self.get_workflow_main().get_all_executors_in_workflow():
                if(o.get_type()=="Operation"):
                    code = code.replace(o.get_code(get_OG=True), o.convert_to_DSL2())
                else:
                    raise Exception(f"Executor of type '{o.get_type()}' was extracted in a DSL1 workflow! This shoudn't happen! The code is '{o.get_code()}'")

            #Putting || back
            code = code.replace("$OR$", "||")
            #put_modified_operations_back
            #TODO -> add the other things necessary to reformat code
           
            #Somethimes this is incorrect but that's due to the fact that the DSL1 analysis isn't as clean as the DSL2 analyse (concerning the conditions)
            #What i mean that when searching for channels, DSL1 doesn't consider the conditions when searching from the processes while DSL2 does
            #The conversion works well but it's just comparing to the old DSL1 workflow doesn't make sense
            #If you want to put this line back you need #TODO update the DSL1 parsing to consider the blocks when defining the processes 
            #A good example is KevinMenden/hybrid-assembly
            self.rewrite_and_initialise(code, render_graphs=False, def_check_the_same = False)
            
            return code
    
    """#This function draws processes from a pool and checks if they are direclty dependend on each other
    def draw_pool_and_check_dependencies(self, pool, alpha=-1):
        edges_create_cycles = self.graph.get_edges_that_create_cycle()
        def get_object(address):
            address = int(re.findall(r"\dx\w+", address)[0], base=16)
            return ctypes.cast(address, ctypes.py_object).value

        edges_create_cycles_names = []
        for e in edges_create_cycles:
            n1, n2 = e
            obj1, obj2 = get_object(n1), get_object(n2)
            edges_create_cycles_names.append((obj1.get_alias(), obj2.get_alias()))


        import random

        #Random value between 0 and 1, centered at 0.5
        def get_value():
            val = random.random()
            return val

        searching = True
        timeout = 0
        random_pool = True
        if(alpha != -1):
            random_pool = False
        while(searching and timeout<constant.WHILE_UPPER_BOUND):
            searching = False
            if(random_pool):
                alpha = get_value()
            nb_2_select = int(alpha*len(set(pool)))

            #Taking one from one the processes until we've reached the number
            sampled = []
            while(len(sampled)<nb_2_select):
                element = random.sample(pool, 1)
                sampled+=element
                #Removing all occurances of element in the list
                #We do this cause their can be mulitple of the same element
                #In the case we are searching with the frequency
                pool = list(filter(lambda a: a != element[0], pool))
            ##This was 'simple' way of doing it (in the case there wasn't any duplicates in the pool)
            ##The new method in the case there are multiples and also in the case there aren't
            #sampled = random.sample(set(pool), nb_2_select)
            
            sampled_str = []
            for s in sampled:
                sampled_str.append(s.get_alias())
            for e in edges_create_cycles_names:
                if(e[0] in sampled_str and e[1] in sampled_str):
                    #So that means there are the 2 nodes which form the cycle edge in the relevant processes
                    #-> it means we need to regenerated relevant processes
                    searching = True
            if(not searching):
                name_select = []
                for p in sampled:
                    name_select.append(p.get_alias())
                return name_select
            timeout+=1
        if(timeout>=constant.WHILE_UPPER_BOUND):
            raise BioFlowInsightError(f"The WHILE_UPPER_BOUND was exceeded. BioFlow-Insight was unable to select random processes.", type="Unable to select random processes")
    """


    """#This methods generates a random set of processes to consider as relavant 
    def generate_random_relevant_processes(self, alpha = -1):
        if(self.duplicate):
            processes_called = []
            if(self.get_DSL()=="DSL2"):
                for c in self.get_workflow_main().get_all_calls_in_workflow():
                    p = c.get_first_element_called()
                    if(p.get_type()=="Process"):
                        processes_called.append(p)
            else:
                processes_called = self.get_first_file().get_processes()
            return self.draw_pool_and_check_dependencies(processes_called)
        else:
            raise BioFlowInsightError("Trying to generate random relevant processes however option 'duplicate' is not activated.")
    """
         
    """def get_random_relevant_processes_which_use_bioinformatics_tools(self, scripts_2_tools = {}):
        if(self.duplicate):
            processes_called = []
            if(self.get_DSL()=="DSL2"):
                for c in self.get_workflow_main().get_all_calls_in_workflow():
                    p = c.get_first_element_called()
                    if(p.get_type()=="Process"):
                        processes_called.append(p)
            else:
                processes_called = self.get_first_file().get_processes()
            processes_with_bioinfo_tools = []
            for p in processes_called:
                if(scripts_2_tools!={}):
                    tools = scripts_2_tools[p.get_script_code()]
                else:
                    tools = p.get_tools()
                if(len(tools)>0):
                    processes_with_bioinfo_tools.append(p)
            return self.draw_pool_and_check_dependencies(processes_with_bioinfo_tools)
        else:
            raise BioFlowInsightError("Trying to generate random relevant processes however option 'duplicate' is not activated.")
    """

    """def get_random_relevant_processes_which_use_bioinformatics_tools_considering_their_frequency(self, scripts_2_tools = {}):
        
        OG_path = os.getcwd()
        #Change working directory to the one of the file
        os.chdir("/".join((str(__file__).split("/")[:-1])))
        with open("../ressources/tool_2_nb_usage.json", 'r') as file:
            tool_2_nb_usage = json.load(file)
        os.chdir(OG_path)

        if(self.duplicate):
            processes_called = []
            if(self.get_DSL()=="DSL2"):
                for c in self.get_workflow_main().get_all_calls_in_workflow():
                    p = c.get_first_element_called()
                    if(p.get_type()=="Process"):
                        processes_called.append(p)
            else:
                processes_called = self.get_first_file().get_processes()
            process_to_min_frequency = {}
            for p in processes_called:
                if(scripts_2_tools!={}):
                    tools = scripts_2_tools[p.get_script_code()]
                else:
                    tools = p.get_tools()
                
                if(len(tools)>0):
                    min_value = np.inf
                    for t in tools:
                        try:
                            val = tool_2_nb_usage[t]
                            if(t in ['python', 'r', 'perl', 'julia']):#Cause in this case it is a custom script -> one should hope that it is important in this case
                                val = 1
                        except:
                            val = 1
                        if(val<min_value):
                            min_value = val
                    process_to_min_frequency[p] = min_value
            sample_of_processes = []
            total_nb = np.sum(list(process_to_min_frequency.values()))
            max_nb = np.max(list(process_to_min_frequency.values()))
            for p in process_to_min_frequency:
                freq = process_to_min_frequency[p]
                nb_to_add = (max_nb-freq)+1
                #nb_to_add = int(total_nb*(1-(freq/total_nb)**4))
                sample_of_processes+=nb_to_add*[p]
            return self.draw_pool_and_check_dependencies(sample_of_processes)
        else:
            raise BioFlowInsightError("Trying to generate random relevant processes however option 'duplicate' is not activated.")

    """


    #TODO -> add excpetion Channel exists in multiple forms -> check with 132
    #Cycle exists in workflow too -> 667
    def get_relevant_following_best_general_score(self, 
                                                  reduction_alpha = 0.2, 
                                                  reduction_beta = 0.8, 
                                                  number_of_tries = 50,
                                                  process_pre_selection = "bioinfo_freq",
                                                  concordance_factor = 1,
                                                  uniformity_factor = 1,
                                                  min_nb_clusters_factor = 1,
                                                  min_nb_non_relevant_cluster_factor = 1,
                                                  relevant_processes = []):#This parameter is to force relevant proceses is the user absolutely wants the 
        
        import copy
        min_score, min_processes = np.inf, []
        already_tried = []
        #working_workflow = copy.deepcopy(self)
        
        processes_called = self.get_processes_called()
        number_processes_called = len(processes_called)
        all_process_as_relevant = []
        for p in processes_called:
            all_process_as_relevant.append(p.get_alias())
        all_process_as_relevant = list(set(all_process_as_relevant))
        #working_workflow.rewrite_workflow_remove_subworkflows(relevant_processes = all_process_as_relevant, render_graphs = False)
    
        w = copy.deepcopy(self)
        #w = copy.deepcopy(working_workflow)
        scripts_2_tools = {}
        print("Extracting the tools from the processes")
        print('-'*len(processes_called)+">")
        for p in processes_called:
            print('.', end='')
            try:
                scripts_2_tools[p.get_script_code()] = self.scripts_2_tools[p.get_script_code()]
            except:
                scripts_2_tools[p.get_script_code()] = p.get_tools()
        print("\n")
        print("Testing different combinations")
        print('-'*number_of_tries+">")
        for i in range(number_of_tries):
            print('.', end='')
            #print(i/number_of_tries*100)
            #w = copy.deepcopy(w_save)
            
            def get_randomn_processes():
                if(process_pre_selection == "bioinfo"):
                    random_relevant_processes = w.get_random_relevant_processes_which_use_bioinformatics_tools(scripts_2_tools = scripts_2_tools)
                elif(process_pre_selection == "bioinfo_freq"):
                    random_relevant_processes = w.get_random_relevant_processes_which_use_bioinformatics_tools_considering_their_frequency(scripts_2_tools = scripts_2_tools)
                elif(process_pre_selection == "None"):
                    random_relevant_processes = w.generate_random_relevant_processes()
                else:
                    raise Exception('process_pre_selection option not recognised')
                return list(set(random_relevant_processes+relevant_processes))
            
            max_number_clusters = 30

            random_relevant_processes = get_randomn_processes()
            escape, escape_upper_bound = 0, 1000
            while(escape<escape_upper_bound and (set(random_relevant_processes) in already_tried
                  or not(len(random_relevant_processes)<=np.min((reduction_beta*number_processes_called, max_number_clusters)))
                  or not(len(random_relevant_processes)>=reduction_alpha*number_processes_called))):
                #print("here", random_relevant_processes)
                escape+=1
                random_relevant_processes = get_randomn_processes()
            #Cause it means we've already searched the majority of the possibilities
            if(escape>=escape_upper_bound):
                return min_processes
            already_tried.append(set(random_relevant_processes))
            #Here the nb of conditions returned is the number of conditions in the clusters after the rewrite
            def get_nb_conditions_in_clusters(clusters):
                nb_conditions_in_clusters = []
                for cluster in clusters:
                    all_conditions_cluster = []
                    for c in cluster:
                        flat_condition_for_element, flat_condition_for_element_tab = "", [] 
                        conditions_for_element = c.get_all_conditions()
                        if(len(conditions_for_element)==0):
                            all_conditions_cluster.append("no value")
                        else:
                            for condition in conditions_for_element:
                                flat_condition_for_element_tab.append(condition.get_value())
                            flat_condition_for_element = " && ".join(flat_condition_for_element_tab)
                            all_conditions_cluster.append(flat_condition_for_element)

                    all_conditions_cluster = list(set(all_conditions_cluster))
                    
                    if(len(all_conditions_cluster)==1):
                        nb_conditions_in_clusters.append(0)
                    else:
                        try:
                            all_conditions_cluster.remove("no value")
                        except:
                            None
                        nb_conditions_in_clusters.append(len(all_conditions_cluster))
                return nb_conditions_in_clusters


            def get_score_from_set_relevant_processes(w, random_relevant_processes):
                #w = copy.deepcopy(w_save)
                #_, cluster_organisation = w.convert_workflow_2_user_view(relevant_processes=random_relevant_processes, render_graphs = False)
                #print(random_relevant_processes)

                #tab_nb_executors_per_cluster_1, tab_nb_processes_per_cluster_1, tab_nb_conditions_per_cluster_1 = [], [], []
                #for c in cluster_organisation:
                #    tab_nb_executors_per_cluster_1.append(cluster_organisation[c]["nb_executors"])
                #    tab_nb_processes_per_cluster_1.append(cluster_organisation[c]["nb_processes"])
                #    tab_nb_conditions_per_cluster_1.append(cluster_organisation[c]["nb_conditions"])
                
                #w = copy.deepcopy(w_save)
                w.generate_user_view(relevant_processes = random_relevant_processes, render_graphs=False, use_process_dependency_graph = False)
                clusters = w.graph.get_clusters_from_user_view()
                cluster_with_processes = []
                for cluster in clusters:
                    there_is_a_process = False
                    for ele in cluster:
                        if(ele.get_type() == "Process"):
                            there_is_a_process = True
                    cluster_with_processes.append(cluster)

                #Number executors per cluster
                tab_nb_executors_per_cluster = []
                for cluster in cluster_with_processes:
                    tab_nb_executors_per_cluster.append(len(cluster))
                
                
                #Number condtions per cluster
                tab_nb_conditions_per_cluster = get_nb_conditions_in_clusters(cluster_with_processes)
                #Number of processes per cluster
                tab_nb_processes_per_cluster = []
                for cluster in cluster_with_processes:
                    nb_processes = 0
                    for ele in cluster:
                        if(ele.get_type()=="Process"):
                           nb_processes+=1
                    tab_nb_processes_per_cluster.append(nb_processes) 


                nb_clusters = len(cluster_with_processes)
                nb_non_relevant_clusters = 0
                for cluster in cluster_with_processes:
                    cluster_with_relevant_process = False
                    for c in cluster:
                        if(c.get_type()=="Process"):
                            if(c.get_alias() in random_relevant_processes):
                                #This means it's relvant cluster
                                cluster_with_relevant_process = True
                    if(not cluster_with_relevant_process):
                        nb_non_relevant_clusters+=1

                uniformity_variance = 0
                average_number_of_process_per_cluster = np.mean(tab_nb_processes_per_cluster)
                for x in tab_nb_processes_per_cluster:
                    uniformity_variance += (average_number_of_process_per_cluster-x)**2/nb_clusters
                
                min_nb_clusters_value = (nb_clusters / number_processes_called)**2
                dico_results = {"min_nb_clusters":min_nb_clusters_value, "min_nb_non_relevant_cluster":(nb_non_relevant_clusters / nb_clusters), "uniformity":(uniformity_variance / number_processes_called), "concordance":np.max(np.array(tab_nb_conditions_per_cluster)/np.array(tab_nb_executors_per_cluster))  }
                score = concordance_factor * np.max(np.array(tab_nb_conditions_per_cluster)/np.array(tab_nb_executors_per_cluster)) + \
                        uniformity_factor * (uniformity_variance / number_processes_called) + \
                        min_nb_clusters_factor * min_nb_clusters_value + \
                        min_nb_non_relevant_cluster_factor * (nb_non_relevant_clusters / nb_clusters)
                return score, cluster_with_processes, dico_results

            
            score, cluster_organisation, dico_results = get_score_from_set_relevant_processes(w, random_relevant_processes)
            #print(dico_results)
            if(len(cluster_organisation)>=reduction_alpha*number_processes_called and 
               len(cluster_organisation)<=np.min((reduction_beta*number_processes_called, max_number_clusters)) and 
               score<min_score):
                #print()
                #print("concordance",  np.max(np.array(tab_nb_conditions_per_cluster)/np.array(tab_nb_executors_per_cluster)) )
                #print("uniformity",   (uniformity_variance / number_processes_called) )
                #print("min_nb_clusters",  (nb_clusters / number_processes_called) )
                #print("min_nb_non_relevant_cluster",  (nb_non_relevant_clusters / nb_clusters))
                #print("score", score)
                print()
                print(random_relevant_processes)
                print("-->", dico_results)
                print(score)
                min_processes = random_relevant_processes
                min_score = score
        
        #remove the GG since we're working on the rewritten workflow
        processes_returned = []
        for p in min_processes:
            processes_returned.append(p.split('_GG_')[0])

        return processes_returned

    #Method that returns the order of execution for each executor
    def get_order_execution_executors(self):
        dico = {}
        seen = {}
        dico = self.get_workflow_main().get_order_execution_executors(dico, seen)
        tab = []
        def explore_dico(dico):
            if(type(dico)!=dict):
                None
            else:
                for val in dico:
                    tab.append(val)
                    explore_dico(dico[val])
        explore_dico(dico)

        return tab



    def add_to_ternary_operation_dico(self, old, new):
        self.ternary_operation_dico[new] = old

    def add_map_element(self, old, new):
        self.map_element_dico[new] = old

    def put_back_old_ternary_operations(self, code, ternary_operation_dico):
        for new in ternary_operation_dico:
            old = ternary_operation_dico[new]
            code = code.replace(new.strip(), old)
        return code
    
    def put_modified_operations_back(self, code, dico_operations):
        searching = True
        while(searching):
            searching = False
            for match in re.finditer(r"\.(\w+)_modified\s*\{\s*(¤[^¤]+¤)\s*\}", code):
                operator = match.group(1)
                inside = match.group(2)#Cause we want to remove the extras ...'''
                code = code.replace(match.group(0), f".{operator} {{ {dico_operations[inside]} }}")
                searching = True
                break
        return code

    """
    #TODO -> write tests for this method
    #Function that rewrites the workflow code
    #Rewriting everything in one file + simplifying the operations and calls to simplify the analysis
    def simplify_workflow_code(self):
        code = self.get_first_file().get_code()
        #This tag is used as an identification to safely manipulate the string 
        tag = str(time.time())
        
        
        #params_section = f"//PARAMS_SECTION_{tag}"
        function_section = f"//FUNCTION_SECTION"
        process_section = f"//PROCESS_SECTION"
        subworkflow_section = f"//SUBWORKFLOW_SECTION"

        ankers = function_section+ "\n"*3 + process_section+ "\n"*3 + subworkflow_section+ "\n"*3

        

        #Place ankers
        pos_start = 0
        start_code_pattern = r"\#\!\s*\/usr\/bin\/env\s+nextflow"
        for match in re.finditer(start_code_pattern, code):
            pos_start = match.span(0)[1]+1
        code = code[:pos_start]+ankers+code[pos_start:]
        
        #Remove the includes
        for match in re.finditer(constant.FULL_INLCUDE_2, code):
            full_include = match.group(0)
            for temp in re.finditer(fr"{re.escape(full_include)} *addParams\(", code):
                raise BioFlowInsightError("There is an 'addParams' in an include. BioFlow-Insight doesn not how to rewrite this.", type="Rewrite Error")
            code = re.sub(fr"{re.escape(full_include)}.*", "", code)

        processes, subworkflows, functions = [], [], []
        for c in self.get_workflow_main().get_all_calls_in_workflow():
            ele = c.get_first_element_called()
            if(ele.get_type()=="Process"):
                processes.append(ele)
            elif(ele.get_type()=="Subworkflow"):
                subworkflows.append(ele)
            elif(ele.get_type()=="Function"):
                functions.append(ele)
            else:
                raise Exception("This shoudn't happen")
        
        #Get calls to functions made outside of themain which might have been imported -> so we need to add them
        for c in self.get_first_file().get_calls_made_outside_of_main():
            ele = c.get_first_element_called()
            if(ele.get_type()=="Function"):
                functions.append(ele)
            else:
                raise Exception("This shoudn't happen -> either a call to a process or subworkflow outside of main or subworkflow")

        #Simplifying main
        tmp = code
        old = self.get_workflow_main().get_code(get_OG = True)
        new = self.get_workflow_main().simplify_code()
        code = code.replace(old, new)
        if(tmp==code and old!=new):
            raise Exception("This shouldn't happen -> code not replaced")

        #Adding processes into code
        for p in processes:
            if(p.get_code_with_alias_and_id() not in code):
                code = code.replace(process_section, '\n'+p.simplify_code()+'\n'+process_section)

        #Adding subworkflows into code
        for sub in subworkflows:
            if(sub.get_code_with_alias_and_id() not in code):
                code = code.replace(subworkflow_section, subworkflow_section+'\n'+sub.simplify_code()+'\n')

        #Adding functions into code
        for fun in functions:
            if(fun.get_code() not in code):
                code = code.replace(function_section, function_section+'\n'+fun.get_code()+'\n')
        
        #Remove the ankers
        #code = code.replace(function_section, "")
        #code = code.replace(process_section, "")
        #code = code.replace(subworkflow_section, "")
        ankers = {"function_section":function_section,
                  "process_section":process_section,
                  "subworkflow_section":subworkflow_section}
        
        return code"""

    def get_subworkflows_called(self):
        subs = []
        for c in self.get_workflow_main().get_all_calls_in_workflow():
            ele = c.get_first_element_called()
            if(ele.get_type()=="Subworkflow"):
                subs.append(ele)
        return subs
    
    def get_processes_called(self):
        processes_called = []
        if(self.get_DSL()=="DSL2"):
            for c in self.get_workflow_main().get_all_calls_in_workflow():
                p = c.get_first_element_called()
                if(p.get_type()=="Process"):
                    processes_called.append(p)
        else:
            processes_called = self.get_first_file().get_processes()
        return processes_called


    """
    def rewrite_and_initialise(self, code, render_graphs, def_check_the_same = True):
        temp_process_dependency_graph = self.graph.get_process_dependency_graph() 
        temp_spec_graph = self.graph.full_dico

        #Remove the "_GG_\d+"
        #code = re.sub(r"_GG_\d+", "", code)

        #Write new code in temporary file
        temp_file = self.get_output_dir()/f"temp_{str(self)[-7:-2]}.nf"
        with open(temp_file, "w") as file:
            file.write(code)
        
        f = open(self.get_output_dir()/ "debug" / "rewritten.nf", "w")
        f.write(code)
        f.close()

        #Replace old analysis with new analysis (simplified code)
        temp = self.get_cycle_status()
        self.__init__(str(temp_file), display_info = False, duplicate=True)
        self.cycle_in_workflow = temp
        self.initialise()
        os.remove(temp_file)
        self.graph.initialise()
        if(def_check_the_same and not self.graph.check_if_process_dependendy_is_equivalent_to_other_without_subworkflows(temp_process_dependency_graph)):
            if(render_graphs==True):
                #generate_graph(self.get_output_dir()/ "debug" /"spec_graph_OG", temp_spec_graph, render_graphs = True)
                generate_graph(self.get_output_dir()/ "debug" /"spec_graph", self.graph.full_dico, render_graphs = True)
                #generate_graph(self.get_output_dir()/ "debug" /"process_dependency_graph_OG", temp_process_dependency_graph, render_graphs = True)
                generate_graph(self.get_output_dir()/ "debug" /"process_dependency_graph", self.graph.get_process_dependency_graph() , render_graphs = True)
            if(self.channel_that_is_defined_used_and_redefined_used_in_another_block!=""):
                raise BioFlowInsightError(f"Given that the channel '{self.channel_that_is_defined_used_and_redefined_used_in_another_block}' is defined and used in multiple conditional blocks. The rewrite could not be done with the proprosed relavant processes. Either correct the defintion of the workflow or give another set of relevant processes.", type="Channel exists in multiple forms")
            else:
                raise Exception("Something went wrong: The flat dependency graph is not the same!")
    """
    """
    def check_relevant_processes_in_workflow(self, relevant_processes):
        #Check all relevat processes are in wf
        workflow_processes = {}
        for c in self.get_workflow_main().get_all_calls_in_workflow():
            ele = c.get_first_element_called()
            if(ele.get_type()=="Process"):
                short_name = ele.get_alias().split("_GG_")[0]
                try:
                    temp = workflow_processes[short_name]
                except:
                    workflow_processes[short_name] = []
                workflow_processes[short_name].append(ele.get_alias())
        
        temporary_relevant = []
        for p in relevant_processes:
            if(p not in workflow_processes):
                raise BioFlowInsightError(f"The element '{p}' given as a relevant processes is not present in the workflow's processes", 24)
            temporary_relevant+=workflow_processes[p]
        relevant_processes = temporary_relevant
        return relevant_processes"""


    def generate_user_view(self, relevant_processes = [], render_graphs = True, use_process_dependency_graph = False):
        alias_2_tools = self.alias_2_tools
        self.graph.initialise()
        self.graph.generate_user_view(relevant_processes = relevant_processes, render_graphs = render_graphs, use_process_dependency_graph = use_process_dependency_graph, alias_2_tools = alias_2_tools)


    

    #This Function returns the channels on which the subworkflow (things_added_in_cluster) depend on
    def get_takes(self, things_added_in_cluster):
        #Basiccaly this is a deco of channels to opeartions -> when the value is an empty list 
        #This means that the channel is totally definied in the subworkflow -> so we are searching for 
        #Channels which aren't totatly defined in the subworkflow 
        channels_2_sources = {}

        for ele in things_added_in_cluster:
            if(ele.get_type() == "Operation"):
                for o in ele.get_origins():
                    if(o.get_type() in ["Channel", "Emitted"]):
                        channels_2_sources[o] = replace_thing_by_call(o.get_source())
                    else:
                        if(o.get_first_element_called().get_type()=="Function"):
                            None
                        else:
                            raise Exception("This shouldn't happen")
            elif(ele.get_type() == "Call"):
                for param in ele.get_parameters():
                    if(param.get_type()=="Channel"):
                        raise Exception("This shouldn't happen -> with the rewrite all the params should be channels")
                    else: 
                        for o in param.get_origins():
                            if(o.get_type()=="Channel"):
                                channels_2_sources[o] = replace_thing_by_call(o.get_source())
                            else:
                                raise Exception("This shouldn't happen -> with the rewrite all the params should be channels")
            else:
                raise Exception("This shouldn't happen")
            
        takes = []
        names_added = []
        for channel in channels_2_sources:
            if(set(channels_2_sources[channel]).intersection(things_added_in_cluster)!=set(channels_2_sources[channel])):
                if(channel.get_name() not in names_added):
                    takes.append(channel)
                    names_added.append(channel.get_name())
        return takes
    
    #This Function returns the channels the subworkflow (things_added_in_cluster) emits (other things depend on)
    def get_emits(self, things_added_in_cluster):
        channel_2_sink = {}
        #Basiccaly this is a deco of channels to opea -> this doesn't really work yetrtions -> when the value is an empty list 
        #This means that the channel is totally definied in the subworkflow -> so we are searching for 
        #Channels which aren't totatly defined in the subworkflow
        #This means that things outside the subworkflow depend on this channel 
        channel_2_sink = {}

        for ele in things_added_in_cluster:
            if(ele.get_type() == "Operation"):
                for o in ele.get_gives():
                    channel_2_sink[o] = replace_thing_by_call(o.get_sink())
            elif(ele.get_type() == "Call"):
                #thing = ele.get_first_element_called()
                for e in ele.get_later_emits():
                    channel_2_sink[e] = replace_thing_by_call(e.get_sink())
            else:
                raise Exception("This shouldn't happen")

        emits = []  
        names_added = []
        for channel in channel_2_sink:
            if(set(channel_2_sink[channel]).intersection(things_added_in_cluster)!=set(channel_2_sink[channel])):
                if(channel.get_name() not in names_added):
                    emits.append(channel)
                    names_added.append(channel.get_name())
        return emits



   