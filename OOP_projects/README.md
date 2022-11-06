### Object Oriented Programming with Python

> Based on tutorial by JimShapedCoding on freecodecamp: https://www.youtube.com/watch?v=Ej_02ICOIgs&list=WL

---

### Basics

#### instance attr vs class attr

class attr belongs to the class but we can access from instance level as well as class level

```
class Item:
    pay_rate = 0.8 # discount
    def __init__(self, name: str, price: float, quantity=0) -> None:

        validate_input(name, price, quantity)

        self.name = name
        self.price = price
        self.quantity = quantity
```

```
print (Item.pay_rate)
>>> 0.8
```

We can also access these class attrs from instance level as well

```
item1 = Item('Phone', 100, 5)
print (item1.pay_rate)
>>> 0.8
```

How this works is first the object will try and fetch the attr from instance level - if not found, it will fetch from class level

If we have this attr defined at both class and instance levels:

```
class Item:
    # NOTE: these are class attrs
    pay_rate = 0.8 # discount
    def __init__(self, name: str, price: float, quantity=0) -> None:

        validate_input(name, price, quantity)

        self.name = name
        self.price = price
        self.quantity = quantity
        self.pay_rate = 1

item1 = Item('Phone', 100, 5)

print (Item.pay_rate)

print (item1.pay_rate)

>>> 0.8
>>> 1
```

Using `__dict__` - gets all attrs belonging to this object

```
print (Item.__dict__)
>>>
{'__module__': '__main__', 'pay_rate': 0.8, '__init__': <function Item.__init__ at 0x100b8eb80>, 'calculate_total_price': <function Item.calculate_total_price at 0x100b8ec10>, '__dict__': <attribute '__dict__' of 'Item' objects>, '__weakref__': <attribute '__weakref__' of 'Item' objects>, '__doc__': None}

print (item1.__dict__)
>>>
{'name': 'Phone', 'price': 100, 'quantity': 5}
```

Note that `pay_rate` is not there in the attrs of the item1 instance


### Create an inventory list functionality

We basically want to list out all items in our store

We can store inventory as a class attr

`__repr__`: object representation - use this to display object

-- see main.py to see use of a class attr


#### Using Class method for Separating out our data


__Using a Class Method__:

When we want to load in the data, we want to create objects from the loaded data using that function 

We cannot do `item.instantiate_from_csv()` as we want `instantiate_from_csv` to take care of initializing the objs


1. Setup fpath as a class var

`fpath = os.path.join(os.getcwd(), 'OOP_projects', 'data', 'items.csv')`

2. Create a class method to load in the csv and instantiate an item object for each record

Note that the `cls` is like `self` but signifies the class. 

```
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
```

> It can modify a class state that would apply across all the instances of the class. For example, it can modify a class variable that will be applicable to all the instances.

For example if u want to instantiate hundreds of objects from a file - use a class method


#### Static method

 This method can’t access or modify the class state. It is present in a class because it makes sense for the method to be present in class.

 > https://www.geeksforgeeks.org/class-method-vs-static-method-python/

 - We generally use static methods to create utility functions.


Static methods do not receive the obj/class as the first arg - just like a regular function

The validation of input function and a function to check if an arg is an int seem like good candidates for static methods


```
@staticmethod
    def validate_input(name: str, price: float, quantity: float) -> Union[bool, AssertionError]:
        assert price >=0 and quantity>=0, 'Price and quantity should be >= 0'

    @staticmethod
    def is_integer(num):
        
        # if float
        if isinstance(num, float):
            # if 7.0 it will return True, False if has fractional part
            return num.is_integer()
        # if int like 7
        elif isinstance(num, int):
            return True
        return False

```

Ok, so what is the diff bw writing static methods and independent functions outside the class? - not much, but if the function is related to the class then its good practice to use static methods

Also note - do not call a static or class method from an instance level - you will not receive error but its not good practice


### Inheritence

Now we might have phones of class `Item` but these phones might be broken

```
phone1 = Item(name='nokia10', price=1000, quantity=5)
phone1.broken_phones = 1
phone2 = Item(name='nokia11', price=2500, quantity=5)
phone2.broken_phones = 2
```

Now if we were to calculate broken phones

```
@classmethod
    def calculate_broken_phones(cls):
        for item_ in Item.inventory:
            print (item_.broken_phones)

```

Not all items might have this `broken_phones` attr - so we can get error:

```
AttributeError: 'Item' object has no attribute 'broken_phones'
```

We can modify this by:

```
@classmethod
    def calculate_broken_phones(cls):
        num_broken_phones = 0
        for item_ in Item.inventory:
            if 'broken_phones' in item_.__dict__:
                num_broken_phones += item_.broken_phones

        return num_broken_phones
```

