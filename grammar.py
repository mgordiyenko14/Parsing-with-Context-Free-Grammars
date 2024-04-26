"""
COMS W4705 - Natural Language Processing - Fall 2023
Homework 2 - Parsing with Context Free Grammars 
Daniel Bauer
"""

import sys
from collections import defaultdict
from math import fsum, isclose

class Pcfg(object): 
    """
    Represent a probabilistic context free grammar. 
    """

    def __init__(self, grammar_file): 
        self.rhs_to_rules = defaultdict(list)
        self.lhs_to_rules = defaultdict(list)
        self.startsymbol = None 
        self.read_rules(grammar_file)      
 
    def read_rules(self,grammar_file):
        
        for line in grammar_file: 
            line = line.strip()
            if line and not line.startswith("#"):
                if "->" in line: 
                    rule = self.parse_rule(line.strip())
                    lhs, rhs, prob = rule
                    self.rhs_to_rules[rhs].append(rule)
                    self.lhs_to_rules[lhs].append(rule)
                else: 
                    startsymbol, prob = line.rsplit(";")
                    self.startsymbol = startsymbol.strip()
                    
     
    def parse_rule(self,rule_s):
        lhs, other = rule_s.split("->")
        lhs = lhs.strip()
        rhs_s, prob_s = other.rsplit(";",1) 
        prob = float(prob_s)
        rhs = tuple(rhs_s.strip().split())
        return (lhs, rhs, prob)

    def verify_grammar(self):
        """
        Return True if the grammar is a valid PCFG in CNF.
        Otherwise return False. 
        """
        # TODO, Part 1
        # CNF: only one terminal symbol or 2 non-terminal symbols on the right side 
        # iterates through every rule

        nonterminals = set(self.lhs_to_rules.keys())
        
        for rhs in self.rhs_to_rules.keys():
            if len(rhs)==1:
                if rhs in nonterminals:
                    print("NT -> NT not CNF")
                    return False
            elif len(rhs)==2:
                if rhs[0] not in nonterminals or rhs[1] not in nonterminals:
                    print("NT -> term NT or NT -> NT term")
                    return False
            elif len(rhs)>2:
                print("more than 2 rhs elemnts")
                return False
        
        for lhs in nonterminals:
            sum = 0
            for rhs in range(len(self.lhs_to_rules[lhs])):
                sum += self.lhs_to_rules[lhs][rhs][2] #accessing the 3rd element of the tuple
            if (not isclose(1.0, sum)):
                print("probs don't sum to 1")
                return False
        
        print("valid")
        return True 


if __name__ == "__main__":
    with open('atis3.pcfg','r') as grammar_file:
        grammar = Pcfg(grammar_file)
    result = grammar.verify_grammar()
    if result ==True:
        print("this grammar is in valid CNF form")
    elif result == False:
        print("this grammar is not in valid CNF form")
