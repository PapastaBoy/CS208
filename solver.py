from enum import Enum
from typing import Dict, List


class PartialValuation:
    """Represents a partial valuation used for finding a satisfying
    assignment for a collection of clauses."""

    def __init__(self, num_vars: int, logging: bool) -> None:
        self._assignment: Dict[int, bool] = {}
        self._decisions: List[tuple[int, str]] = []
        self._unassigned = set(range(1, num_vars + 1))
        self._logging = logging

        if logging:
            print("INIT     : " + str(self))

    def assignment(self) -> Dict[int, bool]:
        """Returns the underlying assignment of this partial valuation."""

        return self._assignment.copy()

    def is_assigned(self, literal: int) -> bool:
        """Returns 'True' if the given literal is assigned in this
        partial valuation; otherwise returns 'False'."""

        return abs(literal) in self._assignment

    def is_true(self, literal: int) -> bool:
        """Returns True if the partial valuation makes this literal
        true, and False if not. If the literal is unassigned, then an
        exception is thrown."""
        val = self._assignment[abs(literal)]
        if literal < 0:
            return not (val)
        else:
            return val

    def backtrack(self) -> bool:
        """Attempts to backtrack to the last decision point. If
           backtracking is successful returns True. If there is no
           decision point to backtrack to, returns False."""

        while len(self._decisions) > 0:
            (var, kind) = self._decisions.pop()
            if kind == 'd':
                self._assignment[var] = not (self._assignment[var])
                self._decisions.append((var, 'f'))
                break
            else:
                del (self._assignment[var])
                self._unassigned.add(var)

        if self._logging:
            print('BACKTRACK: ' + str(self))

        if len(self._decisions) == 0:
            return False
        else:
            return True

    def guess(self, value) -> bool:
        """Picks an unassigned variable and makes a decision point for
        it. Tries 'value' as the initial guess. Returns 'False' if
        there are no unassigned variables, otherwise returns 'True'."""

        if len(self._unassigned) == 0:
            return False

        # use pop to pick some unassigned variable
        var = self._unassigned.pop()
        self._assignment[var] = value
        self._decisions.append((var, 'd'))

        if self._logging:
            print('GUESS    : ' + str(self))

        return True

    def force(self, literal: int) -> None:
        """Force the literal to be true in the partial valuation. The
        literal's variable must be unassigned."""

        var = abs(literal)
        assert (var in self._unassigned)
        self._assignment[var] = (literal > 0)
        self._decisions.append((var, 'f'))
        self._unassigned.remove(var)

        if self._logging:
            print('UNITPROP : ' + str(self))

    def __str__(self) -> str:
        """Returns a string representation of the partial valuation."""

        trace = []
        for (var, kind) in self._decisions:
            if self._assignment[var]:
                assigned_value = 'T'
            else:
                assigned_value = 'F'
            trace.append(str.format('{0} {1}: {2}', var, kind, assigned_value))
        return '[' + '; '.join(trace) + ']'


class Result(Enum):
    SAT = 1
    UNSAT = 2
    UNKNOWN = 3
    UPDATED = 4


def scan_clause(clause: List[int], partial_valuation: PartialValuation, do_unit_prop) -> Result:
    unassigned_literals = []

    for literal in clause:
        if partial_valuation.is_assigned(literal):
            if partial_valuation.is_true(literal):
                return Result.SAT
        else:
            unassigned_literals.append(literal)

    if len(unassigned_literals) == 0:
        return Result.UNSAT
    elif do_unit_prop and len(unassigned_literals) == 1:  # this bit does unit propagation
        partial_valuation.force(unassigned_literals[0])
        return Result.UPDATED
    else:
        return Result.UNKNOWN


def scan_clauses(clauses: List[List[int]], partial_valuation: PartialValuation, do_unit_prop) -> Result:
    allTrue = True
    updated = False

    for clause in clauses:
        status = scan_clause(clause, partial_valuation, do_unit_prop)
        if status == Result.UNKNOWN:
            allTrue = False
        elif status == Result.UNSAT:
            return Result.UNSAT
        elif status == Result.UPDATED:
            updated = True

    if allTrue:
        return Result.SAT
    elif updated:
        return Result.UPDATED
    else:
        return Result.UNKNOWN


def solve(num_vars: int, clauses: List[List[int]], do_unit_prop=True, logging=True) -> Result | Dict[int, bool]:
    p = PartialValuation(num_vars, logging)

    while True:
        status = scan_clauses(clauses, p, do_unit_prop)

        if status == Result.SAT:
            return p.assignment()
        elif status == Result.UPDATED:
            pass  # go round again
        elif status == Result.UNSAT:
            ok = p.backtrack()
            if not ok:
                return Result.UNSAT
        else:  # status == Result.UNKNOWN
            ok = p.guess(True)
            if not ok:
                ok = p.backtrack()
                if not ok:
                    return Result.UNSAT
