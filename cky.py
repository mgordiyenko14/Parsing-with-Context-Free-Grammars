"""
COMS W4705 - Natural Language Processing - Fall 2023
Homework 2 - Parsing with Probabilistic Context Free Grammars 
Daniel Bauer
"""
import math
import sys
from collections import defaultdict
import itertools
from grammar import Pcfg

### Use the following two functions to check the format of your data structures in part 3 ###
def check_table_format(table):
    """
    Return true if the backpointer table object is formatted correctly.
    Otherwise return False and print an error.  
    """
    if not isinstance(table, dict): 
        sys.stderr.write("Backpointer table is not a dict.\n")
        return False
    for split in table: 
        if not isinstance(split, tuple) and len(split) ==2 and \
          isinstance(split[0], int)  and isinstance(split[1], int):
            sys.stderr.write("Keys of the backpointer table must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write("Value of backpointer table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str): 
                sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            bps = table[split][nt]
            if isinstance(bps, str): # Leaf nodes may be strings
                continue 
            if not isinstance(bps, tuple):
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Incorrect type: {}\n".format(bps))
                return False
            if len(bps) != 2:
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Found more than two backpointers: {}\n".format(bps))
                return False
            for bp in bps: 
                if not isinstance(bp, tuple) or len(bp)!=3:
                    sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has length != 3.\n".format(bp))
                    return False
                if not (isinstance(bp[0], str) and isinstance(bp[1], int) and isinstance(bp[2], int)):
                    print(bp)
                    sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has incorrect type.\n".format(bp))
                    return False
    return True

def check_probs_format(table):
    """
    Return true if the probability table object is formatted correctly.
    Otherwise return False and print an error.  
    """
    if not isinstance(table, dict): 
        sys.stderr.write("Probability table is not a dict.\n")
        return False
    for split in table: 
        if not isinstance(split, tuple) and len(split) ==2 and isinstance(split[0], int) and isinstance(split[1], int):
            sys.stderr.write("Keys of the probability must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write("Value of probability table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str): 
                sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            prob = table[split][nt]
            if not isinstance(prob, float):
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a float.{}\n".format(prob))
                return False
            if prob > 0:
                sys.stderr.write("Log probability may not be > 0.  {}\n".format(prob))
                return False
    return True



class CkyParser(object):
    """
    A CKY parser.
    """

    def __init__(self, grammar): 
        """
        Initialize a new parser instance from a grammar. 
        """
        self.grammar = grammar

    def is_in_language(self,tokens):
        """
        Membership checking. Parse the input tokens and return True if 
        the sentence is in the language described by the grammar. Otherwise
        return False
        """
        # TODO, part 2
        # table = defaultdict(tuple)
        n = len(tokens)
        pi = defaultdict(tuple)

        #init diagonal
        for i in range(0, n):
            terminal_tup = tuple(tokens[i].split())
            NT_list = []
            for lhs in self.grammar.rhs_to_rules[terminal_tup]:
                # print("here" + lhs[0])
                NT_list.append(lhs[0])
            # print(NT_list)
            pi[(i,i+1)] = NT_list
        # print(pi)
        for length in range(2, n+1):
            # print('len', length, n-length)
            for i in range(0, n-length+1):
                # LHS_list =[]
                # print('i', i)
                j = i+length
                pi[i,j]=[]
                # print('j', j)
                for k in range(i+1, j):
                    # print('k',k)
                    # print(length,i,j,k)
                    B = pi[(i,k)]
                    C = pi[(k,j)]
                    # print("B, C ", B, C)
                    LHS_list =[]
                    for element_b in B:
                        for element_c in C:
                            rhs_curr = tuple([element_b, element_c])
                            # print(rhs_curr)
                            if self.grammar.rhs_to_rules[rhs_curr]:
                                for lhs in self.grammar.rhs_to_rules[rhs_curr]:
                                    if (lhs[0] not in pi[(i,j)]):
                                        pi[(i, j)].append(lhs[0])
                    # print(i,j,LHS_list)
                    # pi[(i, j)] = LHS_list
        # print(pi)
        # return False 
        if self.grammar.startsymbol in pi[(0,n)]:
            return True
        return False
       
    def parse_with_backpointers(self, tokens):
        """
        Parse the input tokens and return a parse table and a probability table.
        """
        # TODO, part 3
        table= defaultdict(tuple)
        #table -> span: dict
        probs = {}
        n = len(tokens)
        # pi = defaultdict(tuple)

        #init diagonal
        for i in range(0, n):
            terminal_tup = tuple(tokens[i].split())
            NT_list = {}
            probs_list = {}
            for lhs in self.grammar.rhs_to_rules[terminal_tup]:
                # print("here" + lhs[0])
                NT_list[lhs[0]] = tokens[i]
                probs_list[lhs[0]] = math.log2(lhs[2])
            # print(NT_list)
            table[(i,i+1)] = NT_list
            probs[(i,i+1)] = probs_list
        # print(table[(0,1)]['FLIGHTS'])
        # print(probs[(0,1)]['FLIGHTS'])
        # print(table)
        for length in range(2, n+1):
            # print('len', length, n-length)
            for i in range(0, n-length+1):
                j = i+length
                table[i,j]={}
                probs[i,j] = {}
                for k in range(i+1, j):
                    B = table[(i,k)]
                    C = table[(k,j)]
                    for element_b in B:
                        for element_c in C:
                            rhs_curr = tuple([element_b, element_c]) # found rhs

                            if self.grammar.rhs_to_rules[rhs_curr]: # if such rule exists
                                for lhs in self.grammar.rhs_to_rules[rhs_curr]: # we look at every LHS outcome of this rule, LHS = M
                                    new_prob = math.log2(lhs[2]) + probs[(i,k)][element_b] + probs[(k,j)][element_c] #calculate the probability of the parse tree with the current M

                                    # print("new_prob ", new_prob)
                                    if (lhs[0] not in table[(i,j)]): # if lhs was not seen, just add the prob
                                        table[(i, j)][lhs[0]] = ((element_b, i,k),(element_c,k,j))
                                        probs[(i,j)][lhs[0]] = new_prob
                                    else: # if the lhs was seen
                                        if (probs[(i,j)][lhs[0]]) < (new_prob): # add the highst probability tree 
                                            table[(i, j)][lhs[0]] = ((element_b, i,k),(element_c,k,j))
                                            probs[(i,j)][lhs[0]] = new_prob
        # print(table[(0,3)]['NP'])
        # print(probs[(0,3)]['NP'])
        # probs = {}
        return table, probs


def get_tree(chart, i,j,nt): 
    """
    Return the parse-tree rooted in non-terminal nt and covering span i,j.
    """
    # TODO: Part 4
    if type(chart[(i, j)][nt]) == str:
        return (nt, chart[(i, j)][nt])
    
    tree_left = chart[(i,j)][nt][0]
    tree_right = chart[(i,j)][nt][1]
    return(nt, (get_tree(chart, tree_left[1], tree_left[2], tree_left[0])), 
    (get_tree(chart, tree_right[1], tree_right[2], tree_right[0])))
 
       
if __name__ == "__main__":
    
    with open('atis3.pcfg','r') as grammar_file: 
        grammar = Pcfg(grammar_file) 
        parser = CkyParser(grammar)
        toks =['flights', 'from','miami', 'to', 'cleveland','.'] 
        # print(parser.is_in_language(toks))
        # parser.parse_with_backpointers(toks)
        table,probs = parser.parse_with_backpointers(toks)
        assert check_table_format(table)
        assert check_probs_format(probs)
        # print(get_tree(table, 0, len(toks), grammar.startsymbol))
        
