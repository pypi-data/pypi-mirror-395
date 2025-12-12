import re
import glob
import copy
import ctypes
import multiprocessing

from .code_ import Code
from .condition import Condition
from .nextflow_building_blocks import Nextflow_Building_Blocks
from .outils import remove_jumps_inbetween_parentheses, remove_jumps_inbetween_curlies, sort_and_filter, get_dico_from_tab_from_id, check_if_element_in_tab_rocrate, get_python_packages, get_R_libraries, get_perl_modules, process_2_DSL2, extract_tools
from .bioflowinsighterror import BioFlowInsightError

from . import constant

def get_object(address):
    address = int(re.findall(r"\dx\w+", address)[0], base=16)
    return ctypes.cast(address, ctypes.py_object).value

class Process(Nextflow_Building_Blocks):
    def __init__(self, code, nextflow_file):
        self.nextflow_file = nextflow_file
        self.code = Code(code, origin = self, initialise=False)
        #Origin is only used in the case DSL1
        self.origin = None
        self.name = ""
        self.alias = ""
        self.printed_name = ""
        self.inputs = []
        self.raw_input_names = []#This is used to convert DSL1 workflows to DSL2
        self.outputs = []
        self.outputs_per_line = []

        self.input_code = ""
        self.output_code = ""
        self.when_code = ""
        self.pusblishDir_code = ""
        self.script_code = ""

        self.called_by = []#List of calls
        self.initialised = False
        self.number_times_copied = 0
        self.initialise_name()


    def copy(self):
        process = copy.copy(self)
        process.name = ""
        process.alias = ""
        process.printed_name = ""
        process.inputs = []
        process.raw_input_names = []#This is used to convert DSL1 workflows to DSL2
        process.outputs = []
        process.input_code = ""
        process.output_code = ""
        process.when_code = ""
        process.pusblishDir_code = ""
        process.script_code = ""
        process.called_by = []#List of calls
        process.initialised = False
        num = self.number_times_copied
        self.number_times_copied += 1
        return process, num

    def set_origin(self, thing):
        if(self.nextflow_file.get_DSL()=="DSL1"):
            self.origin = thing
        else:
            raise Exception("This shouldn't happen")

    
    def add_to_ternary_operation_dico(self, old, new):
        self.nextflow_file.add_to_ternary_operation_dico(old, new)
    
    def add_map_element(self, old, new):
        self.nextflow_file.add_map_element(old, new)

    def add_to_emits(self, emit):
        self.later_emits.append(emit)
    
    def get_later_emits(self):
        return self.later_emits
    
    def set_alias(self, alias):
        self.alias = alias

    def set_printed_name(self, name):
        self.printed_name = name

    def get_alias(self):
        return self.alias
    
    def get_alias_and_id(self):
        return f"{self.alias}_GG_{id(self)}"
    
    def get_printed_name(self):
        return self.printed_name

    def get_number_times_called(self):
        return self.number_times_called
    
    def incremente_number_times_called(self):
        self.number_times_called+=1
    
    def add_to_calls(self, call):
        self.called_by.append(call)

    def get_call(self):
        if(len(self.called_by)!=1):
            raise Exception("TODO2 -> need to update the calls for DSL1")
        return self.called_by[0]
    
    def get_calls(self):
        return self.called_by
    
    
    def get_script_code(self):
        code = " "+self.script_code+" "
        if(self.script_code.count('"""')==2):
            return self.script_code.split('"""')[1]
        if(self.script_code.count('"""')==4):
            return self.script_code.split('"""')[1]+self.script_code.split('"""')[3]
        if(self.script_code.count('"""')==6):
            return self.script_code.split('"""')[1]+self.script_code.split('"""')[3]+self.script_code.split('"""')[5]
        if(self.script_code.count("'''")==2):
            return self.script_code.split("'''")[1]
        if(self.script_code.count("'''")==4):
            return self.script_code.split("'''")[1]+self.script_code.split("'''")[3]
        if(self.script_code.count("'''")==6):
            return self.script_code.split("'''")[1]+self.script_code.split("'''")[3]+self.script_code.split("'''")[5]
        return self.script_code
    
    def get_name(self):
        return self.name
    
    #Method which returns the DSL type of a process, i use the presence 
    #of from and into as a proxy. By default it's DSL2
    def which_DSL(self):
        DSL = "DSL2"
        pattern = constant.FROM
        for match in re.finditer(pattern, self.code.get_code()):
            DSL = "DSL1"
        pattern = constant.INTO
        for match in re.finditer(pattern, self.code.get_code()):
            DSL = "DSL1"
        return DSL

    def is_initialised(self):
        return self.initialised

    #def get_sink(self):
    #    return [self]
    
    def get_type(self):
        return "Process"

    
    
    def get_input_code_lines(self):
        tab = []
        for l in self.input_code.split('\n'):
            tab.append(l.strip())
        return tab

    def get_inputs(self):
        return self.inputs
    
    def get_nb_inputs(self):
        return len(self.inputs)
    
    def get_outputs(self):
        return self.outputs
    
    def get_output_code_lines(self):
        tab = []
        for l in self.output_code.split('\n'):
            tab.append(l.strip())
        return tab
    
    def get_nb_outputs(self):
        return len(self.outputs)
    
    #TODO -> Have a much better way of doing this  
    def extract_tools(self):
        script = self.script_code.lower()
        for tool in constant.TOOLS:
            if tool in script:
                self.tools.append(tool)
    

    def initialise_parts(self):
        code = self.get_code()
        
        #Check to see if the process is empty
        temp_code = re.sub(constant.PROCESS_HEADER, "", code)
        temp_code = temp_code[:-1].strip()
        if(len(temp_code)==0):
            raise BioFlowInsightError('ep', self, self.get_name())

        publishDir_multiple, publishDir_pos= False, (0, 0)
        for match in re.finditer(r"publishDir", code):
            #if(publishDir_multiple):
            #    raise BioFlowInsightError(f"Multiple 'publishDir' were found in the process '{self.get_name()}'.", num = 22, origin=self)
            publishDir_pos = match.span(0)
            publishDir_multiple = True

        input_multiple, input_pos= False, (0, 0)
        for match in re.finditer(constant.INPUT, code):
            if(input_multiple):
                raise BioFlowInsightError('meip', self, 'input', self.get_name())
            input_pos = match.span(0)
            input_multiple = True

        output_multiple, output_pos= False, (0, 0)
        for match in re.finditer(constant.OUTPUT, code):
            if(output_multiple):
                raise BioFlowInsightError('meip', self, 'output', self.get_name())
            output_pos = match.span(0)
            output_multiple = True

        when_multiple, when_pos= False, (0, 0)
        for match in re.finditer(constant.WHEN, code):
            if(when_multiple):
                raise BioFlowInsightError('meip', self, 'when', self.get_name())
            when_pos = match.span(0)
            when_multiple = True

        script_pos= (0, 0)
        for match in re.finditer(constant.SCRIPT, code):
            script_pos = match.span(0)
            break

        positions = [publishDir_pos, input_pos, output_pos, when_pos, script_pos]
        variables_index = ['pusblishDir', 'input', 'output', 'when', 'script']
        if(positions!=[(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]):
            positions, variables_index = sort_and_filter(positions, variables_index)
        

            for i in range(len(positions)):
                temp_code = ""
                if(i==len(positions)-1):
                    temp_code =  code[positions[i][1]:code.rfind('}')].strip()
                else:
                    temp_code =  code[positions[i][1]:positions[i+1][0]].strip()
                
                if(variables_index[i]=='input'):
                    self.input_code = temp_code
                elif(variables_index[i]=='output'):
                    self.output_code = temp_code
                elif(variables_index[i]=='pusblishDir'):
                    self.pusblishDir_code = temp_code
                elif(variables_index[i]=='when'):
                    self.when_code = temp_code
                elif(variables_index[i]=='script'):
                    self.script_code = temp_code
                    #self.extract_tools()
                else:
                    raise Exception("This shoudn't happen!")
        else:
            self.input_code = ""
            self.output_code = ""
            self.pusblishDir_code = ""
            self.when_code = ""
            self.script_code = ""



    #Method that returns the input part of the process code
    def get_input_code(self):
        return self.input_code


    #Function that extracts the inputs from a process 
    def initialise_inputs_DSL1(self):
        code = "\n"+self.get_input_code()+"\n"
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        #Simplying the inputs -> when there is a jump line '.' -> it turns it to '.'
        code = re.sub(constant.JUMP_DOT, '.', code)

        def add_channel(name):
            channels = self.origin.get_channels_from_name_same_level(name)
            channels += self.origin.get_channels_from_name_above_level(name)
            channels += self.origin.get_channels_from_name_inside_level(name)
            channels += self.origin.get_channels_from_name_other_blocks_on_same_level(name)
            if(len(channels)==0):
                from .channel import Channel
                input = Channel(name=name, origin=self.origin)
                self.origin.add_channel(input)
                input.add_sink(self)
                self.inputs.append(input)
            else:
                for ch in channels:
                    self.inputs.append(ch)
                    ch.add_sink(self)

        
        for line in code.split("\n"):
            placed = False

            #Case there is a single channel as an input -> doesn't use from to import channel -> uses file (see https://github.com/nextflow-io/nextflow/blob/45ceadbdba90b0b7a42a542a9fc241fb04e3719d/docs/process.rst)
            patterns = [constant.FILE1, constant.FILE2, constant.PATH1, constant.PATH2]
            for pattern in patterns:
                for match in re.finditer(pattern, line+"\n"):
                    #In the first case it's "file ch" in the second "file (ch)" 
                    try:
                        extracted = match.group(1).strip()
                    except:
                        extracted = match.group(2).strip()
                    placed = True
                    add_channel(extracted)
                    self.raw_input_names.append(extracted)
            
            if(not placed):
                #Case there are multiple channels as input (e.g. channel1.mix(channel2))
                pattern = constant.FROM
                for match in re.finditer(pattern, line+"\n"):
                    extracted = match.group(1).strip()
                    self.raw_input_names.append(extracted)
                    placed = True
                    if(bool(re.fullmatch(constant.WORD, extracted))):
                        add_channel(extracted)
                    else:
                        from .operation import Operation
                        operation = Operation(code=extracted, origin=self.origin)
                        operation.initialise()
                        operation.is_defined_in_process(self)
                        self.inputs+=operation.get_origins()
            
            if(not placed):
                if(re.fullmatch(constant.WORD, line.strip())):
                    add_channel(line)
                    self.raw_input_names.append(line)
        
        #self.inputs = list(set(self.inputs))#TODO Check this

    #Function that extracts the inputs from a process (for DSLS workflows)
    def initialise_inputs_DSL2(self):
        code = self.get_input_code()
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        for input in code.split("\n"):
            input = input.strip()
            if(input!=""):
                self.inputs.append(input)            


    #Method that returns the input part of the process code
    def get_output_code(self):
        return self.output_code
    
    def get_file_extensions_outputs(self):
        code = self.get_output_code()
        extensions = []
        for match in re.finditer(r"(\.\w+)+|\.\w+", code):
            extensions.append(match.group(0))
        return extensions
    
    def get_input_parameters(self):
        code = self.get_input_code()

        #This is to remove the from for the DSL1 processes
        #But also remoce the 'stageAs'
        lines = code.split('\n')
        code = ""
        for l in lines:
            code+=l.split(" from ")[0].split("stageAs")[0]
            code+'\n'

        parameters = []
        for match in re.finditer(r"\w+(\.\w+)*", code):
            parameters.append(match.group(0))
        parameters = list(set(parameters))#Here we can a unique cause a parameter can only be given once in any case
        words_2_remove = ["path", "val", "tuple", "into", "stageAs", "emit", "file", "set"]
        for word in words_2_remove:
            try:
                parameters.remove(word)
            except:
                None
        return parameters

    def get_modules(self):
        return self.modules
    
    def get_commands(self):
        return self.commands
    
    def get_code_with_alias(self):
        code = self.get_code()
        def replacer(match):
            return match.group(0).replace(match.group(1), self.get_alias())
        return re.sub(r"process\s*(\w+)\s*\{", replacer, code)
    
    def get_code_with_alias_and_id(self):
        code = self.get_code()
        def replacer(match):
            return match.group(0).replace(match.group(1), self.get_alias_and_id())
        from .constant import PROCESS_HEADER
        return re.sub(PROCESS_HEADER, replacer, code)


    def simplify_code(self):
        return self.get_code_with_alias_and_id()

    #Function that extracts the outputs from a process (DSL1)
    def initialise_outputs_DSL1(self):
        code = self.get_output_code()
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)

        def add_channel(name):
            channels = self.origin.get_channels_from_name_same_level(name)
            channels += self.origin.get_channels_from_name_above_level(name)
            channels += self.origin.get_channels_from_name_inside_level(name)
            channels += self.origin.get_channels_from_name_other_blocks_on_same_level(name)
            if(len(channels)==0):
                from .channel import Channel
                output = Channel(name=name, origin=self.origin)
                self.origin.add_channel(output)
                output.add_source(self)
                self.outputs.append(output)
            else:
                for ch in channels:
                    self.outputs.append(ch)
                    ch.add_source(self)

        pattern =constant.INTO_2
        for match in re.finditer(pattern, code):
            outputs = match.group(1).split(',')
            tab = []
            for i in range(len(outputs)):
                add_channel(outputs[i].strip())
                tab.append(self.outputs[-1])
            self.outputs_per_line.append(tab)
        
        patterns = [constant.FILE1, constant.FILE2]
        for pattern in patterns:
            for match in re.finditer(pattern, code):
                add_channel(match.group(1))
                self.outputs_per_line.append([self.outputs[-1]])

    #Function that extracts the inputs from a process (for DSLS workflows)
    def initialise_outputs_DSL2(self):
        code = self.get_output_code()
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        for output in code.split("\n"):
            output = output.strip()
            if(output!=""):
                self.outputs.append(output) 


    def initialise_name(self):
        for match in re.finditer(constant.PROCESS_HEADER, self.code.get_code()):
            self.name = match.group(1)
            self.name = self.name.replace("'", "")
            self.name = self.name.replace('"', '')
            if(self.name=="process"):
                raise BioFlowInsightError('pnip', self)
            if(self.alias==""):
               self.alias = self.name
            self.printed_name = self.alias

    def get_name_to_print(self):
        return self.printed_name

    def get_structure(self, dico):
        dico['nodes'].append({'id':str(self), 'name':self.get_name_to_print(), "shape":"ellipse", 'xlabel':"", 'fillcolor':'', "artificial": False})

    def initialise_inputs_outputs(self):
        DSL = self.nextflow_file.get_DSL()
        if(DSL=="DSL1"):
            if(self.origin!=None):
                self.initialise_inputs_DSL1()
                self.initialise_outputs_DSL1()
        elif(DSL=="DSL2"):
            self.initialise_inputs_DSL2()
            self.initialise_outputs_DSL2()
        else:
            raise Exception("Workflow is neither written in DSL1 nor DSL2!")


    def initialise(self):
        if(not self.initialised):
            self.initialised = True
            self.initialise_name()
            self.initialise_parts()
            self.initialise_inputs_outputs()

    def convert_input_code_to_DSL2(self):
        code = "\n"+self.get_input_code()+"\n"
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        #Simplying the inputs -> when there is a jump line '.' -> it turns it to '.'
        code = re.sub(constant.JUMP_DOT, '.', code)
        #code = process_2_DSL2(code) 
        lines = []
        for line in code.split("\n"):
            if(" def " in " "+line):
                raise BioFlowInsightError("uiip", self, line.strip(), self.get_name())
            if(re.fullmatch(r"params\.\w+", line.strip())):
                raise BioFlowInsightError("cciop", self, line.strip(), self.get_name())
            temp = process_2_DSL2(line.split(" from ")[0]) 
            lines.append(temp)
            #TODO -> need to determine if it's on it's own is it either a path or val
        code = "\n".join(lines)
        return code
    
    def convert_output_code_to_DSL2(self):
        code = self.get_output_code()
        code = remove_jumps_inbetween_parentheses(code)
        code = remove_jumps_inbetween_curlies(code)
        lines = []
        for line in code.split("\n"):
            line = line.replace(" into ", ", emit: ")
            line = line.replace(" mode flatten", "")
            #Remove optionnal true #TODO check if this breaks soemthing
            line = line.replace("optional true", "")
            line = process_2_DSL2(line) 
            lines.append(line)
        code = "\n".join(lines)
        #Removing the extra emits
        #For it to only have one,
        for line in self.outputs_per_line:
            def replacer(match):
                return match.group(1)
            for o in line[1:]:
                code = re.sub(fr"\,\s*{re.escape(o.get_code())}(\s|\,|\))", replacer, code+"\n")
        return code
    
    #This method is to detect which are the channels which need to be flattened
    #See https://github.com/nextflow-io/nextflow/blob/be1694bfebeb2df509ec4b42ea5b878ebfbb6627/docs/dsl1.md
    def get_channels_to_flatten(self):
        code = self.output_code
        channels = []
        for match in re.finditer(r"(\w+) mode flatten", code):
            channels.append(match.group(1))
        return channels
    
    #This method cleans the raw_input_names to use when rewriting DSL1 workflows
    def clean_raw_input_names(self, raw_input_names):
        for i in range(len(raw_input_names)):
            if(bool(re.fullmatch(r"\w+\.val", raw_input_names[i]))):
                raw_input_names[i] = raw_input_names[i].split('.')[0]
        return raw_input_names
    
    def get_parameters_call(self):
        return ', '.join(self.clean_raw_input_names(self.raw_input_names))


    def convert_to_DSL2(self):
        if(self.get_DSL()=="DSL2"):
            print("Workflow is already written in DSL2")
        else:
            code = self.get_code()
            call = [f"{self.get_name()}({self.get_parameters_call()})"]
            if(self.input_code!=""):
                temp = code
                old, new = self.input_code, self.convert_input_code_to_DSL2()
                code = code.replace(old, new)
                if(old!= new and temp==code):
                    raise Exception("This souldn't happen")
            if(self.output_code!=""):
                temp = code
                old, new = self.output_code, self.convert_output_code_to_DSL2()
                code = code.replace(old, new)
                if(old!= new and temp==code):
                    print(f'"{self.output_code}"')
                    print(f'"{self.convert_output_code_to_DSL2()}"')
                    raise Exception("This souldn't happen")
            channels_to_flatten = self.get_channels_to_flatten()
 

            #Rewriting the attributions of the channels for it to match the new values emitted (single values)
            index = 0
            for line in self.outputs_per_line:
                for emitted in line:
                    o = self.outputs[index]
                    if(o.get_code() in channels_to_flatten):
                        call.append(f"{o.get_code()} = {self.get_name()}.out.{line[0].get_code()}.flatten()")
                    else:
                        call.append(f"{o.get_code()} = {self.get_name()}.out.{line[0].get_code()}")
                    index+=1

            #for o in self.outputs:
            #    if(o.get_code() in channels_to_flatten):
            #        call.append(f"{o.get_code()} = {self.get_name()}.out.{o.get_code()}.flatten()")
            #    else:
            #        call.append(f"{o.get_code()} = {self.get_name()}.out.{o.get_code()}")
            call = "\n".join(call)
            return code, call
    
    def get_tools(self, extract_general_tools = False):
        #FOR now -> i've disabled this functionnality 
        return []

        #manager = multiprocessing.Manager()
        #tools = manager.dict()
        #p = multiprocessing.Process(target=extract_tools, kwargs={"script":self.get_script_code(), "extract_general_tools":extract_general_tools, "tools_2_return":tools})
        #p.start()
        ## Wait for 60 seconds or until process finishes
        #p.join(60)
        ## If thread is still active
        #if p.is_alive():
        #    return []
        #else:
        #    return list(tools.keys())
        ##return extract_tools(self.get_script_code(), extract_general_tools = extract_general_tools, tools)
    
    def get_all_conditions(self):
        if(self.nextflow_file.get_DSL()=="DSL2"):
            if(len(self.called_by)!=1):
                raise Exception("This shouldn't happen")
            return self.called_by[0].get_all_conditions()
        else:
            conditions = {}
            return self.origin.get_all_conditions(conditions)


    def add_2_rocrate(self, dico, parent_key):
        process_key = self.get_rocrate_key(dico)
        dico_process = get_dico_from_tab_from_id(dico, process_key)
        if(dico_process==None):
            dico_process = {}
            dico_process["@id"] = process_key
            dico_process["name"] = f"Process#{self.get_alias()}"
            dico_process["@type"] = ["SoftwareSourceCode"]
            #ADD INPUTS
            dico_process["input"] = []
            for input in self.get_inputs():
                if(type(input)==str):
                    name_input = input
                else:
                    name_input = input.get_code()
                dico_input = get_dico_from_tab_from_id(dico, name_input)
                if(dico_input==None):
                    dico_input = {"@id":f"#{name_input}", "name": name_input, "@type": "FormalParameter"}
                    dico["@graph"].append(dico_input)
                dico_process["input"].append({"@id":dico_input["@id"]})
            #ADD OUTPUTS
            dico_process["output"] = []
            for output in self.get_outputs():
                if(type(output)==str):
                    name_output = output
                else:
                    name_output = output.get_code()
                dico_output = get_dico_from_tab_from_id(dico, name_output)
                if(dico_output==None):
                    dico_output = {"@id":f"#{name_output}", "name": name_output, "@type": "FormalParameter"}
                    dico["@graph"].append(dico_output)
                dico_process["output"].append({"@id":dico_output["@id"]})
            #ADD isPartOf
            dico_process["isPartOf"] = []
            dico_process["isPartOf"].append({"@id":parent_key})
            #ADD hasPart
            dico_process["hasPart"] = []
            for tool in self.get_tools():
                dico_tool = get_dico_from_tab_from_id(dico, tool)
                if(dico_tool==None):
                    dico_tool = {"@id":tool, 
                                   "name": tool,
                                   "@type": "Tool"
                                   #TODO in later versions
                                   , "url": f"https://bio.tools/t?page=1&q={tool}&sort=score"
                                   #, "identifier": "tool_identifier"
                                   }
                    dico["@graph"].append(dico_tool)
                dico_process["hasPart"].append({"@id":dico_tool["@id"]})

            dico["@graph"].append(dico_process)
        else:
            if(not check_if_element_in_tab_rocrate(dico_process["isPartOf"], parent_key)):
                dico_process["isPartOf"].append({"@id":parent_key})
        self.get_nextflow_file().add_to_has_part(dico, process_key)
    

    def get_inputs_DBfile(self):
        input_params = self.get_input_parameters()
        for i in range(len(input_params)):
            input_params[i] = f'"{input_params[i]}"'
        generic_ids = []
        params = list(set(input_params))
        index = 0
        for p in params:
            generic_ids.append(f"sf:input{index}_{self.get_alias()}")
            index+=1
        return params, generic_ids
    
    def get_outputs_DBfile(self):
        output_params = self.get_outputs()
        for i in range(len(output_params)):
            output_params[i] = output_params[i].replace(",", "\\,")
            output_params[i] = output_params[i].replace("'", "\\'")
            output_params[i] = output_params[i].replace('"', '\\"')
            output_params[i] = f'"{output_params[i]}"'
        generic_ids = []
        params = list(set(output_params))
        index = 0
        for p in params:
            generic_ids.append(f"sf:output{index}_{self.get_alias()}")
            index+=1
        return params, generic_ids
    
    def get_DBfile_description(self):
        text = ""
        text+= f"# {self.get_alias()} Step"
        text+= f"\nsf:step{self.get_alias()} rdf:type sf:Step"

        input_params, generic_ids_inputs = self.get_inputs_DBfile()
        if(len(input_params)!=0):
            text+= f" ;\n\tsf:inputVariable {', '.join(generic_ids_inputs)}"

        output_params, generic_ids_outputs = self.get_outputs_DBfile()
        if(len(output_params)!=0):
            text+= f" ;\n\tsf:outputVariable {', '.join(generic_ids_outputs)}"

        tools = self.get_tools()
        for i in range(len(tools)):
            tools[i] = f"sf:TOOL{tools[i]}"
        if(len(tools)!=0):
            text+= f" ;\n\tsf:use {', '.join(tools)}"

        isFollowedBy = self.get_link_dico_processes()[str(self)]
        for i in range(len(isFollowedBy)):
            isFollowedBy[i] = f'sf:step{get_object(isFollowedBy[i]).get_alias()}'
        if(len(isFollowedBy)!=0):
            text+= f" ;\n\tsf:isFollowedBy {', '.join(isFollowedBy)}"
        
        text+=" ."
        
        for t in tools:
            name = t[7:]#To remove the sf:TOOL"
            text+= f"""\n\n{t} rdf:type sf:Command ;
\tschema:name "{name}" ;
\tschema:url <https://bio.tools/t?page=1&q={name}&sort=score> ."""
            
        
            
        for i in range(len(input_params)):
            gen_id = generic_ids_inputs[i]
            name = input_params[i]
            text+=f"\n\n{gen_id} rdf:type sf:Variable ;\n\tschema:name {name} ."

        for i in range(len(output_params)):
            gen_id = generic_ids_outputs[i]
            name = output_params[i]
            text+=f"\n\n{gen_id} rdf:type sf:Variable ;\n\tschema:name {name} ."

            
        return text
    
        
        




