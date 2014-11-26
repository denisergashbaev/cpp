from copy import deepcopy

from SAT.dpll.formula import Clause


def unit_propagation(formula):
    """:type : dpll.formula.Formula"""
    while True:
        unit_clauses = formula.get_unit_clauses()
        if not unit_clauses:
            break
        literal = unit_clauses[0].literals[0]
        formula.add_solution(literal)
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
        return True, formula
    elif formula.has_empty_clause():
        print "not satisfiable: %s " % formula
        return False, formula

    propagation_literal = select_literal(formula)

    satisfiable, solution_formula = dpll(formula, propagation_literal)
    if satisfiable:
        return satisfiable, solution_formula
    else:
        return dpll(formula, propagation_literal.get_inverse())



