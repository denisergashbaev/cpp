from copy import deepcopy
import dimacs_reader
from dpll.formula import Clause


def recurse(original_formula):
    """
    :type original_formula:dpll.formula.Formula
    """
    formula = deepcopy(original_formula)
    unit_clauses = formula.get_unit_clauses()
    if unit_clauses:
        """:type : dpll.formula.Formula"""
        formula.remove_unit_clause(unit_clauses[0])
    if not formula.get_unit_clauses():
        for non_unit_clause in formula.get_non_unit_clauses():
            activate_clause = Clause()
            activate_clause.add_literal(non_unit_clause.literals[0])
            print "activating clause %s based on non-unit clause %s" % (activate_clause, non_unit_clause)
            formula.remove_unit_clause(activate_clause)
            break

    if formula.is_empty():
        print "satisfiable"
    elif formula.is_contradiction():
        print "not satisfiable: %s " % formula
    else:
        recurse(formula)

cnf_files = ["only_unit_clauses--not_satisfiable.txt",
         "only_unit_clauses--satisfiable.txt",
         "non_unit_clauses--satisfiable.txt"]

for cnf_file in cnf_files:
    print "=================\n"
    print "reading file %s\n" % cnf_file
    recurse(dimacs_reader.read_cnf_output("", cnf_file))



