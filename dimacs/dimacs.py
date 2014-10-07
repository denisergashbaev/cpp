__author__ = 'denis'

def encode(number_of_vars, number_of_clauses, lines):
    output = "p cnf %s %s\n" % (number_of_vars, number_of_clauses)
    for line in lines:
        output += " ".join(line) + " 0\n"
    return output