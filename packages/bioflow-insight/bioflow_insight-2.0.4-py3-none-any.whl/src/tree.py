class Tree:
    def __init__(self, value, condition, children):
        self.value = value
        self.condition = condition
        self.children = children
        self.minimal = False
        self.compared_minimal = []
        self.compared_to_all_siblings = False


    def checked_if_already_compared_minimal(self, couple):
        if(couple in self.compared_minimal):
            return True
        return False
    
    def add_compared_minimal(self, couple):
        self.compared_minimal.append(couple)

    def set_compared_to_all_siblings(self, val):
        self.compared_to_all_siblings = val
    

    def set_minimal(self, val):
        self.minimal = val
    
    def get_minimal(self):
        return self.minimal

    def is_this_full_tree(self):
        return self.value==None and self.condition==None
    
    def update_value(self, val):
        self.value = val
    
    def set_condition(self, val):
        self.condition = val
    

    def create_copy(self):
        t = Tree(value=self.value, condition=self.condition, children=[])
        if(not self.is_a_leaf()):
            for c in self.children:
                t.children.append(c.create_copy())
        return t
            
    
    def is_a_leaf(self):
        return self.children==[] 
    
    #This method returns all the children in the immediate depth 
    #And if a child is a tree it returns all the recursive children of that tree
    def get_shallow_children(self):
        tab = []
        for child in self.children:
            leafs = child.get_all_leafs_in_tree(val={})
            if(leafs!=[]):
                tab.append(leafs)
        return tab
    
    def add_child(self, child):
        self.children.append(child)

    def add_children(self, cluster):
        for c in cluster:
            temp = Tree(value=c, condition=None, children = [])
            self.add_child(temp)

    def get_all_leafs_in_tree(self, val):
        if(self.is_a_leaf()):#and type(self.value)!=str):
            val[self.value] = ""
        for child in self.children:
            child.get_all_leafs_in_tree(val)
        return list(val.keys())
    
    #Transfers the tree's children to self
    def transfer_children(self, tree):
        for i in range(len(tree.children)):
            self.children.append(tree.children[i])

    def get_condition(self):
        return self.condition
    
    def get_children(self):
        return self.children
    
    def get_children_which_are_not_leaves_which_havent_been_compared_to_all_siblings(self):
        tab = []
        for c in self.children:
            if(not c.is_a_leaf() and not c.compared_to_all_siblings):
                tab.append(c)
        return tab
    
    def get_condition_in_commun(self, tree):
        return ""


    def get_conditions_on_all_leaves(self):
        conditions_on_all_leaves = []
        if(self.condition!=None):
            conditions_on_all_leaves.append(self.condition)
            if(len(self.children)==1):
                conditions_on_all_leaves+= self.children[0].get_conditions_on_all_leaves()
        return conditions_on_all_leaves

    def get_conditions_in_commun(self, other_tree):
        conditions_on_all_leaves_tree1 = self.get_conditions_on_all_leaves()
        conditions_on_all_leaves_tree2 = other_tree.get_conditions_on_all_leaves() 
        conditions_in_commun = []
        for i in range(len(conditions_on_all_leaves_tree1)):
            for y in range(len(conditions_on_all_leaves_tree2)):
                cond1, cond2 = conditions_on_all_leaves_tree1[i], conditions_on_all_leaves_tree2[y]
                if(cond1.get_value()==cond2.get_value()):
                    conditions_in_commun.append((cond1, cond2))
        return conditions_in_commun
    
    
    def get_node_with_condition(self, condition):
        if(self.condition==condition):
            return self
        else:
            if(len(self.children)!=1):
                raise Exception("this shoudn't happen")
            return self.children[0].get_node_with_condition(condition)

    #This methods brings the condition to the top of the tree 
    #Becoming the first internal node
    def bring_condition_to_the_top(self, condition):
        if(self.condition!=condition):
            conditions_on_all_leaves = self.get_conditions_on_all_leaves()
            
            if(condition in conditions_on_all_leaves):
                children_are_all_leaves = True
                for c in self.children:
                    if(not c.is_a_leaf()):
                        children_are_all_leaves = False
                if(len(self.children)!=1 and not children_are_all_leaves):
                    self.show_tree()
                    raise Exception("this shoudn't happen")
                node_with_condition = self.get_node_with_condition(condition)
                temp_condition = self.get_condition()
                self.set_condition(condition)
                node_with_condition.set_condition(temp_condition)
            else:
                raise Exception("this shoudn't happen")




    def get_value_condition(self):
        try:
            return self.condition
        except:
            return None



    def fill_tree(self, tree, parent_id):
        tree.create_node(str(get_val(self.value)),  id(self), parent=parent_id)
        for child in self.children:
            child.fill_tree(tree, id(self))
        
    def merge_2_children_together(self, child1, child2):

        new_child = Tree(value=child1.get_condition().get_value(), condition = None, children=[])
        new_child.transfer_children(child2)
        new_child.transfer_children(child1)
        
        self.children.remove(child1)
        self.children.remove(child2)
        self.children.append(new_child)


    def get_number_of_groups(self, num):
        for child in self.children:
            if(not child.is_a_leaf()):
                num = child.get_number_of_groups(num+1)
        return num
    
    def get_number_of_unique_groups(self, num):
        if(self.value!='root'):
            if(len(self.children)==1 and not self.children[0].is_a_leaf()):
                None
            else:
                num+=1
        for child in self.children:
            if(not child.is_a_leaf()):
                num = child.get_number_of_unique_groups(num)
        return num
    
    def get_size_of_groups(self, tab):
        for child in self.children:
            if(not child.is_a_leaf()):
                tab.append(len(child.children))
                tab = child.get_size_of_groups(tab)
        return tab
    
    def get_groups(self, dico):
        for child in self.children:
            if(not child.is_a_leaf()):
                dico[child] = child.get_all_leafs_in_tree({})
                child.get_groups(dico)
        return dico
    
    #This is the percentage of nodes which are in a group
    def get_coverage(self):
        if(self.children!=[]):
            nb_swallow_leafs = 0
            for child in self.children:
                if(child.is_a_leaf()):
                    nb_swallow_leafs+=1
            nb_leafs = len(self.get_all_leafs_in_tree({}))
            return (nb_leafs-nb_swallow_leafs)/nb_leafs*100
        return 0
    
    #This is the percentage of processes which are in a group
    def get_coverage_processes(self):
        if(self.children!=[]):
            nb_swallow_leafs = 0
            for child in self.children:
                if(child.is_a_leaf() and child.value.get_type()=="Process"):
                    nb_swallow_leafs+=1
            if(nb_swallow_leafs==0):
                return 0
            total = 0
            for leaf in self.get_all_leafs_in_tree({}):
                if(leaf.get_type()=="Process"):
                    total+=1
            return (total-nb_swallow_leafs)/total*100
        return 0

    def show_tree(self):
        from treelib import Node, Tree
        tree = Tree()
        tree.create_node("Root", "root")
        for child in self.children:
            child.fill_tree(tree, "root")
        tree.show()

    def remove_clouds(self):
        to_remove, to_add= [], []
        for child in self.children:
            if(child.is_a_leaf() and child.value.get_type()=="Cloud"):
                operations = child.value.get_operations()
                for o in operations:
                    to_add.append(Tree(value=o, condition=child.condition, children=[]))
                to_remove.append(child)
            else:
                child.remove_clouds()
        for r in to_remove:
            self.children.remove(r)
        self.children+=to_add
            
                


def get_val(node):
    try:
        if(node.get_type()=="Process"):
            return node.get_name()
        elif(node.get_type()=="Operation"):
            return node.get_code(get_OG = True)
        elif(node.get_type()=="Cloud"):
            return "Cloud"
    except:
        return node
