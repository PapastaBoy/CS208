class Numbering:
    """A Numbering object stores an assignment of numbers to names,
    allowing lookup in both directions. It is capable of generating
    new assignments of between numbers and names."""

    def __init__(self):
        self.next_number = 1
        self.identifier_to_number = {}
        self.number_to_identifier = {}

    def number_of(self, identifier):
        """Takes an identifier (a string) and returns the number
        associated to it. If there is no number associated with it,
        then generate a new number."""

        if identifier in self.identifier_to_number:
            return self.identifier_to_number[identifier]

        number = self.next_number
        self.next_number += 1
        self.identifier_to_number[identifier] = number
        self.number_to_identifier[number] = identifier

        return number

    def identifier_of(self, number):
        """Takes a number that was generated by 'number_of' and
        returns the name assigned to that number."""
        if number not in self.number_to_identifier:
            raise Exception("Unknown number: " + str(number))
        return self.number_to_identifier[number]

    def name_assignment(self, assignment):
        """Takes an assignment of numeric variable names to True/False
        values, returns the corresponding assignment of named variable
        names to True/False values for this Numbering."""

        named_assignment = {}

        for (number, value) in assignment.items():
            named_assignment[self.identifier_of(number)] = value

        return named_assignment
