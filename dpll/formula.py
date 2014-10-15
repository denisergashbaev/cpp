from CommonEqualityMixin import CommonEqualityMixin


class Literal(CommonEqualityMixin):
    def __init__(self, literal):
        self.literal = int(literal)

    def get_inverse(self):
        return Literal(self.literal * -1)

    def __repr__(self):
        return str(self.literal)


class Clause(CommonEqualityMixin):
    def __init__(self):
        self.literals = []

    def add_literal(self, literal):
        self.literals.append(literal)

    def is_unit_clause(self):
        return len(self.literals) == 1

    def contains_literal(self, literal):
        return literal in self.literals

    def is_empty(self):
        return len(self.literals) == 0

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.literals)


class Formula:
    def __init__(self):
        """:type: clauses of [Clause]"""
        self.clauses = []
        self.solution = []

    def add_solution(self, literal):
        self.solution.append(literal)

    def add_clause(self, clause):
        self.clauses.append(clause)

    def update_clause(self, index, clause):
        self.clauses[index] = clause

    def get_unit_clauses(self):
        return [clause for clause in self.clauses if clause.is_unit_clause()]

    def get_non_unit_clauses(self):
        return [clause for clause in self.clauses if not clause.is_unit_clause()]

    def get_literals(self):
        literals = []
        for clause in self.clauses:
            for literal in clause.literals:
                literals.append(literal)
        return literals

    def is_empty(self):
        return len(self.clauses) == 0

    def has_empty_clause(self):
        return len([clause for clause in self.clauses if clause.is_empty()]) > 0

    # http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python
    def remove_clauses_containing(self, literal):
        """
        :type unit_clause:Clause
        """
        new_clauses = []
        for clause in self.clauses:
            if clause.contains_literal(literal):
                print "removing clause %s because it's deactivated through unit_clause %s" % (clause, literal)
            else:
                new_clauses.append(clause)
        self.clauses = new_clauses

    def remove_literals_from_clauses(self, remove_literal):
        for clause in self.clauses:
            new_literals = []
            for literal in clause.literals:
                if remove_literal == literal:
                    print "removing literal %s from the clause %s" % (literal, clause)
                else:
                    new_literals.append(literal)
            clause.literals[:] = new_literals


    def __repr__(self):
        return str(self.__class__) + ": " + str(self.clauses)


