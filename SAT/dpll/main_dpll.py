from os.path import join

from SAT.dpll import dpll
import dimacs_reader
from file_operations.file_operations import call_sat_solver, read_sat_output, get_file_names
from sudoku.cnf_converter import create_matrix, write_human_readable


if __name__ == "__main__":

    sudoku_project_name = "sudoku"

    for project_name in [sudoku_project_name, "3-coloring"]:
        cnfs_path = join("..", project_name, "cnfs")
        solutions_path = join("solutions", project_name)


        for cnf_file in get_file_names(cnfs_path):
            print "=================\n"
            print "reading file %s\n" % cnf_file
            mysat_satisfiable, solution_formula = dpll.dpll(dimacs_reader.read_cnf_output(cnfs_path, cnf_file))
            mysat_variables = [str(el.literal) for el in solution_formula.solution]

            sat_file_name = cnf_file + "_sat"
            _, minisat_output_full_file_name = call_sat_solver(solutions_path, sat_file_name, join(cnfs_path, cnf_file))
            minisat_satisfiable, minisat_variables = read_sat_output(minisat_output_full_file_name)

            output = "SAT" if mysat_satisfiable else "UNSAT"
            if mysat_satisfiable:
                output += "\n"
                output += " ".join(mysat_variables) + " 0"
            mysat_output_full_file_name = join(solutions_path, cnf_file+"_mysat")
            with open(mysat_output_full_file_name, 'w') as fh:
                fh.write(output)

            #special treatment for sudoku so that we can validate the solution
            if project_name == sudoku_project_name:
                sudoku_name = cnf_file[:cnf_file.find("__")]
                matrix = create_matrix(join("..", sudoku_project_name, "sudokus"), sudoku_name)
                matrix_range = range(len(matrix))

                write_human_readable(matrix_range, mysat_variables, matrix, mysat_output_full_file_name)
                write_human_readable(matrix_range, minisat_variables, matrix, minisat_output_full_file_name)
