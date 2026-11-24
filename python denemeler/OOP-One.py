from typing import Self

class Car:
    def __init__(self, brand: str, rpm: int) -> None:
        self.brand = brand
        self.rpm = rpm
    def drive(self) -> None:
        print(f'You are driving a {self.brand}')
    def brake(self) -> None:
        print(f'You pull the brake! {self.rpm} is going down.')

Bentley: Car = Car("Bentley", 20000)

Bentley.drive()
Bentley.brake()