
import re 
import os
import copy

from . import constant

from .code_ import Code
from .nextflow_building_blocks import Nextflow_Building_Blocks
from .bioflowinsighterror import BioFlowInsightError





#Remove ' and " from a given string
def clean_string(txt):
    txt = txt.replace("'", "")
    txt = txt.replace('"', "")
    return txt

class Include(Nextflow_Building_Blocks):
    def __init__(self, code, file, importing, nextflow_file):
        self.nextflow_file_origin = nextflow_file
        self.importing = importing
        self.code = Code(code = code, origin = self, initialise=False)
        self.nextflow_file = None
        self.define_file(file)
        self.defines = {}
        #self.initialise()

    def get_string_line(self, bit_of_code):
        return self.nextflow_file_origin.get_string_line(bit_of_code)
    
    def get_origin(self):
        return self.nextflow_file_origin

    def get_file_address(self, short = False):
        return self.nextflow_file_origin.get_file_address(short = short)

    def get_duplicate_status(self):
        return self.nextflow_file_origin.get_duplicate_status()

    def get_nextflow_file(self):
        return self.nextflow_file


    #def get_list_name_includes(self):
    #    if(self.get_duplicate_status()):
    #        names = []
    #        for ele in self.defines:
    #            names.append(ele.get_alias())
    #        return names
    #    else:
    #        return list(self.aliases.keys())
        
    def define_file(self, file):
        from .nextflow_file import Nextflow_File
        address = clean_string(file)
        root = self.nextflow_file_origin.get_file_address()
        root = '/'.join(str(root).split('/')[:-1])
        found_file = False

        if(os.path.isfile(address)):
            found_file = True
        
        if(not found_file):
            if(address[-1]in [';']):
                address = address[:-1]

            if(address.split('/')[0] in ["$projectDir", "${projectDir}", "${baseDir}", "$baseDir"]):
                address = '/'.join(address.split('/')[1:])
                #root = self.get_root_directory()
                root = self.nextflow_file_origin.get_root_directory()
            address = root+'/'+address
            if(os.path.isfile(address)):
                found_file = True
        
        if(not found_file):
            if(address[-3:]!=".nf"):
                address+=".nf"
            if(os.path.isfile(address)):
                found_file = True

        if(not found_file and os.path.isfile(address[:-3]+"/main.nf")):
            self.nextflow_file = Nextflow_File(address[:-3]+"/main.nf", workflow = self.nextflow_file_origin.get_workflow(), first_file=False)
        
        #TODO -> check if the nextflow_file is defined somewhere else? 
        #In the cas the nextflow file is imported multiple times

        else:
            if(os.path.isfile(address)):
                self.nextflow_file = Nextflow_File(address, workflow = self.nextflow_file_origin.get_workflow(), first_file=False)
            else:
                wf_dir = self.nextflow_file_origin.get_workflow().get_workflow_directory()
                address = str(os.path.normpath(address))[len(wf_dir)+1:]
                raise BioFlowInsightError("fdne", self, self.get_string_line(self.get_code()), address)

        
        #If not duplicate -> we need to see if there is another include which has already defined the file
        #TODO -> if you wanna generalise this to all include (inbetween files -> you just need to update get_include() )
        if(not self.get_duplicate_status()):
            other_includes = self.nextflow_file_origin.get_includes()
            for other in other_includes:
                if(self.nextflow_file.get_file_address()==other.nextflow_file.get_file_address()):
                    self.nextflow_file = other.nextflow_file



    def initialise(self):
        self.nextflow_file.initialise()

        for include in self.importing:
            include = include.strip()
            found = False
            if(include!=''):
                if(re.fullmatch(constant.WORD, include)):
                    self.defines[include] = self.nextflow_file.get_element_from_name(include)
                    found = True
                else:
                    pattern_as = constant.INCLUDE_AS
                    for match in re.finditer(pattern_as, include):
                        found = True
                        #if(self.get_duplicate_status()):
                        thing_as, num = self.nextflow_file.get_element_from_name(match.group(1)).copy()
                        thing_as.set_alias(match.group(3))
                        self.defines[match.group(3)] = thing_as
                        #else:
                        #    self.defines[match.group(3)] = self.nextflow_file.get_element_from_name(match.group(1))
                if('-' in include):
                    raise BioFlowInsightError("dinoens", self, include)
                if(not found):
                    raise BioFlowInsightError("utii", self, include)


    
    


