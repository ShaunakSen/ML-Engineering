from typing import Union


def validate_input(name: str, price: float, quantity: float) -> Union[bool, AssertionError]:
    assert price >=0 and quantity>=0, 'Price and quantity should be >= 0'

class Item:
    # NOTE: these are class attrs
    pay_rate = 0.8 # discount
    def __init__(self, name: str, price: float, quantity=0) -> None:

        validate_input(name, price, quantity)

        self.name = name
        self.price = price
        self.quantity = quantity
        # self.pay_rate = 1
    

    def calculate_total_price(self) -> float:
        return self.price * self.quantity

    def apply_discount(self):
        self.price = self.price * self.pay_rate
        print (f'After Discount of {100-self.pay_rate*100}% price: {self.price}')


# print (Item.__dict__) # gets all attrs belonging to this object
item1 = Item('Phone', 100, 5)
# print (item1.__dict__)
item1.apply_discount()
print(item1.calculate_total_price())
print (item1.price)

# item 2 but we want diff discount - set the class attr to the instance
item2 = Item('Laptop', 50000, 3)
item2.pay_rate = 0.5
item2.apply_discount()
print (item2.calculate_total_price())
print (item2.price)


