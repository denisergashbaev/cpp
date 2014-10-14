from copy import deepcopy
import dimacs_reader
from dpll.formula import Clause


def unit_propagation(formula):
    """:type : dpll.formula.Formula"""
    while True:
        unit_clauses = formula.get_unit_clauses()
        if not unit_clauses:
            break
        literal = unit_clauses[0].literals[0]
        formula.remove_clauses_containing(literal)
        formula.remove_literals_from_clauses(literal.get_inverse())


def select_literal(formula):
    return formula.get_literals()[0]


def dpll(original_formula, propagation_literal=None):
    """
    :type original_formula:dpll.formula.Formula
    """
    formula = deepcopy(original_formula)
    if propagation_literal:
        new_clause = Clause()
        new_clause.add_literal(propagation_literal)
        formula.add_clause(new_clause)

    unit_propagation(formula)

    if formula.is_empty():
        print "satisfiable"
        return True
    elif formula.has_empty_clause():
        print "not satisfiable: %s " % formula
        return False

    propagation_literal = select_literal(formula)

    return dpll(formula, propagation_literal) or dpll(formula, propagation_literal.get_inverse())

cnf_files = ["only_unit_clauses--not_satisfiable.txt",
         "only_unit_clauses--satisfiable.txt",
         "non_unit_clauses--satisfiable.txt",
         "graph-010-003___cnf-30-118.txt",
         "graph-010-010___cnf-30-196.txt"]

for cnf_file in cnf_files:
    print "=================\n"
    print "reading file %s\n" % cnf_file
    dpll(dimacs_reader.read_cnf_output("cnfs", cnf_file))



