from storify import Storify
from storify.model import Model

import random

class Person(Model):
    def __init__(self) -> None:
        super().__init__()  # Initialize the parent class

        self.name = random.choice(["Greg", "John", "Jane", "Bob", "Alice", "Tom", "Jerry", "SpongeBob", "Patrick", "Squidward"])
        self.age = random.randrange(1, 100)
        self.food = random.choice(["Pizza", "Burger", "Salad", "Ice Cream", "Sushi"])

def main():
    # Initialize Storify with a custom root directory
    storify = Storify(root="example_data", models=[Person])
    db_name = "example_db"

    # Check if the database exists
    if storify.db_exists(db_name):
        print(f"Database '{db_name}' exists. It will be loaded.")

    # Initialize a new database
    db = storify.get_db(name=db_name)

    # Add some data to the database
    db["key"] = "value"
    
    if "randon_number" not in db:
        db["randon_number"] = random.randrange(0, 99999999)

    # Get some data from the database
    print(db["key"])
    print(f"Our random number is {db['randon_number']}")

    # Remove some data from the database
    del db["key"]

    # Use a model
    if "people" not in db:
        db["people"] = []

    person = Person()
    db["people"].append(person)

    # Print out all people in our database
    for person in db["people"]:
        print(f"{person.name} is {person.age} years old and likes {person.food}")

    # Flush all databases (force save)
    storify.flush()

if __name__ == "__main__":
    main()