from storify import Storify
from storify.model import Model

import random

class Car(Model):
    name: str
    color: str
    year: int = 2024

def main():
    storify = Storify(models=[Car])
    db = storify.get_db(name="car_db")

    if "cars" not in db:
        db["cars"] = []

    car = Car()

    car.name = random.choice(["Tesla", "Toyota", "Ford", "Chevy", "Volvo"])
    car.color = random.choice(["Red", "Blue", "Green", "Yellow", "Black", "White"])
    car.year = random.randint(1900, 2024)
    
    db["cars"].append(car)

    for car in db["cars"]:
        print(car.color, car.year, car.name)

    db.flush()

if __name__ == "__main__":
    main()
