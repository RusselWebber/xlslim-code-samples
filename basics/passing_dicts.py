from typing import Dict, List


def create_person_dict(first_name: str, last_name: str, age: int) -> Dict:
    """Creates a new Person dictionary."""
    return {"first_name": first_name, "last_name": last_name, "age": age}


def describe(p: Dict) -> str:
    """Returns a string describing the person in the dictionary."""
    return (
        f"{p.get('first_name')} {p.get('last_name')} is {p.get('age'):.0f} years old."
    )


def average_age(people: List[Dict]) -> float:
    """Returns the average age of the people."""
    return sum((p.get("age") for p in people)) / len(people)


if __name__ == "__main__":
    # The same data as shown in the Excel spreadsheet
    first_person = create_person_dict("Bob", "Smith", 25)
    second_person = create_person_dict("Alice", "Jones", 52)
    third_person = create_person_dict("John", "Harris", 33)

    for p in [first_person, second_person, third_person]:
        print(describe(p))
    print("Average age: ", average_age(first_person, second_person, third_person))
