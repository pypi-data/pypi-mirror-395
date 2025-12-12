import re 
from . import constant
from .code_ import Code
import copy
from .root import Root
from .main import Main
from .bioflowinsighterror import BioFlowInsightError
from .outils import remove_jumps_inbetween_parentheses, replace_group1, get_dico_from_tab_from_id, check_if_element_in_tab_rocrate




class Subworkflow(Main):
    def __init__(self, code, nextflow_file, name):
        Main.__init__(self, code, nextflow_file)
        self.name = name.replace("'", "").replace('"', '')
        self.alias = self.name
        self.printed_name = self.name
        #These are the different parts of of a subworkflow -> work corresponds to the main 
        self.take = []
        self.take_code = ""
        self.takes_channels = []
        self.work = None
        self.main_code = ""
        self.emit = []
        self.emit_code = ""
        self.call = []

        #These are probably to remove
        self.initialised = False
        self.later_emits = []
        self.number_times_called = 0

        self.called_by = []#List of calls
        self.number_times_copied = 0

        self.elements_in_order = True

        #This for when i analyse trough the language server
        self.elements_in_workflow = []

    def copy(self):
        sub = copy.copy(self)
        sub.alias = self.name
        sub.printed_name = self.printed_name 
        sub.take = []
        sub.takes_channels = []
        sub.work = None
        sub.emit = []
        sub.call = []
        sub.initialised = False
        sub.later_emits = []
        sub.number_times_called = 0
        sub.called_by = []
        num = self.number_times_copied
        self.number_times_copied+=1
        return sub, num
    
    def add_elements_to_workflow(self, ele):
        self.elements_in_workflow.append(ele)

    def get_elements_to_workflow(self):
        return self.elements_in_workflow

    def add_to_calls(self, call):
        self.called_by.append(call)

    def get_call(self):
        if(len(self.called_by)!=1):
            raise Exception("This shouldn't happen")
        return self.called_by[0]
    
    #TODO make sure this is uptodate
    def get_calls_by_name(self, name):            
        tab = []
        for call in self.root.get_calls_same_level():
            #call.initialise()
            for c in call.get_all_calls():
                if(c.first_element_called.get_alias()==name):
                    tab.append(c)
        #Here it is important that BioFlow-Insight is not a Nextflow verificator
        #Here i'm checking the call inside the block
        if(len(tab)==0):
            for call in self.root.get_calls_inside_level():
                #call.initialise()
                for c in call.get_all_calls():
                    if(c.first_element_called.get_alias()==name):
                        tab.append(c)
        return tab
        

    def add_to_emits(self, emit):
        self.later_emits.append(emit)
    
    def get_later_emits(self):
        return self.later_emits

    def get_code_with_alias(self):
        code = self.get_code()
        def replacer(match):
            return match.group(0).replace(match.group(1), self.get_alias())
        return re.sub(r"workflow\s*(\w+)\s*\{", replacer, code)
    
    def get_code_with_alias_and_id(self):
        code = self.get_code()
        def replacer(match):
            return match.group(0).replace(match.group(1), self.get_alias_and_id())
        from .constant import SUBWORKFLOW_HEADER
        return re.sub(SUBWORKFLOW_HEADER, replacer, code)

    def get_code_to_simplify(self):
        return self.get_code_with_alias_and_id()
    
    def simplify_code(self):
        name = self.get_alias()

        code = self.get_code()
        #Renaming the channels defined inside the subworkflow
        executors = {}
        self.root.get_all_executors_in_subworkflow(calls=executors)
        channels_to_rename = []
        for exe in executors:
            if(exe.get_type()=="Operation"):
                for g in exe.gives:
                    channels_to_rename.append(g.get_code())
                #channels_to_rename+=exe.gives
        #for ch in channels_to_rename:
        #    code = replace_group1(code, fr"[^\w]({re.escape(ch.get_code())})[^\w]", f"{ch.get_code()}_{name}")


        code = super().simplify_code()

        #Putting the take, main and emit in that order, if needs be
        if(not self.elements_in_order):
            w = copy.deepcopy(self)
            temp_take, temp_work, temp_emit = w.take, w.work, w.emit
            w.code = Code(code, origin=w, initialise=False)
            w.initialise_parts()
            w.take, w.work, w.emit = temp_take, temp_work, temp_emit
            code = re.sub(r"take *:\s+"+re.escape(w.take_code), "//anker", code)
            code = re.sub(r"main *:\s+"+re.escape(w.main_code), "//anker", code)
            code = re.sub(r"emit *:\s+"+re.escape(w.emit_code), "//anker", code)
            new_body = f"take:\n\t\t{w.take_code}\n\n\tmain:\n\t\t{w.main_code}\n\n\temit:\n\t\t{w.emit_code}\n\n"
            code = code.replace("//anker", new_body, 1)
            code = code.replace("//anker", "")


        for o in self.emit:
            code = code.replace(o.get_code(get_OG = True), o.simplify_code(return_tab = False), 1)

        #Renaming the takes in the subworkflow (only body)
        code_up_to_emit, code_after_emit = code, ""
        for match in re.finditer(constant.EMIT_SUBWORKFLOW, code):
            start, _ = match.span(0)
            code_up_to_emit = code[:start]
            code_after_emit = code[start:]

        for t in self.take:
            if(len(t.get_gives())!=1):
                raise Exception("This shoudn't happen")
            ch = t.get_gives()[0]
            code_up_to_emit = replace_group1(code_up_to_emit, fr"[^\w\.]({re.escape(ch.get_code())})[^\w]", f"{ch.get_code()}_{name}")



        #Renaming the emits so that the name of the subworkflow appears in the param name
        #The renaming of the emits outside the subworkflow is done at the emit level (when we simplify the emit)
        for e in self.emit:
            if(len(e.gives)==1):
                ch = e.gives[0]
                if(ch.get_type()=="Channel"):
                    temp = code_after_emit
                    code_after_emit = replace_group1(code_after_emit, fr"[^\w\.]({re.escape(ch.get_code())})[^\w]", f"{ch.get_code()}_{name}")
                    if(temp==code_after_emit):
                        raise Exception("This shoudn't happen -> code hasn't been replaced")
                elif(ch.get_type()=="Emitted"):
                    #Case it's an emitted -> we don't change anything -> it is already unique (since the ID has been added to the call)
                    None
                else:
                    raise Exception("This shouldn't happen")
            else:
                ch = e.origins[0]
                if(ch.get_type()=="Channel"):
                    temp = code_after_emit
                    code_after_emit = replace_group1(code_after_emit, fr"[^\w\.]({re.escape(ch.get_code())})[^\w]", f"{ch.get_code()}_{name}")
                    code_up_to_emit+=f"\n{ch.get_code()}_{name} = {ch.get_code()}"
                    if(temp==code_after_emit):
                        raise Exception("This shoudn't happen -> code hasn't been replaced")
                elif(ch.get_type()=="Emitted"):
                    #Case it's an emitted -> we don't change anything -> it is already unique (since the ID has been added to the call)
                    None
                else:
                    raise Exception("This shouldn't happen")
        


        #In the emits replacing the 'ch = ....' by 'ch' and adding 'ch = ....' at the end of the body
        to_replace = []
        for match in re.finditer(r"(\w+) *= *.+", code_after_emit):
            old, new = match.group(0), match.group(1)
            to_replace.append((old, new))
        for r in to_replace:
            old, new = r
            code_up_to_emit+=f"\n{old}"
            temp = code_after_emit
            code_after_emit = code_after_emit.replace(old, new)
            if(temp==code_after_emit):
                raise Exception("This shoudn't happen -> code hasn't been replaced")

        ##Renaming the takes in the emits -> if the takes are given as emits
        #for e in self.emit:
        #    channels_take = []
        #    for t in self.take:
        #        channels_take.append(t.get_gives()[0])
        #    re_write_channel = False
        #    for o in e.origins:
        #        if(o in channels_take):
        #            re_write_channel = True
        #    if(re_write_channel):
        #        ch = e.origins[0]
        #        temp = code_after_emit
        #        code_after_emit = replace_group1(code_after_emit, fr"[^\w]({re.escape(ch.get_code())})[^\w]", f"{ch.get_code()}_{name}")
        #        if(temp==code_after_emit):
        #            raise Exception("This shoudn't happen -> code hasn't been replaced")

        code = code_up_to_emit+'\n'+code_after_emit

        #Renaming the channels defined inside the subworkflow
        for ch in channels_to_rename:
            code = replace_group1(code, fr"[^\w\.]({re.escape(ch)})[^\w]", f"{ch}_{name}")
        
        to_replace = []
        for match in re.finditer(r"(\w+) *= *(\w+) *\n", code):
            if(match.group(1)==match.group(2)):
                to_replace.append(match.group(0))
        for r in to_replace:
            code = code.replace(r, "", 1)

        return code


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

    def get_type(self):
        return "Subworkflow"

    def get_name(self):
        return self.name
    
    def get_work(self):
        return self.work.get_code()
    

    #Method which initiliases the different parts of a workflow (take/main/emit)
    def initialise_parts(self):
        code = self.get_code()
        take_multiple, take_pos= False, (0, 0)
        for match in re.finditer(constant.TAKE, code):
            if(take_multiple):
                raise BioFlowInsightError("meis", self, "take", self.get_name())
            take_pos = match.span(0)
            take_multiple = True

        main_multiple, main_pos= False, (0, 0)
        for match in re.finditer(constant.MAIN, code):
            if(main_multiple):
                raise BioFlowInsightError("meis", self, "main", self.get_name())
            main_pos = match.span(0)
            main_multiple = True

        emit_multiple, emit_pos= False, (0, 0)
        for match in re.finditer(constant.EMIT_SUBWORKFLOW, code):
            if(emit_multiple):
                raise BioFlowInsightError("meis", self, "emit", self.get_name())
            emit_pos = match.span(0)
            emit_multiple = True

        #Case everything is there
        if(take_pos!=(0, 0) and main_pos!=(0, 0) and emit_pos!=(0, 0)):
            if(take_pos[0]<main_pos[0] and main_pos[0]<emit_pos[0]):
                self.take = Code(code[take_pos[1]:main_pos[0]].strip(), origin = self, initialise=False)
                self.work = Code(code[main_pos[1]:emit_pos[0]].strip(), origin = self, initialise=False)
                self.emit = Code(code[emit_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
            elif(take_pos[0]<emit_pos[0] and emit_pos[0]<main_pos[0]):
                self.take = Code(code[take_pos[1]:emit_pos[0]].strip(), origin = self, initialise=False)
                self.emit = Code(code[emit_pos[1]:main_pos[0]].strip(), origin = self, initialise=False)
                self.work = Code(code[main_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
                self.elements_in_order = False
            elif(emit_pos[0]<take_pos[0] and take_pos[0]<main_pos[0]):
                self.emit = Code(code[emit_pos[1]:take_pos[0]].strip(), origin = self, initialise=False)
                self.take = Code(code[take_pos[1]:main_pos[0]].strip(), origin = self, initialise=False)
                self.work = Code(code[main_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
                self.elements_in_order = False
            elif(emit_pos[0]<main_pos[0] and main_pos[0]<take_pos[0]):
                self.emit = Code(code[emit_pos[1]:main_pos[0]].strip(), origin = self, initialise=False)
                self.work = Code(code[main_pos[1]:take_pos[0]].strip(), origin = self, initialise=False)
                self.take = Code(code[take_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
                self.elements_in_order = False
            elif(main_pos[0]<take_pos[0] and take_pos[0]<emit_pos[0]):
                self.work = Code(code[main_pos[1]:take_pos[0]].strip(), origin = self, initialise=False)
                self.take = Code(code[take_pos[1]:emit_pos[0]].strip(), origin = self, initialise=False)
                self.emit = Code(code[emit_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
                self.elements_in_order = False
            elif(main_pos[0]<emit_pos[0] and emit_pos[0]<take_pos[0]):
                self.work = Code(code[main_pos[1]:emit_pos[0]].strip(), origin = self, initialise=False)
                self.emit = Code(code[emit_pos[1]:take_pos[0]].strip(), origin = self, initialise=False)
                self.take = Code(code[take_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
                self.elements_in_order = False
            else:
                raise Exception("This shoudn't happen")
        #Case nothing is there
        if(take_pos==(0, 0) and main_pos==(0, 0) and emit_pos==(0, 0)):
            #raise Exception(f"Subworkflow {code} doesn't have anything defined")
            firt_curly  = code.find("{")
            last_curly = code.rfind('}')
            self.work = Code(code[firt_curly+1:last_curly], origin = self, initialise=False)
        #Case there is an input but no output
        if(take_pos!=(0, 0) and main_pos!=(0, 0) and emit_pos==(0, 0)):
            if(take_pos[0]<main_pos[0]):
                self.take = Code(code[take_pos[1]:main_pos[0]].strip(), origin = self, initialise=False)
                self.work = Code(code[main_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
            else:
                main = code[main_pos[1]:take_pos[0]].strip()
                take = code[take_pos[1]:code.rfind('}')].strip()
                self.work = Code(main, origin = self, initialise=False)
                self.take = Code(take, origin = self, initialise=False)
                self.elements_in_order = False
        #Case there is no input but an output
        if(take_pos==(0, 0) and main_pos!=(0, 0) and emit_pos!=(0, 0)):
            if(main_pos[0]<emit_pos[0]):
                self.work = Code(code[main_pos[1]:emit_pos[0]].strip(), origin = self, initialise=False)
                self.emit = Code(code[emit_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
            else:
                emit = code[emit_pos[1]:main_pos[0]].strip()
                main = code[main_pos[1]:code.rfind('}')].strip()
                self.work = Code(main, origin = self, initialise=False)
                self.emit = Code(emit, origin = self, initialise=False)
                self.elements_in_order = False
        #Case there is a main but no input and no output
        if(take_pos==(0, 0) and main_pos!=(0, 0) and emit_pos==(0, 0)):
            self.work = Code(code[main_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
        if( main_pos==(0, 0) and (take_pos!=(0, 0) or emit_pos!=(0, 0))):
            if(take_pos!=(0, 0) and emit_pos!=(0, 0)):
                raise Exception("TODO")
            elif(take_pos!=(0, 0) and emit_pos==(0, 0)):
                raise Exception("TODO")
            elif(take_pos==(0, 0) and emit_pos!=(0, 0)):
                self.emit = Code(code[emit_pos[1]:code.rfind('}')].strip(), origin = self, initialise=False)
                firt_curly  = code.find("{")
                self.work = Code(code[firt_curly+1:emit_pos[0]].strip(), origin = self, initialise=False)
                self.elements_in_order
            else:
                raise Exception("Not possible!")
        if(self.take!=[]):
            self.take_code = self.take.get_code()
        if(self.work!=None):
            self.main_code = self.work.get_code()
        if(self.emit!=[]):
            self.emit_code = self.emit.get_code()
    
    def get_channel_from_name_takes(self, name):
        for c in self.takes_channels:
            if(name == c.get_name()):
                return c
        return None

    def initialise_takes(self):
        if(self.take!=[]):
            code = remove_jumps_inbetween_parentheses(self.take.get_code()).split('\n')
            tab = []
            for i in range(len(code)):
                code[i] = code[i].strip()
                if(code[i]!=''):
                    channel = self.get_channel_from_name_takes(code[i])
                    #channel = self.root.get_channel_from_name(code[i])
                    #In the case the channel doesn't exist
                    if(channel==None):
                        from .operation import Operation
                        ope = Operation(f"t: {code[i]}", self)
                        ope.set_as_artificial()
                        from .channel import Channel
                        channel = Channel(code[i], self)
                        ope.add_element_gives(channel)
                        channel.add_source(ope)
                        #ope.initialise_from_subworkflow_take()
                    else:
                        raise BioFlowInsightError("caease", self, code[i], "")
                    tab.append(ope)
                    for channel in ope.get_gives():
                        self.takes_channels.append(channel)
            self.take = tab




    def initialise_emit(self):
        from .operation import Operation
        if(self.emit!=[]):
            code = remove_jumps_inbetween_parentheses(self.emit.get_code()).split('\n')
            tab = []
            for i in range(len(code)):
                code[i] = code[i].strip()
                if(code[i]!=""):
                    element = code[i]
                    left, right = "", ""
                    for match in re.finditer(r"(\w+) *= *(\w+)", element):
                        if(match.group(1)==match.group(2)):
                            element = match.group(1)
                            break

        
                    #V1
                    channels = self.root.get_channels_from_name_same_level(element)
                    if(channels==[]):
                        channels = self.root.get_channels_from_name_inside_level(element)
                    if(channels==[]):
                        channels = self.root.get_channels_from_name_other_blocks_on_same_level(element)

                    #V2
                    #channels = self.root.get_channels_from_name_same_level(code[i])+self.root.get_channels_from_name_inside_level(code[i])+self.root.get_channels_from_name_other_blocks_on_same_level(code[i])
                    
                    
                    if(channels!=[]):
                        ope = Operation(code=f"e: {code[i]}", origin=self)
                        ope.set_as_artificial()
                        for channel in channels:
                            ope.add_element_origins(channel)
                            channel.add_sink(ope)
                        tab.append(ope)
                        
                    else:
                        #raise Exception(f"I don't know how to handle '{code[i]}'")
                        #Case it's an operation 
                        operation = Operation(code[i], self)
                        operation.initialise()
                        operation.change_code(f"e: {code[i]}")
                        operation.set_as_artificial()
                        tab.append(operation)
                        #operation.add_gives(channel)
                        #for gives in operation.get_gives():
                        #    #TODO -> check not add origin too!
                        #    gives.add_sink(operation)
                        #tab.append(operation)
                        ##self.add_operation(operation)
                        ##self.executors.append(operation)
            self.emit = tab
            
            

    

    def get_emit(self):
        return self.emit
    
    def get_nb_emit(self):
        return len(self.emit)

    def get_takes(self):
        return self.take
    
    def get_nb_takes(self):
        return len(self.take)
    
    def get_nb_inputs(self):
        return self.get_nb_takes()
            

    def initialise(self):
        if(not self.initialised):
            self.initialised = True
            self.initialise_parts()
            self.initialise_takes()
            self.modules_defined = self.nextflow_file.get_modules_defined()
            #Check that includes are not defined in the main or subworkflows
            self.check_includes()
            self.root = Root(code=self.get_work(), origin=self, modules_defined=self.modules_defined, subworkflow_inputs = self.takes_channels)
            self.root.initialise()
            self.initialise_emit()
            

    def get_all_executors_in_subworkflow(self):
        dico = {}
        self.root.get_all_executors_in_subworkflow(calls = dico)
        for operation in self.emit:
            dico[operation] = ""
        return list(dico.keys())

    def get_structure(self, dico):
        super().get_structure(dico)

        for ope in self.get_takes():
            #ope.set_operation_type("Branch")
            ope.get_structure(dico)
        
        for ope in self.get_emit():
            #ope.set_operation_type("Branch")
            ope.get_structure(dico)

  
    def add_2_rocrate(self, dico, parent_key):
        sub_key = self.get_rocrate_key(dico)
        dico_sub = get_dico_from_tab_from_id(dico, sub_key)
        if(dico_sub==None):
            dico_sub = {}
            dico_sub["@id"] = sub_key
            dico_sub["name"] = f"Subworkflow#{self.get_alias()}"
            dico_sub["@type"] = ["SoftwareSourceCode", "ComputationalWorkflow"]
            #TODO -> check if this remains true
            #dico_main["conformsTo"] = {"@id": "https://bioschemas.org/profiles/ComputationalWorkflow/0.5-DRAFT-2020_07_21"}
            #dico_main["dct:conformsTo"]= "https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE/"
            
            
            #ADD INPUTS
            dico_sub["input"] = []
            for input in self.get_takes():
                if(type(input)==str):
                    name_input = input
                else:
                    name_input = input.get_code(get_OG = True)
                dico_input = get_dico_from_tab_from_id(dico, name_input)
                if(dico_input==None):
                    dico_input = {"@id":f"#{name_input}", "name": name_input, "@type": "FormalParameter"}
                    dico["@graph"].append(dico_input)
                dico_sub["input"].append({"@id":dico_input["@id"]})
            #ADD OUTPUTS
            dico_sub["output"] = []
            for output in self.get_emit():
                if(type(output)==str):
                    name_output = output
                else:
                    name_output = output.get_code(get_OG = True)
                dico_output = get_dico_from_tab_from_id(dico, name_output)
                if(dico_output==None):
                    dico_output = {"@id":f"#{name_output}", "name": name_output, "@type": "FormalParameter"}
                    dico["@graph"].append(dico_output)
                dico_sub["output"].append({"@id":dico_output["@id"]})


            dico_sub["isPartOf"] = [{"@id": parent_key}]
            dico_sub["hasPart"] = []


            called = []
            for call in self.root.get_all_calls_from_root():
                called.append(call.get_first_element_called())

            for c in called:
                if(c==self):
                    raise Exception("This shoudn't happen!")
                c.add_2_rocrate(dico, sub_key)
                dico_sub["hasPart"].append({"@id":c.get_rocrate_key(dico)})

            dico["@graph"].append(dico_sub)
        else:
            if(not check_if_element_in_tab_rocrate(dico_sub["isPartOf"], parent_key)):
                dico_sub["isPartOf"].append({"@id":parent_key})

        self.get_nextflow_file().add_to_has_part(dico, sub_key)
    
    def get_DBfile_description(self, workflow_name):
        text = ""
        text+= f"# {self.get_alias()} Subworkflow"
        text+=f"""\nsf:subworkflow{self.get_alias()} rdf:type sf:Subworkflow ;
\tp-plan:isSubPlanOf sf:{workflow_name}"""
        
        processes_called, subworkflows_called = [], []
        all_calls = self.get_all_calls_in_subworkflow()
        for c in all_calls:
            if(c.get_first_element_called().get_type()=="Process"):
                processes_called.append(c.get_first_element_called())
            if(c.get_first_element_called().get_type()=="Subworkflow"):
                subworkflows_called.append(c.get_first_element_called())
        
        for i in range(len(processes_called)):
            processes_called[i] = f'sf:step{processes_called[i].get_alias()}'
        if(len(processes_called)!=0):
            text+= f" ;\n\tschema:step {', '.join(processes_called)}"
        
        input_params = []
        for input in self.get_takes():
            input_params.append(f"sf:{input.get_code(get_OG = True)}")
        if(len(input_params)!=0):
            text+= f" ;\n\tsf:inputVariable {', '.join(input_params)}"

        output_params = []
        for output in self.get_emit():
            val = output.get_code(get_OG = True)
            val = val.replace(",", "\\,")
            val = val.replace("'", "\\'")
            val = val.replace('"', '\\"')
            output_params.append(f"sf:{val}")
        if(len(output_params)!=0):
            text+= f" ;\n\tsf:outputVariable {', '.join(output_params)}"
        text+=" ."

        for input in input_params:
            text+=f"\n\n{input} rdf:type sf:Variable ."

        for output in output_params:
            text+=f"\n\n{output} rdf:type sf:Variable ."

        for sub in subworkflows_called:
            text+=f'\n\n{sub.get_DBfile_description(f"subworkflow{self.get_alias()}")}'
            
        return text

        