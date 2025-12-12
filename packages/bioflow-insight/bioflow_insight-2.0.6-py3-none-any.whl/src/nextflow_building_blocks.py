import os
import re
from pathlib import Path

from . import constant

from .outils import extract_curly, extract_end_operation, extract_executor_from_middle, get_end_call, expand_call_to_operation, get_curly_count, get_parenthese_count, expand_pipe_operator, checks_in_condition_if, checks_in_string
from .code_ import Code


class Nextflow_Building_Blocks:
    def __init__(self, code, initialise_code):
        self.code = Code(code = code, origin = self, initialise=initialise_code)
    
    #---------------------------------
    #AUXILIARY METHODS FOR ALL CLASSES
    #---------------------------------

    def add_to_ternary_operation_dico(self, old, new):
        self.origin.add_to_ternary_operation_dico(old, new)
    
    def add_map_element(self, old, new):
        self.origin.add_map_element(old, new)

    def get_code(self, get_OG = False):
        return self.code.get_code(get_OG = get_OG)
    
    def get_modules_defined(self):
        return self.origin.get_modules_defined()
    
    def get_process_from_name(self, name):
        return self.origin.get_process_from_name(name)
    
    def get_origin(self):
        return self.origin
    
    def get_output_dir(self):
        return self.origin.get_output_dir()
    
    def get_DSL(self):
        return self.origin.get_DSL()
    
    def get_processes_annotation(self):
        return self.origin.get_processes_annotation()
    
    def get_duplicate_status(self):
        return self.origin.get_duplicate_status()
    
    #def get_file_address(self):
    #    return self.origin.get_file_address()
    
    def get_nextflow_file(self):
        try:
            return self.origin.get_file_address()
        except:
            return self.nextflow_file
        
    def get_link_dico_processes(self):
        try:
            return self.origin.get_link_dico_processes()
        except:
            return self.nextflow_file.get_link_dico_processes()
        
        
    
    def get_display_info(self):
        return self.origin.get_display_info()
    
    def get_name_processes_subworkflows(self):
        return self.origin.get_list_name_subworkflows()+self.origin.get_list_name_includes()+ self.origin.get_list_name_processes()
    
    ##Only used by the process or subworkflow
    #def is_called(self, called_from):
    #    #if(self.get_type() in ["Subworkflow", "Process"]):
    #    if(self.get_type() in ["Subworkflow"]):
    #
    #        executors = called_from.origin.get_executors()
    #        for exe in executors:
    #            if(exe.get_type()=="Call"):
    #                if(self in exe.get_elements_called()):
    #                    return True
    #            #Case operation
    #            else:
    #                for o in exe.get_origins():
    #                    if(o.get_type()=="Call"):
    #                        if(self in o.get_elements_called()):
    #                            return True
    #        return False
    #
    #    elif(self.get_type() in ["Process"]):
    #        if(self.get_number_times_called()>=1):
    #            return True
    #    raise Exception("You can't do this!")
    
    def get_line(self, bit_of_code):
        return self.origin.get_line(bit_of_code)
    
    def get_string_line(self, bit_of_code):
        return self.origin.get_string_line(bit_of_code)
    
    def get_name_file(self):
        return self.origin.get_name_file()
    
    def get_subworkflow_or_main(self):
        origin = self.get_origin()
        if(origin.get_type() in ["Main", "Subworkflow"]):
            return origin
        else:
            return origin.get_subworkflow_or_main()

    def get_rocrate_key(self, dico):
        return f"{str(self.get_file_address())[len(dico['temp_directory']):]}#{self.get_name()}"

    def get_file_address(self, short = False):
        try:
            return self.origin.get_file_address(short = short)
        except:
            return self.nextflow_file.get_file_address(short = short)
    
    def get_workflow_address(self):
        return self.origin.get_workflow_address()

    
    
    #def get_process_from_name(self, name):
    #    for p in self.get_processes():
    #        if(p.get_name()==name):
    #            return p
    #    return None
    
    #def get_channels(self):
    #    return self.origin.get_channels()

    #def get_processes(self):
    #    return self.processes
    
    def get_workflow_code(self):
        return self.origin.get_workflow_code()
    
    def get_file_conditions(self):
        return self.origin.get_file_conditions()

    #----------------------
    #CHANNELS
    #----------------------

    ##Check if a channel given in parameters is already in channels
    #def check_in_channels(self, channel):
    #    for c in self.channels:
    #        if(c.equal(channel)):
    #            return True
    #    return False

    #def get_channel_from_name(self, name):
    #    for c in self.channels:
    #        if(name == c.get_name()):
    #            return c
    #    #raise Exception(f"{name} is not in the list of channels")
    #    return None

    ##Method that adds channel into the lists of channels
    #def add_channel(self, channel):
    #    if(not self.check_in_channels(channel)):
    #        self.channels.append(channel)
    #    else:
    #        raise Exception("This shoudn't happen!")


    """def add_channels_structure_temp(self, dico, added_operations):
        for c in self.get_channels():
            for source in c.get_source():
                for sink in c.get_sink():
                    if(not(isinstance(source, Operation)) or not(isinstance(sink, Operation))):
                        raise Exception("NOt operations!!")
                    
                    if(source not in added_operations):
                        #dot.node(str(source), "", shape="point", xlabel= source.get_code())
                        dico["nodes"].append({"id":str(source), "name":'', "shape":"point", "xlabel": source.get_code()})
                        added_operations.append(source)
                    if(sink not in added_operations):
                        #dot.node(str(sink), "", shape="point", xlabel= sink.get_code())
                        dico["nodes"].append({"id":str(sink), "name":'', "shape":"point", "xlabel": sink.get_code()})
                        added_operations.append(sink)

                    #dot.edge(str(source), str(sink), label= c.get_name())
                    dico["edges"].append({"A":str(source), "B":str(sink), "label": c.get_name()})
        return dico"""


    #----------------------
    #EXECUTORS
    #----------------------
    


    def get_executors(self):
        return self.executors
    
    
        

    #----------------------
    #OPERATIONS
    #----------------------

    #Method that adds operation into the lists of operations
    def add_operation(self, operation):
        self.operations.append(operation)

    #----------------------
    #INCLUDES
    #----------------------
    def get_all_includes(self):
        return self.origin.get_all_includes()

    def add_include_to_all_includes(self, include):
        self.origin.add_include_to_all_includes(include)

