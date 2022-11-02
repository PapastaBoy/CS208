import re
from time import perf_counter
from numbering import Numbering
from clauses import Clauses
from solver import Result

# This file contains the skeleton of the resource allocation
# encoding. The parts you need to fill in are marked with 'TODO'.

# If this is 'True' then the clauses are printed before solving.
debugging = False


def assignment(task, machine):
    return str.format("assign{}to{}", task, machine)


def resource_allocation(num_tasks, num_machines, conflicts):
    """Solve the resource allocation problem. Takes three arguments:

    1. 'num_tasks' is the number of tasks to be assigned to machines.

    2. 'num_machines' is the number of machines.

    3. 'conflicts' is a list of pairs of task numbers that conflict
    and must not be assigned to the same machine."""

    # Create a Clauses object that will contain the clauses we
    # generate.
    clauses = Clauses()

    # Create a Numbering object that will track the correspondence
    # between names of packages and the numeric variable that
    # represents them.
    numbering = Numbering()

    # Each task must have at least one machine assigned to it
    #  TODO: FILL THIS IN FOR PART 1
    for (x, y) in conflicts:
        # convert numeric conflict to string format Assign{x}To{y}
        for z in range(num_machines):
            var1 = assignment(x, z)
            var2 = assignment(y, z)
            clauses.add([-numbering.number_of(var1), -numbering.number_of(var2)])

    [clauses.add([numbering.number_of(assignment(task, machine)) for machine in range(num_machines)]) for task in range(num_tasks)]

    # Print out the clauses for debugging
    if debugging:
        clauses.print_as_formula(numbering)

    # TODO: ALTER THE WAY THE SOLVER IS CALLED FOR PART 3
    # Solve the clauses
    result = clauses.solve(logging=False)
    if result == Result.UNSAT:
        print("No allocation possible")
        return

    finals = []
    while result != Result.UNSAT:
        finals.append(result)
        clauses.add([x * (-1 if result[x] else 1) for x in result])
        result = clauses.solve(logging=False)

    # Otherwise, convert the solution to a named one and print it out.
    # TODO: ALTER THIS FOR PART 2
    results = []
    for result in finals:
        for item in result:
            task = numbering.identifier_of(item)
            if result[item]:
                results.append([int(item) for item in re.findall(r'\d', task)])

    tasks = []
    named_results = []
    for r in results:
        if r[0] not in tasks:
            tasks.append(r[0])
    i = 0
    for task in tasks:
        machines = []
        for r in results:
            if r[0] == task:
                machines.append(r[1])
        named_results.append((i, machines))
        i += 1


    for x in range(len(named_results[0][1])):
        print(f"For Solution {x + 1}")
        for result in named_results:
            print(f"Task {result[0]} is assigned to machine:  {result[1][x]}")


# TODO: FOR PART 4 YOU NEED TO WRITE ANOTHER FUNCTION


########################################################################
## Leave this bit as it is

## Test 1
print("Test 1: 3 tasks, 1 machine, no conflicts")
resource_allocation(3, 1, [])
print("")

## Test 2
print("Test 2: 3 tasks, 1 machine, tasks 0/1 conflict")
resource_allocation(3, 1, [(0, 1)])
print("")

## Test 3
print("Test 3: 3 tasks, 3 machines, tasks 0/1, 1/2 and 0/2 conflict")
resource_allocation(3, 3, [(0, 1), (1, 2), (0, 2)])
