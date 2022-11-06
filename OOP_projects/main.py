from cmath import e
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
        str_rep = f"{self.__class__.__name__}("
        for atr_, value_ in self.__dict__.items():
            if isinstance(value_, str):
                str_rep += f"'{value_}',"
            else:
                str_rep += f"{value_},"

        str_rep = str_rep[:-1]
        str_rep += ")"
        return str_rep

        # return f"{self.__class__.__name__}('{self.name}',{self.price},{self.quantity})"

    def add_item_to_inventory(item):
        """
        Add an item to the class attr inventory if not exists
        """
        if item not in Item.inventory:
            Item.inventory.append(item)

    def display_inventory():
        """
        Displays each item in the inventory
        """
        for item_ in Item.inventory:
            print (item_)

    def __init__(self, name: str, price: float, quantity=0) -> None:

        Item.validate_input(name, price, quantity)

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

    
    @classmethod
    def calculate_broken_phones(cls):
        num_broken_phones = 0
        for item_ in Item.inventory:
            if 'broken_phones' in item_.__dict__:
                num_broken_phones += item_.broken_phones

        return num_broken_phones



class Phone(Item):

    def __init__(self, name: str, price: float, quantity=0, broken_phones=0) -> None:
        super().__init__(name, price, quantity)
        self.broken_phones = broken_phones
        


Item.instantiate_from_csv()
# phone1 = Item(name='nokia10', price=1000, quantity=5)
# phone1.broken_phones = 1
# phone2 = Item(name='nokia11', price=2500, quantity=5)
# phone2.broken_phones = 2

# Item.display_inventory()

# print(Item.calculate_broken_phones())


phone1 = Phone(name='nokia10', price=1000, quantity=5, broken_phones=2)
Item.display_inventory()

