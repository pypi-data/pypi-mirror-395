import os
import unittest
from src.outils import extract_conditions

class TestExtractConditions(unittest.TestCase):

    #TODO -> finish this

    def test_1(self):
        test = """
        if ((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)) {error "ERROR: please specify methylation context for analysis"}
else if ((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == false)) {context = "--noCpG --CHG "}
else if ((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == true)) {context = "--noCpG --CHH "}
else if ((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == false)) {context = "--noCpG --CHH --CHG "}
else if ((params.noCpG == false) && (params.noCHH == true) && (params.noCHG == true)) {context = " "}
else if ((params.noCpG == false) && (params.noCHH == true) && (params.noCHG == false)) {context = "--CHG "}
else if ((params.noCpG == false) && (params.noCHH == false) && (params.noCHG == true)) {context = "--CHH "}
else {context = "--CHH --CHG "}
"""
        dico = extract_conditions(test)
        results = {'(params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)$$__$$0': (90, 152), '!((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)) && (params.noCpG == true) && (params.noCHH == true) && (params.noCHG == false)$$__$$1': (241, 267), '!((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == false)) && (params.noCpG == true) && (params.noCHH == false) && (params.noCHG == true)$$__$$2': (356, 382), '!((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == false)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == true)) && (params.noCpG == true) && (params.noCHH == false) && (params.noCHG == false)$$__$$3': (472, 504), '!((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == false)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == false)) && (params.noCpG == false) && (params.noCHH == true) && (params.noCHG == true)$$__$$4': (593, 606), '!((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == false)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == false)) && !((params.noCpG == false) && (params.noCHH == true) && (params.noCHG == true)) && (params.noCpG == false) && (params.noCHH == true) && (params.noCHG == false)$$__$$5': (696, 714), '!((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == false)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == false)) && !((params.noCpG == false) && (params.noCHH == true) && (params.noCHG == true)) && !((params.noCpG == false) && (params.noCHH == true) && (params.noCHG == false)) && (params.noCpG == false) && (params.noCHH == false) && (params.noCHG == true)$$__$$6': (804, 822), '!((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == true) && (params.noCHG == false)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == true)) && !((params.noCpG == true) && (params.noCHH == false) && (params.noCHG == false)) && !((params.noCpG == false) && (params.noCHH == true) && (params.noCHG == true)) && !((params.noCpG == false) && (params.noCHH == true) && (params.noCHG == false)) && !((params.noCpG == false) && (params.noCHH == false) && (params.noCHG == true))$$__$$7': (830, 854)}
        #print(dico)
        #for condition in dico:
        #    print(condition)
        #    start, end = dico[condition]
        #    print(test[start:end])
        #    print()
        #print()
        self.assertEqual(results, dico)


