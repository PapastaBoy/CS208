from numbering import Numbering
from clauses import Clauses
from solver import Result

# If this is 'True' then the clauses are printed before solving.
debugging = True


def package_installations(conflicts, dependencies, requirements):
    """Solve the package installation problem. Takes three arguments:

    1. 'conflicts' is a list of pairs of package names that cannot be
    installed simultaneously.

    2. 'dependencies' is a list of pairs of a package name and a list
    of the dependencies of that package.

    3. 'requirements' is a list of lists of choices of packages which
    must be installed."""

    # Create a Clauses object that will contain the clauses we
    # genenerate.
    clauses = Clauses()

    # Create a Numbering object that will track the correspondence
    # between names of packages and the numeric variable that
    # represents them.
    numbering = Numbering()

    # For each conflict, add a constraint that says that we can't
    # install both of them.
    for (package1, package2) in conflicts:
        # Convert the named packages to their numeric representation
        var1 = numbering.number_of(package1)
        var2 = numbering.number_of(package2)

        # Add the clause to the collection of clauses
        clauses.add([-var1, -var2])

    # For each package and its dependencies add clauses saying that if
    # we install 'package1', then we install its dependency too.
    for (package1, depends_on) in dependencies:
        # 'depends_on' is a list of packages
        for package2 in depends_on:
            # Convert the package names to numeric representation
            var1 = numbering.number_of(package1)
            var2 = numbering.number_of(package2)

            #
            clauses.add([-var1, var2])

    # For every requirement, add a clause specifying that one of the
    # choices must be installed.
    for choice in requirements:
        clause = []
        for package in choice:
            clause += [numbering.number_of(package)]
        clauses.add(clause)

    # Print the clauses if debugging is turned on.
    if debugging:
        print("Clauses:")
        clauses.print_as_formula(numbering)

    # Solve the clauses
    result = clauses.solve(logging=False)

    # If the result is UNSAT, then tell the user and return.
    if result == Result.UNSAT:
        print("No installation possible")
        return

    # Otherwise, convert the solution to a named one and print it out.
    named_result = numbering.name_assignment(result)
    print(named_result)


# Tests

print("Test 1: following dependency chains")
package_installations(conflicts=[("libE1", "libE2")],
                      dependencies=[("progA", ["libC", "libD"]),
                                    ("libC", ["libE1"]),
                                    ("libD", ["libE1"])],
                      requirements=[["progA"]])

print("")

print("Test 2: unsolvable diamond dependency")
package_installations(conflicts=[("libE1", "libE2")],
                      dependencies=[("progA", ["libC", "libD"]),
                                    ("libC", ["libE2"]),
                                    ("libD", ["libE1"])],
                      requirements=[["progA"]])

print("")

print("Test 3: upgraded package solves dependency issue")
package_installations(conflicts=[("libE1", "libE2"),
                                 ("libD1", "libD2")],
                      dependencies=[("progA1", ["libC", "libD1"]),
                                    ("progA2", ["libC", "libD2"]),
                                    ("libC", ["libE2"]),
                                    ("libD1", ["libE1"]),
                                    ("libD2", ["libE2"])],
                      requirements=[["progA1", "progA2"]])

print("")
