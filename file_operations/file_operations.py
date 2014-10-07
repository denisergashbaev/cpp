from os import unlink, listdir
from os.path import join, isfile, abspath
import subprocess


def get_file_names(mypath):
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]


def clean_directories(paths):
    for mypath in paths:
        for the_file in get_file_names(mypath):
            file_path = join(mypath, the_file)
            try:
                if isfile(file_path):
                    unlink(file_path)
                    print "deleted %s" % file_path
            except Exception, e:
                print e


def write_cnf(cnfs_path, file_name, output, number_of_variables, number_of_clauses):
    cnf_file_name = '%s___cnf-%s-%s.txt' % (file_name, number_of_variables, number_of_clauses)
    cnf_full_file_name = join(cnfs_path, cnf_file_name)
    with open(cnf_full_file_name, 'w') as fh:
        print "writing cnf into %s" % cnf_file_name
        fh.write(output)
    return cnf_file_name, cnf_full_file_name


def call_sat_solver(solutions_path, cnf_file_name, cnf_full_file_name):
    sat_output_full_file_name = abspath(join(solutions_path, cnf_file_name))
    cmd = "minisat %s %s" % (cnf_full_file_name, sat_output_full_file_name)
    print "calling command %s" % cmd
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return output, sat_output_full_file_name


def read_sat_output(sat_output_full_file_name):
    variables = []
    with open(sat_output_full_file_name, 'r') as fh:
        satisfiable = "SAT" == fh.readline().strip()
        if satisfiable:
            line = fh.readline().split(" ")
            for el in line:
                variables.append(el)
    return satisfiable, variables