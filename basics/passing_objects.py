from typing import List


class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age


def create_person(first_name: str, last_name: str, age: int) -> Person:
    """Creates a new Person object."""
    return Person(first_name, last_name, age)


def describe(p: Person) -> str:
    """Returns a string describing the person."""
    return f"{p.first_name} {p.last_name} is {p.age} years old."


def average_age(people: List[Person]) -> float:
    """Returns the average age of the people."""
    return sum((getattr(p, "age") for p in people)) / len(people)


if __name__ == "__main__":
    # The same data as shown in the Excel spreadsheet
    people = [
        Person("Bob", "Smith", 25),
        Person("Alice", "Jones", 52),
        Person("John", "Harris", 33),
        Person("Mary", "Williams", 18),
    ]
    for p in people:
        print(describe(p))
    print("Average age: ", average_age(people))
