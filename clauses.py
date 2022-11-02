import solver


class Clauses:
    """Objects of class 'Clauses' represent a collection of clauses in
    Conjunctive Normal Form. Use the 'add' method to add an extra
    clause. Objects of this class keep track of how many variables
    there are in the clauses."""

    def __init__(self):
        """Create an empty collection of clauses."""
        self.clauses = []
        self.num_variables = 0

    def add(self, clause):
        """Add a clause. A clause is a list of literals. Literals are
        represented by positive numbers (for positive literals) and
        negative numbers (for negative literals). The number '0' does
        not represent any literal."""
        assert (len(clause) != 0)
        assert (all(map(lambda x: type(x) == int and x != 0, clause)))

        self.clauses += [clause]

        for literal in clause:
            self.num_variables = max(abs(literal), self.num_variables)

    def print(self):
        """Print out the clauses in DIMACS format."""
        print("p cnf %d %d" % (self.num_variables, len(self.clauses)))
        for clause in self.clauses:
            for literal in clause:
                print(str(literal), end=" ")
            print("0")

    def print_as_formula(self, numbering=None) -> None:
        """Print out the clauses as a formula. If a Numbering object
        is provided, this is used to give readable names for the
        atomic propositions instead of their numeric representation."""
        if numbering is None:
            for clause in self.clauses:
                print(" \\/ ".join(map(str, clause)))
        else:
            for clause in self.clauses:
                strings = []
                for literal in clause:
                    if literal < 0:
                        strings += ["-" + numbering.identifier_of(-literal)]
                    else:
                        strings += [numbering.identifier_of(literal)]
                print(" \\/ ".join(strings))

    def evaluate(self, valuation):
        """Evaluates the clauses with the given valuation. Returns
        'True' if all the clauses are satisfied. Otherwise, returns
        'False'."""
        for clause in self.clauses:
            clauseTrue = False
            for literal in clause:
                if literal < 0:
                    clauseTrue = clauseTrue or not (valuation[abs(literal)])
                else:
                    clauseTrue = clauseTrue or valuation[abs(literal)]
            if not clauseTrue:
                return False

        return True

    def solve(self, do_unit_prop=True, logging=True):
        """Solve the clauses to find a satisfying valuation. Returns
        'Result.UNSAT' if there is no such valuation. Returns a
        valuation if one exists."""
        return solver.solve(self.num_variables, self.clauses, do_unit_prop, logging)
