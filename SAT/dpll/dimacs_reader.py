from os.path import join

from dpll.formula import Formula, Clause, Literal


def read_cnf_output(cnf_path, cnf_file_name):
    """
    :rtype : Formula
    """
    formula = Formula()
    with open(join(cnf_path, cnf_file_name), 'r') as fh:
        _, _, number_of_vars, number_of_clauses = fh.readline().strip().split(" ")
        for line in fh:
            line = line.strip()
            clause = Clause()
            for l in line.split(" "):
                l = l.strip()
                if l != "0":
                    literal = Literal(l)
                    clause.add_literal(literal)
            formula.add_clause(clause)
    return formula