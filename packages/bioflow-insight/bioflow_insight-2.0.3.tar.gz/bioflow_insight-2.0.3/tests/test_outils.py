import os
import unittest
from src.outils import *

class TestOutils(unittest.TestCase):

    #TODO -> finish this

    def test_get_next_element_caracter(self):
        test = """This is a test\n!"""
        val, index = get_next_element_caracter(test, 3)
        self.assertEqual(val, 'i')
        self.assertEqual(index, 5)
        val, index = get_next_element_caracter(test, 13)
        self.assertEqual(val, '!')
        self.assertEqual(index, 15)
        val, index = get_next_element_caracter(test, 15)
        self.assertEqual(val, -1)
        self.assertEqual(index, -1)
    
    def test_get_before_element_caracter(self):
        test = """This is a test\n!"""
        val, index = get_before_element_caracter(test, 0)
        self.assertEqual(val, -1)
        self.assertEqual(index, -1)
        val, index = get_before_element_caracter(test, 5)
        self.assertEqual(val, 's')
        self.assertEqual(index, 3)
        val, index = get_before_element_caracter(test, 15)
        self.assertEqual(val, 't')
        self.assertEqual(index, 13)

    def test_remove_comments(self):
        code_with_comments = ''
        with open("tests/ressources/outils/remove_comments_with.nf", 'r') as f:
            code_with_comments = f.read()
    
        with open("tests/ressources/outils/remove_comments_wo.nf", 'r') as f:
            code_wo_comments = f.read()

        produced = remove_comments(code_with_comments)
        with open(candidate := "tests/ressources/outils/remove_comments_wo.candidate.nf", 'w') as f:
            f.write(produced)

        self.assertEqual(produced.strip(), code_wo_comments.strip())
        os.unlink(candidate)
