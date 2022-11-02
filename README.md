# CS208 2022/2023 Semester One; Coursework 1

This coursework is the first of two for CS208 Semester One
("Logic"). You will writing a Python program to encode a problem into
logical constraints to be solved by a SAT solver.

This document explains (i) the problem you are going to solve; (ii)
the tasks you need to complete; (iii) some documentation of another
example encoding that you can use for reference; and (iv) practical
instructions on how to get started and how to submit your work.

## Getting Started

This repository contains Python implementations of a SAT solver and
supporting code, and an implementation of the Package Installation
Problem described in Week 2. There is a file ready for you to
implement a solution to the resource allocation problem described
below.

To get started:

1. Clone this repository, either by using `git clone`, or downloading
   the `zip` file.

2. Once you have a copy of the files, make sure that they work by
   running `python` on the `packages.py` file. The output should look
   like this:

   ```
   > python3 packages.py
   Test 1: following dependency chains
   Clauses:
   -libE1 \/ -libE2
   -progA \/ libC
   -progA \/ libD
   -libC \/ libE1
   -libD \/ libE1
   progA
   {'progA': True, 'libC': True, 'libD': True, 'libE1': True, 'libE2': False}

   .... some more tests ....
   ```

If you have any problems getting hold of the files, installing Python,
or getting it to work, please get in contact via
[Mattermost](https://mattermost.cis.strath.ac.uk/learning/channels/cs208-2022-23).

## The exercise: Solving Allocation of Tasks to Machines

The aim of this exercise is to write a program to solve the problem of
assigning tasks to machines, using an encoding into logical
constraints. We make the following assumptions:

1. We have `num_tasks` tasks to complete.

2. We have `num_machines` machines to do them on.

3. Every task must be assigned to some machine.

4. Certain pairs of tasks conflict, and must not be assigned to the
   same machine.

Given `num_tasks`, `num_machines` and a list of `conflicts`, we have
to find an assignment of tasks to machines that gives every task a
machine without assigning conflicting tasks to the same machine.

We will number the tasks `0...num_tasks-1` and the machines
`0...num_machines-1`. This works well with Pythons `range(n)` function
that returns all the numbers `0..n-1` to iterate over.

**Example:** If we have three tasks and one machine, with no tasks
conflicting, then we can assign all three tasks to the one machine.

**Example:** If we have three tasks and one machine, but tasks `0` and
`1` conflict, then there is no assignment that works.

**Example:** If we have three tasks and three machines, with every
pair of tasks conflicting (so `(0,1)`, `(1,2)`, and `(0,2)`), then we
can assign each task to a separate machine. Note that there are 6 ways
of doing this.

### The Encoding

To encode the allocation task in logic, we will use the following
strategy:

1. We will encode the assertion that task `X` is assigned to machine
   `Y` by the atomic proposition `assignXtoY`. If a valuation sets
   `assignXtoY` to `True`, then task `X` is assigned to machine
   `Y`. If a valuation sets it to `False`, then this assignment is not
   made.

2. To encode the requirement that every task `X` must be assigned to a
   machine, we add a clause like this for each `X`:

   ```
      assignXto0 \/ assignXto1 \/ ... \/ assignXto<num_machines-1>
   ```

3. For each conflict `(X,Y)`, we encode the fact that tasks `X` and
   `Y` cannot be assigned to the same machine by adding a clause for
   each machine `Z` like so:

   ```
      ¬assignXtoZ \/ ¬assignYtoZ
   ```

### What you have to do

You have to complete the following tasks by writing code in the file
`resource_allocation.py`. See the comments in that file for guidance.

1. Implement the strategy above to compute allocations. This means
   filling out the missing parts of the `resource_allocation` function
   to implement the encoding strategy above. *(5 marks)*

   There are example allocations at the end of the file, please feel
   free to add your own for testing.

2. The printing of the assignment of tasks to machines is quite
   unfriendly with the code I have provided. It lists all the
   assignments made as well as the assignments not made. Write some
   code to replace this that just lists each task and which machine(s)
   it is assigned to. *(2 marks)*

3. The basic implementation only computes one possible allocation of
   tasks to machines. Adjust the `resource_allocation` function to
   print out **all** possible allocations. *(4 marks)*

   HINT: You'll have to use a loop that works like this: ask the
   solver for a solution, print this out, then add a clause that
   states "not this solution", then go round the loop again until the
   solver says "no solution".

4. The allocation problem described above assumes that the number of
   machines is fixed. Write some more code to find the **smallest**
   number of machines for a fixed number of tasks and conflicts
   between them. *(4 marks)*

   HINT: You'll need to write another loop. You might need to
   restructure the `resource_allocation` function a bit to return
   whether or not it has found a solution.

When you are happy with your solution, please submit the file
`resource_allocation.py` [via MyPlace](https://classes.myplace.strath.ac.uk/mod/assign/view.php?id=1774227).

## An example to follow: Package Installation Problem

As an example implementation for you to follow, I have included an
implementation of the Package Installation Problem introduced in Week
2 in the file [packages.py](packages.py).

Please read that file carefully to see an example of how to implement
a logical encoding, and how to use the `Numbering` class.

### The Other Python Files

The other Python files are supporting code for you to write your
solution. You should not modify them.

- [numbering.py](numbering.py) contains a class that is useful for
  managing a mapping from names to numbers and back again. This is
  useful because the SAT solver implemented here uses numbers to
  represent atomic propositions. It is used by `packages.py` to give a
  number to each package. You should use it to assign numbers to each

- [clauses.py](clauses.py) contains a class that stores a collection
  of clauses ready for solving. Call the `add(clause)` method to add a
  new clause, and the `solve()` method to solve them. See
  `packages.py` for an example of its use.

- [solver.py](solver.py) is an implementation of a SAT solver,
  following the strategy described in the lectures.

## Plagiarism Warning

You are welcome to discuss your solution with other students, but **do
not** copy each other's code. Submit your own solution to the
problem. Any suspected plagiarism will be investigated and may result
in you getting 0 marks for this assessment, as well as a record being
made for the rest of your degree. We may use automated plagiarism
checkers to check submissions for signs of copying.
