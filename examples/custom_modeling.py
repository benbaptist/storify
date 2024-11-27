import random
from storify import Storify
from storify.model import Model

# This showcases how to use a more customized model with Storify, where the data
# schema is dynamically retrieved/stored by overriding the _to_dict and _from_dict
# methods.

class Person(Model):
    def __init__(self) -> None:
        self.name = "John"
        self.age = 20

    def _to_dict(self):
        # By overriding _to_dict, we can customize the data that is stored in the database.
        # This can be useful if we want to store the data in a different format than the
        # default, or if we want to store more or less data than the default.
        return {
            "name": self.name,
            "age": self.age
        }

    def _from_dict(self, data):
        # By overriding _from_dict, we can customize the data that is loaded from the database.
        # This can be useful if we want to load the data in a different format than the default,
        # or if we want to load more or less data than the default.
        self.name = data["name"]
        self.age = data["age"]
        return self


def main():
    storify = Storify(models=[Person])
    db = storify.get_db(name="custom_modeling_db")

    if "people" not in db:
        db["people"] = []

    for i in range(3):
        person = Person()
        person.name = f"Person {random.randrange(1000)}"
        person.age = random.randrange(1, 100)
        db["people"].append(person)

    for person in db["people"]:
        # print(person)
        print(f"{person.name} is {person.age} years old")

    storify.flush()

if __name__ == "__main__":
    main()