from math import copysign
from dpll.CommonEqualityMixin import CommonEqualityMixin


class Literal(CommonEqualityMixin):
    def __init__(self, literal):
        self.literal = int(literal)

    def is_inverse(self, other_literal):
        """
        :type other_literal:Literal
        """
        return abs(self.literal) == abs(other_literal.literal) \
            and self.get_sign() != other_literal.get_sign()

    def get_sign(self):
        return copysign(1, self.literal)

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

    # http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python
    def remove_inverse_literals(self, remove_literal):
        """
        :type remove_literal:Literal
        """
        new_literals = []
        for literal in self.literals:
            if not literal.is_inverse(remove_literal):
                new_literals.append(literal)
            else:
                print "removing literal %s (inverse of %s) from the clause %s" % (literal, remove_literal, self)
        if self.literals != new_literals:
            print "original literals %s, new literals %s" % (self.literals, new_literals)
        self.literals = new_literals

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.literals)


class Formula:
    def __init__(self):
        """:type: clauses of [Clause]"""
        self.clauses = []

    def add_clause(self, clause):
        self.clauses.append(clause)

    def update_clause(self, index, clause):
        self.clauses[index] = clause

    def get_unit_clauses(self):
        return [clause for clause in self.clauses if clause.is_unit_clause()]

    def get_non_unit_clauses(self):
        return [clause for clause in self.clauses if not clause.is_unit_clause()]

    def is_contradiction(self):
        unit_clauses = self.get_unit_clauses()
        for idx, clause1 in enumerate(unit_clauses):
            for clause2 in unit_clauses[idx+1:]:
                if clause1.literals[0].is_inverse(clause2.literals[0]):
                    return True
        return False

    def is_empty(self):
        return len(self.clauses) == 0

    # http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python
    def remove_unit_clause(self, unit_clause):
        """
        :type unit_clause:Clause
        """
        new_clauses = []
        for clause in self.clauses:
            l = unit_clause.literals[0]
            if clause.contains_literal(l):
                print "removing clause %s because it's deactivated through unit_clause %s" % (clause, l)
            elif unit_clause != clause:
                clause.remove_inverse_literals(l)
                new_clauses.append(clause)
        self.clauses = new_clauses


    def __repr__(self):
        return str(self.__class__) + ": " + str(self.clauses)


