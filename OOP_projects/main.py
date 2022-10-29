from typing import Union


def validate_input(name: str, price: float, quantity: float) -> Union[bool, AssertionError]:
    assert price >=0 and quantity>=0, 'Price and quantity should be >= 0'

class Item:
    # NOTE: these are class attrs
    pay_rate = 0.8 # discount
    inventory = list()

    def __repr__(self) -> str:
        """
        Display a single Item object
        """
        return f'{self.name} | {self.price} | {self.quantity}'

    def add_item_to_inventory(item):
        """
        Add an item to the class attr inventory if not exists
        """
        if item not in Item.inventory:
            Item.inventory.append(item)

        return

    def display_inventory():
        """
        Displays each item in the inventory
        """
        for item_ in Item.inventory:
            print (item_)
        return

    def __init__(self, name: str, price: float, quantity=0) -> None:

        validate_input(name, price, quantity)

        self.name = name
        self.price = price
        self.quantity = quantity

        # add item to inventory now that it is created        
        Item.add_item_to_inventory(self)

    def calculate_total_price(self) -> float:
        return self.price * self.quantity

    def apply_discount(self):
        self.price = self.price * self.pay_rate
        print (f'After Discount of {100-self.pay_rate*100}% price: {self.price}')




item1 = Item("Phone", 100, 1)
item2 = Item("Laptop", 1000, 3)
item3 = Item("Cable", 10, 5)
item4 = Item("Mouse", 50, 5)
item5 = Item("Keyboard", 75, 5)

Item.display_inventory()

