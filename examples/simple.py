from storify import Storify
from storify.model import Model

import random

class Person(Model):
    def __init__(self) -> None:
        self.name = random.choice(["Greg", "John", "Jane", "Bob", "Alice", "Tom", "Jerry", "SpongeBob", "Patrick", "Squidward"])
        self.age = random.randrange(1, 100)
        self.food = random.choice(["Pizza", "Burger", "Salad", "Ice Cream", "Sushi"])

def main():
    # Initialize Storify with a custom root directory
    storify = Storify(models=[Person])
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
    # Each time this script is run, a new person is added and printed.
    # People added on previous script runs will still use the Person class model,
    # thanks to Storify's ORM magic. 
    for person in db["people"]:
        print(f"{person.name} is {person.age} years old and likes {person.food}")

    # Flush all databases (force save)
    # Typically, instead of doing this, your code would run storify.tick() frequently to keep all I/O in one thread
    storify.flush()

if __name__ == "__main__":
    main()