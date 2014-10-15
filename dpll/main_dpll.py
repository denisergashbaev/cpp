from os.path import join
import dimacs_reader
import dpll
from file_operations.file_operations import call_sat_solver, read_sat_output, get_file_names

if __name__ == "__main__":

    solutions_path = "solutions"
    cnfs_path = join("..", "3-coloring", "cnfs")


    for cnf_file in get_file_names(cnfs_path):
        print "=================\n"
        print "reading file %s\n" % cnf_file
        mysat_satisfiable, solution_formula = dpll.dpll(dimacs_reader.read_cnf_output(cnfs_path, cnf_file))
        mysat_variables = [str(el.literal) for el in solution_formula.solution]

        print ">>>"
        sat_file_name = cnf_file + "_sat"
        _, sat_output_full_file_name = call_sat_solver(solutions_path, sat_file_name, join(cnfs_path, cnf_file))
        minisat_satisfiable, minisat_variables = read_sat_output(sat_output_full_file_name)

        suffix = "_ERRROR" if mysat_satisfiable != minisat_satisfiable else "_GOOD"
        output = "SAT" if mysat_satisfiable else "UNSAT"
        if mysat_satisfiable:
            output += "\n"
            output += " ".join(mysat_variables) + " 0"
        with open(join(solutions_path, cnf_file+"_mysat_"+suffix), 'w') as fh:
            fh.write(output)
