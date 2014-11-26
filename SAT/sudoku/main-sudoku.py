from SAT.file_operations.file_operations import get_file_names, clean_directories
from SAT.sudoku import cnf_converter

clean_directories(["cnfs", "solutions"])

file_names = get_file_names("sudokus")
for file_name in file_names:
    print "converting %s" % file_name
    cnf_converter.convert_to_cnf(file_name)
