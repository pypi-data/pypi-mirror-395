
import json
import networkx as nx
import numpy as np
import copy
import re
import ctypes

from .outils_graph import *
from .bioflowinsighterror import BioFlowInsightError
from . import constant


def get_object(address):
    address = int(re.findall(r"\dx\w+", address)[0], base=16)
    return ctypes.cast(address, ctypes.py_object).value


class Graph():
    def __init__(self, workflow):
        self.workflow = workflow
        self.full_dico = {}
        self.full_dico_wo_artificial_operations = {}
        #self.full_dico = workflow.get_structure()
        #with open(f"{self.get_output_dir()}/graphs/specification_graph.json", 'w') as output_file :
        #    json.dump(self.full_dico, output_file, indent=4)
        #This dico give for the nodes its sister nodes
        self.link_dico = None
        self.link_dico_wo_artificial = None
        self.link_dico_processes = None
        #Dico to graph without operations
        self.dico_process_dependency_graph = {}
        self.user_view = {}
        self.user_view_with_subworkflows = {}
        self.new_nodes_user_view = []
        self.dico_wo_branch_operation = {}

        #Dictionaries for metadata
        #Dico flattened (without any subworkflows)
        self.dico_flattened = {}
        self.initialised = False



    def get_process_dependency_graph(self):
        return self.dico_process_dependency_graph
    
    def stats_full_graph_wo_artificial_nodes(self):
        dico = {}
        nodes, edges, subworkflows = get_number_nodes_edges(self.full_dico_wo_artificial_operations, 0, 0, 0)
        dico["nodes"] = nodes   
        dico["edges"] = edges
        dico["subworkflows"] = subworkflows
        clouds = self.get_clouds_wo_artificial(bool_get_object = False)
        dico["clouds"] = len(clouds)
        tab = []
        if(len(clouds)!=0):
            for c in clouds:
                tab.append(len(c))
            dico["average_size_cloud"] = float(np.mean(np.array(tab)))
            dico["max_size_cloud"] = int(np.max(np.array(tab)))
        else:
           dico["average_size_cloud"] = 0
           dico["max_size_cloud"] = 0
        return dico

    def initialise(self):
        if(not self.is_initialised()):
            
            self.initialised = True
            self.full_dico = self.workflow.get_structure()
            self.full_dico_wo_artificial_operations = remove_artificial_nodes(self.full_dico)
            with open(f"{self.get_output_dir()}/graphs/specification_graph.json", 'w') as output_file :
                json.dump(self.full_dico, output_file, indent=4)
            #with open(f"{self.get_output_dir()}/graphs/specification_graph_wo_artificial_operations.json", 'w') as output_file :
            #    json.dump(self.full_dico_wo_artificial_operations, output_file, indent=4)
            def get_node_id(dico, process):
                for node in dico["nodes"]:
                    if(node['name']==process):
                        return node['id']
                for sub in dico['subworkflows']:
                    res = get_node_id(dico['subworkflows'][sub], process)
                    if(res!=-1):
                        return res
                return -1

            #This function removes the process -> by the simpliest way -> it doesn't create new links
            def remove_node(dico, node_id):
                #Remove nodes
                nodes_to_remove = []
                for node in dico["nodes"]:
                    if(node['id']==node_id):
                        nodes_to_remove.append(node)
                for node in nodes_to_remove:
                    dico["nodes"].remove(node)

                #Remove edges
                edges_to_remove = []
                for edge in dico["edges"]:
                    if(edge['A']==node_id):
                        edges_to_remove.append(edge)
                    if(edge['B']==node_id):
                        edges_to_remove.append(edge)
                for edge in edges_to_remove:
                    dico["edges"].remove(edge)

                for sub in dico['subworkflows']:
                    remove_node(dico['subworkflows'][sub], node_id)

            

            #self.get_dependency_graph()
            self.intialise_process_dependency_graph()


        
            #self.networkX_wo_operations = self.get_networkx_graph(self.dico_process_dependency_graph, self.networkX_wo_operations)
            self.dico_flattened["nodes"] = []
            self.dico_flattened["edges"] = []
            #This will stay empty -> it's just so we can use the same function
            self.dico_flattened["subworkflows"] = []
            
    
    def get_full_dico(self):
        return self.full_dico

    def is_initialised(self):
        return self.initialised

    def get_output_dir(self):
        return self.workflow.get_output_dir()  

    #Creates the networkX graph
    def get_networkx_graph(self, graph, networkX, first_call=True):
        if(first_call):
            networkX = nx.MultiDiGraph()
        for node in graph['nodes']:
            #Case node is process
            if(is_process(node['id'])):
                networkX.add_node(node['id'], type='Process', code=node['name'])
            #Case node is operation
            elif(is_operation(node['id'])):
                networkX.add_node(node['id'], type='Operation', code=node['xlabel'])
            elif(node['id']=="source"):
                networkX.add_node("source", type='source', code="source")
            elif(node['id']=="sink"):
                networkX.add_node("sink", type='sink', code="sink")
            else:
                raise Exception("This shoudn't happen!")
        
        for edge in graph['edges']:
            if(is_process(edge['A']) and is_process(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='process_2_process')
            elif(is_process(edge['A']) and is_operation(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='process_2_operation')
            elif(is_operation(edge['A']) and is_process(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='operation_2_process')
            elif(is_operation(edge['A']) and is_operation(edge['B'])):
                networkX.add_edge(edge['A'], edge['B'], label = edge['label'], edge_type='operation_2_operation')
            else:
                networkX.add_edge(edge['A'], edge['B'], label = "", edge_type='')      
        for subworkflow in graph['subworkflows']:
            networkX = self.get_networkx_graph(graph['subworkflows'][subworkflow], networkX, first_call=False)
        return networkX



    def get_clouds_wo_artificial(self, bool_get_object):
        self.intia_link_dico()
        link_dico = self.link_dico_wo_artificial
        potential_clouds = {}
        for node in link_dico:
            tab = list(set([node]+link_dico[node]))
            tab.sort()
            c = '_'.join(tab)
            try:
                temp = potential_clouds[c]
            except:
                potential_clouds[c] = []
            potential_clouds[c].append(node)

        clouds = []
        for p in potential_clouds:
            PC = potential_clouds[p]
            if(len(PC)>1):
                clouds.append(PC)

        if(bool_get_object == True):
            temp = []
            for cloud in clouds:
                t = []
                for n in cloud:
                    obj = get_object(n)
                    t.append(obj)
                temp.append(t)
            return temp
        else:
            return clouds



    #Method that initalisise the link dico
    def intia_link_dico(self):
        if(self.link_dico==None or self.link_dico_wo_artificial==None):
            self.link_dico = initia_link_dico_rec(self.full_dico)
            self.link_dico_wo_artificial = initia_link_dico_rec(self.full_dico_wo_artificial_operations)
                

    def get_link_dico(self, bool_get_object, without_artificial_nodes):
        if(not self.is_initialised()):
            self.initialise()
        self.intia_link_dico()
        if(without_artificial_nodes):
            link_dico = self.link_dico_wo_artificial.copy()
        else:
            link_dico = self.link_dico.copy()
        if(bool_get_object == True):
            temp = {}
            for n in link_dico:
                obj = get_object(n)
                temp[obj] = []
                for child in link_dico[n]:
                    temp[obj].append(get_object(child))
            return temp
        else:
            return link_dico


    #Method that initalisise the link process link dico
    def intia_link_dico_processes(self):
        if(self.link_dico_processes==None):
            self.link_dico_processes = initia_link_dico_rec(self.dico_process_dependency_graph)

    def get_specification_graph(self, dirc = 'graphs', filename = "specification_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/ dirc /filename, self.full_dico, render_graphs = render_graphs)
        #generate_graph(self.get_output_dir()/ dirc /(filename+"_without_artificial_nodes"), self.full_dico_wo_artificial_operations, render_graphs = render_graphs)

    def get_specification_graph_wo_labels(self, filename = "specification_graph_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.full_dico, label_edge=False, label_node=False, render_graphs = render_graphs)
    
    def get_specification_graph_wo_orphan_operations(self, filename = "specification_wo_orphan_operations", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.full_dico), render_graphs = render_graphs)
    
    def get_specification_graph_wo_orphan_operations_wo_labels(self, filename = "specification_wo_orphan_operations_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.full_dico), label_edge=False, label_node=False, render_graphs = render_graphs)


    def intialise_process_dependency_graph(self): 
              
        self.intia_link_dico()

        #Function that replicates the workflow's structure wo the operations in the nodes
        def replicate_dico_process_dependency_graphs(dico_struct):
            dico = {}
            dico['nodes'] = []
            dico['edges'] = []
            dico['subworkflows'] = {}
            for node in dico_struct["nodes"]:
                if(is_process(node['id'])):
                    dico['nodes'].append(node)
            for sub in dico_struct['subworkflows']:
                dico['subworkflows'][sub] = replicate_dico_process_dependency_graphs(dico_struct['subworkflows'][sub])
            return dico

        
        dico = replicate_dico_process_dependency_graphs(self.full_dico)


        
        #This is the greedy version 
        #This is a dictionnary which links every node to it's connected process
        node_2_processes = copy.deepcopy(self.link_dico_wo_artificial)
        already_searched = {}
        for nodeA in node_2_processes:
            already_searched[nodeA] = [nodeA]
        changed = True
        while(changed):
            changed = False
            for nodeA in node_2_processes:
                temp = node_2_processes[nodeA].copy()
                for give in node_2_processes[nodeA]:
                    if(is_operation(give)):
                        temp.remove(give)
                        if(nodeA!=give and give not in already_searched[nodeA]):
                            already_searched[nodeA] += give
                            #temp_temp = node_2_processes.get(give, [])
                            try:
                                temp_temp = node_2_processes[give]
                            except:
                                temp_temp = []

                            for node_temp in already_searched[nodeA]:
                                try:
                                    temp_temp.remove(node_temp)
                                except:
                                    None
                            temp+=temp_temp
                            changed = True
                node_2_processes[nodeA] = list(set(temp))
        #print(node_2_processes)

        #This is the optimised version but it is based on the topological order -> thus far i can't get it to work when there is a loop in the workflow
        #topological_order = topological_sort(self.link_dico)
        ##topological_order.reverse()
        #node_2_processes = copy.deepcopy(self.link_dico)
        #for i in [len(topological_order)-1-x for x in range(len(topological_order))]:
        #    updating = topological_order[i]
        #    for y in [len(topological_order)-1-x for x in range(len(topological_order))]:
        #        if(y>i):
        #            fixed = topological_order[y]
        #            if(is_operation(fixed)):
        #                if(fixed in node_2_processes[updating]):
        #                    node_2_processes[updating]+=node_2_processes[fixed].copy()
        #    node_2_processes[updating] = list(set(node_2_processes[updating]))
        #    tab = []
        #    for give in node_2_processes[updating]:
        #        if(is_process(give)):
        #            tab.append(give)
        #        #if(is_operation(give)):
        #        #    node_2_processes[updating].remove(give)
        #        #else:
        #        #    print("**", give)
        #    node_2_processes[updating] = tab




        
        #Getting the dico of paths in the workflow
        path_from_process_to_other_processes = {}
        searching = True
        timeout = 0
        flat_dico = get_flatten_dico(dico.copy())
        process_ids = []
        for node in flat_dico["nodes"]:
            process_ids.append(node['id'])
        while(searching and timeout<constant.WHILE_UPPER_BOUND):
            searching = False
            for nodeA in process_ids:
                try:
                    tmp = path_from_process_to_other_processes[nodeA]
                except:
                    path_from_process_to_other_processes[nodeA] = node_2_processes[nodeA].copy()
                    searching = True
            
                for connectedA in path_from_process_to_other_processes[nodeA]:
                    for nodeB in path_from_process_to_other_processes:
                        if(connectedA==nodeB):
                            for connectedB in path_from_process_to_other_processes[nodeB]:
                                if(connectedB not in path_from_process_to_other_processes[nodeA]):
                                    path_from_process_to_other_processes[nodeA].append(connectedB)
                                    searching = True
            timeout+=1
        if(timeout>=constant.WHILE_UPPER_BOUND):
            raise BioFlowInsightError('ube', None, "BioFlow-Insight was unable to create the dico of paths.")

        #%2x%2x%2x
        #colours = ["#ffbe00", "#0055c8", "#6e6e00", "#a0006e", "#ff5a00", "#82dc73", "#ff82b4", "#d282be", "#d2d200", "#dc9600", "#6e491e", "#00643c", "#82c8e6", "#640082"]
        #colours = ["#4E79A7", "#E15759", "#59A14F", "#EDC948", "#FF9DA7", "#F28E2B", "#76B7B2", "#B07AA1"]
        colours = ["#4E79A7", "#E15759", "#EDC948", "#FF9DA7", "#F28E2B", "#76B7B2", "#B07AA1"]

        #colours = ["#277da1", "#f94144", "#90be6d", "#f9c74f", "#f9844a", "#4d908e","#f3722c", "#577590", ]
        links_added, links_added__with_conditions, links_added_with_index_OG= [], [], []
        def add_edges(dico, condition, checking_conditions, index = 0, added_in_condition = {}, color_index = -1):
            added_colour = False
            for node in dico['nodes']:
                edges = node_2_processes[node['id']]
                for B in edges:
                    link = f"{node['id']} -> {B}"
                    link_with_condition = f"{node['id']} -> {B} ({condition})"
                    link_with_index = f"{node['id']} -> {B} ({index})"
                    if(link_with_condition not in links_added__with_conditions):
                        if(checking_conditions):
                            p1, p2 = get_object(node['id']), get_object(B)
                            if(not self.workflow.get_workflow_main()):
                                conditions_dico = self.workflow.get_most_influential_conditions()
                                conditions_p1 = []
                                for cond in conditions_dico:
                                    if(p1 in conditions_dico[cond]):
                                        conditions_p1.append(cond)
                            else:
                                #Case DSL2
                                if(self.workflow.get_DSL()=="DSL2"):
                                    calls_p1 = p1.get_calls()
                                    conditions = []
                                    for call in calls_p1:
                                        
                                        conditions.append(set(call.get_all_conditions(conditions = {})))
                                    conditions_p1 = set.intersection(*conditions)
                                    #conditions_p1, conditions_p2 = p1.get_call().get_block().get_all_conditions(conditions = {}), p2.get_call().get_block().get_all_conditions(conditions = {})
                                #Case DSL1
                                else:
                                    #TODO -> check that this works correctly
                                    conditions_p1 = p1.origin.get_all_conditions(conditions = {})
                            for c1 in conditions_p1:
                                #TODO -> need to check the condition in a smarter way
                                if(c1.get_value()==condition.get_value()):
                                    #for c2 in conditions_p2:
                                    #    if(c2.get_value()==condition):
                                    if(link not in links_added):
                                        dico['edges'].append({'A': node['id'], 'B': B, 'label': '', "color": colours[color_index%len(colours)], "condition": condition.get_value()})
                                        added_colour = True
                                        added_in_condition[node['id']] = ''
                                        links_added.append(link)
                                        links_added__with_conditions.append(link_with_condition)
                                        links_added_with_index_OG.append(link_with_index)
                                    else:
                                        checking_conditions = False
                        else:
                            if(link not in links_added):
                                dico['edges'].append({'A': node['id'], 'B': B, 'label': ''})
                                links_added.append(link) 
            #if(added_colour):
            #    color_index+=1
            
                    
            for sub in dico['subworkflows']:
                _, temp_added_colour = add_edges(dico["subworkflows"][sub], condition, checking_conditions, index=index, added_in_condition = added_in_condition, color_index=color_index) 
                if(temp_added_colour):
                    added_colour = True
            return checking_conditions, added_colour
        
        links_added_with_index = []
        #def add_edges_flow_edges(dico, added_in_condition):
        #    for index in added_in_condition:
        #        nodes_with_condition = added_in_condition[index]
        #        for node in dico['nodes']:
        #            edges = node_2_processes[node['id']]
        #            for B in edges:
        #                link_with_index = f"{node['id']} -> {B} ({index})"
        #                for node_with_condition in nodes_with_condition:
        #                    if(link_with_index not in links_added_with_index and link_with_index not in links_added_with_index_OG):
        #                        if(node['id'] in path_from_process_to_other_processes[node_with_condition] and B in path_from_process_to_other_processes[node_with_condition]):
        #                            dico['edges'].append({'A': node['id'], 'B': B, 'label': '', "colour": colours[index%len(colours)]})
        #                            links_added_with_index.append(link_with_index) 
        #                   
        #    for sub in dico['subworkflows']:
        #        add_edges_flow_edges(dico["subworkflows"][sub], added_in_condition) 
            
        
        #if(self.workflow.get_duplicate_status()):
        #    print("here")
        if(True):#Right now not generating the colored edges
            checking_conditions = True
            most_influential_conditions = self.workflow.get_most_influential_conditions()
            filtered_most_influential_conditions = {}

            for cond in most_influential_conditions:
                for ele in most_influential_conditions[cond]:
                    if(ele.get_type()!="Operation"):
                        try:
                            temp = filtered_most_influential_conditions[cond]
                        except:
                            filtered_most_influential_conditions[cond] = []
                        filtered_most_influential_conditions[cond].append(ele)
            #filtered_most_influential_conditions = most_influential_conditions
            list_most_influential_conditions = sorted(filtered_most_influential_conditions, key=lambda k: len(filtered_most_influential_conditions[k]), reverse=True)
            #list_most_influential_conditions = list(most_influential_conditions.keys())
            index = 0
            added_in_condition = {}
            
                
            color_index = 0 
            while(checking_conditions and\
                   index<len(list_most_influential_conditions) and index<10):
                
                added_in_condition[index] = {}
                condition = list_most_influential_conditions[index]
                checking_conditions, added_color = add_edges(dico, condition, checking_conditions, index=index, added_in_condition = added_in_condition[index], color_index = color_index)
                if(added_color):
                    color_index+=1
                index+=1
            add_edges(dico, condition="", checking_conditions=False)
            #add_edges_flow_edges(dico, added_in_condition)
            
        else:
            add_edges(dico, condition="", checking_conditions=False)

        self.dico_process_dependency_graph = dico
        self.intia_link_dico_processes()

        with open(f"{self.get_output_dir()}/graphs/process_dependency_graph.json", 'w') as output_file :
            json.dump(self.dico_process_dependency_graph, output_file, indent=4)

    
    def render_process_dependency_graph(self, filename = "process_dependency_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_process_dependency_graph, render_graphs = render_graphs, label_edge=False, label_node=False)
    

    def get_dependency_graph(self):
        self.intia_link_dico()
        nodes_in_graph = []
        branch_operation_ids = []
        #Function that replicates the workflow's structure wo the operations in the nodes
        def replicate_dico(dico_struct):
            dico = {}
            dico['nodes'] = []
            dico['edges'] = []
            dico['subworkflows'] = {}
            for node in dico_struct["nodes"]:
                if(get_type_node(node)!="Branch Operation"):
                    dico['nodes'].append(node)
                    nodes_in_graph.append(node['id'])
            for sub in dico_struct['subworkflows']:
                dico['subworkflows'][sub] = replicate_dico(dico_struct['subworkflows'][sub])
            return dico
        
        dico = replicate_dico(self.full_dico)

        #This is a dictionnary which links every node to it's connected process
        node_2_none_branch = copy.deepcopy(self.link_dico)
        already_searched = {}
        for node in node_2_none_branch:
            already_searched[node] = [node]
        changed = True
        while(changed):
            changed = False
            for node in node_2_none_branch:
                temp = node_2_none_branch[node].copy()
                for give in node_2_none_branch[node]:
                    if(is_operation(give) and give not in nodes_in_graph):
                        temp.remove(give)
                        if(node!=give and give not in already_searched[node]):
                            already_searched[node] += give
                            temp_temp = node_2_none_branch[give]
                            for node_temp in already_searched[node]:
                                try:
                                    temp_temp.remove(node_temp)
                                except:
                                    None
                            temp+=temp_temp
                            changed = True
                node_2_none_branch[node] = list(set(temp))

 
        links_added = []
        def add_edges(dico):
            for node in dico['nodes']:
                edges = node_2_none_branch[node['id']]
                for B in edges:
                    link = f"{node['id']} -> {B}"
                    if(link not in links_added):
                        dico['edges'].append({'A': node['id'], 'B': B, 'label': ''})
                        links_added.append(link)   
            for sub in dico['subworkflows']:
                add_edges(dico["subworkflows"][sub]) 
            
        add_edges(dico)
        self.dico_wo_branch_operation = dico

        with open(f"{self.get_output_dir()}/graphs/dependency_graph.json", 'w') as output_file :
            json.dump(self.dico_wo_branch_operation, output_file, indent=4)
    

    def render_dependency_graph(self, filename = "dependency_graph", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_wo_branch_operation, render_graphs = render_graphs)
    
    def get_dependency_graph_wo_labels(self, filename = "dependency_graph_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, self.dico_wo_branch_operation, label_edge=False, label_node=False, render_graphs = render_graphs)

    def get_dependency_graph_wo_orphan_operations(self, filename = "dependency_graph_wo_orphan_operations", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.dico_wo_branch_operation), render_graphs = render_graphs)
    
    def get_dependency_graph_wo_orphan_operations_wo_labels(self, filename = "dependency_graph_wo_orphan_operations_wo_labels", render_graphs = True):
        generate_graph(self.get_output_dir()/'graphs'/filename, graph_dico_wo_orphan_operations(self.dico_wo_branch_operation), label_edge=False, label_node=False, render_graphs = render_graphs)


    #============================
    #GENERATE USER VIEW
    #============================

    def get_user_view_graph(self, relevant_processes = [], use_process_dependency_graph = False, alias_2_tools = {}):
        #For now i'm only gonna work from the flattened dico
        if(use_process_dependency_graph):
            self.initialise_flattened_dico(self.dico_process_dependency_graph)
        else:
            self.initialise_flattened_dico(self.full_dico)
        dico = remove_artificial_nodes(self.dico_flattened)

        self.user_view, self.new_nodes_user_view = relev_user_view_builder(dico, relevant_modules=relevant_processes, alias_2_tools = alias_2_tools)

        with open(self.get_output_dir()/ "graphs/user_view.json", 'w') as output_file :
            json.dump(self.user_view, output_file, indent=4)
        

        #user_view_with_subworkflows = add_subworkflows_2_dico(self.dico_process_dependency_graph, self.user_view)
        #with open(self.get_output_dir()/ "graphs/user_view_with_subworkflows.json", 'w') as output_file :
        #    json.dump(user_view_with_subworkflows, output_file, indent=4)

        #return self.user_view, user_view_with_subworkflows
        return self.user_view
    
    def generate_user_view(self, relevant_processes = [], render_graphs = True, use_process_dependency_graph = False, alias_2_tools = {}):
        #user_view, user_view_with_subworkflows = self.get_user_view_graph(relevant_processes = relevant_processes)
        user_view = self.get_user_view_graph(relevant_processes = relevant_processes, use_process_dependency_graph = use_process_dependency_graph, alias_2_tools = alias_2_tools)
        #self.user_view_with_subworkflows = user_view_with_subworkflows
        generate_graph(self.get_output_dir()/'graphs'/"user_view", user_view, label_edge=True, label_node=True, render_graphs = render_graphs, root = False, relevant_nodes = copy.deepcopy(relevant_processes))
        #generate_graph(self.get_output_dir()/'graphs'/"user_view_with_subworkflows", user_view_with_subworkflows, label_edge=True, label_node=True, render_graphs = render_graphs, root = False, relevant_nodes = copy.deepcopy(relevant_processes))


    #This method returns the list of the clusters in topological order
    def get_clusters_from_user_view(self):

        topological_order = topological_sort(initia_link_dico_rec(self.user_view))
        tab = []
        for cluster in topological_order:
            temp = []
            for ele in cluster.split("_$$_"):
                temp.append(get_object(ele))
            tab.append(temp)
        return tab

    #============================
    #GENERATE LEVEL GRAPHS
    #============================
    def generate_level_graphs(self, render_graphs = True, label_edge=True, label_node=True):
        dico = self.dico_process_dependency_graph
        #dico = self.full_dico
        max_level = get_max_level(dico)
        for l in range(max_level+1):
            new_dico = get_graph_level_l(dico, l)
            generate_graph(self.get_output_dir()/'graphs'/f"level_{l}", new_dico, label_edge=label_edge, label_node=label_node, render_graphs = render_graphs)
            
    #============================
    #GET NUMBER OF SUBWORKFLOWS
    #============================

    def get_number_subworkflows_process_dependency_graph(self):
        return get_number_of_subworkflows(self.dico_process_dependency_graph)
    
    def get_number_subworkflows_user_view(self):
        return get_number_of_subworkflows(self.user_view_with_subworkflows )
        
    #============================
    #GET node_2_subworkflows
    #============================
    def node_2_subworkflows_process_dependency_graph(self):
        node_2_subworkflows = {}
        fill_node_2_subworkflows(self.dico_process_dependency_graph, node_2_subworkflows)
        return node_2_subworkflows
    
    #This methods returns the nodes to subworkflow dico but for the OG processes
    def node_2_subworkflows_user_view(self):
        node_2_subworkflows = {}
        fill_node_2_subworkflows(self.user_view_with_subworkflows, node_2_subworkflows)
        new_node_2_subworkflows = {}
        for group in self.new_nodes_user_view:
            for node in group:
                for id in node_2_subworkflows: 
                    if(node.replace('<', '').replace('>', '') in id):
                        new_node_2_subworkflows[node] = node_2_subworkflows[id]
        return new_node_2_subworkflows 

    #==========================================================
    #Check if fake dependency is created when created user view
    #==========================================================
    #Here to check if a fake dependency is created, I'm gonna compare the edges 
    #of the level graphs between the user view and the process dependency 
    #Each of the user view edges (with subworkflo) should be in the process dependency edges
    def check_fake_dependency_user_view(self):
        #This function removes the "<>" from the node name
        #And the same for the subworkflows
        def clean_node(node):
            #Case the node is a process
            if(node[0]=="<"):
                #We just remove the '<>' around the name
                node = node[1:-1]
            else:#it's a subworkflow
                for match in re.finditer(r"id_\d+\.\d+\_(.+)", node):
                    node = match.group(1)
            return node

        #First by checking if the node_2_subworkflows are the same, if it's the case i don't need to compare
        if(self.node_2_subworkflows_process_dependency_graph!=self.node_2_subworkflows_user_view):
            dico_process_dependency_graph = self.dico_process_dependency_graph
            user_view_with_subworkflows = self.user_view_with_subworkflows
            user_view_subworkflows = get_subworkflows_names(user_view_with_subworkflows)
            #Get the level workflows for the process dependency graph
            max_level = get_max_level(dico_process_dependency_graph)
            dependency_levels = []
            for l in range(max_level+1):
                new_dico = get_graph_level_l(dico_process_dependency_graph, l)
                dependency_levels.append(new_dico)
            #Get the level workflows for the user view
            max_level = get_max_level(user_view_with_subworkflows)
            user_view_levels = []
            for l in range(max_level+1):
                new_dico = get_graph_level_l(user_view_with_subworkflows, l)
                user_view_levels.append(new_dico)
            #For each level, i'm gonna check the edges
            for i in range(len(user_view_levels)):
                user_view_level = user_view_levels[i]
                dependency_level = dependency_levels[i]
                for sub in user_view_subworkflows:
                    for edge_user in user_view_level["edges"]:
                        if(f"_{sub}" in edge_user["A"] or f"_{sub}" in edge_user["B"]):
                            if(edge_user["A"]!="input" and edge_user["A"]!="output" and edge_user["B"]!="input" and edge_user["B"]!="output"):
                                #This boolean if is to check if the edge 'edge_user' has equivalence in the process dependency graph
                                has_matching_user_dependency = False
                                
                                for edge_process in get_edges(dependency_level):
                                    if(f"_{sub}" in edge_process["A"] or f"_{sub}" in edge_process["B"]):
                                        node = ""
                                        side = ""
                                        #Determine if it's A or B
                                        if(f"_{sub}" in edge_process["A"]):
                                            node = edge_process["B"]
                                            side = "B"
                                        if(f"_{sub}" in edge_process["B"]):
                                            node = edge_process["A"]
                                            side = "A"
                                        node = clean_node(node)
                                        if(node in edge_user[side]):
                                            has_matching_user_dependency = True
                                        
                                if(not has_matching_user_dependency):
                                    #Check if there is an indirect path that exist
                                    node_A = clean_node(edge_user["A"])
                                    node_B = clean_node(edge_user["B"])
                                    nodes_level = get_nodes_from_edges(get_edges(dependency_level))
                                    node_A_temp, node_B_temp = "", ""
                                    for A in node_A.split("_$$_"):
                                        for tmp in nodes_level:
                                            if A in tmp:
                                                node_A_temp = tmp
                                    for B in node_B.split("_$$_"):
                                        for tmp in nodes_level:
                                            if B in tmp:
                                                node_B_temp = tmp
                                    exists, _ = exist_path_dico(node_A_temp, node_B_temp, dependency_level)
                                    if(not exists):
                                        return True     
                                

            
            return False
        else:
            return False
    
    #This method returns a list of processes 
    def get_edges_that_create_cycle(self):
        links_flattened = initia_link_dico_rec(get_flatten_dico(self.get_process_dependency_graph()))
        not_source_2_sink = []
        node_2_sink = []
        for node in links_flattened:
            if(links_flattened[node]==[]):
                node_2_sink.append(node)
            else:
                not_source_2_sink+=links_flattened[node]
        not_source_2_sink = set(not_source_2_sink)
        source_2_node = list(set(links_flattened.keys()).difference(not_source_2_sink))
        links_flattened_source_sink = links_flattened.copy()
        links_flattened_source_sink["source"], links_flattened_source_sink["sink"] = source_2_node, []
        for node in node_2_sink:
            links_flattened_source_sink[node].append("sink")
 
        #The simple loops are included in this
        _, edges_create_cycles = get_number_cycles(links_flattened_source_sink)
        return edges_create_cycles

    #============================
    #METADATA FROM GRAPH
    #============================

    def initialise_flattened_dico(self, dico):
        self.dico_flattened = get_flatten_dico(dico)
        #for node in dico["nodes"]:
        #    self.dico_flattened["nodes"].append(node)
        #for edge in dico["edges"]:
        #    self.dico_flattened["edges"].append(edge)
        #for subworkflow in dico["subworkflows"]:
        #    self.initialise_flattened_dico(dico["subworkflows"][subworkflow])

    def get_metadata(self, graph):
        G = self.get_networkx_graph(graph, None)
        dico = {}
        for node in G.nodes(data=True):
            if(node[1]=={}):
                None
        process_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'Process']
        operation_nodes = [node for node, data in G.nodes(data=True) if data['type'] == 'Operation']

        dico['number_of_processes'] =  len(process_nodes)
        dico['number_of_operations'] =  len(operation_nodes)
        dico['number_of_nodes'] = dico['number_of_processes']+dico['number_of_operations']

        dico['number_of_edges_process_2_process'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="process_2_process")
        dico['number_of_edges_process_2_operation'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="process_2_operation")
        dico['number_of_edges_operation_2_process'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="operation_2_process")
        dico['number_of_edges_operation_2_operation'] = sum(1 for _, _, data in G.edges(data=True) if data['edge_type']=="operation_2_operation")
        
        dico['number_of_edges_source_process'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_process_2_operation']
        dico['number_of_edges_source_operation'] = dico['number_of_edges_operation_2_process'] + dico['number_of_edges_operation_2_operation']
        dico['number_of_edges_sink_process'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_operation_2_process']
        dico['number_of_edges_sink_operation'] = dico['number_of_edges_process_2_operation'] + dico['number_of_edges_operation_2_operation']
        dico['number_of_edges'] = dico['number_of_edges_process_2_process'] + dico['number_of_edges_process_2_operation'] + dico['number_of_edges_operation_2_process'] + dico['number_of_edges_operation_2_operation']
        
        dico["number_of_simple_loops"] = nx.number_of_selfloops(G)

        distribution_in_degrees_for_processes = list(dict(G.in_degree(process_nodes)).values())
        distribution_out_degrees_for_processes = list(dict(G.out_degree(process_nodes)).values())
        distribution_in_degrees_for_operations= list(dict(G.in_degree(operation_nodes)).values())
        distribution_out_degrees_for_operations= list(dict(G.out_degree(operation_nodes)).values())

        dico["distribution_in_degrees_for_processes"] = distribution_in_degrees_for_processes
        dico["distribution_out_degrees_for_processes"] = distribution_out_degrees_for_processes
        dico["distribution_in_degrees_for_operations"] = distribution_in_degrees_for_operations
        dico["distribution_out_degrees_for_operations"] = distribution_out_degrees_for_operations

        dico["distribution_in_degrees_for_all"] = dico["distribution_in_degrees_for_processes"]+dico["distribution_in_degrees_for_operations"]
        dico["distribution_out_degrees_for_all"] = dico["distribution_out_degrees_for_processes"]+dico["distribution_out_degrees_for_operations"]

        dico["average_in_degrees_for_processes"]   = np.array(distribution_in_degrees_for_processes).mean()
        dico["average_out_degrees_for_processes"]  = np.array(distribution_out_degrees_for_processes).mean()
        dico["average_in_degrees_for_operations"]  = np.array(distribution_in_degrees_for_operations).mean()
        dico["average_out_degrees_for_operations"] = np.array(distribution_out_degrees_for_operations).mean()
        dico["average_in_degrees_for_all"] = np.array(dico["distribution_in_degrees_for_all"] ).mean()
        dico["average_out_degrees_for_all"] = np.array(dico["distribution_out_degrees_for_all"] ).mean()


        dico["median_in_degrees_for_processes"]   = np.median(np.array(distribution_in_degrees_for_processes))
        dico["median_out_degrees_for_processes"]  = np.median(np.array(distribution_out_degrees_for_processes))
        dico["median_in_degrees_for_operations"]  = np.median(np.array(distribution_in_degrees_for_operations))
        dico["median_out_degrees_for_operations"] = np.median(np.array(distribution_out_degrees_for_operations))
        dico["median_in_degrees_for_all"] =  np.median(np.array(dico["distribution_in_degrees_for_all"]))
        dico["median_out_degrees_for_all"] = np.median(np.array(dico["distribution_out_degrees_for_all"]))

        #DEsnity = m/n(n-1), where n is the number of nodes and m is the number of edges
        dico['density'] = nx.density(G)
        weakly_connected_components = list(nx.weakly_connected_components(G))
        dico['number_of_weakly_connected_components'] = len(weakly_connected_components)
        
        components_with_over_2_nodes = [comp for comp in weakly_connected_components if len(comp) >= 2]
        dico['number_of_weakly_connected_components_with_2_or_more_nodes'] = len(components_with_over_2_nodes)

        #Getting the number of cycles
        self.initialise_flattened_dico(graph)
        links_flattened = initia_link_dico_rec(self.dico_flattened)
        not_source_2_sink = []
        node_2_sink = []
        for node in links_flattened:
            if(links_flattened[node]==[]):
                node_2_sink.append(node)
            else:
                not_source_2_sink+=links_flattened[node]
        not_source_2_sink = set(not_source_2_sink)
        source_2_node = list(set(links_flattened.keys()).difference(not_source_2_sink))
        links_flattened_source_sink = links_flattened.copy()
        links_flattened_source_sink["source"], links_flattened_source_sink["sink"] = source_2_node, []
        for node in node_2_sink:
            links_flattened_source_sink[node].append("sink")
 
        #The simple loops are included in this
        dico['number_of_cycles'], edges_create_cycles = get_number_cycles(links_flattened_source_sink)
        
        #Remove the edges which create the cycles
        #Since the number of paths from Source 2 sink and the longest path depend on the 
        #Topological ordering 
        #A topological ordering is possible if and only if the graph has no directed cycles, that is, if it is a directed acyclic graph (DAG)
        #We turn the CDG (cyclic directed graphs) into a DAG (directed acyclic graph)
        """for A, B in edges_create_cycles:
            links_flattened_source_sink[A].remove(B)


        #Here we need to update the sink source since some edges have been removed
        #See phyloplace worklfow (all nodes have an output channel) -> none connected to sink
        #TODO clean this cause it's just a copy of what is above
        not_source_2_sink = []
        node_2_sink = []
        for node in links_flattened:
            if(links_flattened_source_sink[node]==[]):
                node_2_sink.append(node)
            else:
                not_source_2_sink+=links_flattened_source_sink[node]
        not_source_2_sink = set(not_source_2_sink)
        source_2_node = list(set(links_flattened.keys()).difference(not_source_2_sink))
        links_flattened_source_sink["source"], links_flattened_source_sink["sink"] = source_2_node, []
        for node in node_2_sink:
            links_flattened_source_sink[node].append("sink")    
        

        structure_type = ""
        if(len(edges_create_cycles)==0):
            structure_type = "DAG"
        else:
            structure_type = "CDG"
        
        dico['structure_type'] = structure_type

        dico['number_of_paths_source_2_sink'] = get_number_paths_source_2_sink(links_flattened_source_sink)
        dico['shortest_path'] = dijkstra(links_flattened_source_sink)
        dico['longest_path'] = get_longest_distance(links_flattened_source_sink)"""

        
        """#Check that the values calculated are the same than what gives networkX
        dico_check = {}
        dico_check['nodes'] = []
        dico_check['edges'] = []
        dico_check['subworkflows'] = {}
        for node in links_flattened_source_sink:
            dico_check["nodes"].append({'id':node, 'xlabel':"", 'name':""})
            for B in links_flattened_source_sink[node]:
                dico_check["edges"].append({'A':node, "B":B, "label":""})

        G_DAG = self.get_networkx_graph(dico_check, None)
        #=====================================
        #ADDING SINK AND SOURCE TO THE GRAPH
        #=====================================
        source_node = "source"
        sink_node = "sink"
        
        if(dico['shortest_path']!=nx.shortest_path_length(G_DAG, source=source_node, target=sink_node)):
            raise Exception(f"{dico['shortest_path']}, {nx.shortest_path_length(G_DAG, source=source_node, target=sink_node)}")
        
        if(dico['longest_path']+1!=len(nx.dag_longest_path(G_DAG))):
            raise Exception(f"{dico['longest_path']}, {len(nx.dag_longest_path(G_DAG))}")
        
        
        #if(len(list(nx.all_simple_paths(G_DAG, source=source_node, target=sink_node)))!=dico['number_of_paths_source_2_sink']):
        #    raise Exception(f"{len(list(nx.all_simple_paths(G_DAG, source=source_node, target=sink_node)))}, {dico['number_of_paths_source_2_sink']}")
        """
        
        return dico


    def get_metadata_specification_graph(self):
        
        dico = self.get_metadata(self.full_dico)
        with open(self.get_output_dir()/ "graphs/metadata_specification_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    def get_metadata_dependency_graph(self):

        dico = self.get_metadata(self.dico_wo_branch_operation)
        with open(self.get_output_dir()/ "graphs/metadata_dependency_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    def get_metadata_process_dependency_graph(self):
        
        dico = self.get_metadata(self.dico_process_dependency_graph)
        with open(self.get_output_dir()/ "graphs/metadata_process_dependency_graph.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    def get_metadata_user_view(self):
        dico = self.get_metadata(self.user_view_with_subworkflows )
        with open(self.get_output_dir()/ "graphs/metadata_user_view.json", 'w') as output_file :
            json.dump(dico, output_file, indent=4)

    #def get_metadata_graph_wo_operations(self):
    #    G = self.networkX_wo_operations
    #    dico = self.get_metadata(G)
    #    with open(self.get_output_dir() / "graphs/metadata_graph_wo_operations.json", 'w') as output_file :
    #        json.dump(dico, output_file, indent=4)

    def get_number_weakly_connected_components_in_process_dependency_graph(self):
        G = self.get_networkx_graph(self.dico_process_dependency_graph, None)
        weakly_connected_components = list(nx.weakly_connected_components(G))
        return len(weakly_connected_components)

    def get_topogical_order(self, clusters):
        #if(self.get_process_dependency_graph_dico()=={}):
        #    self.intialise_process_dependency_graph()  
        link_dico = copy.deepcopy(self.link_dico)
        sorted_nodes = topological_sort(link_dico)
        clusters_sorted = []
        for elements in clusters:
            sub_sorted = []
            for ele in sorted_nodes:
                ele = get_object(ele)
                if(ele in elements):
                    sub_sorted.append(ele)
            clusters_sorted.append(sub_sorted)
        return clusters_sorted
    
    #From a list of processes
    #This method gets the nodes from the larger induced graph from these processes 
    def get_induced_subgraph(self, processes):
        self.intia_link_dico()

        nodes_to_conserve = []

        #Turning the processes into strings so they are compatible with the dico graphs and can be used
        processes_strings = []
        for p in processes:
            processes_strings.append(str(p))
        #Reomving the unwanted processes from the link dico
        link_dico_without_unwanted_processes = copy.deepcopy(self.link_dico)
        to_remove = []
        for node in link_dico_without_unwanted_processes:
            if(is_process(node) and node not in processes_strings):
                to_remove.append(node)
        for r in to_remove:
            link_dico_without_unwanted_processes.pop(r)
        
        #Building tab of edges
        edges = []
        for A in link_dico_without_unwanted_processes:
            for B in link_dico_without_unwanted_processes[A]:
                if(B not in to_remove):
                    edges.append({'A':A, 'B':B})

        for A in processes_strings:
            for B in processes_strings:
                if(A!=B):
                    #While paths still exist we continue to search
                    exists = True
                    temp_edges = copy.deepcopy(edges)
                    while(exists):
                        exists = False
                        exists , visited = exist_path(A, B, temp_edges)
                        nodes_visited = []
                        for n in visited:
                            if(visited[n]):
                                nodes_visited.append(n)
                        #In the case there is a path exists, we remove an edge (the last one, connecting to the last node)
                        #By removing this node -> we break that path
                        for n in nodes_visited:
                            try:
                                temp_edges.remove({'A':n, 'B':B})  
                                break
                            except:
                                None
                        nodes_to_conserve += nodes_visited
        elements = []
        for n in list(set(nodes_to_conserve)):
            elements.append(get_object(n))
        return elements
    
    #Method that checks if a specified structute is the same than the workflows
    def check_if_json_equal_to_full_structure(self, file):
        if(not self.initialised):
            self.initialise()
        spec_graph_wfA = self.full_dico
        with open(file) as json_file:
            spec_graph_wfB = json.load(json_file)
        return check_if_equal(spec_graph_wfA, spec_graph_wfB)
    
    def check_if_process_dependendy_is_equivalent_to_other_without_subworkflows(self, dico):
        A, B = get_flatten_dico(self.dico_process_dependency_graph), get_flatten_dico(dico)
        return check_if_equal(A, B)


            


