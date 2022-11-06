from typing import Union
import pandas as pd
import os


class Item:
    # NOTE: these are class attrs
    pay_rate = 0.8 # discount
    inventory = list()
    fpath = os.path.join(os.getcwd(), 'OOP_projects', 'data', 'items.csv')

    @staticmethod
    def validate_input(name: str, price: float, quantity: float) -> Union[bool, AssertionError]:
        assert price >=0 and quantity>=0, 'Price and quantity should be >= 0'

    @staticmethod
    def check_if_integer(num):
        
        # if float
        if isinstance(num, float):
            # if 7.0 it will return True, False if has fractional part
            return num.is_integer()
        # if int like 7
        elif isinstance(num, int):
            return True
        return False


    def __repr__(self) -> str:
        """
        Display a single Item object
        """
        # repr should be st it can be directly copied and used to create objs
        return f"Item('{self.name}',{self.price},{self.quantity})"

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

        Item.validate_input(name, price, quantity)

        # NOTE: making name a protected class; cant be changed outside this class
        self._name = name
        self.price = price
        self.quantity = quantity

        # add item to inventory now that it is created        
        Item.add_item_to_inventory(self)

    # NOTE: property decorator - read only attr
    @property
    def name(self):
        return self._name

    # NOTE: setter for a read only attr
    @name.setter
    def name(self, value):
        if len(value) > 100:
            raise Exception('name is too long')
        else:
            self._name = value

    def calculate_total_price(self) -> float:
        return self.price * self.quantity

    def apply_discount(self):
        self.price = self.price * self.pay_rate
        print (f'After Discount of {100-self.pay_rate*100}% price: {self.price}')

   

    # NOTE: this is a class method
    @classmethod
    def instantiate_from_csv(cls):
        """
        Read a csv file and create instances for each record
        """
        fpath = cls.fpath
        try:
            df = pd.read_csv(fpath, index_col=False)
        except FileNotFoundError as e:
            print (f'Not found file at {fpath}')
            raise

        records = df.to_dict(orient='list')

        for item_ in  (list(zip(records['name'], records['price'], records['quantity']))):
            Item(name=item_[0], price=item_[1], quantity=item_[2])





